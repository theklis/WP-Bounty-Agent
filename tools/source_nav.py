"""Read-only, best-effort navigation of a supplied WordPress source tree."""

from __future__ import annotations

import hashlib
import os
import re
import stat
import subprocess
from collections import Counter
from pathlib import Path


SKIP_DIRS = {".git", "__MACOSX", "node_modules"}
MAX_TEXT = 4 * 1024 * 1024
MAX_HASH_FILE = 256 * 1024 * 1024
MAX_HASH_TOTAL = 1024 * 1024 * 1024
HEADERS = ("Plugin Name", "Theme Name", "Version", "Description", "Author", "Requires at least", "Requires PHP", "Text Domain")
DISCLAIMER = "Static navigation only: a match does not establish reachability; a missing match does not establish absence. Inspect conditions, wrappers, dynamic registrations, and source paths manually."
ACTION_SCHEDULER_HOOK_INDEX = {
    "as_enqueue_async_action": 0,
    "as_schedule_single_action": 1,
    "as_schedule_recurring_action": 2,
    "as_schedule_cron_action": 2,
}


def _linkish(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def _root(path: Path) -> Path:
    path = Path(path).expanduser()
    if _linkish(path):
        raise ValueError("source root is a symlink/reparse point")
    root = path.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("source root must be a directory")
    return root


def _walk(root: Path):
    files: list[tuple[str, Path, int]] = []
    skipped: list[str] = []
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda e: (e.name.casefold(), e.name))
        except OSError as exc:
            skipped.append(f"{directory.relative_to(root).as_posix()}: unreadable directory ({type(exc).__name__})")
            continue
        for entry in entries:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            try:
                if _linkish(path):
                    skipped.append(f"{relative}: symlink/reparse point")
                elif entry.is_dir(follow_symlinks=False):
                    if entry.name in SKIP_DIRS:
                        skipped.append(f"{relative}: skipped metadata/generated directory")
                    else:
                        stack.append(path)
                elif entry.is_file(follow_symlinks=False):
                    files.append((relative, path, entry.stat(follow_symlinks=False).st_size))
                else:
                    skipped.append(f"{relative}: special file")
            except OSError as exc:
                skipped.append(f"{relative}: unreadable ({type(exc).__name__})")
    files.sort(key=lambda item: (item[0].casefold(), item[0]))
    return files, sorted(skipped)


def _read(path: Path, limit: int = MAX_TEXT) -> tuple[str | None, str | None]:
    try:
        if _linkish(path):
            return None, "symlink/reparse point"
        if path.stat().st_size > limit:
            return None, f"exceeds {limit} byte text limit"
        with path.open("rb") as handle:
            data = handle.read(limit + 1)
        if len(data) > limit:
            return None, f"exceeds {limit} byte text limit"
        if b"\x00" in data:
            return None, "binary/NUL bytes"
        return data.decode("utf-8-sig", errors="replace"), None
    except OSError as exc:
        return None, f"unreadable ({type(exc).__name__})"


def _header(text: str, label: str) -> dict:
    values = {}
    for number, line in enumerate(text[:16384].splitlines(), 1):
        match = re.match(r"\s*(?:/\*+|\*|//|#)?\s*([A-Za-z ]+):\s*(.*?)\s*(?:\*/)?\s*$", line)
        if match and match.group(1) in HEADERS and match.group(2):
            values.setdefault(match.group(1), {"value": match.group(2), "line": number})
    return values if label in values else {}


def _metadata_candidates(root: Path, files):
    candidates = []
    for rel, path, _ in files:
        if "/" in rel:
            continue
        if path.suffix.lower() != ".php" and rel.lower() != "style.css":
            continue
        content, _ = _read(path, 16384)
        if content is None:
            continue
        kind = "theme" if rel.lower() == "style.css" else "plugin"
        fields = _header(content, "Theme Name" if kind == "theme" else "Plugin Name")
        if fields:
            candidates.append({"kind": kind, "file": rel, "fields": fields})
    return candidates


def likely_roots(source: Path) -> dict:
    root = _root(source)
    found = []
    pending = [(root, 0)]
    while pending:
        directory, depth = pending.pop(0)
        try:
            entries = sorted(directory.iterdir(), key=lambda p: (p.name.casefold(), p.name))
        except OSError:
            continue
        files = [(p.name, p, p.stat().st_size) for p in entries if not _linkish(p) and p.is_file()]
        for candidate in _metadata_candidates(directory, files):
            found.append({"root": directory.relative_to(root).as_posix(), "kind": candidate["kind"],
                          "evidence": f"{candidate['file']}:{candidate['fields']['Theme Name' if candidate['kind'] == 'theme' else 'Plugin Name']['line']}"})
        if depth < 3:
            pending.extend((p, depth + 1) for p in entries if not _linkish(p) and p.is_dir() and p.name not in SKIP_DIRS)
    found.sort(key=lambda x: (x["root"], x["evidence"]))
    return {"status": "single" if len(found) == 1 else "none" if not found else "ambiguous", "candidates": found}


def _git(root: Path) -> dict | None:
    try:
        def run(*args):
            return subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(root), *args],
                                  capture_output=True, text=True, timeout=5, check=True).stdout.strip()
        if Path(run("rev-parse", "--show-toplevel")).resolve() != root:
            return None
        return {"commit": run("rev-parse", "HEAD"), "branch": run("branch", "--show-current") or None,
                "dirty": bool(run("status", "--porcelain", "--untracked-files=normal"))}
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def identify(source: Path) -> dict:
    root = _root(source)
    files, skipped = _walk(root)
    candidates = _metadata_candidates(root, files)
    versions = []
    for item in candidates:
        if "Version" in item["fields"]:
            field = item["fields"]["Version"]
            versions.append({"value": field["value"], "evidence": f"{item['file']}:{field['line']}"})
    for name in ("readme.txt", "README", "README.md", "CHANGELOG", "CHANGELOG.md", "changelog.txt", "composer.json", "package.json"):
        path = root / name
        try:
            linked = _linkish(path)
        except FileNotFoundError:
            continue
        if linked or not path.is_file():
            continue
        content, _ = _read(path)
        if content is None:
            continue
        if name.lower() == "readme.txt":
            match = re.search(r"(?im)^Stable tag:\s*(\S+)", content)
            if match and match.group(1).lower() != "trunk":
                versions.append({"value": match.group(1), "evidence": f"{name}:{content.count(chr(10), 0, match.start()) + 1}"})
        if name.lower().startswith(("readme", "changelog")):
            match = re.search(r"(?im)^\s*(?:#+\s*)?Version:\s*(\S+)", content[:8192])
            if match:
                versions.append({"value": match.group(1), "evidence": f"{name}:{content.count(chr(10), 0, match.start()) + 1}"})
        if name in ("composer.json", "package.json"):
            try:
                import json
                value = json.loads(content).get("version")
                if isinstance(value, str) and value:
                    versions.append({"value": value, "evidence": name})
            except (ValueError, AttributeError):
                skipped.append(f"{name}: invalid JSON metadata")
    unique = sorted({item["value"] for item in versions})
    return {"source_root": str(root), "status": "single_candidate" if len(candidates) == 1 and len(unique) <= 1 else "ambiguous" if candidates else "unknown",
            "candidates": candidates, "versions": versions, "version_conflict": len(unique) > 1,
            "git": _git(root), "skipped": skipped,
            "note": "Metadata is a source clue, not verified product identity; resolve conflicts against the supplied archive/commit."}


def _digest(files) -> tuple[str, list[str]]:
    digest = hashlib.sha256()
    skipped = []
    hashed_bytes = 0
    for rel, path, size in files:
        try:
            if size > MAX_HASH_FILE or hashed_bytes + size > MAX_HASH_TOTAL:
                skipped.append(f"{rel}: digest budget exceeded")
                continue
            if _linkish(path):
                raise OSError("became a link")
            value = hashlib.sha256()
            copied = 0
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    copied += len(chunk)
                    if copied > MAX_HASH_FILE or hashed_bytes + copied > MAX_HASH_TOTAL:
                        raise ValueError("digest budget exceeded")
                    value.update(chunk)
            if copied != size:
                raise ValueError("file changed while hashing")
            digest.update(rel.encode("utf-8", "surrogatepass") + b"\x00" + value.digest())
            hashed_bytes += copied
        except OSError as exc:
            skipped.append(f"{rel}: digest unavailable ({type(exc).__name__})")
        except ValueError as exc:
            skipped.append(f"{rel}: {exc}")
    return digest.hexdigest(), skipped


def _digest_complete(walk_skipped: list[str], digest_skipped: list[str]) -> bool:
    return not digest_skipped and not any(
        item.split(":", 1)[0].split("/")[-1] not in {".git", "__MACOSX"}
        for item in walk_skipped
    )


def inventory(source: Path) -> dict:
    root = _root(source)
    files, skipped = _walk(root)
    digest, digest_skipped = _digest(files)
    complete = _digest_complete(skipped, digest_skipped)
    types = Counter()
    top = Counter()
    php_loc = 0
    for rel, path, _ in files:
        suffix = path.suffix.lower()
        types[suffix or "[none]"] += 1
        top[rel.split("/", 1)[0] if "/" in rel else "[root files]"] += 1
        if suffix == ".php":
            content, reason = _read(path)
            if content is None:
                skipped.append(f"{rel}: LOC unavailable ({reason})")
            else:
                php_loc += len(content.splitlines())
    paths = [rel for rel, _, _ in files]
    hints = {}
    for label, pattern in {
        "woocommerce": r"woocommerce|(?:^|/)wc[-_/]", "rest_api": r"(?:^|/)(rest|api)(?:/|[-_.])",
        "admin": r"(?:^|/)admin(?:/|[-_.])", "frontend": r"(?:^|/)(front|public)(?:/|[-_.])",
        "import_export": r"import|export", "backup_archive": r"backup|archive|restore",
        "account_identity": r"auth|account|user|login|register", "payment_webhook": r"payment|webhook|gateway|callback",
        "background": r"cron|queue|job|scheduler|worker",
    }.items():
        matches = [p for p in paths if re.search(pattern, p, re.I)]
        if matches:
            hints[label] = {"count": len(matches), "examples": matches[:5]}
    largest = sorted(((rel, size) for rel, _, size in files if Path(rel).suffix.lower() in {".php", ".js", ".css"}), key=lambda item: (-item[1], item[0]))[:10]
    shown_types = sorted(types.items(), key=lambda item: (-item[1], item[0]))[:30]
    shown_top = sorted(top.items(), key=lambda item: (-item[1], item[0].casefold(), item[0]))[:20]
    return {"source_root": str(root), "source_digest": digest, "digest_complete": complete,
            "total_files": len(files), "file_types": dict(sorted(shown_types)), "other_file_type_count": len(types) - len(shown_types),
            "php_loc_approx": php_loc, "top_level": dict(sorted(shown_top)), "other_top_level_count": len(top) - len(shown_top),
            "largest_source_files": [{"file": rel, "bytes": size} for rel, size in largest],
            "composer_present": any(rel == "composer.json" for rel, _, _ in files),
            "vendor_present": any(rel.startswith("vendor/") for rel, _, _ in files),
            "path_hints": hints, "skipped": sorted(skipped + digest_skipped),
            "note": "Path hints are structural navigation clues, not evidence of reachable behavior or vulnerability."}


def _mask_php(text: str) -> str:
    """Mask comments and quoted strings, preserving length/newlines."""
    out = list(text)
    i = 0
    while i < len(text):
        pair = text[i:i+2]
        if pair in ("//", "/*") or text[i] == "#":
            end = text.find("\n", i) if pair != "/*" else text.find("*/", i + 2)
            end = len(text) if end < 0 else end + (2 if pair == "/*" else 0)
            for j in range(i, end):
                if text[j] != "\n": out[j] = " "
            i = end
        elif text[i] in ("'", '"'):
            quote = text[i]
            j = i + 1
            while j < len(text):
                if text[j] == "\\": j += 2; continue
                if text[j] == quote: j += 1; break
                j += 1
            for k in range(i, min(j, len(text))):
                if text[k] != "\n": out[k] = " "
            i = j
        else:
            i += 1
    return "".join(out)


def _args(text: str, mask: str, start: int) -> list[str]:
    depth = 1
    square = curly = 0
    points = [start]
    for pos in range(start, min(len(mask), start + 65536)):
        char = mask[pos]
        if char == "(": depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                points.append(pos)
                break
        elif char == "[": square += 1
        elif char == "]": square -= 1
        elif char == "{": curly += 1
        elif char == "}": curly -= 1
        elif char == "," and depth == 1 and square == 0 and curly == 0:
            points.append(pos)
    return [text[points[i]:points[i+1]].strip().strip(",").strip() for i in range(len(points)-1)]


def _literal(value: str) -> str | None:
    match = re.fullmatch(r"(['\"])(.*?)\1", value.strip(), re.S)
    return match.group(2) if match else None


def _callback(value: str) -> str | None:
    value = value.strip()
    if _literal(value) is not None:
        return _literal(value)
    if re.fullmatch(r"(?:\$this|[A-Za-z_][\w]*)\s*::\s*[A-Za-z_]\w*", value):
        return re.sub(r"\s+", "", value)
    match = re.fullmatch(r"\[\s*(\$this|['\"][\w\\]+['\"]|[A-Za-z_]\w*)\s*,\s*(['\"])(\w+)\2\s*\]", value)
    if match: return f"{match.group(1)}::{match.group(3)}"
    match = re.fullmatch(r"array\(\s*(\$this|['\"][\w\\]+['\"]|[A-Za-z_]\w*)\s*,\s*(['\"])(\w+)\2\s*\)", value)
    return f"{match.group(1)}::{match.group(3)}" if match else None


def _setting(settings: str, key: str) -> str | None:
    found = re.search(r"['\"]" + key + r"['\"]\s*=>\s*(\[[^\]]*\]|array\([^\)]*\)|[^,\]\)]+)", settings, re.S)
    if not found: return None
    raw = found.group(1).strip()
    return _literal(raw) or _callback(raw)


def _classify(function: str, args: list[str]):
    first = _literal(args[0]) if args else None
    if function in ("add_action", "add_filter"):
        if first is None:
            return "DYNAMIC_REGISTRATION", None, None
        if first.startswith("wp_ajax_nopriv_"): cat, hint = "AJAX_UNAUTH", "registration names unauthenticated AJAX"
        elif first.startswith("wp_ajax_"): cat, hint = "AJAX_AUTH", "registration names authenticated AJAX"
        elif first.startswith("admin_post_nopriv_"): cat, hint = "ADMIN_POST_UNAUTH", "registration names unauthenticated admin-post"
        elif first.startswith("admin_post_"): cat, hint = "ADMIN_POST_AUTH", "registration names authenticated admin-post"
        elif first.startswith("woocommerce_") or first.startswith("wc_"): cat, hint = "WOOCOMMERCE_HOOK", None
        elif re.search(r"auth|login|register|password|reset|recover|profile|account|user_", first, re.I): cat, hint = "IDENTITY_HOOK", None
        elif re.search(r"cron|schedule|queue|async|background|job", first, re.I): cat, hint = "DEFERRED_HOOK", None
        else: cat, hint = "GENERIC_HOOK", None
        return cat, first, hint
    if function in ACTION_SCHEDULER_HOOK_INDEX:
        return "ACTION_SCHEDULER", first, None
    return {"register_rest_route": "REST_ROUTE", "add_shortcode": "SHORTCODE", "register_block_type": "BLOCK",
            "wp_schedule_event": "CRON_SCHEDULE", "wp_schedule_single_event": "CRON_SCHEDULE",
            "add_rewrite_endpoint": "REWRITE_ENDPOINT"}.get(function), first, None


def entrypoints(source: Path) -> dict:
    root = _root(source)
    files, skipped = _walk(root)
    digest, digest_skipped = _digest(files)
    complete = _digest_complete(skipped, digest_skipped)
    records = []
    pattern = re.compile(r"\b(add_action|add_filter|register_rest_route|add_shortcode|register_block_type|wp_schedule_event|wp_schedule_single_event|as_schedule_single_action|as_schedule_recurring_action|as_schedule_cron_action|as_enqueue_async_action|add_rewrite_endpoint)\s*\(")
    for rel, path, _ in files:
        if path.suffix.lower() != ".php": continue
        content, reason = _read(path)
        if content is None:
            skipped.append(f"{rel}: registration scan unavailable ({reason})")
            continue
        mask = _mask_php(content)
        for match in pattern.finditer(mask):
            name = match.group(1)
            args = _args(content, mask, match.end())
            category, hook, hint = _classify(name, args)
            if category is None: continue
            callback = _callback(args[1]) if name in ("add_action", "add_filter", "add_shortcode") and len(args) > 1 else None
            item = {"category": category, "registration": name, "hook_or_route": hook,
                    "file": rel, "line": content.count("\n", 0, match.start()) + 1,
                    "callback": callback, "reachability_hint": hint}
            if name == "register_rest_route":
                item["namespace"] = _literal(args[0]) if len(args) > 0 else None
                item["route"] = _literal(args[1]) if len(args) > 1 else None
                item["hook_or_route"] = "/".join(v for v in (item["namespace"], item["route"]) if v) or None
                settings = args[2] if len(args) > 2 else ""
                for key in ("methods", "callback", "permission_callback"):
                    item[key] = _setting(settings, key)
            if name == "register_block_type" and len(args) > 1:
                item["render_callback"] = _setting(args[1], "render_callback")
            if name in ("wp_schedule_event", "wp_schedule_single_event") and len(args) > (2 if name == "wp_schedule_event" else 1):
                item["hook_or_route"] = _literal(args[2 if name == "wp_schedule_event" else 1])
            if name in ACTION_SCHEDULER_HOOK_INDEX:
                position = ACTION_SCHEDULER_HOOK_INDEX[name]
                item["hook_or_route"] = _literal(args[position]) if len(args) > position else None
            records.append(item)
    records.sort(key=lambda item: (item["category"], item["file"].casefold(), item["line"], item["registration"]))
    return {"source_root": str(root), "source_digest": digest, "digest_complete": complete,
            "entries": records, "skipped": sorted(skipped + digest_skipped), "limitations": DISCLAIMER}
