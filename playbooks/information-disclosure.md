# Private information and secret disclosure

## What should this actor know?

Load this when responses, exports, logs, debug errors, backups, files, rendered views, or webhooks may expose private object data or secrets. Derive the target's visibility rule: which actor may learn which fields of which object in which state. Distinguish a public identifier or internal path from a credential, customer data, API key, reset token, or backup containing further authority. The seriousness of disclosure depends on the boundary crossed and what the information enables.

## Trace the data and its readers

Follow **protected source → query/object lookup → filtering/redaction → response, file, log, email, cache, or external destination → attacker access**. Inspect list and bulk endpoints, export jobs, download links, error branches, admin previews, and background-generated files; a correctly protected detail view does not secure an alternate export. For multisite or vendor plugins, ensure tenant/site scope survives joins and shared caches. For tokens, record whether the disclosed value remains valid and which consumer accepts it. [Ownership knowledge](../knowledge/wordpress/ownership-and-plugin-models.md), [storage knowledge](../knowledge/wordpress/data-and-storage.md), and [filesystem](filesystem-and-archives.md) help trace different carriers.

Ask whether a seemingly low-value disclosure composes: an order key, user email, object reference, callback secret, or internal endpoint may make another path reachable. Link [tokens](tokens-and-state.md) and [chaining](chaining.md) only when the later authority is evidenced. A predictable ID is not disclosure of a secret by itself; a private ID may still be sensitive when it selects a record that lacks object authorization.

## Disproof and local test

Seek public-by-design fields, object-aware access checks, redaction, signed or expiring downloads, nonpublic storage, and error handlers that omit sensitive details. Verify whether the stated attacker can actually read the response/file; a server log inaccessible to them does not establish attacker disclosure. A strong candidate needs exact data, reader reachability, the violated visibility rule, and observable exposure or usable derived authority.

In a local test, create distinct actors and recognizable disposable records. Compare permitted and denied reads, exports, and errors; inspect the exact bytes visible to each. Do not include real credentials or private client data in findings. If a revealed token is claimed to enable takeover or mutation, validate that separate consume step under [authentication/recovery](authentication-and-recovery.md) or [authorization](authorization-and-isolation.md).
