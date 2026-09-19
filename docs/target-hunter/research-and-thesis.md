# Research architecture and form a thesis

Apply these steps to survivors, narrowing again before source reconnaissance. Depth should be enough to justify an audit investment, not enough to declare a flaw. For each consequential statement, record the source, date, product version, and whether it is documented, observed in source, inferred, or unknown.

## Stages 4–7 — Functional security profile and potential

Explain what the software actually does. Name its **actors** (for example guest, customer, staff, vendor, API client), **objects** (booking, order, file, user, token, project), and consequential **operations** (read, modify, import, approve, refund, invite). Note state and authority: custom roles/tables, ownership relationships, tokens, sessions, payments, integrations, files, and background jobs. Model at least one concrete permitted transition and the boundary it crosses. Do not import a generic vulnerability checklist before this model exists.

Assess attack-surface **richness by boundary**, not endpoint count. Guest or low-privilege actions, frontend object creation, cross-user records, custom identity/authorization, REST/AJAX, uploads, imports, webhooks, payment transitions, and deferred privileged work matter when they connect low-trust control to valuable state. One unusual trust boundary can outweigh dozens of simple routes. Ask which actor can reach the feature and what prerequisite account, licence, role, or external event is required. High-privilege-only functionality may be technically important while offering weaker current Wordfence fit; do not call it safe or invalid for that reason.

Describe the **impact ceiling conditionally**: if this boundary failed, what protected data, account authority, roles, site configuration, filesystem, payment state, API secret, or privileged process might it reach? This is a reason to investigate, not evidence of exploitation. Treat more installs as potential exposure and program context, not as a substitute for the boundary model. Codebase size may affect review cost; it is not a quality score.

## Stages 8–9 — History, saturation, and duplicate risk

Search official [Wordfence vulnerability records](https://www.wordfence.com/threat-intel/vulnerabilities/) and, when useful, [CVE](https://www.cve.org/) or [NVD](https://nvd.nist.gov/) records. Record known counts only with search scope/date, then examine dates, affected versions, attacker prerequisites, vulnerability families, impact, credited researchers, and feature clusters. Check whether a prior issue affects the current major version. A historical case is evidence about earlier code and research attention, not proof of a current bug or present bounty scope.

Interpret both abundance and absence. Repeated findings may indicate complex or weak boundaries **and** heavy researcher attention. Sparse findings may mean maturity, limited surface, or an underexplored model. Distinguish **research activity** from **research completeness**: identify which features/classes have recent public coverage and which important boundaries have little visible coverage. Consider recent disclosure density, distinct researchers, public writeups, and patch streaks. Describe duplicate risk as **LOW**, **MODERATE**, **HIGH**, or **UNCLEAR**, with evidence and a caveat that private reports are invisible. Never assign a numeric duplicate probability or infer that all bugs are found.

## Stages 10–11 — Change and practical testability

Review dated changelogs, releases, and, when available, official Git/SVN diffs for newly introduced or refactored security-sensitive workflows: roles, REST/AJAX, registration, import/export, payments, storage migrations, WooCommerce changes, webhooks, tokens, and jobs. State **what boundary changed** and which version contains it. A recent release alone is not a vulnerability signal. Look for novelty in custom models or integration between previously separate systems, not obscurity for its own sake.

Assess **LOW**, **MODERATE**, or **HIGH** local research friction: complete legitimate source, runnable version, free/premium feature match, accounts/roles and test data, dependencies, service credentials, licence gates, setup time, and documentation. Explain the blocker or workaround that is actually authorized. Do not describe premium functionality as locally testable because a free shell exists. A high-friction candidate may still rank well if a consequential, underexplored boundary justifies the cost.

## Stage 12 — Reconnoiter only strongest source candidates

For a small surviving set, inspect official public source at **structure and registration depth**: modules, rough size, AJAX/REST registration, custom models/tables/roles, import/export, token, payment/webhook, file, and background-job components. Sample only enough code to confirm or reject the architectural thesis; note exact repository/ref and paths. Do not trace a complete exploit chain, develop PoCs, run a full audit, or inspect every handler. Keep downloads and indexes in ignored `research/targets/`, and target source read-only.

An entry point, missing check, or dangerous sink observed here is at most a **POTENTIAL AUDIT LEAD**: cite its location, state the untested reachability/control/impact premises, and defer it to [core audit methodology](../audit-methodology/README.md). Do not create a finding or upgrade a status from reconnaissance alone.

## Stage 13 — Write the attack-surface thesis

In a short paragraph, join the target's purpose, actors, objects, attacker-accessible interactions, valuable authority/state, distinctive trust boundaries, recent changes, prior research coverage, source/testability, and strongest unresolved question. Say **why this target may still have unexplored depth** and what evidence would weaken the thesis. Select only a few relevant [specialist playbooks](../../playbooks/README.md), each tied to a real feature. A thesis explains why mistakes could matter; it never states that a vulnerability exists. Compare it with the best alternative target rather than writing isolated praise.
