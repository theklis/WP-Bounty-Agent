# Challenge candidates: phases 9–12

## 9. State a falsifiable hypothesis

Promote an observation only when the target model and trace suggest a concrete security effect. In the [finding template](../../templates/finding.md), name the attacker and required privilege, entry and prerequisites, controlled value or state, target object, expected control, suspected failure, ordered path, and observable impact. Cite supporting source for each material link, identify missing evidence and likely counterevidence, and name the quickest safe way to disprove the claim. A suggestive API call or missing local check is not enough. Prefer a few coherent hypotheses to a list of warnings. Follow the existing [finding lifecycle](../findings.md); this method does not change status meanings.

## 10. Try to break the claim

Before calling a path strong, search upstream, downstream, and in the framework for earlier capability checks, hidden object ownership checks, registration or session restrictions, later canonicalization, token binding, status constraints, alternate filters, duplicate checks, disabled features, and configuration requirements. Test the weakest necessary edge first. Record contrary evidence and the conditions in which it holds. If a required premise fails, mark the specific hypothesis **REJECTED** with its scope; if it remains unknown, keep it a **HYPOTHESIS** and say it is unproven. Rejection is useful evidence about the tested path, not proof that similar code is safe elsewhere. This matches the [learning model](../learning.md).

## 11. Choose where human validation time goes

Prioritize qualitatively using attacker privilege, actual reachability, boundary crossed, potential impact, completeness of source evidence, remaining assumptions, ability to compose with another primitive, and how efficiently a local test can resolve uncertainty. Use **immediate**, **high**, **normal**, or **low/defer**, with a short reason. A low-privilege path to a consequential cross-user or privileged action with a nearly complete trace usually merits earlier testing than a speculative sink. Program relevance may adjust ordering when current, sourced intelligence exists. This priority is a research queue, never CVSS, severity, eligibility, or confirmation.

## 12. Plan a discriminating local test

For a **STRONG CANDIDATE**, use the [validation plan](../../templates/validation-plan.md) to state environment and version, roles/accounts, prerequisite objects and state, baseline/control behavior, request or UI sequence and controlled variation, expected secure and vulnerable outcomes, observable proof, and cleanup. Where relevant, compare own-object success with another user's object being denied; compare valid and invalid token or transition states. Keep tests within authorization. A plan is not an executed PoC; record the actual result and limits only after a human performs it. Only explicit human reproduction can move a finding to **CONFIRMED**.
