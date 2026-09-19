# Benchmark manifest: <neutral case ID>

Coordinator-only record for ignored `research/benchmarks/<case-id>/manifest.md`. **Do not show or make this file readable to the blind auditor.** If contexts share filesystem access, hold coordinator-only details outside that shared workspace and place the completed manifest here after freeze. Copy only the blind handoff fields below into a fresh Context A; keep answer-bearing details and even the case type out of that context. Follow the [benchmark workflow](../docs/benchmarking.md).

## Blind handoff fields only

- Target source path and exact version/commit: `<...>`
- Neutral source origin and complete SHA-256 archive/tree digest: `<official/source location without advisory or fix clues>`
- Authorized local scope and permitted setup assumptions: `<...>`
- Allowed public information and web-research policy: `<platform/API docs allowed; target-specific vulnerability research barred by default>`
- Output paths for normal Source Audit records: `<research/audits/<audit-id>/ and linked research/findings/<audit-id>-*>`
- Neutral audit request: `<perform normal FULL AUDIT; do not imply issue count/type>`

## Coordinator-only preparation

- Case ID and type: `historical known vulnerability | rejected/false-positive | synthetic reasoning | regression/known-answer`
- Preparer/date and source acquisition/provenance: `<...>`
- Original archive or read-only tree; extracted root; exact version and metadata conflicts: `<...>`
- Source digest method and completeness; source location: `<...>`
- Ground-truth path: `ground-truth/truth.md` `<copy the separate ground-truth template only after preparation; keep title/path neutral>`
- Ground-truth provenance/quality kept outside blind handoff: `<references; unknowns; no answer text here if this file might leak>`
- Spoiler screen: `<source filenames, tests, changelog, package metadata, prior conversation/curated knowledge>`
- Contamination/isolation: `none known | POTENTIAL PRIOR-KNOWLEDGE CONTAMINATION | REGRESSION / KNOWN-ANSWER | LIMITED FILE ISOLATION | answer exposed — <why>`
- Case state: `PREPARED | BLIND AUDIT | BLIND FROZEN | REVEALED | COMPARED | COMPLETE | INVALID`

## Run register

| Run ID / audit workspace | Method/tooling commit and dirty state | Curated learning available | Run conditions at blind freeze | Blind start / freeze UTC | Snapshot and freeze verification | Contamination and validity | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

Run conditions: `model/agent/configuration: <...>; reasoning configuration: <...>; important tools: <...>; actual web/documentation policy: <...>; material time/context/effort constraint: <...>; human intervention during BLIND: <...>`. Use `unknown` for material unavailable values; do not infer internal settings or require precise timing/token data.

Never overwrite a prior run. A same-target rerun after a revealed answer is a known-answer regression, not an independent discovery test.

## Freeze record shape

Copy this section to `runs/<run-id>/freeze.md` only after completing the blind audit and snapshot. Record case/run IDs; original audit and finding workspace paths; UTC freeze time; target version and complete digest; method/tooling commit and dirty state; run conditions; contamination declaration; and verification result before reveal. Inventory **every** file under `blind/` in sorted relative-path order:

| Relative path under `blind/` | SHA-256 of file bytes |
| --- | --- |
|  |  |

An optional aggregate digest covers canonical `path<TAB>digest<LF>` rows. Before reveal, record `freeze.md`'s SHA-256 in an independent timestamped coordinator checkpoint outside the run directory. Verify that checkpoint, the exact file set, and every hash before revealing truth and when comparing; never revise frozen blind files after reveal.
