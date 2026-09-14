from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"


EXPECTED_TEXT = {
    "index.html": [
        "Agent Reliability Eval Lab Demo",
        "Case Study",
        "OpenAPI Contract",
        "22 tasks",
        "5 local tools",
        "No Keys",
    ],
    "case-study.html": [
        "Agent Reliability Eval Lab Case Study",
        "Why This Project Exists",
        "How To Inspect It",
        "Honest Limits",
    ],
    "reports/dashboard.html": ["Agent Reliability Lab", "profile_readme_audit"],
    "reports/task-catalog.html": ["Evaluation Task Catalog", "profile-readme-ready"],
    "reports/sample-eval-report.html": ["Agent Reliability Eval Report", "Total Tasks"],
    "reports/failure-catalog.html": ["Failure Categories", "tool_selection"],
    "reports/run-trends-demo.html": ["Saved Run Trends"],
    "reports/run-comparison-demo.html": ["Saved Run Comparison"],
    "reports/planner-comparison.md": ["Planner Comparison", "rule_based"],
    "docs/openapi.json": [
        "\"openapi\": \"3.",
        "\"title\": \"Agent Reliability and Tool-Use Eval Lab\"",
        "\"/eval/run\"",
    ],
}


class DemoLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append(value)


def main() -> None:
    if not SITE_DIR.exists():
        raise SystemExit("site/ does not exist. Run scripts/build_static_demo.py first.")

    index_path = SITE_DIR / "index.html"
    index_html = index_path.read_text(encoding="utf-8")
    assert_expected_text(index_path, index_html)
    assert_references_exist(index_html)

    for relative_path, expected_values in EXPECTED_TEXT.items():
        path = SITE_DIR / relative_path
        if not path.exists():
            raise SystemExit(f"Missing expected demo artifact: {path}")
        content = path.read_text(encoding="utf-8")
        assert_expected_text(path, content, expected_values)

    screenshot = SITE_DIR / "assets" / "eval-report.png"
    if not screenshot.exists():
        raise SystemExit(f"Missing demo screenshot: {screenshot}")
    if screenshot.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"Demo screenshot is not a PNG: {screenshot}")
    if screenshot.stat().st_size < 10_000:
        raise SystemExit(f"Demo screenshot is unexpectedly small: {screenshot}")

    print("static demo check passed")


def assert_expected_text(
    path: Path,
    content: str,
    expected_values: list[str] | None = None,
) -> None:
    values = expected_values if expected_values is not None else EXPECTED_TEXT[path.name]
    for expected in values:
        if expected not in content:
            raise SystemExit(f"Missing expected text {expected!r} in {path}")


def assert_references_exist(index_html: str) -> None:
    parser = DemoLinkParser()
    parser.feed(index_html)
    site_root = SITE_DIR.resolve()

    for reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or parsed.netloc:
            raise SystemExit(f"Unexpected external reference in static demo: {reference}")
        if parsed.path.startswith("#"):
            continue
        target = (site_root / unquote(parsed.path)).resolve()
        if site_root not in [target, *target.parents]:
            raise SystemExit(f"Reference leaves site directory: {reference}")
        if not target.exists():
            raise SystemExit(f"Broken static demo reference: {reference}")


if __name__ == "__main__":
    main()
