# Rendering and cross-site scripting

## The actual viewer and parser matter

Load this when a guest, customer, author, staff member, imported record, or remote service can influence content later rendered to a browser. Derive the rule for the feature: which actor may place which markup in which view, and who is expected to see it. Separate reflected input, stored input, and client-side DOM assembly; for a stored path, identify both writer and later viewer, including admin previews, order/customer screens, shortcodes, blocks, templates, notices, and exported HTML. A lower-privilege author viewing their own content is a different security claim from an administrator or other user rendering it.

## Trace to the final context

Follow **input → sanitization/normalization → storage → retrieval/filtering → template or script assembly → browser context**. Name the exact sink: HTML text, attribute, URL, inline JavaScript, script data, CSS, or DOM API. Evaluate escaping *after* the last transformation for that context. An earlier sanitizer may remove some content yet not protect a later JavaScript or URL context; output encoding that is correct for text may be wrong for an attribute. Conversely, an unescaped value that is fixed, inaccessible to the attacker, or never rendered for another actor is not a cross-user XSS path. [WordPress data/output guidance](../knowledge/wordpress/data-and-storage.md) and [rendering model](../knowledge/wordpress/background-and-rendering.md) resolve API behavior.

Look for cross-component chains: a submission field becomes an admin table cell; an order note reaches a staff preview; shortcode attributes are stored by one role and rendered for another; a server-provided JSON value is later inserted into DOM HTML. Record the creator's capability, any `unfiltered_html` or plugin-specific allowance, the victim's required action, and whether script execution is plausible in that victim's browser. A successful write to the database is not proof of exploitable rendering.

## Challenge and validate

Seek context-correct late escaping, restrictive HTML policy, trusted-only writers, non-rendered or text-only consumers, and browser/content-security constraints in the actual environment. Do not claim a sanitizer is sufficient without matching the final context; do not dismiss a path solely because a sanitizer exists. A strong candidate needs attacker control, a reachable victim view, a context-compatible execution path, and an impact beyond self-XSS when cross-user impact is claimed.

In a local test, use separate creator and viewer accounts and harmless markers to establish which value reaches which output position. If further proof is needed, keep it confined to the authorized test environment and record the observed browser behavior and victim context. If the path discloses a nonce or token and enables another action, verify that second transition under [tokens](tokens-and-state.md) and [chaining](chaining.md) rather than inflating the XSS claim.
