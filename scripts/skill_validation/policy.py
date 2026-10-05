"""Trusted policy and exact-content exception handling for skill validation."""

from __future__ import annotations

from datetime import date
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import re
from typing import Any

from .models import Finding
from .structure import strict_yaml


class PolicyError(ValueError):
    """Raised when trusted policy or exception data is malformed."""


_POLICY_KEYS = {"schema_version", "maintainers", "limits"}
_LIMIT_KEYS = {"max_window_lines"}
_EXCEPTION_KEYS = {
    "rule_id", "path", "content_sha256", "reason", "issue_url",
    "approved_by", "created_on", "expires_on",
}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RULE = re.compile(r"^[A-Z]{3}[0-9]{3}$")
_SAFE_PATH = re.compile(r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9._/@+ -]+$")


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(k, str) for k in value):
        raise PolicyError(f"{where} must be a mapping")
    return value


def _keys(value: dict[str, Any], allowed: set[str], required: set[str], where: str) -> None:
    unknown = set(value) - allowed
    missing = required - set(value)
    if unknown:
        raise PolicyError(f"{where} has unsupported fields")
    if missing:
        raise PolicyError(f"{where} is missing required fields")


def _load_yaml(path: Path) -> Any:
    try:
        data = path.read_bytes()
        if len(data) > 256 * 1024:
            raise PolicyError("policy file exceeds the size limit")
        return strict_yaml(data)
    except PolicyError:
        raise
    except Exception as exc:
        raise PolicyError("policy file is unreadable or invalid YAML") from exc


def validate_policy(value: Any) -> dict[str, Any]:
    policy = _mapping(value, "policy")
    _keys(policy, _POLICY_KEYS, {"schema_version", "maintainers"}, "policy")
    if type(policy["schema_version"]) is not int or policy["schema_version"] != 1:
        raise PolicyError("unsupported policy schema version")
    maintainers = policy["maintainers"]
    if (not isinstance(maintainers, list) or not maintainers
            or any(not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9-]{1,39}", name)
                   for name in maintainers)
            or len(set(maintainers)) != len(maintainers)):
        raise PolicyError("policy maintainers are invalid")
    if "limits" in policy:
        limits = _mapping(policy["limits"], "policy limits")
        _keys(limits, _LIMIT_KEYS, set(), "policy limits")
        if "max_window_lines" in limits:
            n = limits["max_window_lines"]
            if type(n) is not int or not 1 <= n <= 20:
                raise PolicyError("policy window limit is outside the supported range")
    return policy


def load_policy(path: Path) -> dict[str, Any]:
    """Load and strictly validate trusted base policy YAML."""
    return validate_policy(_load_yaml(Path(path)))


def _validate_exception(item: Any, policy: dict[str, Any], today: date) -> dict[str, Any]:
    entry = _mapping(item, "exception")
    _keys(entry, _EXCEPTION_KEYS, _EXCEPTION_KEYS, "exception")
    if not isinstance(entry["rule_id"], str) or not _RULE.fullmatch(entry["rule_id"]):
        raise PolicyError("exception rule identifier is invalid")
    # Only explicitly approved blocking classes can be waived. All parser,
    # containment, budget, incomplete-scan, and credential findings fail closed.
    if entry["rule_id"] not in {"SEC003", "DUP001"}:
        raise PolicyError("this finding class cannot be excepted")
    path = entry["path"]
    if (not isinstance(path, str) or not _SAFE_PATH.fullmatch(path)
            or "*" in path or "?" in path or "\\" in path):
        raise PolicyError("exception path must be an exact repository-relative path")
    if not isinstance(entry["content_sha256"], str) or not _SHA256.fullmatch(entry["content_sha256"]):
        raise PolicyError("exception content hash is invalid")
    for key in ("reason", "issue_url"):
        if not isinstance(entry[key], str) or not entry[key].strip() or len(entry[key]) > 1000:
            raise PolicyError(f"exception {key} is invalid")
    url = entry["issue_url"]
    if not url.startswith(("https://github.com/", "https://gitlab.com/")):
        raise PolicyError("exception issue URL must be an HTTPS issue link")
    approver = entry["approved_by"]
    if not isinstance(approver, str) or approver not in policy["maintainers"]:
        raise PolicyError("exception approver is not a trusted maintainer")
    parsed_dates: list[date] = []
    for key in ("created_on", "expires_on"):
        raw = entry[key]
        if not isinstance(raw, str):
            raise PolicyError(f"exception {key} must be an ISO date")
        try:
            parsed = date.fromisoformat(raw)
        except ValueError as exc:
            raise PolicyError(f"exception {key} must be an ISO date") from exc
        if parsed.isoformat() != raw:
            raise PolicyError(f"exception {key} must be an ISO date")
        parsed_dates.append(parsed)
    created, expires = parsed_dates
    if expires < created or (expires - created).days > 30:
        raise PolicyError("exception lifetime must be between zero and 30 days")
    if created > today or expires < today:
        raise PolicyError("exception is not currently valid")
    return entry


def apply_exceptions(
    findings: tuple[Finding, ...],
    files: tuple[Any, ...],
    exceptions_path: Path,
    today: date,
    policy: dict[str, Any] | None = None,
) -> tuple[Finding, ...]:
    """Downgrade findings only for exact, currently valid trusted exceptions.

    The exception file and policy must be supplied from the trusted base tree by
    the caller. When policy is omitted, the checked-in policy beside the package
    root is loaded for local use.
    """
    if policy is None:
        root = Path(__file__).resolve().parents[2]
        policy = load_policy(root / "security" / "skill-validation-policy.yaml")
    else:
        policy = validate_policy(policy)
    try:
        raw = _load_yaml(Path(exceptions_path))
        doc = _mapping(raw, "exceptions document")
        _keys(doc, {"schema_version", "exceptions"}, {"schema_version", "exceptions"}, "exceptions document")
        if type(doc["schema_version"]) is not int or doc["schema_version"] != 1:
            raise PolicyError("unsupported exceptions schema version")
        entries = doc["exceptions"]
        if not isinstance(entries, list):
            raise PolicyError("exceptions must be a list")
        validated = [_validate_exception(item, policy, today) for item in entries]
    except Exception as exc:
        if isinstance(exc, PolicyError):
            raise
        raise PolicyError("trusted exceptions file is invalid") from exc

    by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    for item in validated:
        key = (item["rule_id"], item["path"], item["content_sha256"])
        if key in by_key:
            raise PolicyError("duplicate exception entry")
        by_key[key] = item
    hashes = {item.path: sha256(item.data).hexdigest() for item in files}
    result: list[Finding] = []
    for item in findings:
        if item.severity == "error" and item.rule_id != "SEC001":
            exception = by_key.get((item.rule_id, item.path, hashes.get(item.path, "")))
            if exception:
                item = replace(
                    item,
                    severity="notice",
                    message="Finding covered by a trusted, time-limited exception: "
                    + _safe_rationale(exception["reason"]),
                )
        result.append(item)
    return tuple(result)


def _safe_rationale(text: str) -> str:
    """Keep exception rationale from injecting report markup or controls."""
    clean = "".join(ch for ch in text if ch >= " " and ch != "\x7f")
    clean = " ".join(clean.split())
    return clean.replace("`", "'").replace("<", "(").replace(">", ")").replace("|", "/")[:300]
