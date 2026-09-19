# REST API security semantics

`register_rest_route()` associates a namespace/path and HTTP method with an endpoint `callback`, a `permission_callback`, and optional argument schemas, validation, and sanitization. Registration normally occurs on `rest_api_init`. Enumerate **all methods** and route variants, including a different callback for read and write. Input can come from URL parameters, query, body, or headers; identify which value ultimately selects an object. [Sources: [`register_rest_route()`](https://developer.wordpress.org/reference/functions/register_rest_route/), [routes and endpoints](https://developer.wordpress.org/rest-api/extending-the-rest-api/routes-and-endpoints/), [schema](https://developer.wordpress.org/rest-api/extending-the-rest-api/schema/)].

## Identity, permission, object

REST authentication establishes a current user where successful. Cookie-authenticated browser requests use a `wp_rest` nonce; without one, the REST API treats the request as unauthenticated even if browser cookies exist. Application Passwords (core since **5.6**) and plugin-defined schemes are other possible identities. A REST nonce is not a capability check. Trace custom authentication filters or bearer tokens to the principal they create. [Official authentication guide](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/).

`permission_callback` decides whether dispatch proceeds; it can use the request to check a specific object's owner/capability. `permission_callback => '__return_true'` is appropriate for an intentionally public operation, so it is not automatically a vulnerability. Conversely, a callback that checks only `is_user_logged_in()` or a broad capability can still expose another user's record if it fails to bind the requested object to that caller. A route's response shape and side effects decide impact. Since **WordPress 5.5**, missing `permission_callback` emits a `_doing_it_wrong` notice; a notice is not evidence of exploitability. [Sources: [adding endpoints](https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/), [`register_rest_route()`](https://developer.wordpress.org/reference/functions/register_rest_route/)].

```php
// Illustrative: this check admits editors generally, but says nothing yet
// about whether the selected record belongs in their permitted scope.
'permission_callback' => function ( $request ) {
    return current_user_can( 'edit_posts' );
},
```

Route `args`, including `validate_callback` and `sanitize_callback`, can reject or transform malformed input, but they do not establish authorization. Verify the value after normalization and where it is used. Sanitization can be correct for one sink but irrelevant to another. Check whether a later lookup or callback substitutes an object after the permission decision. [Sources: [REST schema](https://developer.wordpress.org/rest-api/extending-the-rest-api/schema/), [routes and endpoints](https://developer.wordpress.org/rest-api/extending-the-rest-api/routes-and-endpoints/)].

**Trace next:** method and registration → auth mechanism → permission result → exact resolved object/site → validation/transformation → response or state change. A public endpoint and a restrictive permission callback both need contextual analysis, not a mechanical label. Recheck installed core and plugins when relying on authentication-hook order or version-specific behavior.
