"""Shared immutable records used by the trusted validator."""

from dataclasses import dataclass
import hashlib
import unicodedata


@dataclass(frozen=True)
class SourceFile:
    path: str
    data: bytes
    mode: str


@dataclass(frozen=True)
class Skill:
    name: str
    files: tuple[SourceFile, ...]


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    path: str
    line: int | None
    message: str
    fingerprint: str


@dataclass(frozen=True)
class ScanResult:
    findings: tuple[Finding, ...]
    complete: bool
    candidate_sha: str
    policy_sha: str


def safe_path(path: str) -> str:
    """Escape controls and malformed path spellings before they reach reports."""
    normalized = unicodedata.normalize("NFC", path)
    return "".join(
        f"\\u{ord(char):04x}" if ord(char) < 32 or ord(char) == 127 or unicodedata.category(char) in {"Cf", "Cs"} else char
        for char in normalized
    )


def portable_path_prefixes(path: str) -> tuple[tuple[str, str], ...]:
    """Return (portable key, original spelling) for each component prefix."""
    parts = path.split("/")
    prefixes = []
    for end in range(1, len(parts) + 1):
        spelling = "/".join(parts[:end])
        prefixes.append((unicodedata.normalize("NFC", spelling).casefold(), spelling))
    return tuple(prefixes)


def finding(rule_id: str, severity: str, path: str, line: int | None, message: str, data: bytes) -> Finding:
    """Build a stable opaque fingerprint from a rule, path, and content digest."""
    content_digest = hashlib.sha256(data).hexdigest()
    fingerprint = hashlib.sha256(f"{rule_id}\0{path}\0{content_digest}".encode("utf-8")).hexdigest()
    return Finding(rule_id, severity, safe_path(path), line, message, fingerprint)
