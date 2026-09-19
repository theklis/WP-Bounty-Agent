# Request integrity and CSRF

## Can an attacker origin induce the action?

Load this for a consequential browser action that may use a victim's ambient cookies or session. Derive the invariant: a cross-origin initiator must not be able to make the victim perform this particular state change without an appropriate request-integrity decision. First establish victim role/session, reachable endpoint and method, accepted content type and parameters, browser request behavior, and the underlying sensitive effect. A missing nonce is not automatically a CSRF vulnerability if the request cannot be induced or has no meaningful effect.

## Trace the browser path

Follow **attacker-controlled page/link → victim browser request → ambient credentials → route/handler → nonce or equivalent check → action and object permission → state change**. Check alternate GET/POST transports, AJAX, admin-post, REST cookie authentication, form submission, and redirects. A JSON-only endpoint may have different cross-origin constraints from a simple form; SameSite cookies, CORS, custom headers, and request parsing matter only as actually configured and supported in the target browser/environment. Do not assume a method label alone blocks a request. [Nonce semantics](../knowledge/wordpress/nonces-and-tokens.md), [AJAX/admin-post](../knowledge/wordpress/ajax-and-admin-post.md), and [REST](../knowledge/wordpress/rest-api.md) supply platform specifics.

Separate request integrity from authentication, action authorization, and exact-object ownership. A valid WordPress nonce may support the anti-CSRF decision but is not a capability or owner check; a capability check may permit the victim's own action while leaving cross-origin initiation possible. Conversely, if the action is intentionally public and uses no ambient authority, a nonce may not be the relevant boundary. Record token exposure and whether the attacker can obtain a suitable nonce under the victim context; public or low-privilege nonces have different meaning from private victim-specific ones.

## Counterevidence and local test

Seek strict request parsing, effective nonce/referer defenses, non-ambient authentication, browser-enforced barriers, and a harmless or blocked action. A strong CSRF candidate needs a plausible cross-origin request under the stated victim identity plus observable unauthorized initiation of a consequential action. The severity follows that action, not the absence of a token.

In a local test, use a separate attacker-origin page and a signed-in test victim; compare the induced request with an intentional same-origin request, inspect which cookies/headers travel, and record the resulting object state. Use only authorized test accounts and restore state. If the action also crosses another user's object boundary, link [authorization](authorization-and-isolation.md) as a distinct premise.
