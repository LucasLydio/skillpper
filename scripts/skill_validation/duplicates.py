"""Deterministic exact and lexical-overlap reporting for skill bodies."""

from __future__ import annotations

import hashlib
import re
import unicodedata

from .models import Finding, Skill, finding, safe_path
from .structure import parse_frontmatter


_TOKEN = re.compile(r"[^\W_]+", re.UNICODE)


def _normalized_body(skill: Skill) -> tuple[str, str] | None:
    path = f"{skill.name}/SKILL.md"
    source = next((item for item in skill.files if item.path == path), None)
    if source is None:
        return None
    try:
        metadata, body = parse_frontmatter(source.data)
    except ValueError:
        return None
    description = metadata.get("description")
    if not isinstance(description, str):
        return None
    text = unicodedata.normalize("NFC", body.replace("\r\n", "\n").replace("\r", "\n"))
    text = " ".join(text.split())
    return description, text


def _tokens(description: str, body: str) -> set[str]:
    combined = unicodedata.normalize("NFC", f"{description}\n{body}").casefold()
    return set(_TOKEN.findall(combined))


def _safe_shared_words(words: set[str]) -> list[str]:
    def entropy(word: str) -> float:
        from collections import Counter
        import math
        counts = Counter(word)
        return -sum((count / len(word)) * math.log2(count / len(word)) for count in counts.values())

    safe = []
    for word in sorted(words):
        if 3 <= len(word) <= 24 and word.isalpha() and entropy(word) <= 3.7:
            safe.append(word)
        if len(safe) == 10:
            break
    return safe


def compare_skills(skills: tuple[Skill, ...]) -> tuple[Finding, ...]:
    """Compare each sorted pair once; exact copies block, lexical overlap reviews."""
    records = []
    for skill in skills:
        normalized = _normalized_body(skill)
        if normalized is None:
            continue
        description, body = normalized
        body_bytes = body.encode("utf-8")
        records.append((f"{skill.name}/SKILL.md", body, body_bytes, _tokens(description, body)))
    records.sort(key=lambda record: record[0])

    findings: list[Finding] = []
    for left_index, left in enumerate(records):
        for right in records[left_index + 1:]:
            left_path, left_body, left_bytes, left_tokens = left
            right_path, right_body, right_bytes, right_tokens = right
            pair_bytes = left_bytes + b"\0" + right_bytes
            if left_body == right_body:
                findings.append(finding(
                    "DUP001", "error", left_path, None,
                    f"Skill body duplicates {safe_path(right_path)} after Unicode and whitespace normalization.",
                    pair_bytes,
                ))
                continue
            minimum = min(len(left_tokens), len(right_tokens))
            if minimum < 30:
                continue
            shared = left_tokens & right_tokens
            score = len(shared) / max(1, len(left_tokens | right_tokens))
            if score < 0.65:
                continue
            words = _safe_shared_words(shared)
            details = f" Shared terms: {', '.join(words)}." if words else ""
            findings.append(finding(
                "DUP002", "review", left_path, None,
                f"Potential lexical overlap with {safe_path(right_path)}; similarity {score:.3f}.{details}",
                pair_bytes,
            ))
    return tuple(findings)
