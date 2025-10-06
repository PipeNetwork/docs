use axum::{
    extract::Path,
    http::StatusCode,
    response::{Html, IntoResponse, Response},
    routing::get,
    Router,
};
use moka::future::Cache;
use once_cell::sync::Lazy;
use pulldown_cmark::{html, Options, Parser};
use std::path::PathBuf;
use std::sync::Arc;
use tower_http::services::ServeDir;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

// Global cache: 1000 entries, 10 min TTL
static HTML_CACHE: Lazy<Cache<String, Arc<String>>> = Lazy::new(|| {
    Cache::builder()
        .max_capacity(1000)
        .time_to_live(std::time::Duration::from_secs(600))
        .build()
});

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "pipe_docs_server=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let app = Router::new()
        .route("/", get(serve_index))
        .route("/md/*path", get(serve_markdown))
        .route("/docs/*path", get(serve_markdown_docs))
        .route("/cache/stats", get(cache_stats))
        .nest_service("/static", ServeDir::new("docs"))
        .fallback(get(handler_404));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();

    tracing::info!("Docs server listening on http://0.0.0.0:3000");
    tracing::info!("  - View docs: http://localhost:3000/docs/<path>");
    tracing::info!("  - View rendered markdown: http://localhost:3000/md/<path>");
    tracing::info!("  - View raw files: http://localhost:3000/static/<path>");
    tracing::info!("  - Cache stats: http://localhost:3000/cache/stats");

    axum::serve(listener, app).await.unwrap();
}

async fn serve_index() -> Response {
    let readme_path = PathBuf::from("README.md");

    if let Ok(content) = tokio::fs::read_to_string(&readme_path).await {
        render_markdown_with_template(&content, "Pipe Network Documentation").into_response()
    } else {
        (
            StatusCode::OK,
            Html(r#"
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Pipe Network Documentation</title>
    <style>
        body { font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 0 20px; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { line-height: 1.8; }
    </style>
</head>
<body>
    <h1>Pipe Network Documentation</h1>
    <ul>
        <li><a href="/docs/index.md">Documentation Index</a></li>
        <li><a href="/docs/getting-started/introduction.md">Introduction</a></li>
        <li><a href="/docs/getting-started/quickstart.md">Quickstart</a></li>
        <li><a href="/static/">Browse Raw Files</a></li>
    </ul>
</body>
</html>
            "#)
        ).into_response()
    }
}

async fn serve_markdown(Path(path): Path<String>) -> Response {
    // Security: Sanitize path to prevent traversal
    let sanitized_path = path.replace("..", "");
    serve_markdown_internal(sanitized_path).await
}

async fn serve_markdown_docs(Path(path): Path<String>) -> Response {
    // Security: Prevent path traversal attacks
    let sanitized_path = path.replace("..", "");

    // Prepend "docs/" to the path since /docs/* route should serve from docs/ directory
    let full_path = format!("docs/{}", sanitized_path);

    // Verify the path is still within docs/ directory
    let canonical_base = std::fs::canonicalize("docs").ok();
    let full_path_buf = PathBuf::from(&full_path);

    if let Ok(canonical) = std::fs::canonicalize(&full_path_buf) {
        if let Some(base) = canonical_base {
            if !canonical.starts_with(&base) {
                return (
                    StatusCode::FORBIDDEN,
                    Html("<h1>403 - Forbidden</h1>".to_string()),
                ).into_response();
            }
        }
    }

    serve_markdown_internal(full_path).await
}

async fn serve_markdown_internal(path: String) -> Response {
    let file_path = PathBuf::from(&path);
    let cache_key = path.clone();

    // Try cache first
    if let Some(cached_html) = HTML_CACHE.get(&cache_key).await {
        tracing::debug!("Cache HIT: {}", cache_key);
        return Html((*cached_html).clone()).into_response();
    }

    tracing::debug!("Cache MISS: {}", cache_key);

    match tokio::fs::read_to_string(&file_path).await {
        Ok(content) => {
            let title = file_path
                .file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("Documentation");

            let html = render_markdown_with_template(&content, title);
            let html_string = html.0;

            // Store in cache
            HTML_CACHE.insert(cache_key, Arc::new(html_string.clone())).await;

            Html(html_string).into_response()
        }
        Err(_) => (
            StatusCode::NOT_FOUND,
            Html("<h1>404 - File Not Found</h1>".to_string()),
        ).into_response(),
    }
}

fn render_markdown_with_template(markdown: &str, title: &str) -> Html<String> {
    let mut options = Options::empty();
    options.insert(Options::ENABLE_TABLES);
    options.insert(Options::ENABLE_FOOTNOTES);
    options.insert(Options::ENABLE_STRIKETHROUGH);
    options.insert(Options::ENABLE_TASKLISTS);

    let parser = Parser::new_ext(markdown, options);
    let mut html_output = String::new();
    html::push_html(&mut html_output, parser);

    // Fix relative links: convert "docs/" to "/docs/"
    html_output = html_output.replace("href=\"docs/", "href=\"/docs/");

    let full_html = format!(
        r#"<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #24292e;
        }}
        pre {{
            background: #f6f8fa;
            padding: 16px;
            overflow: auto;
            border-radius: 6px;
        }}
        code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 85%;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #dfe2e5;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background: #f6f8fa;
            font-weight: 600;
        }}
        blockquote {{
            border-left: 4px solid #dfe2e5;
            padding-left: 16px;
            color: #6a737d;
            margin: 0;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        img {{
            max-width: 100%;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{
            font-size: 2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 8px;
        }}
        h2 {{
            font-size: 1.5em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 8px;
        }}
    </style>
</head>
<body>
    {}
    <hr style="margin-top: 40px;">
    <p style="color: #6a737d; font-size: 14px;"><a href="/">← Back to Index</a></p>
</body>
</html>"#,
        title, html_output
    );

    Html(full_html)
}

async fn cache_stats() -> Response {
    let entry_count = HTML_CACHE.entry_count();
    let weighted_size = HTML_CACHE.weighted_size();

    let stats_html = format!(
        r#"<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Cache Statistics</title>
    <style>
        body {{ font-family: system-ui; max-width: 600px; margin: 40px auto; padding: 0 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f6f8fa; }}
    </style>
</head>
<body>
    <h1>Cache Statistics</h1>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Cached Entries</td><td>{}</td></tr>
        <tr><td>Weighted Size</td><td>{}</td></tr>
        <tr><td>Max Capacity</td><td>1000 entries</td></tr>
        <tr><td>TTL</td><td>10 minutes</td></tr>
    </table>
    <p><a href="/">← Back to Index</a></p>
</body>
</html>"#,
        entry_count, weighted_size
    );

    Html(stats_html).into_response()
}

async fn handler_404() -> Response {
    (
        StatusCode::NOT_FOUND,
        Html("<h1>404 - Page Not Found</h1><p><a href=\"/\">Go to Index</a></p>"),
    ).into_response()
}

#[cfg(test)]
mod tests {
    use super::*;
    use axum::{body::Body, http::Request};
    use tower::ServiceExt;

    fn test_app() -> Router {
        Router::new()
            .route("/", get(serve_index))
            .route("/md/*path", get(serve_markdown))
            .route("/docs/*path", get(serve_markdown_docs))
            .route("/cache/stats", get(cache_stats))
            .nest_service("/static", ServeDir::new("docs"))
            .fallback(get(handler_404))
    }

    #[test]
    fn test_markdown_rendering() {
        let markdown = "# Hello\n\nThis is **bold** text.";
        let result = render_markdown_with_template(markdown, "Test");

        assert!(result.0.contains("<h1>Hello</h1>"));
        assert!(result.0.contains("<strong>bold</strong>"));
        assert!(result.0.contains("<title>Test</title>"));
    }

    #[test]
    fn test_markdown_with_code_blocks() {
        let markdown = "```rust\nfn main() {}\n```";
        let result = render_markdown_with_template(markdown, "Code");

        assert!(result.0.contains("<pre>"));
        // Code is rendered inside pre tag
        assert!(result.0.contains("fn main()"));
    }

    #[test]
    fn test_markdown_with_tables() {
        let markdown = "| Header |\n|--------|\n| Cell   |";
        let result = render_markdown_with_template(markdown, "Table");

        assert!(result.0.contains("<table>"));
        assert!(result.0.contains("<th>"));
        assert!(result.0.contains("<td>"));
        assert!(result.0.contains("Header"));
        assert!(result.0.contains("Cell"));
    }

    #[tokio::test]
    async fn test_404_handler() {
        let app = test_app();

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/nonexistent")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::NOT_FOUND);
    }

    #[tokio::test]
    async fn test_cache_stats_endpoint() {
        let app = test_app();

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/cache/stats")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body = axum::body::to_bytes(response.into_body(), usize::MAX)
            .await
            .unwrap();
        let body_str = String::from_utf8(body.to_vec()).unwrap();

        assert!(body_str.contains("Cache Statistics"));
        assert!(body_str.contains("Cached Entries"));
        assert!(body_str.contains("Max Capacity"));
    }

    #[tokio::test]
    async fn test_cache_behavior() {
        // Clear cache for test
        let test_cache: Cache<String, Arc<String>> = Cache::builder()
            .max_capacity(10)
            .build();

        // First access - should be None
        let key = "test_key".to_string();
        assert!(test_cache.get(&key).await.is_none());

        // Insert value
        let value = Arc::new("test_value".to_string());
        test_cache.insert(key.clone(), value.clone()).await;

        // Second access - should be Some
        let cached = test_cache.get(&key).await;
        assert!(cached.is_some());
        assert_eq!(*cached.unwrap(), "test_value");

        // Verify cache get/set works
        test_cache.run_pending_tasks().await;
    }

    #[tokio::test]
    async fn test_cache_expiration() {
        let test_cache: Cache<String, Arc<String>> = Cache::builder()
            .max_capacity(10)
            .time_to_live(std::time::Duration::from_millis(100))
            .build();

        let key = "expire_test".to_string();
        let value = Arc::new("value".to_string());

        test_cache.insert(key.clone(), value).await;
        assert!(test_cache.get(&key).await.is_some());

        // Wait for expiration
        tokio::time::sleep(std::time::Duration::from_millis(150)).await;

        // Should be expired (need to trigger eviction)
        test_cache.run_pending_tasks().await;
        assert_eq!(test_cache.entry_count(), 0);
    }
}
