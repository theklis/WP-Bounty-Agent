# Authentication and account recovery

## Identity before permission

Load this for custom login, API keys, application credentials, magic links, cookies/sessions, login hooks, invitation, activation, password reset, or email-change flows. Define the intended principal for each transport and state transition. Derive rules that accepted credentials establish only their intended principal and scope, and that recovery authority reaches only the intended account and action. These are target-specific expectations, not assumptions that every endpoint requires login. Establishing identity never grants permission for every action or object.

## Trace authentication and alternate paths

Follow credential origin, distribution, browser/header transport, validation, token-to-user lookup, session creation, and the WordPress or plugin principal ultimately set. Inspect custom hooks and filters that establish current user, plus alternate REST, AJAX, admin-post, and webhook entry points. Compare branches that use cookies, application credentials, API keys, and custom sessions: does one accept a claimed user ID/email from the request, or skip a check present elsewhere? Test whether identity can change after permission code has run or whether a plugin-defined role is mistaken for a WordPress capability. The [WordPress identity reference](../knowledge/wordpress/identity-and-capabilities.md) and [request model](../knowledge/wordpress/request-model.md) resolve platform questions.

## Trace account recovery as a chain

For reset, email change, activation, invitation, and magic links, map **requester → target account → token creation/storage → delivery destination → who can learn it → expiry/revocation → consumption → account/session effect**. Ask whether a prior profile update can redirect delivery, whether a token is bound to the intended user and purpose, whether target-user substitution occurs after validation, and whether old sessions or tokens remain useful after recovery where relevant. A token leak or weak token property alone is not a proven takeover; show a reachable consume path and actual account authority gained. Use [tokens and state](tokens-and-state.md) for deeper token lifecycle and [privilege/configuration](privilege-and-configuration.md) if recovery changes capabilities.

## Falsification and validation

Look for core authentication behavior, immutable account binding, purpose-specific tokens, hard stops, delivery verification, session invalidation, and restrictions on who can initiate or complete recovery. Distinguish a guest starting a legitimate reset for someone else from the guest gaining control of that account. A strong candidate needs evidence of the stated attacker's credential or recovery control, principal mapping, reachable completion, and consequential account effect.

For local validation, use separate test accounts and compare valid versus wrong-account, wrong-purpose, expired, or reused credentials. Record which principal the system establishes at every step and whether an authenticated session or account change results; do not infer takeover from a successful token lookup alone. [Nonce and token semantics](../knowledge/wordpress/nonces-and-tokens.md) are relevant, but WordPress nonces are not authentication credentials.
