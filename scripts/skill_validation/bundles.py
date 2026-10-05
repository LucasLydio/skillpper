"""Bounded, no-extraction validation of optional skill ZIP bundles."""

from __future__ import annotations

import io
import posixpath
import re
import stat
import unicodedata
import zipfile
import zlib

from .models import Finding, Skill, SourceFile, finding


MAX_BUNDLE_BYTES = 20 * 1024 * 1024
MAX_EXPANDED_BYTES = 50 * 1024 * 1024
MAX_TEXT_BYTES = 1024 * 1024
MAX_BINARY_BYTES = 5 * 1024 * 1024
MAX_FILES = 500
MAX_PATH_BYTES = 1024
MAX_MEMBER_RATIO = 100
_NESTED_SUFFIXES = {".zip", ".skill", ".tar", ".gz", ".tgz", ".7z", ".rar", ".bz2", ".xz"}
_RASTER_SIGNATURES = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff", ".jpeg": b"\xff\xd8\xff"}


def _finding(bundle: SourceFile, rule: str, message: str, path: str | None = None) -> Finding:
    return finding(rule, "error", path or bundle.path, None, message, bundle.data)


def _safe_member_path(raw: str) -> tuple[str | None, bool]:
    """Return a normalized safe POSIX path and whether this is a directory."""
    if not isinstance(raw, str) or not raw or raw.startswith("/") or "\\" in raw or "\x00" in raw:
        return None, False
    directory = raw.endswith("/")
    path = raw[:-1] if directory else raw
    try:
        path_bytes = path.encode("utf-8")
    except UnicodeEncodeError:
        return None, directory
    if not path or len(path_bytes) > MAX_PATH_BYTES:
        return None, directory
    if any(re.match(r"^[A-Za-z]:", part) for part in path.split("/")):
        return None, directory
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return None, directory
    if any(unicodedata.category(char) in {"Cc", "Cf", "Cs"} for char in path):
        return None, directory
    if posixpath.normpath(path) != path:
        return None, directory
    return path, directory


def _prefix_collision(paths: list[str]) -> bool:
    """Detect case or normalization differences in any shared path component."""
    spellings: dict[str, str] = {}
    for path in paths:
        components = path.split("/")
        for index in range(1, len(components) + 1):
            prefix = "/".join(components[:index])
            key = unicodedata.normalize("NFC", prefix).casefold()
            previous = spellings.get(key)
            if previous is not None and previous != prefix:
                return True
            spellings[key] = prefix
    return False


def _nested_signature(prefix: bytes) -> bool:
    if prefix.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08", b"\x1f\x8b", b"7z\xbc\xaf\x27\x1c", b"Rar!")):
        return True
    return len(prefix) >= 262 and prefix[257:262] == b"ustar"


def _source_findings(bundle: SourceFile, skill: Skill) -> list[Finding]:
    findings: list[Finding] = []
    source_paths: list[str] = []
    seen: set[str] = set()
    for item in skill.files:
        path = item.path
        normalized, directory = _safe_member_path(path)
        if normalized is None or directory or not path.startswith(skill.name + "/"):
            findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source contains an unsafe path"))
            continue
        if item.mode not in {"100644", "100755"}:
            findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source contains a nonregular entry"))
        if normalized in seen:
            findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source contains duplicate paths"))
        seen.add(normalized)
        source_paths.append(normalized)
        suffix = posixpath.splitext(normalized.lower())[1]
        if suffix in _NESTED_SUFFIXES:
            findings.append(_finding(bundle, "BUNDLE_SOURCE", "nested archives are unsupported"))
        if len(item.data) > MAX_BINARY_BYTES:
            findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source file exceeds the supported size"))
        elif suffix in _RASTER_SIGNATURES:
            if item.mode == "100755" or not item.data.startswith(_RASTER_SIGNATURES[suffix]):
                findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source image has an invalid signature"))
        elif suffix == ".webp":
            if (item.mode == "100755" or len(item.data) < 12
                    or item.data[:4] != b"RIFF" or item.data[8:12] != b"WEBP"):
                findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source image has an invalid signature"))
        else:
            if len(item.data) > MAX_TEXT_BYTES:
                findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source text exceeds the supported size"))
            try:
                item.data.decode("utf-8")
            except UnicodeDecodeError:
                findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source contains opaque binary data"))
    if _prefix_collision(source_paths):
        findings.append(_finding(bundle, "BUNDLE_SOURCE", "skill source contains case or Unicode path collisions"))
    return findings


def validate_bundle(bundle: SourceFile, skill: Skill) -> tuple[Finding, ...]:
    """Validate ZIP metadata and streamed bytes without extracting archive data."""
    findings = _source_findings(bundle, skill)
    if len(bundle.data) > MAX_BUNDLE_BYTES:
        return tuple(findings + [_finding(bundle, "BUNDLE_LIMIT", "compressed skill bundle exceeds 20 MiB")])
    try:
        archive = zipfile.ZipFile(io.BytesIO(bundle.data), "r")
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile, ValueError):
        return tuple(findings + [_finding(bundle, "BUNDLE_INVALID", "skill bundle is not a valid ZIP archive")])

    with archive:
        try:
            infos = archive.infolist()
        except (OSError, EOFError, RuntimeError, UnicodeDecodeError, zipfile.BadZipFile, zipfile.LargeZipFile):
            return tuple(findings + [_finding(bundle, "BUNDLE_INVALID", "ZIP member directory is malformed")])
        members: list[tuple[zipfile.ZipInfo, str, bool, int]] = []
        member_paths: list[str] = []
        invalid = False
        total_declared = 0
        file_count = 0
        expected = {item.path for item in skill.files}
        allowed_directories: set[str] = set()
        for path in expected:
            components = path.split("/")[:-1]
            for end in range(1, len(components) + 1):
                allowed_directories.add("/".join(components[:end]))

        if len(infos) > MAX_FILES:
            findings.append(_finding(bundle, "BUNDLE_LIMIT", "bundle exceeds 500 member entries"))
            invalid = True

        # Preflight every member before opening any compressed data.
        for info in infos:
            # ZipInfo.filename is truncated at NUL for compatibility with older
            # extraction APIs. Validate the preserved original spelling too.
            original_name = getattr(info, "orig_filename", None)
            normalized, is_dir = _safe_member_path(original_name)
            if original_name != info.filename:
                normalized = None
            if normalized is None:
                findings.append(_finding(bundle, "BUNDLE_PATH", "bundle contains an unsafe member path"))
                invalid = True
                continue
            member_paths.append(normalized)
            mode = (info.external_attr >> 16) & 0xFFFF
            kind = stat.S_IFMT(mode)
            if ((is_dir and kind not in (0, stat.S_IFDIR))
                    or (not is_dir and kind not in (0, stat.S_IFREG))):
                findings.append(_finding(bundle, "BUNDLE_TYPE", "bundle contains a symlink or special file"))
                invalid = True
            if info.flag_bits & 0x1:
                findings.append(_finding(bundle, "BUNDLE_ENCRYPTED", "encrypted ZIP members are unsupported"))
                invalid = True
            if is_dir:
                if normalized not in allowed_directories:
                    findings.append(_finding(bundle, "BUNDLE_PATH", "bundle contains an unused or out-of-scope directory"))
                    invalid = True
                if info.file_size != 0:
                    findings.append(_finding(bundle, "BUNDLE_TYPE", "directory entries may not contain data"))
                    invalid = True
                members.append((info, normalized, True, 0))
                continue
            file_count += 1
            if file_count > MAX_FILES:
                findings.append(_finding(bundle, "BUNDLE_LIMIT", "bundle exceeds 500 files"))
                invalid = True
            suffix = posixpath.splitext(normalized.lower())[1]
            limit = MAX_TEXT_BYTES if suffix not in {".png", ".jpg", ".jpeg", ".webp"} else MAX_BINARY_BYTES
            if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                mode_permissions = stat.S_IMODE((info.external_attr >> 16) & 0xFFFF)
                if mode_permissions & 0o111:
                    findings.append(_finding(bundle, "BUNDLE_TYPE", "raster image has executable permissions", normalized))
                    invalid = True
            if info.file_size < 0 or info.file_size > limit:
                findings.append(_finding(bundle, "BUNDLE_LIMIT", "bundle member exceeds its supported size"))
                invalid = True
            if info.compress_size < 0 or info.file_size / max(1, info.compress_size) > MAX_MEMBER_RATIO:
                findings.append(_finding(bundle, "BUNDLE_RATIO", "bundle member exceeds the 100:1 expansion ratio"))
                invalid = True
            total_declared += info.file_size
            if total_declared > MAX_EXPANDED_BYTES:
                findings.append(_finding(bundle, "BUNDLE_LIMIT", "bundle exceeds 50 MiB expanded"))
                invalid = True
            if suffix in _NESTED_SUFFIXES:
                findings.append(_finding(bundle, "BUNDLE_NESTED", "nested archives are unsupported"))
                invalid = True
            members.append((info, normalized, False, limit))

        if len(member_paths) != len(set(member_paths)) or _prefix_collision(member_paths):
            findings.append(_finding(bundle, "BUNDLE_COLLISION", "bundle contains duplicate or case/Unicode-colliding paths"))
            invalid = True

        if invalid:
            return tuple(findings)

        actual: dict[str, bytes] = {}
        total_actual = 0
        try:
            for info, path, is_dir, limit in members:
                if is_dir:
                    continue
                chunks: list[bytes] = []
                size = 0
                prefix = bytearray()
                with archive.open(info, "r") as stream:
                    while True:
                        chunk = stream.read(64 * 1024)
                        if not chunk:
                            break
                        size += len(chunk)
                        total_actual += len(chunk)
                        if size > limit or total_actual > MAX_EXPANDED_BYTES:
                            raise ValueError("expanded content exceeds budget")
                        if len(prefix) < 512:
                            prefix.extend(chunk[:512 - len(prefix)])
                        chunks.append(chunk)
                if size != info.file_size:
                    raise ValueError("member size differs from ZIP metadata")
                if _nested_signature(bytes(prefix)):
                    raise ValueError("nested archive signature")
                actual[path] = b"".join(chunks)
        except (OSError, EOFError, RuntimeError, NotImplementedError,
                zipfile.BadZipFile, zipfile.LargeZipFile, ValueError, zlib.error):
            findings.append(_finding(bundle, "BUNDLE_INVALID", "bundle member data failed bounded integrity checks"))
            return tuple(findings)

    expected = {item.path: item.data for item in skill.files}
    for path in sorted(actual.keys() - expected.keys()):
        findings.append(_finding(bundle, "BUNDLE_EXTRA", "bundle contains a file absent from the skill source", path))
    for path in sorted(expected.keys() - actual.keys()):
        findings.append(_finding(bundle, "BUNDLE_MISSING", "bundle omits a skill source file", path))
    for path in sorted(actual.keys() & expected.keys()):
        if actual[path] != expected[path]:
            findings.append(_finding(bundle, "BUNDLE_MISMATCH", "bundle bytes differ from the skill source", path))
    return tuple(sorted(findings, key=lambda item: (item.path, item.rule_id)))
