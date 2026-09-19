# Request model and indirect reachability

## Bootstrap and callbacks

Active plugin code is loaded during WordPress bootstrap; registration with `add_action()` or `add_filter()` makes a callback eligible when the named hook fires. An action invokes behavior; a filter can change data later consumed by another component. Registration alone does **not** prove external reachability: trace the request or event that fires the hook, any conditional registration, priority, dynamic hook name, and the caller context at execution. Plugin and theme hooks can also be invoked by other plugins. [`plugins_loaded`, `init`, and `wp_loaded` have different timing](https://developer.wordpress.org/apis/hooks/action-reference/); do not assume current-user state or a pluggable function is usable at arbitrary early file-load time. [Sources: [plugin basics](https://developer.wordpress.org/plugins/plugin-basics/), [hooks](https://developer.wordpress.org/plugins/hooks/), [action reference](https://developer.wordpress.org/apis/hooks/action-reference/), [current user](https://developer.wordpress.org/reference/functions/wp_get_current_user/)].

## Request families

| Family | Reachability question | Security implication |
| --- | --- | --- |
| Frontend | Does URL/template selection, `init`, `template_redirect`, or content rendering fire this callback? | Frontend is not synonymous with guest-only; logged-in and guest requests may share a path. |
| Admin page | Does a menu/page hook, `admin_init`, or form handler fire it? | Admin area context does not imply Administrator role; lower-privilege users may enter some admin paths. |
| `admin-ajax.php` | Which `wp_ajax_*` or `wp_ajax_nopriv_*` action is registered? | Login branch changes, but action-specific permission is still needed. |
| `admin-post.php` | Which `admin_post_*` or `admin_post_nopriv_*` action is registered? | The name “admin” describes a dispatcher, not a privilege grant. |
| REST | Which route, method, authentication method, and callbacks match? | Route visibility and `permission_callback` require contextual review. |
| Cron/background | Who can schedule or store arguments later read by the callback? | The original request's identity may not be present when work runs. |

The hook and dispatcher behavior is described in [WordPress action references](https://developer.wordpress.org/apis/hooks/action-reference/), [AJAX hooks](https://developer.wordpress.org/reference/hooks/wp_ajax_action/), [admin-post hooks](https://developer.wordpress.org/reference/hooks/admin_post_action/), and [REST route registration](https://developer.wordpress.org/reference/functions/register_rest_route/). Trace the installed version and registered callback, not just the hook string in isolation.

## Rendering is execution too

`add_shortcode()` registers a callback invoked when content is processed as a shortcode; its attributes and body can derive from an author or stored post content. Server-rendered blocks can call a PHP `render_callback`, and templates can call plugin functions directly. Determine who may create/edit the content and who later views it, including admin previews and frontend visitors. A stored value can cross actor boundaries without a direct HTTP handler. [Sources: shortcode callback](https://developer.wordpress.org/reference/functions/add_shortcode/), [block registration](https://developer.wordpress.org/reference/functions/register_block_type/).

**Trace next:** request/event → hook registration condition → callback → input origin → current user and object context → downstream actions. A missing direct route is not proof that a function is unreachable. For detail, read [AJAX/admin-post](ajax-and-admin-post.md), [REST](rest-api.md), or [deferred/rendering](background-and-rendering.md).
