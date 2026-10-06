import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CLITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'trusted'
        self.repo.mkdir()
        shutil.copytree(ROOT / 'scripts', self.repo / 'scripts',
                        ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / 'security', self.repo / 'security')
        (self.repo / 'README.md').write_text('A harmless project.\n')
        self.git('init', '-q')
        # Keep the trusted base checkout byte-identical to Git blobs on
        # Windows, where global autocrlf settings otherwise rewrite files.
        self.git('config', 'core.autocrlf', 'false')
        self.git('config', 'core.eol', 'lf')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'trusted scanner')
        self.base = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.repo), '-c', 'core.hooksPath=/dev/null', *args],
                                capture_output=True, text=True, check=True)
        return result.stdout

    def run_cli(self, *args):
        result = subprocess.run([sys.executable, '-I', str(self.repo / 'scripts/validate_skills.py'),
                                 *args, '--json', str(self.root / 'report.json'),
                                 '--markdown', str(self.root / 'report.md')],
                                capture_output=True, text=True, timeout=60)
        return result

    def test_base_scanner_ignores_candidate_replacements(self):
        sentinel = self.root / 'executed'
        payload = f'from pathlib import Path\nPath({str(sentinel)!r}).write_text("executed")\n'
        (self.repo / 'scripts/validate_skills.py').write_text(payload)
        (self.repo / 'scripts/yaml.py').write_text(payload)
        (self.repo / 'security/skill-validation-policy.yaml').write_text('disable_all: true\n')
        (self.repo / 'README.md').write_text('credential: ghp_' + 'x' * 36)
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'untrusted payload')
        candidate = self.git('rev-parse', 'HEAD').strip()
        self.git('checkout', '-q', '--detach', self.base)
        result = self.run_cli('--repo', str(self.repo), '--base-sha', self.base, '--candidate-sha', candidate)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        report = json.loads((self.root / 'report.json').read_text())
        self.assertIn('SEC001', {f['rule_id'] for f in report['findings']})
        self.assertFalse(sentinel.exists())
        self.assertNotIn('ghp_' + 'x' * 36, result.stdout + result.stderr + json.dumps(report))

    def test_worktree_mode_rejects_symlink_without_reading_target(self):
        secret = self.root / 'outside.txt'
        secret.write_text('not part of candidate')
        (self.repo / 'README.md').unlink()
        try:
            (self.repo / 'README.md').symlink_to(secret)
        except OSError:
            self.skipTest('symlinks unavailable for this platform/account')
        result = self.run_cli('--worktree', str(self.repo))
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads((self.root / 'report.json').read_text())['complete'])

    def test_unavailable_candidate_is_not_success(self):
        result = self.run_cli('--repo', str(self.repo), '--base-sha', self.base, '--candidate-sha', 'f' * 40)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads((self.root / 'report.json').read_text())['complete'])

    def test_modified_trusted_policy_is_rejected(self):
        (self.repo / 'security/skill-validation-policy.yaml').write_text('schema_version: 1\nmaintainers: [attacker]\n')
        result = self.run_cli('--repo', str(self.repo), '--base-sha', self.base, '--candidate-sha', self.base)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads((self.root / 'report.json').read_text())['complete'])


if __name__ == '__main__':
    unittest.main()
