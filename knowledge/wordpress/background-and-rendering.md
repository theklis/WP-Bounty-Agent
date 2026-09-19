# Deferred work and rendering boundaries

## WP-Cron and queued work

WP-Cron uses scheduled events and hook callbacks; scheduling is usually triggered by site traffic rather than a continuously running daemon. Plugins may also use their own queues or external job systems. For a security review, the key path is **untrusted request → stored argument/state → later callback → privileged action**. At execution time, the original browser caller's cookies, nonce, and current-user context may be absent; the worker must not treat a stored value as authorized merely because it was queued. Trace who could schedule or modify the event, arguments, cancellation, and the exact consumer. [Sources: [WP-Cron](https://developer.wordpress.org/plugins/cron/), [scheduling events](https://developer.wordpress.org/plugins/cron/scheduling-wp-cron-events/), [`wp_schedule_event()`](https://developer.wordpress.org/reference/functions/wp_schedule_event/)].

An import may be accepted by one handler and applied later; a webhook may enqueue an order update; a transient may determine which file to delete. Review the state transition and authorization at the time of the sensitive action. Lack of an immediate sink in the request handler does not close the investigation. Timing and queue implementation are plugin/version-specific.

## Shortcodes, blocks, and templates

`add_shortcode()` callbacks consume attributes and content from rendered material. Dynamic server-side blocks can use a PHP `render_callback`; templates and preview paths can execute them under different viewer contexts. Ask who may create or edit the stored content, whether lower-privilege authors can influence attributes, who later renders it, and which output context receives the result. Stored content need not be trusted just because it came from WordPress tables. [Sources: [`add_shortcode()`](https://developer.wordpress.org/reference/functions/add_shortcode/), [block registration](https://developer.wordpress.org/reference/functions/register_block_type/), [dynamic rendering](https://developer.wordpress.org/block-editor/getting-started/fundamentals/static-dynamic-rendering/)].

Admin preview and frontend rendering may use different templates, users, or filters. A rendering callback that reads private data may expose it to viewers even without a direct API route. Conversely, a shortcode or block registration alone proves only a possible execution path; establish actual content reachability and impact. [Related: request model](request-model.md), [output contexts](data-and-storage.md).
