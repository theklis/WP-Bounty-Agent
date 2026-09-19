# Review coverage and stop: phases 13–15

## 13. Track meaningful coverage

Track actors, major features, entry-point families, sensitive objects, trust boundaries, high-impact operations, state/token systems, integrations, relevant vulnerability families, and cross-handler chains. For each scoped item, use **mapped** (identified only), **reviewed** (main paths and checks inspected), **deep-reviewed** (material cross-file/state paths and counterevidence traced), **deferred** (reason and trigger to revisit), **not applicable** (reason), or **unresolved** (specific missing evidence). Record source/version references and next questions in the [audit record](../../templates/audit-record.md). One item may need more than one row if different actors or operations have different depth.

Coverage is a map of what reasoning occurred, not a percentage of files opened or a claim that all branches are safe. Do not invent numerical completeness. Ask which important boundary, actor, state consumer, or high-impact action remains outside the reviewed scope. Defer low-value branches consciously and make the consequence visible.

## 14. Change perspective for a second pass

For a serious audit, make a conceptual second pass after the first candidate and coverage review. Choose an attacker perspective the first pass underused: guest, low-privilege account, owner of one object targeting another, stored-content controller, API client, webhook sender, tenant member, or site/network boundary actor. Also change analytical direction: start from a sensitive effect and trace backward; from issued secrets to consumers; from low-trust writes to privileged reads; from ownership decisions to later object substitution; or from background jobs to their inputs. Ask explicitly: **Which first-pass assumption could be wrong?**

Record the changed lens, paths revisited, newly found surfaces or checks, hypotheses added/rejected, and coverage deltas. A repeat reading of the same files with the same assumptions is not a second pass. If a newly found dependency changes the model, return to the earlier phase and update the record.

## 15. Stop honestly for the stated scope

An audit may stop when major scoped features and actors are mapped; important boundaries, entry families, and high-impact operations have appropriate review depth; strong candidates have a human validation plan and other hypotheses retain explicit unresolved premises; the second pass is recorded for a serious audit; and blind spots, exclusions, and deferred paths are stated. These are judgement checks, not a guarantee of exhaustive security. If time or access ends earlier, document the narrower completed scope and what remains.

The final local summary should identify target/version/scope, major architecture and deep-dive themes, meaningful surfaces reviewed, candidate statuses and human-test needs, rejected paths with counterevidence, second-pass changes, and unresolved or deferred areas. Say **“no vulnerability identified in the reviewed path”** when that is all the evidence supports. Never label the product “secure” from incomplete review, and never imply a source-backed candidate has been human-confirmed.
