import stat
import unittest
from pathlib import Path

from scripts.skill_validation.bundles import validate_bundle
from scripts.skill_validation.models import Skill, SourceFile


ROOT = Path(__file__).resolve().parents[1]


class SkillBundleTests(unittest.TestCase):
    def test_optional_archives_match_their_complete_source_tree(self):
        bundles = sorted(ROOT.glob("*.skill"))
        self.assertTrue(bundles, "expected at least one distributable skill bundle")

        for bundle_path in bundles:
            with self.subTest(bundle=bundle_path.name):
                source_root = ROOT / bundle_path.stem
                self.assertTrue(source_root.is_dir())
                files = []
                for source_path in sorted(source_root.rglob("*")):
                    if source_path.is_symlink():
                        mode = "120000"
                        data = source_path.readlink().as_posix().encode("utf-8")
                    elif source_path.is_file():
                        mode = "100755" if source_path.stat().st_mode & stat.S_IXUSR else "100644"
                        data = source_path.read_bytes()
                    else:
                        continue
                    relative = source_path.relative_to(ROOT).as_posix()
                    files.append(SourceFile(relative, data, mode))
                skill = Skill(bundle_path.stem, tuple(files))
                archive = SourceFile(bundle_path.name, bundle_path.read_bytes(), "100644")
                self.assertEqual(validate_bundle(archive, skill), ())


if __name__ == "__main__":
    unittest.main()
