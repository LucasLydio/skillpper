import io
import stat
import unittest
import zipfile

from scripts.skill_validation.models import Skill, SourceFile
from scripts.skill_validation.bundles import validate_bundle


def make_zip(entries, *, compression=zipfile.ZIP_DEFLATED):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=compression) as archive:
        for name, data in entries:
            if isinstance(name, zipfile.ZipInfo):
                archive.writestr(name, data)
            elif isinstance(data, zipfile.ZipInfo):
                archive.writestr(data, b"" if data.filename.endswith("/") else b"link")
            else:
                archive.writestr(name, data)
    return stream.getvalue()


class SkillBundleValidationTests(unittest.TestCase):
    def setUp(self):
        self.entries = (
            SourceFile("demo/SKILL.md", b"---\nname: demo\ndescription: Demo skill\n---\nInstructions\n", "100644"),
            SourceFile("demo/skill-review.yaml", b"schema_version: 1\n", "100644"),
            SourceFile("demo/docs/guide.md", b"# Guide\n", "100644"),
        )
        self.skill = Skill("demo", self.entries)

    def bundle(self, entries, name="demo.skill"):
        return SourceFile(name, make_zip(entries), "100644")

    def ids(self, bundle, skill=None):
        return {item.rule_id for item in validate_bundle(bundle, skill or self.skill)}

    def test_exact_valid_archive_including_manifest_passes(self):
        bundle = self.bundle([(item.path, item.data) for item in self.entries])
        self.assertEqual(validate_bundle(bundle, self.skill), ())

    def test_extra_missing_and_changed_files_fail_exact_parity(self):
        base = [(item.path, item.data) for item in self.entries]
        self.assertIn("BUNDLE_EXTRA", self.ids(self.bundle(base + [("demo/hidden.py", b"print(1)")])))
        self.assertIn("BUNDLE_MISSING", self.ids(self.bundle(base[:-1])))
        changed = [(item.path, b"changed" if item.path.endswith("guide.md") else item.data) for item in self.entries]
        self.assertIn("BUNDLE_MISMATCH", self.ids(self.bundle(changed)))

    def test_rejects_unsafe_duplicate_and_casefold_paths(self):
        valid = [(item.path, item.data) for item in self.entries]
        for extra in ("../outside.txt", "/absolute.txt", "C:/drive.txt", "demo\\escape.txt", "demo/bad\x01.txt"):
            with self.subTest(extra=extra):
                self.assertTrue(self.ids(self.bundle(valid + [(extra, b"x")])) )
        duplicate = self.bundle(valid + [("demo/SKILL.md", b"again")])
        self.assertTrue(self.ids(duplicate))
        collision = self.bundle(valid + [("demo/Docs/guide.md", b"case")])
        self.assertIn("BUNDLE_COLLISION", self.ids(collision))
        prefix_collision = self.bundle(valid + [("demo/Guide/a.md", b"a"), ("demo/guide/b.md", b"b")])
        self.assertIn("BUNDLE_COLLISION", self.ids(prefix_collision))
        unicode_collision = self.bundle(valid + [("demo/caf\u00e9/a.md", b"a"), ("demo/cafe\u0301/b.md", b"b")])
        self.assertIn("BUNDLE_COLLISION", self.ids(unicode_collision))

    def test_safe_directory_entries_are_allowed_even_with_windows_zero_mode(self):
        info = zipfile.ZipInfo("demo/docs/")
        info.create_system = 0
        info.external_attr = 0
        bundle = self.bundle([(item.path, item.data) for item in self.entries] + [("demo/docs/", info)])
        self.assertEqual(validate_bundle(bundle, self.skill), ())

    def test_rejects_directory_entries_outside_skill_and_unused_empty_directories(self):
        valid = [(item.path, item.data) for item in self.entries]
        for dirname in ("outside/", "demo/empty/"):
            with self.subTest(dirname=dirname):
                info = zipfile.ZipInfo(dirname)
                self.assertTrue(self.ids(self.bundle(valid + [(dirname, info)])))

    def test_rejects_nul_hidden_in_original_zip_member_name(self):
        entries = [(item.path, item.data) for item in self.entries]
        entries[0] = ("demo/SKILL.mdXignored", self.entries[0].data)
        raw = bytearray(make_zip(entries))
        original_name = b"demo/SKILL.mdXignored"
        start_positions = []
        start = 0
        while True:
            offset = raw.find(original_name, start)
            if offset < 0:
                break
            start_positions.append(offset)
            start = offset + len(original_name)
        self.assertEqual(len(start_positions), 2)
        nul_offset = len(b"demo/SKILL.md")
        for offset in start_positions:
            raw[offset + nul_offset] = 0
        bundle = SourceFile("demo.skill", bytes(raw), "100644")
        self.assertTrue(self.ids(bundle))

    def test_archive_images_cannot_carry_executable_mode(self):
        sources = self.entries + (
            SourceFile("demo/assets/tiny.png", b"\x89PNG\r\n\x1a\n", "100644"),
            SourceFile("demo/assets/tiny.jpg", b"\xff\xd8\xff", "100644"),
            SourceFile("demo/assets/tiny.webp", b"RIFF\x04\x00\x00\x00WEBP", "100644"),
        )
        skill = Skill("demo", sources)
        entries = [(item.path, item.data) for item in sources]
        for index, (path, data) in enumerate(entries):
            if path.endswith((".png", ".jpg", ".webp")):
                info = zipfile.ZipInfo(path)
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o755) << 16
                entries[index] = (info, data)
        self.assertTrue(self.ids(self.bundle(entries), skill))

    def test_rejects_symlink_encrypted_nested_archive_and_bad_crc(self):
        valid = [(item.path, item.data) for item in self.entries]
        symlink = zipfile.ZipInfo("demo/link")
        symlink.create_system = 3
        symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.assertTrue(self.ids(self.bundle(valid + [("demo/link", symlink)])))
        # Mutate the central-directory encryption flag while preserving the archive shape.
        encrypted = bytearray(make_zip(valid))
        offset = encrypted.find(b"PK\x01\x02")
        self.assertGreaterEqual(offset, 0)
        encrypted[offset + 8] |= 1
        self.assertTrue(self.ids(SourceFile("demo.skill", bytes(encrypted), "100644")))
        nested = self.bundle(valid + [("demo/other.zip", b"PK\x03\x04\x00")])
        self.assertTrue(self.ids(nested))
        corrupt = bytearray(make_zip(valid))
        central_offset = corrupt.find(b"PK\x01\x02")
        self.assertGreaterEqual(central_offset, 0)
        corrupt[central_offset + 16] ^= 0x01
        self.assertTrue(self.ids(SourceFile("demo.skill", bytes(corrupt), "100644")))

    def test_rejects_too_many_entries_and_excessive_compression_ratio(self):
        many = [(f"demo/f{i}.txt", b"x") for i in range(501)]
        self.assertTrue(self.ids(self.bundle(many)))
        directories = []
        for index in range(501):
            info = zipfile.ZipInfo(f"demo/d{index}/")
            directories.append((info.filename, info))
        self.assertTrue(self.ids(self.bundle(directories)))
        bomb = self.bundle([("demo/SKILL.md", b"A" * 100_000)])
        self.assertTrue(self.ids(bomb))

    def test_rejects_source_symlink_and_opaque_binary(self):
        archive = self.bundle([(item.path, item.data) for item in self.entries])
        symlink_skill = Skill("demo", (SourceFile("demo/SKILL.md", b"x", "120000"),))
        self.assertTrue(self.ids(archive, symlink_skill))
        opaque_skill = Skill("demo", self.entries + (SourceFile("demo/blob.bin", b"\x00\xff", "100644"),))
        opaque_archive = self.bundle([(item.path, item.data) for item in opaque_skill.files])
        self.assertTrue(self.ids(opaque_archive, opaque_skill))


if __name__ == "__main__":
    unittest.main()
