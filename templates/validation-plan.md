# Human validation plan: <finding ID>

Fill in ignored `research/` for a [STRONG CANDIDATE](finding.md) and use with the [VALIDATE workflow](../docs/source-audit/manual-validation.md). This is an authorized local walkthrough for the researcher, not evidence that any step succeeded. Link the audit/finding records rather than duplicating their evidence ledger.

- Finding/audit IDs, exact target version/source, and key source references: `<...>`
- Why test this first; main uncertainty: `<...>`
- Expected setup difficulty / validation effort: `LOW | MEDIUM | HIGH — <short reason for each; not severity>`

## What this feature does

`<Purpose, ordinary users, objects, normal workflow, and why this boundary matters. Define plugin-specific terms.>`

## What we are testing

`<In 2–5 plain sentences: actor → controlled input/state → expected control → suspected failure → effect. State what remains unproven.>`

## What you need

- **Required:** `<verified plugin/settings/environment version, named actor accounts, objects/state, and local authorization>`
- **Helpful:** `<Burp, separate browser profiles, mail capture, local database view, etc., only where useful>`
- **Unknown setup:** `<what must be discovered before a meaningful test; do not guess>`

## How to reach it

`<Evidence-backed UI path or registration/request route. If the UI path is unknown, say how to discover the normal request in the running plugin.>`

## Necessary premises and test order

| ID | Necessary premise / chain bridge | Source support or unknown | Cheapest discriminating local check |
| --- | --- | --- | --- |
| P1 |  |  |  |

## Step-by-step validation

Group only the needed actions into checkpoints. Number every action. Start with an unchanged legitimate baseline when applicable; change one security-relevant value at a time. Identify which actor owns each session, nonce, token, and object without copying secrets into this plan.

### Checkpoint 1 — <reachability and baseline>

1. `<...>`
2. `<...>`

**If this happens:** `<meaningful response/state branches and next check; distinguish setup failure from a defeated premise>`

### Checkpoint 2 — <attacker control and boundary>

3. `<...>`

**If this happens:** `<...>`

### Checkpoint 3 — <consumer and final effect, only if needed>

4. **Write phase:** `<which actor writes which state and where>`
5. **Persistence check:** `<how to verify that exact state was stored>`
6. **Consumer phase:** `<which later request, render, or job reads it and how to trigger it locally>`
7. **Final effect:** `<which observation proves or defeats the claimed authority transition>`

**If this happens:** `<...>`

Remove Checkpoint 3 when no stored or deferred bridge is part of the claim.

Stop after each checkpoint and invite the researcher to report observed, redacted results before continuing a complex path.

| Human checkpoint / date | Observed result and local evidence reference | Premise resolved, still unknown, or next check |
| --- | --- | --- |
|  |  |  |

## Outcomes and troubleshooting

- **Vulnerable result:** `<exact observable cross-boundary effect that would support the hypothesis>`
- **Blocking result:** `<specific necessary premise contradicted, under which tested actor/version/configuration; do not call the plugin secure>`
- **If it does not work:** `<hypothesis-specific checks for actor, feature, nonce/request shape, object binding, upstream control, deferred trigger, or version before interpreting failure>`

## Evidence to save and researcher result

- Save: `<baseline and changed request/response with secrets redacted; actors/roles and object IDs; before/after state; source references; each chain bridge; useful screenshot only if needed>`
- Cleanup: `<restore local state or remove test objects>`
- Actual tester/date, steps, observed result, impact limits, and remaining unknowns: `<complete only after human testing in the finding's Human outcome section>`

Only explicit human reproduction can establish **CONFIRMED**. A plan or a failed request cannot do so.
