# Model the target: phases 0–3

## 0. Establish the audit state

Before substantial source review, establish the mode and research question, target name, plugin/theme type, exact version or commit, source origin if known, authorized scope, known exclusions, expected WordPress/WooCommerce dependencies, local research workspace, relevant knowledge loaded, and unresolved assumptions. Record these internally or in the local [audit record](../../templates/audit-record.md); a routine preflight need not become a long user-facing report. Identify source paths and environment versions before citing line numbers. Treat target source as read-only and place extracted files, indexes, notes, and test artifacts in the local `research/` workspace according to [repository policy](../repository-policy.md).

## 1. Explain the software before looking for faults

State its purpose and security-relevant features in ordinary language. Map actors beyond WordPress roles where applicable: customers, staff, vendors, tenants, API clients, or external services may have distinct authority. Map objects and their relationships: who creates, owns, manages, shares, or is assigned to each object, and what a token may authorize. Record legitimate state transitions and sensitive operations by *effect* (for example, revealing a private record, changing a payment state, restoring an archive), not by API name. Note trust assumptions and expected behavior. This initial security model is provisional; revise it when code contradicts it.

Choose a few **deep-dive themes** from the model before tracing everything. Selection factors are exposed actor privilege, objects with cross-user or cross-tenant relationships, authority of the operation, persisted or deferred state, integration boundaries, and the complexity of the workflow. A shortcode that only renders public data needs little payment-state analysis; a booking system may need deep ownership, token, payment, and cross-handler review; a backup tool needs archive, restore, and filesystem attention; membership software needs role and subscription transitions. A WooCommerce extension may depend on order state and webhook trust; a form plugin on submission visibility and later rendering; a file manager on path authority; a REST-heavy SaaS integration on remote identity, tokens, and callbacks. Record why each theme was selected or deferred. Load only [specialist playbooks](../../playbooks/README.md) relevant to those themes; do not assume a vulnerability family merely from the feature name.

## 2. Map reachable attack surfaces

Work from registration and invocation to handler, rather than counting declarations. Include applicable AJAX (`wp_ajax_*`, `wp_ajax_nopriv_*`), REST, `admin_post_*` and `admin_post_nopriv_*`, frontend forms, shortcodes, blocks, templates, hooks, webhooks, imports/exports, uploads/downloads, payment callbacks, WooCommerce integrations, custom routing, identity/recovery flows, API clients, and cron/queue/CLI paths reached through attacker-influenced state. [WordPress request knowledge](../../knowledge/wordpress/request-model.md) helps resolve actual dispatch behavior.

For each important surface, record actor and authentication context, prerequisite state, controllable parameters, referenced objects, checks, downstream handlers, state read/written, sensitive effects, and links to other surfaces. Include evidence of registration and reachability, or mark reachability unknown. Prioritize surfaces by authority and boundary crossing; a quiet background consumer can matter more than many public display endpoints.

## 3. Name the trust boundaries

Derive boundaries from the actual model: guest to account, customer to staff, one user's object to another's, tenant to tenant, site to network, frontend input to privileged worker, webhook sender to payment state, public identifier to secret authority, uploaded file to served/executable location, or external URL to internal request. For each, state the permitted transition, the evidence expected to authorize it, the exact enforcement point, and whether attacker-controlled state can affect the decision. A boundary can span handlers or requests. If the enforcement point is unknown, keep that uncertainty visible instead of assuming a check exists or is absent.

Use the [audit record](../../templates/audit-record.md) as a compact map. The output of these phases is a target-specific theory of where authority moves, not a generic endpoint inventory.
