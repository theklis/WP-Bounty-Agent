"""Conservative ZIP inspection and extraction for local source audits."""

from __future__ import annotations

import hashlib
import ntpath
import os
import shutil
import stat
import tempfile
import unicodedata
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path


CHUNK = 64 * 1024
WINDOWS_DEVICES = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
WINDOWS_DEVICES.update(f"{prefix}{digit}" for prefix in ("COM", "LPT") for digit in "123456789¹²³")
SUPPORTED_METHODS = {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED, zipfile.ZIP_BZIP2, zipfile.ZIP_LZMA}


class ZipSafetyError(ValueError):
    """The archive or extraction destination cannot be handled safely."""


@dataclass(frozen=True)
class Limits:
    max_members: int = 10_000
    max_total_bytes: int = 512 * 1024 * 1024
    max_file_bytes: int = 128 * 1024 * 1024

    def __post_init__(self) -> None:
        if min(self.max_members, self.max_total_bytes, self.max_file_bytes) <= 0:
            raise ZipSafetyError("archive limits must be positive")


def _digest_file(handle) -> str:
    handle.seek(0)
    digest = hashlib.sha256()
    for chunk in iter(lambda: handle.read(CHUNK), b""):
        digest.update(chunk)
    handle.seek(0)
    return digest.hexdigest()


def _canonical_part(part: str) -> str:
    return unicodedata.normalize("NFC", part).casefold()


def _member_path(name: str) -> tuple[tuple[str, ...] | None, list[str]]:
    issues: list[str] = []
    if "\x00" in name:
        issues.append("NUL in member name")
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or ntpath.splitdrive(name)[0]:
        issues.append("absolute, drive, or UNC path")
    if normalized.endswith("/"):
        normalized = normalized[:-1]
    parts = normalized.split("/")
    if not normalized or any(part in ("", ".", "..") for part in parts):
        issues.append("empty, dot, or traversal path component")
    for part in parts:
        if any(ord(char) < 32 or char in '<>:"|?*' for char in part):
            issues.append("control or Windows-invalid character")
        if part.endswith((".", " ")):
            issues.append("trailing dot or space")
        if part.split(".", 1)[0].upper() in WINDOWS_DEVICES:
            issues.append("Windows reserved device name")
    return (tuple(parts) if not issues else None), sorted(set(issues))


def _inspect_open(handle, archive: Path, limits: Limits):
    digest = _digest_file(handle)
    archive_bytes = os.fstat(handle.fileno()).st_size
    try:
        zf = zipfile.ZipFile(handle, "r")
        infos = zf.infolist()
    except (zipfile.BadZipFile, OSError, ValueError) as exc:
        if "zf" in locals():
            zf.close()
        raise ZipSafetyError(f"invalid ZIP: {exc}") from exc

    issues: list[str] = []
    plans = []
    members = []
    seen: dict[str, str] = {}
    implicit_dirs: set[str] = set()
    total = 0
    if len(infos) > limits.max_members:
        issues.append(f"member count exceeds limit ({len(infos)} > {limits.max_members})")

    for info in infos:
        name = info.orig_filename
        parts, path_issues = _member_path(name)
        kind = "directory" if info.is_dir() else "file"
        if name.endswith("\\"):
            path_issues.append("backslash directory marker is ambiguous")
        if info.flag_bits & 1:
            path_issues.append("encrypted member")
        if info.compress_type not in SUPPORTED_METHODS:
            path_issues.append(f"unsupported compression method {info.compress_type}")
        if info.create_system not in (0, 3):
            path_issues.append(f"unsupported ZIP host system {info.create_system}")
        if info.external_attr & 0x400:
            path_issues.append("reparse/special attribute")
        mode = info.external_attr >> 16
        if info.create_system == 3:
            file_type = stat.S_IFMT(mode)
            if file_type not in (0, stat.S_IFREG, stat.S_IFDIR):
                path_issues.append("symlink or special-file entry")
            if file_type == stat.S_IFDIR and kind != "directory":
                path_issues.append("directory mode conflicts with member name")
            if file_type == stat.S_IFREG and kind == "directory":
                path_issues.append("file mode conflicts with directory name")
        if info.create_system == 0 and info.external_attr & 0x10 and kind != "directory":
            path_issues.append("directory attribute conflicts with member name")
        if kind == "directory" and info.file_size:
            path_issues.append("directory entry contains data")
        if kind == "file":
            total += info.file_size
            if info.file_size > limits.max_file_bytes:
                path_issues.append(f"member exceeds size limit ({info.file_size} bytes)")

        if parts is not None:
            keys = ["/".join(_canonical_part(part) for part in parts[:i]) for i in range(1, len(parts) + 1)]
            key = keys[-1]
            if key in seen:
                path_issues.append(f"normalized/case-insensitive collision with {seen[key]}")
            if kind == "file" and key in implicit_dirs:
                path_issues.append("file conflicts with a child path")
            if any(parent in seen and seen[parent] != "directory" for parent in keys[:-1]):
                path_issues.append("parent path is a file")
            seen[key] = kind if key not in seen else seen[key]
            implicit_dirs.update(keys[:-1])

        issues.extend(f"{name!r}: {issue}" for issue in sorted(set(path_issues)))
        plans.append((info, parts, kind))
        members.append({"name": name, "normalized": "/".join(parts) if parts else None,
                        "kind": kind, "expanded_bytes": info.file_size})

    if total > limits.max_total_bytes:
        issues.append(f"declared expanded size exceeds limit ({total} > {limits.max_total_bytes})")
    report = {
        "archive": str(archive), "sha256": digest, "archive_bytes": archive_bytes,
        "member_count": len(infos), "file_count": sum(item[2] == "file" for item in plans),
        "directory_count": sum(item[2] == "directory" for item in plans),
        "declared_expanded_bytes": total,
        "limits": asdict(limits), "status": "safe" if not issues else "rejected",
        "issues": sorted(set(issues)),
        "members": sorted(members, key=lambda item: (item["name"].casefold(), item["name"])),
    }
    return report, plans, zf


def inspect_zip(archive: Path, limits: Limits = Limits()) -> dict:
    archive = Path(archive).expanduser().resolve(strict=True)
    with archive.open("rb") as handle:
        report, _, zf = _inspect_open(handle, archive, limits)
        zf.close()
        return report


def _safe_cleanup(stage: Path, workspace: Path) -> None:
    if (stage.name.startswith(".source-stage-") and not stage.is_symlink()
            and not (getattr(stage.lstat(), "st_file_attributes", 0) & 0x400)
            and stage.resolve(strict=True).parent == workspace):
        shutil.rmtree(stage)


def extract_zip(archive: Path, workspace: Path, limits: Limits = Limits()) -> dict:
    """Inspect and extract to workspace/source; never replace an existing source."""
    archive = Path(archive).expanduser().resolve(strict=True)
    workspace_input = Path(workspace).expanduser()
    if workspace_input.is_symlink() or (getattr(workspace_input.lstat(), "st_file_attributes", 0) & 0x400):
        raise ZipSafetyError("workspace must not be a symlink/reparse point")
    workspace = workspace_input.resolve(strict=True)
    if not workspace.is_dir():
        raise ZipSafetyError("workspace must be an existing ordinary directory")
    source = workspace / "source"
    if source.exists() or source.is_symlink():
        raise ZipSafetyError("workspace/source already exists; refusing overwrite")

    with archive.open("rb") as handle:
        report, plans, zf = _inspect_open(handle, archive, limits)
        try:
            if report["status"] != "safe":
                raise ZipSafetyError("ZIP inspection rejected: " + "; ".join(report["issues"]))
            stage = Path(tempfile.mkdtemp(prefix=".source-stage-", dir=workspace))
            try:
                stage_root = stage.resolve(strict=True)
                copied_total = 0
                for info, parts, kind in plans:
                    assert parts is not None  # successful inspection established this
                    destination = stage.joinpath(*parts)
                    if not destination.resolve(strict=False).is_relative_to(stage_root):
                        raise ZipSafetyError(f"destination escapes staging directory: {info.orig_filename!r}")
                    if kind == "directory":
                        destination.mkdir(parents=True, exist_ok=True)
                        continue
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    copied_file = 0
                    with zf.open(info, "r") as infile, destination.open("xb") as outfile:
                        while chunk := infile.read(CHUNK):
                            copied_file += len(chunk)
                            copied_total += len(chunk)
                            if copied_file > limits.max_file_bytes or copied_total > limits.max_total_bytes:
                                raise ZipSafetyError("expanded data exceeded extraction budget")
                            outfile.write(chunk)
                    if copied_file != info.file_size:
                        raise ZipSafetyError(f"expanded size differs from ZIP declaration: {info.orig_filename!r}")
                if _digest_file(handle) != report["sha256"]:
                    raise ZipSafetyError("archive changed during extraction")

                from source_nav import likely_roots  # imported here to keep ZIP inspection independent
                roots = likely_roots(stage)
                if source.exists() or source.is_symlink():
                    raise ZipSafetyError("workspace/source appeared during extraction; refusing overwrite")
                if stage_root.parent != workspace or source.resolve(strict=False).parent != workspace:
                    raise ZipSafetyError("source move would leave the requested workspace")
                stage.rename(source)
                stage = None
                return {**report, "status": "extracted", "source": str(source),
                        "actual_expanded_bytes": copied_total, "product_roots": roots}
            except BaseException as exc:
                if stage is not None and stage.exists():
                    _safe_cleanup(stage, workspace)
                if isinstance(exc, (KeyboardInterrupt, SystemExit, ZipSafetyError)):
                    raise
                raise ZipSafetyError(f"extraction failed: {type(exc).__name__}: {exc}") from exc
        finally:
            zf.close()
