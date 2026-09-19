# Source Audit workflow

Use this **Codex-guided workflow** when a researcher supplies legitimate local WordPress plugin/theme source and asks for AUDIT, QUICK TRIAGE, DEEP DIVE, CHAIN REVIEW, SECOND PASS, or RESUME, or requests `VALIDATE <finding ID>` for an existing candidate. It is an operational route through the approved [Core Audit Methodology](../audit-methodology/README.md), not a command parser, scanner, or claim that source review confirms vulnerabilities. Research only public source or authorized local environments; do not discover or test third-party production sites.

For `AUDIT <path>`: resolve the exact input, follow [intake and workspace](intake-and-workspace.md), create or resume the ignored audit record, then follow [audit orchestration](audit-orchestration.md). Use [modes, resume, and output](resume-and-output.md) when the requested depth differs or the audit spans sessions. A ZIP may be placed in ignored `research/targets/`; an authorized source tree may be supplied by path. Do not modify either source. If no usable source path was supplied, establish it before claiming any source coverage.

| Need | Read or use |
| --- | --- |
| Safe ZIP/tree intake, exact identity, and local layout | [Intake and workspace](intake-and-workspace.md) |
| Practical sequence from structural read through second pass | [Audit orchestration](audit-orchestration.md) |
| QUICK TRIAGE, focused modes, large targets, resume, and exit | [Modes, resume, and output](resume-and-output.md) |
| Researcher-ready candidate test and checkpoint follow-up | [VALIDATE manual walkthrough](manual-validation.md) |
| Research phases and reasoning standards | [Core Audit Methodology](../audit-methodology/README.md) |
| Working record and distinct candidate claims | [Audit record](../../templates/audit-record.md), [finding](../../templates/finding.md), and [validation plan](../../templates/validation-plan.md) |
| Optional ZIP, identity, inventory, and registration navigation | [Safe helper tooling](../../tools/README.md) |

Read [WordPress knowledge](../../knowledge/wordpress/README.md) when platform semantics affect a premise and [specialist playbooks](../../playbooks/README.md) only for selected themes. Apply the [evidence model](../evidence.md) and [finding lifecycle](../findings.md) throughout. Only explicit human reproduction can make a finding **CONFIRMED**. Give the researcher substantive progress updates at architecture, surface, candidate, coverage, and second-pass checkpoints; distinguish work completed from work planned.
