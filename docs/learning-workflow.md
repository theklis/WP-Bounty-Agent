# LEARN FROM RESULT workflow

Use this Codex-guided workflow when a researcher reports a manual result, corrects an interpretation, identifies an audit miss, or asks to review a learning proposal. Natural language is sufficient; no command parser or automated promotion exists. Apply the [learning model](learning.md), [finding lifecycle](findings.md), and [repository policy](repository-policy.md). Keep filled [lesson proposals](../templates/lesson.md), raw feedback, and supporting evidence under ignored `research/lessons/`; link to existing local audit/finding records rather than copying sensitive material.

## 1. Ground the outcome

Locate the audit, finding, case, and [journal](../templates/journal.md) context, or record what the human has supplied. Identify the target and source version, tested actor and conditions, date, and what the human actually observed. Compare the original hypothesis and validation plan with the outcome. Mark each important premise as correct, incorrect, untested, or newly discovered. Do not fill gaps with an inferred chain or impact. Ask for missing detail only when existing records cannot support the proposed learning.

Update the local finding history where appropriate. **CONFIRMED** still requires explicit human reproduction with the evidence required by the [finding lifecycle](findings.md); a terse confirmation without reproduction detail is an incomplete outcome record. **REJECTED** needs the failed necessary premise and counterevidence. A correction, missed path, or no-finding result may be recorded in the audit/journal without inventing a finding. Keep technical validity separate from current Wordfence eligibility, CVE relevance or assignment, and severity.

| Human input | Learning analysis |
| --- | --- |
| Confirmed finding | Identify the failed boundary, exact preconditions, decisive source and human evidence, competing controls, and the research move that exposed it. For chains, capture each primitive, authority/state transfer, later consumer, and final effect. |
| Rejected hypothesis or correct no-finding | Preserve what looked dangerous, the exact failed premise and tested conditions, the blocking control or alternate explanation, and an earlier discriminating check for future audits. Check whether reachability, attacker control, final sink grammar/context, object binding, token purpose, or framework behavior defeated the path. Retain any independently useful primitive. |
| Researcher correction | Record the correction, mistaken assumption, why the old reading failed, and whether this is target-specific, workflow-level, or a platform fact requiring independent sources. Do not defend the old interpretation or rewrite unrelated knowledge. |
| Missed known vulnerability | Compare the actual path with the prior coverage and candidate decisions. Locate the missed entry family, actor/object relationship, invariant, state consumer, chain edge, playbook selection, deferred partition, or mistaken falsification. Propose a better search question or second-pass lens, not merely a new checklist item. |

## 2. Propose, then challenge the learning

Create a **PROPOSED** local [lesson record](../templates/lesson.md). State the source outcome and basis, a narrow reusable research move, applicability, a likely falsifier, contrary evidence, and the reason the proposed scope is supported. Distinguish the target-specific fact from any reusable observation, heuristic, or platform claim. A useful proposal may conclude that the outcome belongs only in a sanitized [case](../templates/case.md), with no general pattern yet.

Challenge both directions of overlearning. A rejected path does not make the component or vulnerability class safe; a confirmed path does not make every similar component vulnerable. If one primitive worked but a later ownership or token check stopped the chain, record that split explicitly. Prefer a testable question such as “Does the later consumer re-bind the selected object to the actor?” to a verdict about all implementations. Do not promote by occurrence count. Explain whether support comes from a well-understood case and independent reasoning, multiple independent outcomes, public research, or explicit researcher judgment.

## 3. Review and route

Use these lesson states, separate from finding statuses:

| State | Meaning |
| --- | --- |
| **PROPOSED** | Local draft; not authoritative guidance for future audits. |
| **REVIEWED** | Human has examined evidence, scope, and sanitization; decision or remaining conditions are recorded. Review alone does not authorize curation. |
| **CURATED** | Explicit human approval plus completed checks; sanitized tracked knowledge may be used within its stated scope. |
| **REJECTED** | Proposal declined or unsupported; retain the decision and provenance locally. This does not change the source finding's status. |
| **SUPERSEDED** | Previously curated guidance narrowed or replaced after new evidence; preserve and link its history and successor. |

Review provenance and claim strength; verify the outcome and contrary evidence; check public-source attribution or approved sanitized summaries; remove secrets and private/client details; check licensing/disclosure limits; choose one primary destination in [the knowledge index](../knowledge/README.md); and confirm the record states what should **not** be generalized. A human request to “learn from this” normally authorizes a proposal. Explicit “approve,” “promote,” or “curate” may authorize curation after these checks if evidence is sufficient. Never silently promote a proposal or treat an AI hypothesis as a human outcome. Do not force-add ignored files or create Git commits automatically.

Cases preserve a bounded path and its human result. Patterns generalize a falsifiable trust-boundary or authority-transfer question across applicable architectures. Lessons capture operational improvements to research, prioritization, falsification, and review. A case can link a pattern or lesson without duplicating its text. Target-specific private details remain local even when a sanitized derivative is approved.

If an outcome suggests a stable method or specialist procedure change, record a **METHODOLOGY CHANGE CANDIDATE** or **PLAYBOOK CHANGE CANDIDATE** in the proposal: current weakness, supporting outcomes, proposed wording/action, affected documents, potential downside, and evidence basis. Curation of the lesson does not approve that change. Obtain separate human review before editing [core audit method](audit-methodology/README.md) or [specialist playbooks](../playbooks/README.md). A platform-semantic correction likewise needs appropriate platform sources and review before changing [WordPress knowledge](../knowledge/wordpress/README.md).

## 4. Use and revise curated guidance

During later audits or hunts, retrieve only relevant **CURATED** records by architecture, actor/object boundary, selected playbook, feature, or workflow question. Apply their stated preconditions and actively check their counterexamples. Do not load all cases into every audit or use proposed lessons as established facts.

When a later outcome conflicts with curated guidance, link the two records and check version, actor, preconditions, control placement, and source quality. Narrow or correct the older lesson; if replaced, mark it **SUPERSEDED** and link the successor. Keep the earlier rationale and review decision visible. Treat changing bounty rules in dated [intelligence](current-intelligence.md), and keep CVE assignment and severity assessment separate from the technical lesson.
