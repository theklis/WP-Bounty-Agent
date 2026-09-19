# Data handling, database queries, and persistent state

## What each transformation proves

**Validation** decides whether a value meets an expected domain (for example, an existing object ID belonging to the caller). **Normalization** converts representations (for example, `absint()`), often losing information. **Sanitization** changes or removes disallowed content (`sanitize_text_field()`, `sanitize_key()`, `sanitize_email()`); it does not grant authority and is not universal sink protection. `intval()` and `absint()` constrain numeric shape, not whether the resulting ID is the right object. **Escaping/encoding** make output safe for a specific parser/context: `esc_html()` for HTML text, `esc_attr()` for attributes, `esc_url()` for URL output, and JSON encoding for JSON rather than HTML. `wp_kses()`/`wp_kses_post()` allow restricted HTML, not arbitrary safety for JavaScript, SQL, or URLs. Prefer escaping at output after all transformations; stored data may later flow to a new sink. [Sources: [sanitizing](https://developer.wordpress.org/apis/security/sanitizing/), [escaping](https://developer.wordpress.org/apis/security/escaping/)].

Trace input → transformations → stored form → each later output context. A sanitization call is evidence about one transformation, not a conclusion. For example, text safe in HTML body may still be unsafe in an unquoted attribute or script. Conversely, an unescaped value is not a finding until attacker control, reachability, and an exploitable rendering context are shown.

## `$wpdb` and custom tables

`$wpdb->prepare()` binds values through placeholders such as `%s`, `%d`, and `%f`; modern core also supports `%i` for identifiers. It does not make arbitrary SQL fragments, operators, or a user-selected `ORDER BY` expression safe. For dynamic columns or sort directions, map a small accepted input set to trusted SQL fragments; inspect table-prefix construction and custom-table queries. `esc_sql()` is not a substitute for a correctly prepared whole query. `wpdb` CRUD helpers reduce manual string assembly for their values but do not provide actor authorization. [Sources: [`wpdb::prepare()`](https://developer.wordpress.org/reference/classes/wpdb/prepare/), [`esc_sql()`](https://developer.wordpress.org/reference/functions/esc_sql/), [`wpdb` class](https://developer.wordpress.org/reference/classes/wpdb/)].

**Version note:** `%i` was added in **WordPress 6.2**. Verify the target's minimum supported core version before relying on it. [Core development note](https://make.wordpress.org/core/2022/10/08/escaping-table-and-field-names-with-wpdbprepare-in-wordpress-6-1/).

```php
// Illustrative: binding a value does not validate a chosen SQL identifier.
$sql = $wpdb->prepare( "SELECT * FROM {$table} ORDER BY {$sort} LIMIT %d", $limit );
// Trace who controls $table/$sort; map choices to trusted identifiers/fragments.
```

Stored attacker input can become **second-order** query input: follow option, meta, or custom-table values into later query assembly. A prepared value at one request does not imply that a later query safely handles it.

## Options, meta, and transients

`get_option()`/`update_option()` store site settings; `get_site_option()`/`update_site_option()` address network-level settings in multisite. Meta APIs attach values to users, posts, and terms; transients are temporary cached state and may expire earlier than their stated maximum. These APIs store/retrieve data; they do not enforce the caller's entitlement to change a named option or another user's meta. `update_option()` explicitly expects plugin code to check capabilities before sensitive updates. [Sources: [options](https://developer.wordpress.org/apis/options/), [`update_option()`](https://developer.wordpress.org/reference/functions/update_option/), [`update_post_meta()`](https://developer.wordpress.org/reference/functions/update_post_meta/), [transients](https://developer.wordpress.org/apis/transients/)].

Identify the key namespace, object ID, scope (site versus network), writer, reader, and effect. Security-relevant values include default role, role/capability data, integration credentials, webhook URLs, upload settings, and plugin access rules. Autoload controls startup loading/performance, not trust. A low-privilege write can become significant if a privileged callback later consumes the stored value. Include custom tables and cross-request state, not only the standard options table. [Related: [ownership](ownership-and-plugin-models.md), [background work](background-and-rendering.md)].

## Serialization and complex data

PHP `serialize()` encodes values, including objects; `unserialize()` reconstructs them. WordPress `maybe_serialize()`/`maybe_unserialize()` help store complex values; `maybe_unserialize()` calls PHP `unserialize()` when the value appears serialized. That is not a trust check. If an attacker controls the serialized bytes reaching an unserialize path, investigate possible object instantiation, loaded classes, and magic methods; do not infer object injection merely from the helper's presence. PHP warns against unserializing untrusted input. JSON parsing avoids PHP object reconstruction by default, but later use of decoded fields still needs validation and permission checks. [Sources: [`maybe_serialize()`](https://developer.wordpress.org/reference/functions/maybe_serialize/), [`maybe_unserialize()`](https://developer.wordpress.org/reference/functions/maybe_unserialize/), [PHP `unserialize()`](https://www.php.net/function.unserialize.php)].
