# Modes, large targets, resume, and output

All entry intents verify or reuse the same [safe intake](intake-and-workspace.md), source identity, [evidence rules](../evidence.md), and local record. These are natural-language workflows, not command parser syntax.

| Intent | Depth and expected result |
| --- | --- |
| **AUDIT / FULL AUDIT** | Broad [audit orchestration](audit-orchestration.md) across major scoped functions, a challenged candidate queue, meaningful coverage, and a changed-perspective second pass. |
| **QUICK TRIAGE** | Confirm source/version; use optional [navigation helpers](../../tools/README.md) to speed initial inventory and entry mapping; explain purpose, actors, objects, public/low-privilege surfaces, and consequential state/authority transitions; select about 2–5 deep-dive themes, note leads and setup blockers, and recommend whether a full audit is worth time. Label coverage partial; tool output alone is insufficient and does not imply a full audit, finding, or human test. |
| **DEEP DIVE** | Focus on a named component, boundary, feature, candidate, or vulnerability family. Read enough adjacent registration, callers, state, and controls to test the path; update the shared model and scoped coverage. |
| **CHAIN REVIEW** | Start from existing observations/candidates; correlate handlers, requests, actors, tokens, stored state, integrations, and privileged consumers. Evidence every necessary edge and challenge the weakest link. |
| **SECOND PASS** | Use the existing record and [changed-perspective method](../audit-methodology/coverage-and-review.md). Change attacker lens **and** analytical direction; record assumption challenged, paths added/rejected, and coverage delta. Re-reading the same files with the same lens does not qualify. |
| **RESUME** | Verify the source identity and existing record, read current candidate links and coverage/deferred queue, then continue the next unresolved partition without repeating completed work. |

For a human outcome after an audit, follow [LEARN FROM RESULT](../learning-workflow.md); do not auto-curate a lesson. A [BENCHMARK](../benchmarking.md) uses this same Source Audit workflow during its blind phase and keeps ground truth outside that audit context.

## Partition large targets without losing the whole

Keep one overarching `audit.md`. Partition by feature, subsystem, actor/object relationship, entry family, or trust boundary—whichever preserves the meaningful state transitions. Prioritize partitions by reachability and consequence; record **mapped**, **reviewed**, **deep-reviewed**, **deferred**, **not applicable**, or **unresolved** in the existing coverage table with source references and the next question. Link cross-partition writers, consumers, tokens, and findings in the path table. A deferred partition needs a reason and trigger to revisit; file counts and lines of code do not measure security coverage. A long audit may pause with honest partial coverage rather than consuming context on low-value files.

## Resume and version control

The audit record's state (`INITIALIZING`, `MODELLING`, `ANALYZING`, `VALIDATION QUEUE`, `SECOND PASS`, `PAUSED`, or `COMPLETE FOR CURRENT SCOPE`) describes workflow progress, not a finding's lifecycle status. On RESUME: locate `audit.md`; compare original input, archive digest or repository commit/dirty state, complete tree digest where applicable, extracted/source root, and recorded version with the current source; read architecture, selected themes, coverage, linked findings and plans, rejected paths, and last next action. A matching branch or dirty-state flag alone does not prove a mutable tree is unchanged. Recheck any premise affected by a changed environment or source. Continue from the highest-value unresolved row, updating the same record. If source identity changed, follow the [version-change rule](intake-and-workspace.md) before using old line references or results.

Reuse generated inventories and indexes only when the recorded archive digest, commit/source state, and a complete helper source digest still match. If the digest is incomplete, verify skipped material and source identity manually. A matching digest establishes bytes, not index coverage: check `php_text_scan_complete`, skipped paths, and dynamic/wrapped registrations before relying on entry leads. Mark stale navigation data and regenerate after a change; do not carry line references across versions without rechecking source.

## Progress and honest exit

For a substantial audit, tell the researcher when the architecture and main surface map are established, when a deep dive changes the model, when a candidate's key premise remains unresolved, and what the second pass changed. Report research progress, not a stream of opened files; never describe an unperformed test as successful.

A full audit reaches **COMPLETE FOR CURRENT SCOPE** only when major scoped functions and actors are modeled, important entry families and trust boundaries have appropriate review depth, relevant state/token systems and selected playbooks were considered, surviving candidates were challenged, any strong candidates have human validation plans, a changed-perspective second pass is recorded, and blind spots/deferred areas are explicit. The queue may be empty when no candidate survives. If time, access, or evidence ends earlier, use **PAUSED** or a narrower completed scope with the missing work stated.

The final local summary in `audit.md` and the user-facing response should state exact target/version and scope; functional security model; themes and meaningful surfaces reviewed; candidate IDs, status, confidence, priority, weakest premise, and manual validation needs; rejected paths with specific counterevidence; second-pass changes; uncovered or deferred areas; and next research actions. If no strong candidate survives, say **“no vulnerability identified in the reviewed path”** under the recorded conditions. Never call the product secure, invent a finding to fill the queue, or call a source-backed candidate **CONFIRMED** without explicit human reproduction.
