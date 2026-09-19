# Privilege and security-sensitive configuration

## What authority changes?

Load this when user creation/update, role assignment, capability mutation, plugin staff roles, options, user/post/term meta, or custom settings affect future authority. Derive the invariant for each transition: which actor may assign which role, update which user's field, or change which site/network setting, and under what state. A writable field is worth deep review when a later consumer gives it security meaning. Treat action permission, exact-user/object ownership, and site or network scope separately.

## Trace durable escalation

Reconstruct **low-privilege entry → controllable field/key/value → validation and authorization → stored change → effective role/capability/configuration → newly reachable privileged operation**. Inspect mass assignment and partial profile updates: can the client choose `role`, capabilities, user ID, owner, default role, recovery email, plugin staff assignment, or a security option independently of allowed fields? Follow custom roles through installation or upgrades and check whether a role name comparison reflects effective capabilities. For multisite, distinguish per-site authority from network settings and super-admin effects. [Identity/capabilities](../knowledge/wordpress/identity-and-capabilities.md) and [ownership/multisite](../knowledge/wordpress/ownership-and-plugin-models.md) give platform semantics.

For configuration and meta, identify key namespace, object/site scope, writer, reader, and effect. High-value consumers include registration defaults, file handling, recovery destinations, integration secrets, endpoints, template/rendering choices, and background jobs. An arbitrary meta or option update is not automatically severe: ask what **specific** later behavior it changes. A stored value can be inert until another handler reads it under greater authority; then use [chaining](chaining.md). [Data/storage knowledge](../knowledge/wordpress/data-and-storage.md) distinguishes API storage from permission enforcement.

## Counterevidence and test

Seek server-side field allowlists, immutable role assignments, object-aware capability checks, restricted option-name maps, type normalization, and site-context checks. Check whether the alleged capability is actually granted in the target configuration and whether the changed setting is later consumed. A strong candidate needs the full authority change and a meaningful newly permitted operation, not merely a successful update call.

In a local test, compare an allowed profile/settings edit with an attempted privileged field or another user's record. Observe the persisted value and then the effective capability or downstream behavior; restore test roles/settings afterward. If the later consumer is unknown, keep a configuration-write hypothesis rather than claiming escalation.
