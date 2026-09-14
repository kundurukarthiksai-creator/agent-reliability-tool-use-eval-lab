import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
REPORTS_DIR = ROOT / "reports"
ASSETS_DIR = ROOT / "docs" / "assets"


REPORT_FILES = [
    "dashboard.html",
    "task-catalog.html",
    "sample-eval-report.html",
    "sample-eval-report.json",
    "quality-gate.json",
    "sample-failure-report.html",
    "sample-failure-report.json",
    "failure-catalog.html",
    "failure-catalog.json",
    "planner-comparison.md",
    "planner-comparison.json",
    "run-comparison-demo.html",
    "run-comparison-demo.json",
    "run-trends-demo.html",
    "run-trends-demo.json",
]


def main() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)

    reports_output = SITE_DIR / "reports"
    assets_output = SITE_DIR / "assets"
    reports_output.mkdir(parents=True)
    assets_output.mkdir(parents=True)

    for filename in REPORT_FILES:
        source = REPORTS_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing report artifact: {source}")
        shutil.copy2(source, reports_output / filename)

    screenshot = ASSETS_DIR / "eval-report.png"
    if screenshot.exists():
        shutil.copy2(screenshot, assets_output / screenshot.name)

    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")
    (SITE_DIR / "index.html").write_text(render_index(), encoding="utf-8")
    print(f"built {SITE_DIR}")


def render_index() -> str:
    links = [
        ("Dashboard", "reports/dashboard.html", "Start with the portfolio demo index."),
        ("Task Catalog", "reports/task-catalog.html", "Inspect all 22 deterministic tasks."),
        ("Eval Report", "reports/sample-eval-report.html", "Review traces, assertions, and scoring."),
        ("Quality Gate", "reports/quality-gate.json", "See the strict regression gate output."),
        ("Failure Catalog", "reports/failure-catalog.html", "Inspect deliberate failure categories."),
        ("Planner Comparison", "reports/planner-comparison.md", "Compare planners in a compact report."),
        ("Run Comparison", "reports/run-comparison-demo.html", "Review saved-run regression signals."),
        ("Run Trends", "reports/run-trends-demo.html", "Review reliability movement over runs."),
    ]
    cards = "\n".join(
        f"""
        <a class="card" href="{href}">
          <span>{label}</span>
          <p>{description}</p>
        </a>
        """.strip()
        for label, href, description in links
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Reliability Eval Lab Demo</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #171a21;
      --muted: #566173;
      --border: #d9e0ea;
      --accent: #0f5db8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 36px 20px 48px;
    }}
    header {{
      display: grid;
      gap: 18px;
      margin-bottom: 28px;
    }}
    h1 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.1;
      letter-spacing: 0;
    }}
    .summary {{
      max-width: 780px;
      margin: 0;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.55;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 28px 0;
    }}
    .metric, .card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
    }}
    .metric {{
      padding: 18px;
    }}
    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .metric strong {{
      display: block;
      margin-top: 8px;
      font-size: 28px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}
    .card {{
      min-height: 130px;
      padding: 18px;
      color: inherit;
      text-decoration: none;
    }}
    .card:hover {{
      border-color: var(--accent);
      box-shadow: 0 10px 30px rgba(20, 32, 52, .08);
    }}
    .card span {{
      color: var(--accent);
      font-size: 16px;
      font-weight: 800;
    }}
    .card p {{
      margin: 12px 0 0;
      color: var(--muted);
      line-height: 1.45;
    }}
    .preview {{
      margin-top: 28px;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    .preview img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    @media (max-width: 840px) {{
      h1 {{ font-size: 29px; }}
      .metrics, .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 520px) {{
      main {{ padding: 28px 16px 40px; }}
      .metrics, .grid {{ grid-template-columns: 1fr; }}
      .card {{ min-height: auto; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Agent Reliability Eval Lab Demo</h1>
      <p class="summary">Static public demo for a deterministic tool-use evaluation lab. The default path runs without API keys, scores 22 tasks across 5 local tools, and publishes the same reports verified by CI.</p>
    </header>
    <section class="metrics" aria-label="Demo metrics">
      <div class="metric"><span>Tasks</span><strong>22</strong></div>
      <div class="metric"><span>Tools</span><strong>5</strong></div>
      <div class="metric"><span>Pass Rate</span><strong>100%</strong></div>
      <div class="metric"><span>CI Path</span><strong>No Keys</strong></div>
    </section>
    <section class="grid" aria-label="Demo links">
      {cards}
    </section>
    <section class="preview" aria-label="Report screenshot">
      <img src="assets/eval-report.png" alt="HTML evaluation report screenshot">
    </section>
  </main>
</body>
</html>
"""


if __name__ == "__main__":
    main()
