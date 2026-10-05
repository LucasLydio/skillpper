"""Deterministic, redacted reports; never emit workflow command annotations."""

from collections import Counter
from dataclasses import asdict
import html
import json
from pathlib import Path
import re

from .models import ScanResult


_SECRET = re.compile(
    r'ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82}'
    r'|(?:AKIA|ASIA)[A-Z0-9]{16}'
    r'|-----BEGIN [^-\r\n]*PRIVATE KEY-----[\s\S]*?-----END [^-\r\n]*PRIVATE KEY-----'
)


def _redact(value: str) -> str:
    value = _SECRET.sub('[REDACTED]', value)
    return ''.join(char if char.isprintable() else '?' for char in value)


def _markdown(value: str) -> str:
    value = html.escape(_redact(value), quote=True)
    for char, escaped in (('|', '&#124;'), ('`', '&#96;'), ('[', '&#91;'),
                          (']', '&#93;'), ('*', '&#42;'), ('_', '&#95;'),
                          ('\\', '&#92;'), (':', '&#58;')):
        value = value.replace(char, escaped)
    return value


def exit_code(result: ScanResult) -> int:
    if not result.complete:
        return 2
    return 1 if any(item.severity == 'error' for item in result.findings) else 0


def write_reports(result: ScanResult, json_path: Path, markdown_path: Path) -> None:
    """Caller supplies trusted destinations. IO failures must fail the CLI."""
    findings = sorted(result.findings, key=lambda f: (f.path, f.rule_id, f.line or 0, f.fingerprint))
    counts = Counter(item.severity for item in findings)
    payload = {
        'schema_version': 1,
        'candidate_sha': result.candidate_sha,
        'policy_sha': result.policy_sha,
        'complete': result.complete,
        'exit_code': exit_code(result),
        'counts': {kind: counts[kind] for kind in ('error', 'review', 'notice')},
        'findings': [
            {key: _redact(value) if isinstance(value, str) else value
             for key, value in asdict(item).items()}
            for item in findings
        ],
    }
    if not result.complete:
        status = 'Scan incomplete. Merge must remain blocked.'
    elif counts['error']:
        status = 'Static checks failed. Resolve blocking findings before merge.'
    else:
        status = 'Static checks passed; maintainer review is still required.'
    lines = [
        '# Skill validation', '', status, '',
        f'Candidate: {_markdown(result.candidate_sha)}',
        f'Policy revision: {_markdown(result.policy_sha)}', '',
        f"Errors: {counts['error']} · Review: {counts['review']} · Notices: {counts['notice']}", '',
        'Static inspection only. Skills and review cases were not executed.', '',
    ]
    if findings:
        lines += ['| Severity | Rule | Location | Finding |', '| --- | --- | --- | --- |']
        for item in findings:
            location = item.path + (f':{item.line}' if item.line is not None else '')
            cells = (item.severity, item.rule_id, location, item.message)
            lines.append('| ' + ' | '.join(_markdown(cell) for cell in cells) + ' |')
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    markdown_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
