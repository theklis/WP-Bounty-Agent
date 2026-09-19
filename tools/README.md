# Source Audit navigation helpers

`wp_audit_helper.py` is an optional Python 3 standard-library helper for repetitive local [Source Audit](../docs/source-audit/README.md) mechanics. Codex may call its functions or CLI internally; researchers need not memorize commands. It reads target source and never executes PHP or contacts a site.

The helper reports its own version (`python tools/wp_audit_helper.py --version`), separate from the repository's [project version](../VERSION). Its output remains navigation data for the guided audit.

```text
python tools/wp_audit_helper.py --format json inspect-zip path/to/plugin.zip
python tools/wp_audit_helper.py extract-zip path/to/plugin.zip research/audits/my-audit
python tools/wp_audit_helper.py identify research/audits/my-audit/source/plugin
python tools/wp_audit_helper.py inventory research/audits/my-audit/source/plugin
python tools/wp_audit_helper.py --format json entrypoints research/audits/my-audit/source/plugin
python tools/wp_audit_helper.py survey research/audits/my-audit/source/plugin
```

Global `--format json` and `--output research/audits/<audit>/indexes/<new-file>` options go **before** the subcommand. Default output is concise Markdown on stdout; JSON includes all inspected ZIP members or entry records. `--output` creates a new file exclusively as a direct child of an existing audit's `indexes/` directory; extraction accepts only the audit workspace root. Neither writes into target source, `knowledge/`, or curated documents. JSON has a schema version and tool version; no timestamp. Keep the archive digest, source digest, and version/commit with an audit record. Regenerate navigation output when source changes.

ZIP inspection rejects unsafe names, normalized/case-insensitive collisions, special entries, encryption, unsupported compression, and excessive declared size. Defaults are 10,000 members, 512 MiB total expanded data, and 128 MiB per file. `--max-members`, `--max-total-mib`, and `--max-file-mib` adjust these budgets for a known target. Extraction rechecks the archive, copies under an empty staging directory with actual byte limits and exclusive file creation, and refuses to replace `workspace/source`. It preserves the archive. It reports likely roots with evidence, marks multiple candidates ambiguous, and marks root detection incomplete if relevant source cannot be read; the researcher decides the product root.

Identity reads the bounded prefix of root plugin/theme files for headers, plus version clues from `readme.txt` and package metadata; conflicting versions remain explicit. Inventory gives counts, approximate PHP lines, large files, and path-only component hints. Entry indexing records recognizable hook/route registrations and 1-based source locations, including AJAX, admin-post, REST, shortcode, block, scheduled work, identity hooks, and WooCommerce hooks. JSON carries callback and permission callback references when statically recognizable. Unreadable, binary, or PHP files over 4 MiB are skipped with a reason; UTF-8 is decoded with replacement for unusual bytes. Source symlinks/reparse points are skipped. Source hashing is capped at 256 MiB per file and 1 GiB total; an incomplete digest is marked and cannot by itself validate RESUME. `php_text_scan_complete` only reports whether the traversed PHP text was readable within these limits; it does not mean all registrations were recognized. Markdown shows that flag and skipped-path counts; JSON gives reasons.

**Static limits:** dynamic hook names, registration wrappers, framework abstractions, inherited/generated routes, multi-endpoint REST settings, PHP attributes, runtime conditions, and indirect or unusual namespaced callbacks may be missed or left unknown. REST callback hints come only from recognizable top-level settings; nested argument callbacks are not route handlers. A match does not establish reachability; absence does not establish absence. Path hints do not establish behavior. Inspect registrations, invocation, actors, objects, state, authority, and effects using the approved methodology. A failed helper can be replaced by safe manual inspection.

**Boundary:** tools produce navigation artifacts; [Core Audit Methodology](../docs/audit-methodology/README.md) produces security hypotheses; explicit human reproduction is required for confirmation. The helpers do not create findings, assess vulnerability, severity, bounty scope, or CVE status, execute target code, or scan live sites.

Run synthetic local tests with `python -m unittest discover -s tests -v`.
