import json
import tempfile
import unittest
from pathlib import Path

from scripts.skill_validation.models import Finding, ScanResult
from scripts.skill_validation.report import exit_code, write_reports


class ReportTests(unittest.TestCase):
    def result(self, findings=(), complete=True):
        return ScanResult(tuple(findings), complete, 'a' * 40, 'b' * 40)

    def item(self, severity='review', path='demo/SKILL.md', message='Needs review.'):
        return Finding('SEC002', severity, path, 3, message, 'c' * 64)

    def test_exit_contract(self):
        self.assertEqual(exit_code(self.result()), 0)
        self.assertEqual(exit_code(self.result([self.item()])), 0)
        self.assertEqual(exit_code(self.result([self.item('error')])), 1)
        self.assertEqual(exit_code(self.result(complete=False)), 2)
        self.assertEqual(exit_code(self.result([self.item('error')], False)), 2)

    def test_reports_are_deterministic_and_show_review_requirement(self):
        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = Path(directory) / 'report.json', Path(directory) / 'report.md'
            result = self.result([self.item()])
            write_reports(result, json_path, markdown_path)
            first = (json_path.read_bytes(), markdown_path.read_bytes())
            write_reports(result, json_path, markdown_path)
            self.assertEqual(first, (json_path.read_bytes(), markdown_path.read_bytes()))
            data = json.loads(first[0])
            self.assertEqual(data['schema_version'], 1)
            self.assertEqual(data['counts']['review'], 1)
            self.assertEqual(data['candidate_sha'], 'a' * 40)
            self.assertIn('maintainer review is still required', first[1].decode())

    def test_candidate_text_cannot_leak_token_or_inject_markup(self):
        fake = 'ghp_' + 'x' * 36
        path = f'demo/{fake}/<script>|`\n::error::bad.md'
        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = Path(directory) / 'a.json', Path(directory) / 'a.md'
            write_reports(self.result([self.item(path=path, message=fake)]), json_path, markdown_path)
            for content in (json_path.read_text(), markdown_path.read_text()):
                self.assertNotIn(fake, content)
                self.assertNotIn('\n::error::', content)
            self.assertNotIn('<script>', markdown_path.read_text())

    def test_incomplete_report_does_not_say_passed(self):
        with tempfile.TemporaryDirectory() as directory:
            json_path, markdown_path = Path(directory) / 'a.json', Path(directory) / 'a.md'
            write_reports(self.result(complete=False), json_path, markdown_path)
            self.assertIn('incomplete', markdown_path.read_text().lower())
            self.assertNotIn('checks passed', markdown_path.read_text())

    def test_bad_destination_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(OSError):
                write_reports(self.result(), Path(directory), Path(directory) / 'a.md')


if __name__ == '__main__':
    unittest.main()
