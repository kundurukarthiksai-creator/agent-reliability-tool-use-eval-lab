# Product Steering

## Purpose

Agent Reliability and Tool-Use Eval Lab evaluates whether an agent can choose the right tool, call it with structured input, and produce supported output.

## Audience

Primary audience:

- SWE internship recruiters who need quick proof that the project is more than a chatbot.
- Engineers who care about testing, observability, and agent reliability.
- Students and builders learning backend, AI tooling, and evaluation discipline.

## Positioning

The project should communicate:

- deterministic evaluation before generative polish;
- tool-use traces over vague chat transcripts;
- reproducible reports over screenshots alone;
- honest limitations over inflated claims.

## Non-Goals

- Do not turn the first screen into a generic AI chatbot.
- Do not optimize for profile language before the project has proof.
- Do not add paid API dependency to core tests.
- Do not claim production usage unless it is true and public-safe.

## Public-Ready Bar

The project is not public-profile ready until it has:

- passing CI;
- clear README;
- sample eval report;
- known limitations;
- at least one screenshot or report artifact;
- no required secrets for the default path.
