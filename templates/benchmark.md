# Benchmark comparison: <case ID / run ID>

Fill only after the blind artifacts are frozen, their exact file set and SHA-256 hashes verified, and ground truth revealed under the [benchmark workflow](../docs/benchmarking.md). Keep this record in ignored `research/benchmarks/<case-id>/runs/<run-id>/comparison.md`. Preserve the frozen audit unchanged.

- Target/version and complete source digest: `<...>`
- Methodology/tooling commit, dirty state, and curated learning available: `<...>`
- Run conditions at blind freeze: `<model/agent/configuration; reasoning configuration; important tools; actual web/documentation policy; material time/context/effort constraint; human intervention during BLIND; unknown where material and unavailable>`
- Run type and blind integrity: `<historical/negative/synthetic/regression; clean/limited/invalid, reason>`
- Contamination/isolation: `<none known / potential prior knowledge / known-answer / limited file isolation / answer exposed; evidence>`
- Freeze inventory, external timestamped freeze-digest checkpoint, verification date, and blind artifact references: `<...>`
- Ground-truth source, version scope, reveal date, and quality: `<VERIFIED GROUND TRUTH / INFERRED OR INCOMPLETE GROUND TRUTH by premise>`

## Known path and blind disposition

Repeat for each known issue or tested negative path. A negative benchmark can have no vulnerable issue. Match the path and failed/effective control, not merely an advisory title or CWE.

- Truth path: `<actor → entry → controlled data/state → checks → bridge → effect, or exact blocker; cite truth/source>`
- Blind candidate IDs and statuses: `<OBSERVATION / HYPOTHESIS / STRONG CANDIDATE / CONFIRMED only with human reproduction / REJECTED; queue placement>`
- Comparison outcome: `WELL RECONSTRUCTED | PARTIAL PATH | RELATED SIGNAL | MISSED | INCORRECTLY REJECTED | CORRECTLY REJECTED or NOT EXAMINED (negative path)`
- Discovery measurement: `clean | limited by contamination | known-answer regression | invalid — <reason>`
- Why this outcome fits despite any wording/CWE difference: `<...>`

| Reasoning dimension | YES / PARTIAL / NO / NOT APPLICABLE / UNKNOWN | Blind evidence versus truth and rationale |
| --- | --- | --- |
| Exact target/version/source identity |  |  |
| Relevant feature and entry or deferred consumer mapped |  |  |
| Actor and prerequisites correct |  |  |
| Attacker-controlled primitive identified |  |  |
| Failed boundary or effective blocking control understood |  |  |
| Cross-request/state or authority bridge reconstructed |  |  |
| Final sensitive effect understood |  |  |
| Relevant counterchecks and falsification examined |  |  |
| Candidate survived or was rejected appropriately |  |  |
| Reached human-validation queue where warranted |  |  |
| Qualitative priority likely to receive researcher attention |  |  |
| SECOND PASS contribution and coverage change |  |  |
| Relevant subsystem coverage and material evidence sufficient |  |  |

For a chain, list each necessary edge and distinguish found primitives from a missed or contradicted bridge. Say whether SECOND PASS first found or materially strengthened the path.

| Necessary edge or control | Ground-truth evidence/quality | Blind evidence/status | Missed, inferred, or contradicted premise |
| --- | --- | --- | --- |
|  |  |  |  |

## Other blind candidates and false positives

Absence from the advisory is not disproof. Use **DISPROVED FALSE POSITIVE** only when a necessary premise is actually defeated; keep reasonable unknowns **UNRESOLVED**.

| Blind candidate ID | Post-reveal disposition: SUPPORTED / DISPROVED FALSE POSITIVE / UNRESOLVED | Failed premise or remaining uncertainty and evidence | Escalation cause, if disproved |
| --- | --- | --- | --- |
|  |  |  |  |

- Verified false-positive burden and unresolved candidates: `<counts with denominators and evidence; advisory absence is not disproof>`

## Diagnosis and report

### What the audit got right

`<specific feature, surface, primitive, control, or second-pass success>`

### What it missed

`<specific missing edge, actor/object, consumer, control, or coverage; diagnostic miss categories and evidence>`

### What it got wrong

`<incorrect rejection/escalation and disproved premise; leave genuinely unresolved candidates unresolved>`

### Why, and what would have found it earlier

`<root reasoning failure or success; reusable discriminating question, not an endpoint-specific rule>`

### Proposed learning and regression plan

`<local PROPOSED lesson/pattern/change-candidate link via LEARN FROM RESULT; no auto-curation>`

`<same-target rerun labelled REGRESSION / KNOWN-ANSWER, or different unexposed target for clean discovery retest; retain prior run>`
