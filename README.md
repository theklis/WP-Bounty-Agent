# wp-bounty-agent

`wp-bounty-agent` is the planned foundation for an AI-assisted research partner for legitimate WordPress vulnerability research, with an initial emphasis on potential Wordfence Intelligence bug bounty and CVE-relevant work. It is designed to help an experienced researcher understand plugins, form testable security hypotheses, and prioritize manual verification. It does not declare vulnerabilities on its own.

## Intended workflow

Start with a permitted public source tree or local test target. Understand the plugin's purpose, actors, data objects, and trust boundaries. Map reachable features, trace complete paths through code and state, and write evidence-backed hypotheses with explicit missing proof and ways to falsify them. A human researcher reproduces and assesses impact before any finding becomes **CONFIRMED**. Confirmed and rejected results may later become reviewed, reusable lessons.

The [TARGET HUNT workflow](docs/target-hunter/README.md), [Source Audit workflow](docs/source-audit/README.md), [LEARN FROM RESULT workflow](docs/learning-workflow.md), and [blind benchmark workflow](docs/benchmarking.md) are available as Codex-guided methods. [Local helper tooling](tools/README.md) can assist Source Audit navigation. These workflows are not CLI commands. Source understanding and plugin-specific business logic take priority over generic vulnerability checklists. The repository retains inspectable methodology and reviewed knowledge; it does not retrain an AI model.

## Current status

**Milestones 1–6** provide the foundation, [WordPress knowledge](knowledge/wordpress/README.md), [core audit method](docs/audit-methodology/README.md), [specialist playbooks](playbooks/README.md), [dated program intelligence](knowledge/README.md), and [Target Hunter](docs/target-hunter/README.md). **Milestone 7 — Source Audit** makes the method usable against a supplied local source tree or ZIP, with ignored workspaces and resumable records. **Milestone 8 — Safe Helper Tooling** provides optional local navigation. **Milestone 9 — Human-Grounded Learning** adds reviewed result-to-knowledge curation. **Milestone 10 — Blind Benchmarking** evaluates Source Audit with frozen blind results and separate ground truth. There is no scanner, automated hunter, source-audit engine, benchmark runner, integration, or automatic learning mechanism. See the [roadmap](docs/roadmap.md).

## Example requests

TARGET HUNT, local Source Audit, LEARN FROM RESULT, and BENCHMARK requests can be used now as guided workflows. The helper CLI supports only local navigation mechanics:

- “Find a short list of current Wordfence research targets with architectural theses and explain which deserves audit time first.”
- “Audit this locally supplied plugin source tree; start by explaining its actors, objects, and trust boundaries.”
- “Deep dive into the REST endpoints and trace object-level authorization.”
- “Review these two candidate paths for a multi-request attack chain.”
- “Record my manual rejection of this hypothesis and propose a general lesson for review.”
- “Benchmark a prepared historical local source in a fresh blind context, freeze the audit, then compare it with separate ground truth.”

## Navigate

Read the [documentation index](docs/README.md) for the smallest relevant set of instructions. [Knowledge](knowledge/README.md) holds curated reference material; [playbooks](playbooks/README.md) hold specialist methods; [research](research/README.md) is a local, ignored workspace. Repository safety and curation rules are in the [repository policy](docs/repository-policy.md).
