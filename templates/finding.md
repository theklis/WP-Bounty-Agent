# Finding: <short title>

- ID: `<local identifier>`
- Target / component / version or commit: `<identify exact code>`
- Research scope and authorization: `<public source, local test, or other permission>`
- Status: `OBSERVATION | HYPOTHESIS | STRONG CANDIDATE | CONFIRMED | REJECTED`
- Overall confidence and reason: `low | moderate | high — <one sentence>`
- Last reviewed: `<date, researcher>`

## Claim and software context

What does this feature do? Which actors and objects exist, who should control them, and what security effect is proposed?

## Attack path

Describe ordered steps, including prerequisite state and any cross-request or cross-feature transition. For each step, identify actor capability, entry point, controlled input/object, transformation and validation, relevant authentication, authorization, object ownership/isolation, and request-integrity checks, sensitive action, and observable result. Link related finding IDs if the path composes with another record.

## Evidence ledger

| Premise | Supported / inferred / unknown / contradicted | Exact source or test reference, version, and explanation |
| --- | --- | --- |
| Reachability |  |  |
| Attacker control |  |  |
| Transformations and validation |  |  |
| Authentication |  |  |
| Authorization |  |  |
| Object ownership / isolation |  |  |
| Request integrity / anti-CSRF |  |  |
| Sensitive action and impact |  |  |

## Uncertainty and falsification

- Required assumptions: `<configuration, role, timing, integration, framework behavior>`
- Missing evidence or contrary evidence: `<state explicitly; say “this remains unproven” when needed>`
- Fastest safe disproof or manual verification: `<steps in authorized local environment>`
- Impact limits and alternative explanation: `<do not overclaim>`

## Human outcome

Complete only after manual review. Tester and date; target version/configuration; reproduction steps; observed result and evidence; impact assessment; or the rejected premise and counterevidence. **CONFIRMED requires this section to document explicit human validation.** Keep previous status changes and reasons in a dated history below.

## History

- `<date — status change, author, evidence/reason>`
