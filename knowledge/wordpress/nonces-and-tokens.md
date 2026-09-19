# Nonces, request integrity, and state tokens

## Four independent questions

1. **Authentication:** who is the caller, and how was that identity established?
2. **Authorization:** may that caller perform the action?
3. **Object ownership/isolation:** may they act on this specific record, user, site, or tenant?
4. **Request integrity:** is the request protected against cross-site request forgery (CSRF) where relevant?

A WordPress nonce primarily supports the fourth question. It is action-, user/session-, and time-related, but is not single-use, a secret access token, an authentication proof, a capability check, or an ownership check. Core's default guest nonces share user ID `0` unless customized. Exposure in public HTML or to a low-privilege user changes what possession proves. [Official nonce guide](https://developer.wordpress.org/apis/security/nonces/).

`wp_create_nonce( $action )` creates a token for an action. `wp_verify_nonce()` returns `1` or `2` for valid current/previous ticks and `false` otherwise; the default lifetime spans roughly **12–24 hours**, subject to filters and timing. `check_admin_referer()` and `check_ajax_referer()` are request helpers; the latter checks a nonce despite its name, not the HTTP referrer. Verify the action string, supplied field/header, return handling, and whether code continues after a failed check when termination is disabled. `wp_rest` nonces matter for cookie-authenticated REST requests; they do not authorize the route's business action. [Sources: nonce guide](https://developer.wordpress.org/apis/security/nonces/), [`wp_verify_nonce()`](https://developer.wordpress.org/reference/functions/wp_verify_nonce/), [`check_ajax_referer()`](https://developer.wordpress.org/reference/functions/check_ajax_referer/), [REST authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/). Timing, filters, and REST behavior are version/configuration-sensitive; recheck the target's core source.

```php
// Illustrative only: the nonce protects the request, not order ownership.
check_ajax_referer( 'view_order', 'nonce' );
$order_id = absint( $_POST['order_id'] );
// The caller's right to read this particular order still needs a separate check.
```

**Common mistakes:** treating a valid nonce as administrator status; using one broadly exposed nonce for unrelated sensitive actions; assuming a nonce prevents replay; verifying it but ignoring a `false` result; or omitting CSRF analysis because a capability check exists. Missing nonce is not automatically a vulnerability: determine whether a browser can be induced to make the state-changing request with ambient credentials and what effect follows.

## Identifiers, secrets, and persisted authority

An ID selects a resource. A secret token can grant authority only if the consuming code uses it as a credential and the full scheme protects its generation, distribution, storage, comparison, expiry, revocation, binding, and replay behavior. Order keys, reset or invitation tokens, API keys, session IDs, magic links, and plugin-specific bearer tokens need individual analysis. Do not infer secrecy from an opaque format, nor treat predictability as exploitable without an absent access check. A token can be copied into URLs, logs, email, scripts, or another user's reachable response; trace who can obtain it.

For each state/token path, record **origin → who can control or learn it → storage → consumer → granted authority → lifetime/revocation**. Include cookies, transients, options, meta, and custom tables. One request can store a value that another handler or privileged worker later trusts; see [persistent state](data-and-storage.md) and [background processing](background-and-rendering.md). [Framework references: transients](https://developer.wordpress.org/apis/transients/), [options](https://developer.wordpress.org/apis/options/), [REST authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/).
