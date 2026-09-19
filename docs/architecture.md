# Architecture

## Layers and responsibility

| Layer | Location | Responsibility |
| --- | --- | --- |
| Routing | [`AGENTS.md`](../AGENTS.md), [`docs/README.md`](README.md) | Load only task-relevant instructions. |
| Stable method | `docs/`, including [core audit methodology](audit-methodology/README.md) | Define research principles, modes, audit reasoning, lifecycle, evidence, and curation rules. |
| Curated reference | [`knowledge/`](../knowledge/README.md) | Preserve sourced knowledge and reviewed, generalizable lessons. Time-sensitive records carry verification dates. |
| Specialist method | [`playbooks/`](../playbooks/README.md) | Future focused audit procedures; indexed and loaded on demand. |
| Templates | [`templates/`](../templates/README.md) | Give local records consistent evidence and provenance fields. |
| Per-target work | [`research/`](../research/README.md) | Keep target inputs, working notes, candidate findings, benchmarks, and feedback local by default. |

No runtime service or database is part of this milestone. A future workflow can operate on local files and explicitly choose relevant methods. Keep source evidence linked to the exact target version or commit; a path and line number alone may become stale.

## Information flow

Authorized target or sourced program record → local research record → evidence-backed finding with a status → human test and feedback → reviewed, sanitized lesson or reference. Promotion into `knowledge/` is a deliberate curation action, never an automatic side effect of a promising hypothesis. Git history should show meaningful changes to method and curated knowledge.

A finding can represent a sequence of requests and state changes. Its model identifies actors, objects, entry points, transitions, authorization decisions, and resulting impact. Specialist playbooks may enrich that model later without redefining the lifecycle or asserting confirmation.

Current bounty terms, installation thresholds, and CVE guidance can change. Store such facts in dated, sourced records under the appropriate `knowledge/` area and recheck them before use. Stable research principles remain in `docs/`.
