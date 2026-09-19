# AJAX and admin-post dispatchers

## `admin-ajax.php`

WordPress dispatches the request's `action` to `wp_ajax_{$action}` for a logged-in caller and `wp_ajax_nopriv_{$action}` for a guest. Both hooks can be registered for the same action. Registration determines which login branch can reach a callback, **not** whether the actor may perform the operation or access the selected object. A low-privilege logged-in user can reach a `wp_ajax_*` handler unless the callback or downstream code imposes a narrower rule. [Sources: [AJAX handbook](https://developer.wordpress.org/plugins/javascript/ajax/), [`wp_ajax_{$action}`](https://developer.wordpress.org/reference/hooks/wp_ajax_action/), [action reference](https://developer.wordpress.org/apis/hooks/action-reference/)].

For each registered action, trace **actor → action name → request fields → nonce/request-integrity check → capability → object relationship → read/write → downstream calls → response**. Check whether the callback uses `$_REQUEST`, whether a failed nonce check terminates, and whether response helpers end execution. `check_ajax_referer()` alone is not a permission or ownership decision. A JSON success response may reveal sensitive data even with no write. [Source: [`check_ajax_referer()`](https://developer.wordpress.org/reference/functions/check_ajax_referer/)].

Review shared state across handlers. A public or low-privilege action might store an identifier, option, transient, or token that a separate privileged-looking action later consumes. Neither handler alone may contain the whole path. Trace both registration conditions and the actor allowed at each step; persisted values do not become trusted because they were read from the database. [Related: state and tokens](nonces-and-tokens.md), [data and storage](data-and-storage.md).

## `admin-post.php` and admin hooks

`admin_post_{$action}` is for authenticated requests and `admin_post_nopriv_{$action}` for guests. The GET/POST `action` selects a handler. The `admin-` prefix does not mean Administrator-only; the authenticated branch admits other logged-in roles. `admin_init` or a menu callback also needs a concrete reachability and permission analysis; UI visibility is not a substitute for handler checks. [Sources: [`admin_post_{$action}`](https://developer.wordpress.org/reference/hooks/admin_post_action/), [action reference](https://developer.wordpress.org/apis/hooks/action-reference/)].

For state-changing browser requests, assess CSRF protection separately from action permission and object ownership. After a handler redirects, inspect the destination and whether execution terminates. An admin page can contain forms sent to a different dispatcher, so trace the actual receiving callback, not just the page that renders the form. [Related: nonces](nonces-and-tokens.md), [redirects](files-and-network.md).

**Counterevidence to seek:** registration absent in the tested configuration; an earlier hard stop; action-specific capability and object check applied to the same resolved record; or inputs that cannot reach the alleged state change. A public AJAX action may be entirely intentional.
