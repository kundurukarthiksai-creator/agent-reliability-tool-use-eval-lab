# Assets

## `eval-report.png`

Screenshot of `reports/sample-eval-report.html`.

Regenerate after intentional HTML report layout changes:

```powershell
.\.venv\Scripts\python scripts\render_report.py
$report = (Resolve-Path reports/sample-eval-report.html).Path -replace "\\", "/"
npx playwright screenshot --browser=chromium --viewport-size=1440,1100 "file:///$report" "docs/assets/eval-report.png"
```

The command uses a local absolute `file:///` URL because Playwright needs a browser-readable path.
