use axum::{
    body::{to_bytes, Body},
    http::{header, Request, StatusCode},
    Router,
};
use pipe_docs_server::app;
use std::fs;
use tempfile::TempDir;
use tower::ServiceExt;

fn fixture() -> (TempDir, Router) {
    let root = TempDir::new().unwrap();
    fs::create_dir_all(root.path().join("docs/storage")).unwrap();
    fs::create_dir_all(root.path().join("internal")).unwrap();
    fs::write(
        root.path().join("README.md"),
        "# Mainnet\n\n[API](docs/storage/api.md)",
    )
    .unwrap();
    fs::write(root.path().join("docs/storage/api.md"), "# Storage API\n\n## Billing and credit\n\n**Mainnet**\n\n## Billing and credit\n\n```sh\necho ready\n```\n\n| A | B |\n|---|---|\n| 1 | 2 |\n").unwrap();
    fs::write(
        root.path().join("docs/tokenomics-params.json"),
        br#"{"version":"3.0.0"}"#,
    )
    .unwrap();
    fs::write(
        root.path().join("docs/whitepaper.pdf"),
        b"%PDF-1.4\n\xff\x00\xfe\n%%EOF",
    )
    .unwrap();
    fs::write(root.path().join("internal/notes.md"), "internal-only").unwrap();
    let router = app(root.path().to_path_buf());
    (root, router)
}

async fn request(router: Router, path: &str, method: &str) -> axum::response::Response {
    router
        .oneshot(
            Request::builder()
                .method(method)
                .uri(path)
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap()
}

#[tokio::test]
async fn renders_markdown_with_working_anchors_and_root_links() {
    let (_root, router) = fixture();
    let response = request(router.clone(), "/docs/storage/api.md", "GET").await;
    assert_eq!(response.status(), StatusCode::OK);
    assert!(response.headers()[header::CONTENT_TYPE]
        .to_str()
        .unwrap()
        .starts_with("text/html"));
    let body = String::from_utf8(
        to_bytes(response.into_body(), usize::MAX)
            .await
            .unwrap()
            .to_vec(),
    )
    .unwrap();
    assert!(body.contains("id=\"billing-and-credit\""));
    assert!(body.contains("id=\"billing-and-credit-1\""));
    assert!(body.contains("<strong>Mainnet</strong>"));
    assert!(body.contains("<table>"));
    assert!(body.contains("echo ready"));
    let response = request(router, "/", "GET").await;
    let body = String::from_utf8(
        to_bytes(response.into_body(), usize::MAX)
            .await
            .unwrap()
            .to_vec(),
    )
    .unwrap();
    assert!(body.contains("href=\"/docs/storage/api.md\""));
}

#[tokio::test]
async fn serves_binary_pdf_and_json_without_html_wrapping() {
    let (root, router) = fixture();
    for (name, mime) in [
        ("whitepaper.pdf", "application/pdf"),
        ("tokenomics-params.json", "application/json"),
    ] {
        let expected = fs::read(root.path().join("docs").join(name)).unwrap();
        for prefix in ["/docs/", "/static/"] {
            let response = request(router.clone(), &format!("{prefix}{name}"), "GET").await;
            assert_eq!(response.status(), StatusCode::OK);
            assert_eq!(response.headers()[header::CONTENT_TYPE], mime);
            assert_eq!(
                to_bytes(response.into_body(), usize::MAX)
                    .await
                    .unwrap()
                    .as_ref(),
                expected
            );
            let head = request(router.clone(), &format!("{prefix}{name}"), "HEAD").await;
            assert_eq!(head.status(), StatusCode::OK);
            assert_eq!(head.headers()[header::CONTENT_TYPE], mime);
            assert!(to_bytes(head.into_body(), usize::MAX)
                .await
                .unwrap()
                .is_empty());
        }
    }
}

#[tokio::test]
async fn raw_markdown_does_not_return_cached_html() {
    let (root, router) = fixture();
    assert_eq!(
        request(router.clone(), "/docs/storage/api.md", "GET")
            .await
            .status(),
        StatusCode::OK
    );
    let response = request(router, "/static/storage/api.md", "GET").await;
    assert_eq!(
        response.headers()[header::CONTENT_TYPE],
        "text/plain; charset=utf-8"
    );
    assert_eq!(
        to_bytes(response.into_body(), usize::MAX)
            .await
            .unwrap()
            .as_ref(),
        fs::read(root.path().join("docs/storage/api.md")).unwrap()
    );
}

#[tokio::test]
async fn old_product_urls_redirect_to_current_documents() {
    let (_root, router) = fixture();
    for (old, new) in [
        (
            "/docs/pipe-firestarter-storage.md",
            "/docs/storage/overview.md",
        ),
        ("/docs/cdn-api/api-documentation.md", "/docs/storage/api.md"),
        ("/docs/mica.pdf", "/docs/archive/README.md"),
        ("/md/docs/storage/api.md", "/docs/storage/api.md"),
    ] {
        let response = request(router.clone(), old, "GET").await;
        assert_eq!(response.status(), StatusCode::PERMANENT_REDIRECT);
        assert_eq!(response.headers()[header::LOCATION], new);
    }
}

#[tokio::test]
async fn removed_pages_and_files_outside_public_docs_are_unavailable() {
    let (_root, router) = fixture();
    for path in [
        "/docs/nodes/devnet-2.md",
        "/docs/nodes/testnet.md",
        "/md/internal/notes.md",
        "/docs/%2e%2e/internal/notes.md",
        "/static/%2e%2e/internal/notes.md",
        "/md/docs/%2e%2e/internal/notes.md",
        "/md/%2Finternal/notes.md",
        "/docs//internal/notes.md",
        "/docs/.hidden",
        "/unknown",
    ] {
        let response = request(router.clone(), path, "GET").await;
        assert_eq!(response.status(), StatusCode::NOT_FOUND, "{path}");
    }
}

#[cfg(unix)]
#[tokio::test]
async fn symlinks_cannot_expose_internal_files() {
    let (root, router) = fixture();
    std::os::unix::fs::symlink(
        root.path().join("internal/notes.md"),
        root.path().join("docs/external.md"),
    )
    .unwrap();
    for path in ["/docs/external.md", "/static/external.md"] {
        assert_eq!(
            request(router.clone(), path, "GET").await.status(),
            StatusCode::NOT_FOUND
        );
    }
}

#[tokio::test]
async fn cache_is_scoped_to_each_repository() {
    let (_first, first) = fixture();
    let (second_root, second) = fixture();
    fs::write(
        second_root.path().join("docs/storage/api.md"),
        "# Different repository",
    )
    .unwrap();
    request(first, "/docs/storage/api.md", "GET").await;
    let response = request(second, "/docs/storage/api.md", "GET").await;
    let body = String::from_utf8(
        to_bytes(response.into_body(), usize::MAX)
            .await
            .unwrap()
            .to_vec(),
    )
    .unwrap();
    assert!(body.contains("Different repository"));
    assert!(!body.contains("Billing and credit"));
}
