# Repository policy

## Placement

- `docs/` contains stable method and project status.
- `knowledge/` contains intentionally curated, sourced reference material and reviewed lessons. Dated bounty/CVE intelligence belongs here, separate from stable method.
- `playbooks/` contains focused specialist procedures, indexed by topic.
- `templates/` defines record shapes; filled target records belong under `research/`.
- `research/` holds local target sources, archives, notes, candidate findings, benchmark runs, and raw feedback. Its contents are ignored except for its README.

Treat supplied plugin/theme source as read-only unless the human researcher explicitly asks for modification. Reading, indexing, parsing, and executing authorized local test code are permitted; do not silently fix or rewrite the audited source. Put extracted artifacts, analysis, notes, indexes, PoCs, and temporary output in the appropriate local `research/` workspace, not in the target tree.

Do not copy a target source tree, ZIP, raw traffic, exploit artifact, credentials, private client material, or generated index into tracked directories simply to make it accessible to future sessions. A public, redistributable example may be curated deliberately after checking license, provenance, size, scope, and sensitive content. Review every forced Git add; `.gitignore` is a guardrail, not a secret detector. If a secret enters history, remove and rotate it using an appropriate incident process.

## Current information

For changing program terms, eligibility thresholds, CVE guidance, and ecosystem facts, record the primary source, URL or document identifier, retrieval/verification date, applicability, and stale/unknown status. Recheck before making a target or submission decision. Do not copy a transient rule into `docs/` as a timeless instruction. The [intelligence template](../templates/intelligence-record.md) provides fields, not current facts.

## Review before commit

Inspect `git status` and the staged diff. Ensure target data and secrets are absent; links work; claims have provenance; status labels match evidence; and future features are described honestly. Favor small commits that make changes in research method auditable.
