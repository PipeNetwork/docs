use axum::{
    extract::{Path, State},
    http::{header, StatusCode},
    response::{Html, IntoResponse, Redirect, Response},
    routing::get,
    Router,
};
use moka::future::Cache;
use once_cell::sync::Lazy;
use pulldown_cmark::{html, Event, Options, Parser, Tag, TagEnd};
use std::collections::HashMap;
use std::path::{Component, Path as FilePath, PathBuf};
use std::sync::Arc;

static HTML_CACHE: Lazy<Cache<PathBuf, Arc<String>>> = Lazy::new(|| {
    Cache::builder()
        .max_capacity(1000)
        .time_to_live(std::time::Duration::from_secs(600))
        .build()
});

#[derive(Clone)]
struct AppState {
    root: PathBuf,
}

pub fn app(root: PathBuf) -> Router {
    Router::new()
        .route("/", get(serve_index))
        .route("/md/*path", get(serve_markdown))
        .route("/docs/*path", get(serve_document))
        .route("/static/*path", get(serve_raw))
        .route("/cache/stats", get(cache_stats))
        .fallback(get(handler_404))
        .with_state(AppState { root })
}

async fn serve_index(State(state): State<AppState>) -> Response {
    match tokio::fs::read_to_string(state.root.join("README.md")).await {
        Ok(content) => render_markdown_with_template(&content, "Pipe Network Documentation").into_response(),
        Err(_) => render_markdown_with_template(
            "# Pipe Network Mainnet\n\n[Storage](/docs/storage/overview.md) · [Node setup](/docs/nodes/mainnet.md) · [Tokenomics](/docs/Tokenomics.md)",
            "Pipe Network Documentation",
        ).into_response(),
    }
}

async fn serve_markdown(Path(path): Path<String>, State(state): State<AppState>) -> Response {
    if path == "README.md" {
        return serve_index(State(state)).await;
    }
    let Some(relative) = path.strip_prefix("docs/") else {
        return handler_404().await;
    };
    // Keep old Markdown entrypoints working with one canonical URL. This also
    // makes relative links resolve the same way as /docs links.
    if !safe_relative_path(relative) {
        return handler_404().await;
    }
    Redirect::permanent(&format!("/docs/{relative}")).into_response()
}

fn legacy_target(path: &str) -> Option<&'static str> {
    match path {
        "pipe-firestarter-storage.md" => Some("/docs/storage/overview.md"),
        "cdn-api/api-documentation.md" => Some("/docs/storage/api.md"),
        "mica.pdf" => Some("/docs/archive/README.md"),
        _ => None,
    }
}

async fn serve_document(Path(path): Path<String>, State(state): State<AppState>) -> Response {
    if let Some(target) = legacy_target(&path) {
        return Redirect::permanent(target).into_response();
    }
    serve_file(&state, &path, false).await
}

async fn serve_raw(Path(path): Path<String>, State(state): State<AppState>) -> Response {
    serve_file(&state, &path, true).await
}

fn safe_relative_path(path: &str) -> bool {
    !path.is_empty()
        && !path.contains('\\')
        && path
            .split('/')
            .all(|part| !part.is_empty() && !part.starts_with('.'))
        && FilePath::new(path)
            .components()
            .all(|part| matches!(part, Component::Normal(_)))
}

async fn serve_file(state: &AppState, relative: &str, raw: bool) -> Response {
    if !safe_relative_path(relative) {
        return handler_404().await;
    }
    let Ok(base) = tokio::fs::canonicalize(state.root.join("docs")).await else {
        return handler_404().await;
    };
    let Ok(path) = tokio::fs::canonicalize(base.join(relative)).await else {
        return handler_404().await;
    };
    if !path.starts_with(&base) || !path.is_file() {
        return handler_404().await;
    }
    let extension = path.extension().and_then(|s| s.to_str()).unwrap_or("");
    let content_type = match extension {
        "md" => "text/plain; charset=utf-8",
        "json" => "application/json",
        "pdf" => "application/pdf",
        "py" => "text/plain; charset=utf-8",
        _ => return handler_404().await,
    };
    if extension == "md" && !raw {
        if let Some(content) = HTML_CACHE.get(&path).await {
            return Html((*content).clone()).into_response();
        }
        let Ok(content) = tokio::fs::read_to_string(&path).await else {
            return handler_404().await;
        };
        let title = path
            .file_stem()
            .and_then(|s| s.to_str())
            .unwrap_or("Documentation");
        let rendered = render_markdown_with_template(&content, title).0;
        HTML_CACHE.insert(path, Arc::new(rendered.clone())).await;
        return Html(rendered).into_response();
    }
    match tokio::fs::read(&path).await {
        Ok(bytes) => ([(header::CONTENT_TYPE, content_type)], bytes).into_response(),
        Err(_) => handler_404().await,
    }
}

fn heading_anchor(text: &str) -> String {
    let filtered: String = text
        .to_ascii_lowercase()
        .chars()
        .filter(|c| c.is_ascii_alphanumeric() || matches!(c, ' ' | '_' | '-'))
        .map(|c| if c == ' ' { '-' } else { c })
        .collect();
    let mut result = String::new();
    for character in filtered.chars() {
        if character != '-' || !result.ends_with('-') {
            result.push(character);
        }
    }
    result.trim_matches('-').to_string()
}

fn escape_html(value: &str) -> String {
    value
        .replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
}

fn render_markdown_with_template(markdown: &str, title: &str) -> Html<String> {
    let mut options = Options::empty();
    options.insert(Options::ENABLE_TABLES);
    options.insert(Options::ENABLE_FOOTNOTES);
    options.insert(Options::ENABLE_STRIKETHROUGH);
    options.insert(Options::ENABLE_TASKLISTS);

    let mut events: Vec<_> = Parser::new_ext(markdown, options).collect();
    let mut headings = HashMap::<String, usize>::new();
    for index in 0..events.len() {
        if !matches!(events[index], Event::Start(Tag::Heading { .. })) {
            continue;
        }
        let mut text = String::new();
        for event in &events[index + 1..] {
            match event {
                Event::End(TagEnd::Heading(_)) => break,
                Event::Text(value) | Event::Code(value) => text.push_str(value),
                Event::SoftBreak | Event::HardBreak => text.push(' '),
                _ => {}
            }
        }
        let base = heading_anchor(&text);
        let count = headings.entry(base.clone()).or_default();
        let anchor = if *count == 0 {
            base
        } else {
            format!("{base}-{count}")
        };
        *count += 1;
        if let Event::Start(Tag::Heading { id, .. }) = &mut events[index] {
            *id = Some(anchor.into());
        }
    }
    let mut html_output = String::new();
    html::push_html(&mut html_output, events.into_iter());

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
        escape_html(title),
        html_output
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
    )
        .into_response()
}
