# Filesystem, archives, imports, and backups

## Map the file authority

Load this for upload, write/overwrite, read/download, delete, rename, copy/move, archive extraction, import/export, backup/restore, temporary files, or media processing. Derive separate rules for **who may choose the file**, **where the operation may resolve**, **what content/type may land there**, and **who may later retrieve or execute it**. A site administrator, staff member, contributor, guest, and background worker may cross different boundaries. Path safety and object authorization are independent: a path inside an allowed directory can still name another user's private file.

## Trace resolved source and destination

Follow **attacker-controlled name/path/content → normalization and type checks → temporary storage → canonical source/destination → filesystem operation → web exposure or later consumer**. Inspect basename handling, encoded separators, path joining, base-directory containment after resolution, symlink behavior where relevant, overwrite rules, extension/MIME checks, server execution configuration, and cleanup. For read/download/export, include the response headers and exact bytes returned; for delete/restore, include the object or job that selects the path. `WP_Filesystem` or media helpers perform operations but do not decide the web caller's permission; [filesystem knowledge](../knowledge/wordpress/files-and-network.md) covers the APIs.

## Archives and trust transfer

For ZIP/tar import or restore, treat each entry name and embedded configuration value as new input. Trace **archive creator → uploaded or selected archive → entry path and metadata → extraction destination → post-extraction processing → restored state**. Ask whether extraction can escape the intended root, overwrite privileged files, follow links, expose secrets in a public backup location, or feed serialized/configuration data to privileged consumers. A backup created by a trusted worker may be downloadable by a lower-privilege actor; a safe upload path may later become unsafe through rename or restore. Examine archive listing, deletion, remote destination, and public URLs as separate operations. Pair with [serialization](sql-and-serialization.md), [network](network-and-webhooks.md), or [disclosure](information-disclosure.md) only when the path reaches them.

## Counterevidence and validation

Seek resolved-path containment, destination-specific allowlists, verified type/content checks, extraction safeguards, authorization tied to the actual file/job, nonpublic placement, and server configuration that prevents execution. An arbitrary upload is **not automatically RCE**: prove a later execution route if claiming execution. A traversable name is not impact unless it reaches a protected source/destination and produces a consequential effect. A strong candidate needs the operation's exact path after transformation, attacker authority over it, the absent boundary, and observable read/write/delete/execution consequences.

Use disposable files and a local installation for validation. Compare allowed versus out-of-scope paths, a user's own versus another user's export, and pre- versus post-rename/extraction placement; record server behavior and cleanup. Avoid destructive tests on real data. [Authorization](authorization-and-isolation.md) and [execution](code-execution.md) add depth when those boundaries are implicated.
