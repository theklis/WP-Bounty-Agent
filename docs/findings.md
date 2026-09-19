# Finding lifecycle

A finding is a testable claim about one complete security path or attack chain for a specified target version. Keep the working record under local `research/findings/`; use the [template](../templates/finding.md). A finding may link multiple handlers, requests, users, objects, and persisted states. Its status describes validation, not severity.

| Status | Meaning | Evidence to enter |
| --- | --- | --- |
| **OBSERVATION** | Directly noticed code or behavior with no complete vulnerability claim. | Exact source or local behavior reference, target version, and what was seen. |
| **HYPOTHESIS** | A plausible attack path with unresolved premises. | Proposed actor, entry, control, boundary, action, impact, assumptions, and a falsification test. |
| **STRONG CANDIDATE** | Source evidence supports a complete plausible path and no known blocking check remains. | Reachability, attacker control, relevant transformations, authentication, authorization, object ownership/isolation, and request integrity where applicable, expected impact, and explicit remaining manual proof. |
| **CONFIRMED** | A human researcher reproduced the security effect under recorded conditions. | Human validation record: tester, date, target version/configuration, steps, observed result, evidence, and impact limits. No automated upgrade. |
| **REJECTED** | A required premise failed or the claimed impact did not follow. | Failed premise, counterevidence or test result, version, and what remains useful. |

Normal progression is observation → hypothesis → strong candidate → human-confirmed result. A finding can be rejected from any unconfirmed state. New evidence may reopen a rejected record with a dated explanation; retain its earlier reasoning. A strong candidate can return to hypothesis when a premise becomes uncertain. Human testing can also reject a strong candidate. No label is a substitute for the evidence fields in [the evidence model](evidence.md).

Keep one record per distinct claim, link related records for chains, and avoid duplicating the same uncertain premise as several findings. Do not publish or submit from a draft record without the researcher's own review of scope, impact, and disclosure rules.
