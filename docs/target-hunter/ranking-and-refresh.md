# Rank, compare, refresh, and hand off

## Stages 14–15 — Relative research priority

Rank only after the [functional profiles and theses](research-and-thesis.md) exist. Use **TOP TARGET**, **STRONG TARGET**, **EXPLORATORY**, or **DEPRIORITIZE** as qualitative research priorities, never as vulnerability confidence or a 0–100 score. Weigh current program fit, reachable lower-privilege boundaries, impact ceiling, architectural depth, source/testability, underexplored changes, history, saturation, duplicate risk, friction, and missing evidence. No one dimension decides the order. Explain why target A merits time before B and what fact could reverse that decision.

Choose audit themes from the actual architecture, with a reason for each: for example authorization and isolation for cross-owner objects, tokens/state for invitation flows, or commerce for order transitions. Do not recommend every playbook. A focused hunt and a comparison of user-supplied targets use the same dimensions and evidence standard. If none merits sustained work, say **no strong shortlist** and broaden discovery rather than promoting weak candidates to fill a quota.

## Stage 16 — Deliver a usable audit handoff

A completed [hunt summary](../../templates/target-hunt-summary.md) states research date, constraints and tier status, current source checks and freshness limits, candidates screened and decisive exclusions, normally 3–7 ranked survivors, and one best next target. Each shortlisted [profile](../../templates/target-profile.md) gives exact product/slug/version, authoritative source/download and ref, current install/scope facts with dates, last update, dependencies, local setup and licence limits, actors/objects/workflows, relevant components, prior findings and research saturation, thesis, selected playbooks, uncertainty, and reason for its rank. Include enough detail to open an [audit record](../../templates/audit-record.md) against a specific source version later.

The handoff names **what to audit first** and why. It does not contain a completed Source Audit, exploit claim, automatic bounty verdict, or proof of vulnerability. A candidate that is technically valuable but out of current bounty scope may be noted separately, without mislabeling it a Wordfence priority. Keep all filled material and downloaded source in ignored `research/targets/`.

## Compare specific targets

Given named candidates, verify their identities and current facts, apply the same filters and profiles, and put them side by side on program conditions, boundary quality, attacker accessibility, history/saturation, recent change, testability, and uncertainty. Use a common research date and say when data were checked at different times. Explain the ordering and the strongest counterargument for the winner. Do not select on installs, CVE count, endpoint count, or code size alone.

## Refresh an existing shortlist

Keep the old dated record. Recheck current version, installs, source and product availability, last update, relevant new vulnerabilities/researchers, Wordfence scope and tier conditions, and boundary-changing code or feature changes. Record deltas and classify each thesis **STRENGTHENED**, **UNCHANGED**, **WEAKENED**, or **INVALIDATED**, with reasons. Reorder only if the changes matter; do not repeat the entire discovery funnel when the original model and sources still support it. If the old source/version can no longer be reproduced, mark the handoff stale and resolve that before audit.
