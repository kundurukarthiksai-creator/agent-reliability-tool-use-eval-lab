# Interview Walkthrough

## Thirty-Second Version

Agent Reliability and Tool-Use Eval Lab is a deterministic evaluation system for tool-using agents. It tests whether a planner chooses the right tool, records the tool-call trace, scores structured output, and publishes reviewer-friendly reports. The default path runs without API keys, which keeps the core reliability claims reproducible in CI.

## Problem

Many agent demos look convincing because the final answer reads well. That does not prove the agent selected the right tool, passed the right inputs, handled missing data, or exposed why a failure happened.

This project narrows the problem to inspectable tool-use behavior:

- task fixture;
- planner decision;
- selected tool;
- tool-call trace;
- assertion-level scoring;
- failure category;
- public report.

## Design Choices

- Use deterministic fixtures so CI can verify behavior without paid model calls.
- Separate planner selection from tool execution so wrong-tool failures are visible.
- Keep tool outputs structured so assertions can check exact fields.
- Publish generated artifacts to a no-key static demo so reviewers can inspect evidence without running the app.
- Keep the optional OpenAI planner adapter outside the default CI path.

## Tradeoffs

- The default planner is rule-based, which is less impressive than an LLM demo but much easier to verify.
- Synthetic fixtures reduce real-world messiness, but they make the evaluation path public-safe and repeatable.
- The corpus is focused instead of broad; this makes the current claims honest and testable.
- The static demo favors inspection over flashy interaction.

## Current Proof

- `42/42` deterministic tasks pass.
- `8` local tools are exercised.
- `42/42` tool-call traces are recorded.
- The strict quality gate requires full pass rate, full average score, zero failed tasks, and no non-passing failure categories.
- GitHub Actions verifies the deterministic path.
- GitHub Pages publishes the public demo.

## Strong Interview Answer

I would describe the project as an eval harness, not a chatbot. The key design decision was to make tool-use behavior auditable. Each task has an expected tool, structured input, and assertions over structured output. The runner asks a planner to choose a tool, executes that tool, records a trace, and scores the result. If something fails, the report separates tool-selection failures, tool-execution failures, and output-assertion failures.

The main tradeoff is that the default planner is deterministic. That is intentional because the baseline needs to run in CI without API keys or flaky model calls. I added an optional OpenAI planner adapter for manual experiments, but kept it out of the default proof path. That way the public project proves reproducible infrastructure first, and LLM experiments can be layered on later without weakening the baseline.

## Good Follow-Up Questions

- How would you expand this from synthetic fixtures to real-world tasks?
- How would you compare multiple planners fairly?
- How would you prevent the eval corpus from becoming stale?
- What should fail the quality gate?
- How would you run larger experiment sweeps on ASU Sol later?

## Honest Limits

- This is not a research benchmark.
- This does not prove universal agent reliability.
- The default planner is not an LLM planner.
- The fixtures are public-safe and synthetic.
- Larger scale experiment sweeps are future work.
