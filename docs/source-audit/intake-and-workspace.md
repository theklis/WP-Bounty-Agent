# Intake, source identity, and workspace

## Start with one identified input

Resolve the supplied path and establish authorization, requested mode/scope, known exclusions, local test assumptions, and any [Target Hunter profile](../../templates/target-profile.md). An existing profile is a lead and setup aid, not audit evidence: verify that its version/ref and component match the actual source. Record conflicts and missing facts in the [audit record](../../templates/audit-record.md). Do not infer researcher tier or a final bounty/CVE outcome from the input.

Use a distinct, ignored workspace for each source identity, for example:

```text
research/audits/<slug>-<version-or-ref>-<short-input-id>/
  audit.md
  source/       # extracted ZIP only; omit for a source tree reviewed in place
  notes/        # optional journal or focused notes
  indexes/      # optional generated navigation data
  artifacts/    # optional local test output
research/findings/<audit-id>-F01.md
research/findings/<audit-id>-F01-validation.md  # only when useful
```

Copy [the audit template](../../templates/audit-record.md) to `audit.md`; create optional directories only when needed. Keep distinct finding and validation records in ignored `research/findings/` and link their IDs from `audit.md`. Preserve an existing workspace: resume it only after verifying the same source identity, and never overwrite an unrelated audit. If identity is unresolved, use a provisional, collision-free workspace name and record the uncertainty; do not present its guessed slug/version as fact. Supplied archives and trees, extracted code, indexes, notes, and proof artifacts must stay untracked under [repository policy](../repository-policy.md).

## ZIP intake: inspect before extracting

1. Preserve the original ZIP at its supplied path; record that path, size, and SHA-256 digest. Inspect its member list and declared expanded sizes before writing files. Set a reasonable file-count, expanded-size, and disk-space budget for this target; stop if the archive is implausibly large or cannot be safely handled.
2. Treat `/` and `\` as separators before checking names. Reject absolute, drive-qualified, or UNC paths; `..` path components; NUL; Windows reserved device names, alternate-stream `:`, or trailing dot/space names; links or other special-file entries; and normalized destination collisions, including case-insensitive collisions on Windows. Reject ambiguous or encrypted archives that cannot be safely inspected. Check that every resolved destination remains below a **new empty staging directory** inside this audit workspace. Never follow an archive-provided link or a pre-existing reparse point.
3. Extract only after the entire member list passes. Use bounded per-member copying into exclusively created destinations and enforce the size budget while copying. Do not blindly extract into the repository root, call an unchecked bulk extraction, or overwrite `source/`. If extraction fails or a size/CRC check fails, leave the original ZIP untouched, verify the staging directory's resolved path is still inside this audit workspace before removing it, and record the failure.
4. After extraction, identify the actual plugin/theme root within the extracted tree. A ZIP may contain a wrapper directory, documentation, multiple products, or unexpected files. Keep the structure visible under `source/`; stop audit analysis on an ambiguous product root until it is resolved. Confirm the staged and final paths remain inside this audit workspace before moving the extracted tree to `source/`. Record the extraction method, chosen product root, digest, and any unusual structure. Treat the extracted tree as read-only.

The optional [ZIP helper](../../tools/README.md) can inspect and extract into a new audit workspace with documented budgets. Review its rejection report and root candidates; do not accept an ambiguous product root by guess. Python's [ZIP documentation](https://docs.python.org/3/library/zipfile.html) warns about untrusted extraction, resource exhaustion, and overwrites. If the helper fails, use a safe manual alternative or leave the archive unextracted until intake can be resolved safely.

For a supplied **source tree**, record its canonical path and inspect in place without writes. Check symlinks/reparse points before following them outside the authorized source. If it is a Git checkout, record commit/ref, branch, and dirty state; a ref alone does not identify uncommitted changes. For mutable or non-Git trees, record a complete file inventory/digest where feasible; mark gaps explicitly and recheck affected files before reusing evidence. If the tree sits in an unignored part of this repository, use an ignored local copy for audit work so it cannot be staged accidentally; preserve the original. Generated indexes and tests still go in the audit workspace, not the target tree. Do not execute target code merely to identify it.

## Establish exact software identity

Inspect the main plugin PHP header or theme `style.css`, source readme/changelog, package metadata, and repository metadata as applicable. Record name, slug, version, edition, source root and origin, archive digest or commit/ref, WordPress/PHP requirements, WooCommerce or other major dependencies, bundled libraries, and apparent source completeness. An archive filename or Target Hunter profile is a clue, not authority over conflicting source metadata. Preserve conflicts and mark the exact version unresolved until evidence resolves them; qualify all source references and later scope assessments accordingly.

The [identity and inventory helpers](../../tools/README.md) may supply initial metadata and structural clues. Check their evidence against the actual source and resolve conflicts in the audit record; helper output does not establish exact identity on its own.

If the source changes mid-audit, pause and record old and new identity. Decide explicitly which architecture notes remain useful and which references, candidates, tests, and coverage need revalidation. A materially different version normally gets a new workspace or a clearly separated versioned record; do not silently continue under old line references.
