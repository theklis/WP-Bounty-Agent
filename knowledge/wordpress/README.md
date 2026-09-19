# WordPress security knowledge

Security semantics for source review, not a developer guide or vulnerability checklist. Load the smallest relevant set. First establish the plugin's own actors, objects, and workflow; use these references to test what WordPress does and does not guarantee. A public route, dangerous sink, or missing check is not by itself a vulnerability. Follow the complete reachable path and its counterevidence under the [evidence model](../../docs/evidence.md).

| When reviewing | Load |
| --- | --- |
| Entry points, loading, hooks, indirect calls | [Request model and hooks](request-model.md) |
| Login, users, roles, capabilities | [Identity and capabilities](identity-and-capabilities.md) |
| Per-record access, custom roles, tenants, multisite | [Ownership and plugin models](ownership-and-plugin-models.md) |
| Nonces, cookies, keys, token/state chains | [Nonces and tokens](nonces-and-tokens.md) |
| `admin-ajax.php` or `admin-post.php` | [AJAX and admin-post](ajax-and-admin-post.md) plus identity/ownership as needed |
| REST routes | [REST API](rest-api.md) plus identity/ownership/token material as needed |
| Input, output, SQL, options, meta, serialization | [Data and storage](data-and-storage.md) |
| Uploads, paths, outbound HTTP, redirects | [Files and network](files-and-network.md) |
| Cron, queues, shortcodes, blocks, templates | [Deferred work and rendering](background-and-rendering.md) |
| WooCommerce orders, checkout, customers, webhooks | [WooCommerce](woocommerce.md) plus ownership/tokens |
| Quick API question | [Security API reference](api-security-reference.md), then its linked topic |

References in these files are official WordPress, WooCommerce, or PHP documentation and code references. Consulted **2026-09-19**. Conceptual trust-boundary guidance is stable; details about a specific core, PHP, or WooCommerce version must be rechecked against the target's installed source. Version-dependent details are flagged where they matter. This area contains no current bounty rules or target findings. See the [knowledge index](../README.md).
