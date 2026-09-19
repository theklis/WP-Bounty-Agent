# wp-bounty-agent

`wp-bounty-agent` is the planned foundation for an AI-assisted research partner for legitimate WordPress vulnerability research, with an initial emphasis on potential Wordfence Intelligence bug bounty and CVE-relevant work. It is designed to help an experienced researcher understand plugins, form testable security hypotheses, and prioritize manual verification. It does not declare vulnerabilities on its own.

## Intended workflow

Start with a permitted public source tree or local test target. Understand the plugin's purpose, actors, data objects, and trust boundaries. Map reachable features, trace complete paths through code and state, and write evidence-backed hypotheses with explicit missing proof and ways to falsify them. A human researcher reproduces and assesses impact before any finding becomes **CONFIRMED**. Confirmed and rejected results may later become reviewed, reusable lessons.

The planned modes are [TARGET HUNT, AUDIT, DEEP DIVE, CHAIN REVIEW, SECOND PASS, BENCHMARK, and LEARN FROM RESULT](docs/modes.md). They are descriptions of future workflows, not available commands. Source understanding and plugin-specific business logic take priority over generic vulnerability checklists. The repository will retain inspectable methodology and knowledge; it does not retrain an AI model.

## Current status

**Milestone 1 — Foundation** provides documentation, lifecycle and evidence models, templates, and protected local workspace conventions. **Milestone 2 — WordPress security knowledge** adds a [selectively loaded, source-backed reference](knowledge/wordpress/README.md) for security reasoning. There is no scanner, target hunter, source-audit engine, benchmark runner, integration, or automatic learning mechanism yet. See the [roadmap](docs/roadmap.md) for later milestones.

## Future usage examples

These illustrate intended requests to a future Codex session; no CLI is implemented:

- “Audit this locally supplied plugin source tree; start by explaining its actors, objects, and trust boundaries.”
- “Deep dive into the REST endpoints and trace object-level authorization.”
- “Review these two candidate paths for a multi-request attack chain.”
- “Record my manual rejection of this hypothesis and propose a general lesson for review.”

## Navigate

Read the [documentation index](docs/README.md) for the smallest relevant set of instructions. [Knowledge](knowledge/README.md) holds curated reference material; [playbooks](playbooks/README.md) will hold specialist methods; [research](research/README.md) is a local, ignored workspace. Repository safety and curation rules are in the [repository policy](docs/repository-policy.md).
