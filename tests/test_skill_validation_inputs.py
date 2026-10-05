import hashlib
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from scripts.skill_validation.catalog import discover
from scripts.skill_validation.git_tree import InputError, read_tree
from scripts.skill_validation.models import SourceFile


class SkillValidationInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Input Test")

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args, input=None):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            input=input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout

    def commit_files(self, files):
        for name, data in files.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.git("add", "--all")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD").decode().strip()

    def test_reads_regular_tree_and_preserves_utf8_names_and_modes(self):
        sha = self.commit_files({"alpha/SKILL.md": b"---\nname: alpha\n---\nBody\n", "alpha/refs/café.md": b"ref"})

        files = read_tree(self.repo, sha, max_bytes=1024)

        self.assertEqual([(f.path, f.mode, f.data) for f in files], [
            ("alpha/SKILL.md", "100644", b"---\nname: alpha\n---\nBody\n"),
            ("alpha/refs/café.md", "100644", b"ref"),
        ])

    def test_reads_immutable_revision_after_rename_and_deletion(self):
        old_sha = self.commit_files({"alpha/SKILL.md": b"old", "alpha/old.md": b"move me", "beta/SKILL.md": b"delete me"})
        self.git("mv", "alpha/old.md", "alpha/new.md")
        self.git("rm", "beta/SKILL.md")
        self.git("commit", "-qm", "rename and delete")
        new_sha = self.git("rev-parse", "HEAD").decode().strip()

        old_paths = {f.path for f in read_tree(self.repo, old_sha, max_bytes=1024)}
        new_paths = {f.path for f in read_tree(self.repo, new_sha, max_bytes=1024)}

        self.assertIn("alpha/old.md", old_paths)
        self.assertIn("beta/SKILL.md", old_paths)
        self.assertNotIn("alpha/old.md", new_paths)
        self.assertNotIn("beta/SKILL.md", new_paths)
        self.assertIn("alpha/new.md", new_paths)

    def test_bundle_only_change_is_discovered_as_orphan(self):
        sha = self.commit_files({"alpha.skill": b"bundle", "some-root.md": b"overview"})
        files = read_tree(self.repo, sha, max_bytes=1024)

        skills, findings = discover(files)

        self.assertEqual(skills, ())
        self.assertEqual([(f.rule_id, f.path, f.severity) for f in findings], [("INV003", "alpha.skill", "error")])

    def test_preserves_agent_yaml_inside_skill(self):
        sha = self.commit_files({"alpha/SKILL.md": b"body", "alpha/agents/reviewer.yaml": b"name: reviewer\n"})

        skills, findings = discover(read_tree(self.repo, sha, max_bytes=1024))

        self.assertEqual(findings, ())
        self.assertEqual(skills[0].name, "alpha")
        self.assertEqual([f.path for f in skills[0].files], ["alpha/SKILL.md", "alpha/agents/reviewer.yaml"])

    def test_orphan_bundle_and_missing_skill_manifest_are_reported(self):
        files = (
            SourceFile("alpha/notes.md", b"notes", "100644"),
            SourceFile("orphan.skill", b"zip", "100644"),
        )

        skills, findings = discover(files)

        self.assertEqual(skills, ())
        self.assertEqual({(f.rule_id, f.path) for f in findings}, {("INV002", "alpha"), ("INV003", "orphan.skill")})

    def test_infrastructure_and_root_documents_are_not_reported_as_skills(self):
        self.assertEqual(discover(()), ((), ()))
        files = (
            SourceFile("README.md", b"repo", "100644"),
            SourceFile("scripts/check.py", b"print('safe')", "100644"),
            SourceFile("security/policy.yaml", b"version: 1", "100644"),
            SourceFile(".conductor/config.yaml", b"trusted: false", "100644"),
        )
        self.assertEqual(discover(files), ((), ()))

    def test_unexpected_root_directory_is_reported(self):
        skills, findings = discover((SourceFile("random/data.txt", b"data", "100644"),))
        self.assertEqual(skills, ())
        self.assertEqual([(f.rule_id, f.path) for f in findings], [("INV002", "random")])

    def test_rejects_symlinks_and_gitlinks_before_reading_content(self):
        self.git("config", "core.filemode", "true")
        (self.repo / "target").write_text("target")
        (self.repo / "link").symlink_to("target")
        self.git("add", "target", "link")
        self.git("update-index", "--add", "--cacheinfo", "160000", "1111111111111111111111111111111111111111", "submodule")
        self.git("commit", "-qm", "unsafe modes")
        sha = self.git("rev-parse", "HEAD").decode().strip()

        with self.assertRaisesRegex(InputError, "unsupported Git entry mode"):
            read_tree(self.repo, sha, max_bytes=1024)

    def test_control_character_path_blocks_without_echoing_raw_name(self):
        self.git("config", "core.quotePath", "false")
        path = self.repo / "alpha" / "bad\nname.md"
        path.parent.mkdir()
        path.write_bytes(b"secret-ish data")
        self.git("add", "--all")
        self.git("commit", "-qm", "control path")
        sha = self.git("rev-parse", "HEAD").decode().strip()

        with self.assertRaises(InputError) as raised:
            read_tree(self.repo, sha, max_bytes=1024)
        self.assertNotIn("\n", str(raised.exception))

    def test_rejects_bad_revision_and_resource_overruns_before_blob_read(self):
        sha = self.commit_files({"alpha/SKILL.md": b"x" * 64})
        for revision, limit in (("HEAD", 1024), ("0" * 40, 1024), (sha, 32)):
            with self.subTest(revision=revision, limit=limit):
                with self.assertRaises(InputError):
                    read_tree(self.repo, revision, max_bytes=limit)

    def test_rejects_case_colliding_git_paths(self):
        self.commit_files({"alpha/SKILL.md": b"body"})
        self.git("config", "core.ignorecase", "false")
        one = self.git("hash-object", "-w", "--stdin", input=b"one").decode().strip()
        two = self.git("hash-object", "-w", "--stdin", input=b"two").decode().strip()
        self.git("update-index", "--add", "--cacheinfo", "100644", one, "alpha/Guide.md")
        self.git("update-index", "--add", "--cacheinfo", "100644", two, "alpha/guide.md")
        self.git("commit", "-qm", "case collision")
        sha = self.git("rev-parse", "HEAD").decode().strip()

        with self.assertRaisesRegex(InputError, "case-colliding paths"):
            read_tree(self.repo, sha, max_bytes=1024)

    def test_caps_tree_listing_output_before_requesting_any_blobs(self):
        from unittest.mock import patch
        from scripts.skill_validation import git_tree

        sha = self.commit_files({"alpha/SKILL.md": b"body"})
        with patch.object(git_tree, "MAX_TREE_OUTPUT_BYTES", 1):
            with self.assertRaisesRegex(InputError, "output exceeds"):
                read_tree(self.repo, sha, max_bytes=1024)

    def test_discover_reports_case_colliding_synthetic_paths(self):
        files = (
            SourceFile("alpha/SKILL.md", b"body", "100644"),
            SourceFile("alpha/Guide.md", b"one", "100644"),
            SourceFile("alpha/guide.md", b"two", "100644"),
        )

        skills, findings = discover(files)

        self.assertEqual([skill.name for skill in skills], ["alpha"])
        self.assertEqual([(f.rule_id, f.path) for f in findings], [("INV004", "alpha/guide.md")])

    def test_rejects_case_colliding_directory_prefixes(self):
        self.commit_files({"alpha/SKILL.md": b"body"})
        self.git("config", "core.ignorecase", "false")
        one = self.git("hash-object", "-w", "--stdin", input=b"one").decode().strip()
        two = self.git("hash-object", "-w", "--stdin", input=b"two").decode().strip()
        self.git("update-index", "--add", "--cacheinfo", "100644", one, "alpha/Guide/A.md")
        self.git("update-index", "--add", "--cacheinfo", "100644", two, "alpha/guide/B.md")
        self.git("commit", "-qm", "case-colliding directories")
        sha = self.git("rev-parse", "HEAD").decode().strip()

        with self.assertRaisesRegex(InputError, "case-colliding paths"):
            read_tree(self.repo, sha, max_bytes=1024)

    def test_discover_rejects_case_colliding_directory_prefixes(self):
        files = (
            SourceFile("alpha/SKILL.md", b"body", "100644"),
            SourceFile("alpha/Guide/A.md", b"one", "100644"),
            SourceFile("alpha/guide/B.md", b"two", "100644"),
        )

        skills, findings = discover(files)

        self.assertEqual([skill.name for skill in skills], ["alpha"])
        self.assertEqual([(f.rule_id, f.path) for f in findings], [("INV004", "alpha/guide/B.md")])

    def test_discover_blocks_skill_manifests_outside_direct_skill_roots(self):
        files = (
            SourceFile("alpha/SKILL.md", b"body", "100644"),
            SourceFile("alpha/nested/SKILL.md", b"nested instructions", "100644"),
            SourceFile("docs/hidden/SKILL.md", b"ignored root instructions", "100644"),
        )

        skills, findings = discover(files)

        self.assertEqual([skill.name for skill in skills], ["alpha"])
        self.assertEqual({(f.rule_id, f.path) for f in findings}, {
            ("INV005", "alpha/nested/SKILL.md"),
            ("INV005", "docs/hidden/SKILL.md"),
        })

    def test_unicode_directory_spellings_cannot_alias(self):
        files = (
            SourceFile('alpha/SKILL.md', b'body', '100644'),
            SourceFile('alpha/caf\u00e9/a.md', b'one', '100644'),
            SourceFile('alpha/cafe\u0301/b.md', b'two', '100644'),
        )
        _, findings = discover(files)
        self.assertIn('INV004', {item.rule_id for item in findings})

    def test_git_reader_enforces_timeout_during_bounded_stdout_read(self):
        from scripts.skill_validation.git_tree import _run_command

        start = time.monotonic()
        with self.assertRaisesRegex(InputError, "timed out"):
            _run_command(
                [sys.executable, "-c", "import sys,time; sys.stdout.write('x'); sys.stdout.flush(); time.sleep(10)"],
                timeout=0.1,
                max_output_bytes=10,
            )
        self.assertLess(time.monotonic() - start, 2)

    def test_blob_which_would_write_a_sentinel_is_only_returned_as_data(self):
        sentinel = self.repo / "sentinel-created-on-execution"
        code = f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('executed')\n".encode()
        sha = self.commit_files({"alpha/SKILL.md": b"description", "alpha/refs/payload.py": code})

        files = read_tree(self.repo, sha, max_bytes=4096)

        self.assertFalse(sentinel.exists())
        self.assertEqual(next(f.data for f in files if f.path.endswith("payload.py")), code)

    def test_finding_fingerprint_uses_rule_path_and_content_digest(self):
        from scripts.skill_validation.models import finding

        first = finding("SEC001", "error", "a.md", 2, "redacted", b"secret")
        second = finding("SEC001", "error", "a.md", 2, "redacted", b"different")
        expected_content_hash = hashlib.sha256(b"secret").hexdigest()
        self.assertNotEqual(first.fingerprint, second.fingerprint)
        self.assertEqual(len(first.fingerprint), 64)
        self.assertEqual(first.fingerprint, hashlib.sha256(f"SEC001\0a.md\0{expected_content_hash}".encode()).hexdigest())


if __name__ == "__main__":
    unittest.main()
