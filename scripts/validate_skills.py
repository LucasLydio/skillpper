#!/usr/bin/env python3
"""Inspect skills as data. Git mode uses this checkout's verified base policy."""

import argparse
from datetime import date
from pathlib import Path
import re
import stat
import subprocess
import sys

# With python -I, only this explicitly trusted package directory is added.
TRUSTED_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TRUSTED_ROOT / 'scripts'))

from skill_validation.git_tree import InputError, read_tree, _safe_tree_path, _per_file_limit
from skill_validation.models import ScanResult, SourceFile, finding
from skill_validation.policy import apply_exceptions, load_policy
from skill_validation.report import exit_code, write_reports
from skill_validation.runner import MAX_SCAN_BYTES, validate


def _git(repo: Path, *args: str) -> bytes:
    try:
        result = subprocess.run(['git', '-C', str(repo), *args], check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=30)
        return result.stdout
    except (OSError, subprocess.SubprocessError):
        raise InputError('Git operation failed') from None


def _read_worktree(root: Path) -> tuple[SourceFile, ...]:
    """Local author aid: Git selects paths, lstat prevents following symlinks."""
    paths = _git(root, 'ls-files', '--cached', '--others', '--exclude-standard', '-z')
    result = []
    total = 0
    counts = {}
    seen = set()
    for raw in sorted(set(paths.split(b'\0')) - {b''}):
        name, first = _safe_tree_path(raw)
        folded = name.casefold()
        if folded in seen:
            raise InputError('Case-colliding paths are unsupported')
        seen.add(folded)
        counts[first] = counts.get(first, 0) + 1
        if counts[first] > 500:
            raise InputError('File-count limit exceeded')
        path = root / name
        if not path.exists() and not path.is_symlink():
            # A tracked deletion belongs to the proposed local worktree state.
            continue
        for parent in path.parents:
            if parent == root:
                break
            if parent.is_symlink():
                raise InputError('Symlink ancestor is unsupported')
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode):
            raise InputError('Only regular files can be inspected')
        limit = _per_file_limit(name)
        if metadata.st_size > limit:
            raise InputError('Per-file limit exceeded')
        with path.open('rb') as stream:
            data = stream.read(limit + 1)
        if len(data) > limit:
            raise InputError('Per-file limit exceeded')
        total += len(data)
        if total > MAX_SCAN_BYTES:
            raise InputError('Scan budget exceeded')
        result.append(SourceFile(name, data, '100755' if metadata.st_mode & stat.S_IXUSR else '100644'))
    return tuple(result)


def _verify_trusted_base(repo: Path, base_sha: str) -> None:
    if repo != TRUSTED_ROOT:
        raise InputError('Git mode requires the trusted launcher inside the base checkout')
    if _git(repo, 'rev-parse', 'HEAD').decode('ascii').strip() != base_sha:
        raise InputError('Trusted checkout is not the declared base revision')
    sources = read_tree(repo, base_sha, MAX_SCAN_BYTES)
    protected = ('scripts/skill_validation/', 'security/')
    exact = {'scripts/validate_skills.py', 'scripts/requirements-validation.txt'}
    for source in sources:
        if source.path in exact or source.path.startswith(protected):
            path = repo / source.path
            if path.is_symlink() or not path.is_file() or path.read_bytes() != source.data:
                raise InputError('Trusted validator or policy differs from the base revision')
    if not any(source.path == 'scripts/validate_skills.py' for source in sources):
        raise InputError('Base revision has no validator; bootstrap is not yet enforced')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--repo', type=Path)
    mode.add_argument('--worktree', type=Path)
    parser.add_argument('--base-sha')
    parser.add_argument('--candidate-sha')
    parser.add_argument('--json', type=Path, required=True)
    parser.add_argument('--markdown', type=Path, required=True)
    args = parser.parse_args()
    candidate_sha = 'worktree'
    policy_sha = 'local-worktree-policy'
    try:
        if args.repo is not None:
            if not all(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', value)
                       for value in (args.base_sha, args.candidate_sha)):
                raise InputError('Git mode requires full base and candidate commit SHAs')
            candidate_sha, policy_sha = args.candidate_sha, args.base_sha
            repo = args.repo.resolve()
            _verify_trusted_base(repo, args.base_sha)
            files = read_tree(repo, args.candidate_sha, MAX_SCAN_BYTES)
        else:
            if args.base_sha or args.candidate_sha:
                raise InputError('Revision arguments cannot be used with worktree mode')
            files = _read_worktree(args.worktree.resolve())
        policy_dir = TRUSTED_ROOT / 'security'
        policy = load_policy(policy_dir / 'skill-validation-policy.yaml')
        result = validate(files, policy, candidate_sha, policy_sha)
        if result.complete:
            findings = apply_exceptions(result.findings, files,
                                        policy_dir / 'skill-validation-exceptions.yaml', date.today(), policy=policy)
            result = ScanResult(findings, True, candidate_sha, policy_sha)
    except Exception:
        result = ScanResult((finding('SCAN001', 'error', 'validation', None,
                                    'Input, policy, or scan failed. No passing result is available.', b''),),
                            False, candidate_sha, policy_sha)
    try:
        write_reports(result, args.json, args.markdown)
    except Exception:
        print('Could not write validation reports. Scan must not be treated as passing.', file=sys.stderr)
        return 2
    code = exit_code(result)
    print(f'Skill validation exit code: {code}. See the generated redacted report.')
    return code


if __name__ == '__main__':
    sys.exit(main())
