# Tokens, secrets, sessions, and stored authority

## Define what possession grants

Load this when reset/invitation links, API keys, order keys, magic links, bearer tokens, custom cookies, session IDs, transients, or queued state influence authority. For each token, derive who may issue it, for which actor/object/action, who may learn it, and what the consumer should grant. Separate a locator from a credential and a WordPress nonce from a bearer secret: a nonce primarily supports request integrity, not authentication, authorization, ownership, or single use. Token opacity or unpredictability does not repair a missing object permission check.

## Follow issue → leak/control → consume

Trace **generation → binding to user/object/purpose/environment → storage/delivery → disclosure or attacker control → transformations → every consumer → granted action → expiry/revocation/replay**. Include URL logs, HTML, exports, emails, API responses, backups, database state, and cross-handler copies when reachable by the stated attacker. Check token-to-user and token-to-object mapping at consumption, not just issuance; a second endpoint may accept a token for a substituted object. A temporary key can outlive its intended request or be reused by a privileged background worker. [Nonce/token knowledge](../knowledge/wordpress/nonces-and-tokens.md) and [deferred-work knowledge](../knowledge/wordpress/background-and-rendering.md) provide WordPress semantics.

Look for downgrade paths: a strong credential gets copied into a weaker/public context, a token for one purpose is accepted for another, or a server-side session value chosen by a low-privilege actor is treated as prior authorization. For custom sessions, identify creation, fixation/rotation, binding to the authenticated principal, and invalidation after account changes where relevant. Pair with [authentication/recovery](authentication-and-recovery.md), [commerce](commerce.md), or [chaining](chaining.md) only for actual downstream consumers.

## Disproof and validation

Seek purpose- and object-bound comparisons, unguessable values with controlled distribution, session linkage, expiration, revocation, one-time consumption where intended, and independent permission checks. A disclosed token is not automatically exploitable if it has no usable consumer or is bound to an inaccessible principal; replay is not a flaw when repeated use is intended or harmless. A strong candidate needs evidence of attacker acquisition/control, accepted consumption under stated conditions, and a security effect.

In an authorized local test, compare the right versus wrong user/object/purpose, expired versus live token, and first versus repeat use. Record which authority each successful consume step actually grants. Do not fabricate token-leak or takeover results from source appearance alone.
