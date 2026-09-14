# Project Steering

This project exists to prove reliable tool-use evaluation, not to look like another AI wrapper.

Read these files before making non-trivial changes:

- `.kiro/steering/product.md`
- `.kiro/steering/tech.md`
- `.kiro/steering/quality.md`

Hard rules:

- Keep CI deterministic and free of required API keys.
- Do not replace the deterministic baseline with an LLM-only path.
- Every new tool or planner must add at least one meaningful test.
- Reports must expose failures clearly instead of hiding them behind a single score.
- Do not make production, employer, or benchmark claims that the repo cannot prove.
