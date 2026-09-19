# Using current intelligence

Use this layer only when a research decision depends on changing program or CVE rules. Technical findings still follow the [evidence model](evidence.md) and [finding lifecycle](findings.md). Program scope, CVE relevance, CVE assignment, and severity are separate decisions. A current snapshot is a dated aid, not a standing eligibility verdict.

## Record status

| Status | Meaning |
| --- | --- |
| **CURRENT AS OF** date | Primary source checked on that date for the stated scope; later changes remain possible. |
| **RECHECK REQUIRED** | A decision needs fresher evidence, a source conflicts, or a condition may have changed. Do not make a final eligibility or routing claim from this record. |
| **UNVERIFIED** | Claim lacks direct current primary-source support. Do not apply it. |
| **SUPERSEDED** | A newer identified record replaces this one; preserve the old record and link both directions. |
| **HISTORICAL** | Evidence of past practice or a bounded event, not current scope. |

Record the issuer, source title and URL or identifier, retrieval date, explicitly stated effective date, population and conditions, and any supersession. Keep **Source says** separate from **Research interpretation** and unresolved questions. The [intelligence template](../templates/intelligence-record.md) is for new records; the [bounty](../knowledge/bounty/README.md) and [CVE](../knowledge/cve/README.md) indexes route to current snapshots.

## Revalidation

Recheck the relevant primary pages and target facts before TARGET HUNT ranking, a consequential scope statement, a bounty value discussion, a submission, or a CNA routing recommendation. Recheck sooner after a program notice, changed tier, changed product availability or install count, new CVE rules, or conflicting source. Record the new verification date and what changed. Do not invent a fixed expiry interval when none is supplied.

Temporary events require an official source, explicit applicability, and stated start/end or equivalent validity conditions. If the end passed, mark the event **HISTORICAL**. If the end or current operation cannot be established, mark it **RECHECK REQUIRED** and do not apply it. Historical vulnerability database entries describe prior cases, not current program rules.

For future historical case study or benchmark records, retain provenance, affected versions, CWE where supported, attacker prerequisites, CVE ID and state if any, researcher credit, and relevant dates. These fields aid comparison without importing a database or converting a past case into present scope.

When official sources disagree, record both statements and their dates, check for explicit supersession and operative terms, and retain the conflict if unresolved. The affected decision is **RECHECK REQUIRED**; never select the more favorable rule by default. Filled target assessments and private verification notes belong in ignored `research/`.
