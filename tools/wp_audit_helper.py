"""Small command-line interface for Source Audit navigation artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source_nav import entrypoints, identify, inventory
from zip_intake import Limits, ZipSafetyError, extract_zip, inspect_zip


VERSION = "0.1.0"
SCHEMA = 1


def _positive(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only Source Audit navigation helper; never a vulnerability scanner")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="new artifact inside repository research/audits/ (default: stdout)")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("inspect-zip", "extract-zip", "identify", "inventory", "entrypoints", "survey"):
        child = sub.add_parser(command)
        child.add_argument("path", type=Path, help="archive or target source directory")
        if command == "extract-zip": child.add_argument("workspace", type=Path, help="existing ignored audit workspace")
        if command in ("inspect-zip", "extract-zip"):
            child.add_argument("--max-members", type=_positive, default=10_000)
            child.add_argument("--max-total-mib", type=_positive, default=512)
            child.add_argument("--max-file-mib", type=_positive, default=128)
    return parser


def _markdown(payload: dict) -> str:
    command = payload["command"]
    data = payload["data"]
    lines = [f"# Source Audit helper: {command}", "", f"Tool {VERSION}; schema {SCHEMA}.", "",
             "Navigation artifact only. Inspect source and apply the audit methodology; no security conclusion follows from this output.", ""]
    if command in ("inspect-zip", "extract-zip"):
        lines += [f"- Archive: `{data['archive']}`", f"- SHA-256: `{data['sha256']}`", f"- Status: {data['status']}",
                  f"- Archive bytes: {data['archive_bytes']}", f"- Members: {data['member_count']} ({data['file_count']} files, {data['directory_count']} directories)",
                  f"- Declared expanded bytes: {data['declared_expanded_bytes']}"]
        if "source" in data: lines.append(f"- Extracted source: `{data['source']}`")
        if "product_roots" in data:
            lines.append(f"- Product roots: {data['product_roots']['status']}; inspect evidence in JSON output if ambiguous")
        for issue in data["issues"][:30]: lines.append(f"- Rejection: {issue}")
        if len(data["issues"]) > 30: lines.append(f"- Additional issues: {len(data['issues']) - 30}")
        lines.append("\nFull member names and limits are available with `--format json`.")
    elif command == "identify":
        lines += [f"- Source: `{data['source_root']}`", f"- Status: {data['status']}",
                  f"- Version conflict: {data['version_conflict']}"]
        for item in data["candidates"]:
            label = "Plugin Name" if item["kind"] == "plugin" else "Theme Name"
            lines.append(f"- {item['kind']}: {item['fields'][label]['value']} ({item['file']}:{item['fields'][label]['line']})")
        for item in data["versions"]: lines.append(f"- Version clue: {item['value']} ({item['evidence']})")
        if data["git"]: lines.append(f"- Git: {data['git']}")
        lines.append(f"\n{data['note']}")
    elif command == "inventory":
        lines += [f"- Source: `{data['source_root']}`", f"- Source digest: `{data['source_digest']}` (complete: {data['digest_complete']})",
                  f"- Files: {data['total_files']}; PHP LOC approximate: {data['php_loc_approx']}",
                  f"- File types: {data['file_types']}", f"- Top level: {data['top_level']}",
                  f"- Additional file types/top-level groups: {data['other_file_type_count']}/{data['other_top_level_count']}",
                  f"- Composer: {data['composer_present']}; vendor: {data['vendor_present']}"]
        for label, hint in data["path_hints"].items(): lines.append(f"- {label}: {hint['count']} path matches; examples: {', '.join(hint['examples'])}")
        lines.append(f"\n{data['note']}")
    elif command == "entrypoints":
        lines += [f"- Source: `{data['source_root']}`", f"- Source digest: `{data['source_digest']}` (complete: {data['digest_complete']})",
                  f"- Registration leads: {len(data['entries'])}", "", "| Category | Registration | File:line | Callback |", "|---|---|---|---|"]
        for item in data["entries"][:200]:
            display = (item["hook_or_route"] or item["registration"] or "dynamic").replace("|", "\\|")
            lines.append(f"| {item['category']} | {display} | {item['file']}:{item['line']} | {item['callback'] or ''} |")
        if len(data["entries"]) > 200: lines.append(f"\nShowing 200 of {len(data['entries'])}; use JSON for all records.")
        lines.append(f"\n{data['limitations']}")
    elif command == "survey":
        lines += [f"- Source: `{data['identity']['source_root']}`", f"- Identity status: {data['identity']['status']}",
                  f"- Source digest: `{data['inventory']['source_digest']}`", f"- Files: {data['inventory']['total_files']}",
                  f"- Registration leads: {len(data['entrypoints']['entries'])}",
                  "", "Use individual commands or JSON for evidence and full navigation records."]
    return "\n".join(lines) + "\n"


def _write_output(path: Path, content: str) -> None:
    repo = Path(__file__).resolve().parent.parent
    allowed = (repo / "research" / "audits").resolve(strict=False)
    destination = path.expanduser().resolve(strict=False)
    if not destination.is_relative_to(allowed) or destination == allowed:
        raise ValueError("output must be a new file under repository research/audits/")
    parent = destination.parent
    if not parent.is_dir() or parent.is_symlink():
        raise ValueError("output parent must be an existing ordinary audit workspace directory")
    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def _check_audit_workspace(path: Path) -> None:
    repo = Path(__file__).resolve().parent.parent
    allowed = (repo / "research" / "audits").resolve(strict=False)
    destination = path.expanduser().resolve(strict=True)
    if not destination.is_relative_to(allowed) or destination == allowed:
        raise ValueError("extraction workspace must be under repository research/audits/<audit>/")


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command in ("inspect-zip", "extract-zip"):
            limits = Limits(args.max_members, args.max_total_mib * 1024**2, args.max_file_mib * 1024**2)
            if args.command == "extract-zip": _check_audit_workspace(args.workspace)
            data = inspect_zip(args.path, limits) if args.command == "inspect-zip" else extract_zip(args.path, args.workspace, limits)
        elif args.command == "identify": data = identify(args.path)
        elif args.command == "inventory": data = inventory(args.path)
        elif args.command == "entrypoints": data = entrypoints(args.path)
        else: data = {"identity": identify(args.path), "inventory": inventory(args.path), "entrypoints": entrypoints(args.path)}
        payload = {"tool_version": VERSION, "schema_version": SCHEMA, "command": args.command, "data": data}
        rendered = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n" if args.format == "json" else _markdown(payload)
        if args.output: _write_output(args.output, rendered)
        else: sys.stdout.write(rendered)
        return 0 if data.get("status") != "rejected" else 2
    except (OSError, ValueError, ZipSafetyError) as exc:
        print(f"wp_audit_helper: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
