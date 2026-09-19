# Core audit methodology

Use this method for authorized review of locally supplied WordPress plugin or theme source. It defines research decisions, not an executable AUDIT command, scanner, or vulnerability playbook. The phases are a loop: new evidence can change the architecture model, surface map, or earlier candidate. Depth follows the target's functions and trust boundaries; opening every file is not the goal.

| Phases | Read | Working result |
| --- | --- | --- |
| 0–3: preflight, functionality, reachability, boundaries | [Model the target](model-the-target.md) | Security model, deep-dive themes, surface and boundary maps |
| 4–8: state, controls, flows, business rules, chains | [Trace security paths](trace-security-paths.md) | Evidence-linked paths across handlers, requests, and state |
| 9–12: hypotheses, falsification, priority, validation | [Challenge candidates](challenge-candidates.md) | Falsifiable findings and human test plans |
| 13–15: coverage, second pass, exit | [Review coverage and stop](coverage-and-review.md) | Blind spots, changed-perspective review, honest summary |

Use the compact [audit record](../../templates/audit-record.md) only for sections that help the current scope, the existing [finding template](../../templates/finding.md) for each distinct claim, and the [validation plan](../../templates/validation-plan.md) for a strong candidate. Put filled records in ignored `research/`; keep supplied target source read-only. The [journal](../../templates/journal.md) can capture decisions and dead ends without repeating the entire map.

The [research principles](../research-principles.md), [evidence model](../evidence.md), and [finding lifecycle](../findings.md) govern every phase. Load only relevant [WordPress knowledge](../../knowledge/wordpress/README.md) when platform behavior affects a premise. Specialist playbooks may later deepen selected themes; they do not replace this method. A candidate is only as strong as its weakest required link. A complete plausible path can become a **STRONG CANDIDATE**; only explicit human validation can make it **CONFIRMED**.

**Mode use:** AUDIT builds the broad model and selects depth. DEEP DIVE enters at a specific feature, boundary, or path while checking its surrounding model. CHAIN REVIEW joins existing primitives and tests every transition. SECOND PASS changes attacker or analytical perspective and records what the first pass missed. These are method descriptions for future workflows, not commands.
