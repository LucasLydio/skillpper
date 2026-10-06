import unittest

from scripts.skill_validation.duplicates import compare_skills
from scripts.skill_validation.models import Skill, SourceFile


def skill(name, body, description="A clear description for a learning workflow."):
    raw = f"---\nname: {name}\ndescription: {description}\n---\n{body}".encode("utf-8")
    return Skill(name, (SourceFile(f"{name}/SKILL.md", raw, "100644"),))


class SkillDuplicateTests(unittest.TestCase):
    def test_identical_bodies_under_different_names_are_blocked(self):
        body = "# Steps\n1. Ask the learner to predict.\n2. Explain the result.\n"
        findings = compare_skills((skill("alpha", body), skill("beta", body)))
        self.assertEqual(len(findings), 1)
        self.assertEqual((findings[0].rule_id, findings[0].severity), ("DUP001", "error"))

    def test_unicode_whitespace_and_line_endings_normalize_for_exact_matching(self):
        findings = compare_skills((
            skill("alpha", "Cafe\u0301\r\n  pratique\t maintenant.\r\n"),
            skill("beta", "Café pratique maintenant.\n"),
        ))
        self.assertEqual([item.rule_id for item in findings], ["DUP001"])

    def test_common_boilerplate_with_different_bodies_is_not_exact_duplicate(self):
        left = "Shared instruction.\n\nA unique exploration of sorting algorithms.\n"
        right = "Shared instruction.\n\nA unique exploration of database transactions.\n"
        findings = compare_skills((skill("alpha", left), skill("beta", right)))
        self.assertNotIn("DUP001", {item.rule_id for item in findings})

    def test_one_skill_is_not_compared_with_itself(self):
        self.assertEqual(compare_skills((skill("alone", "A body."),)), ())

    def test_substantive_lexical_overlap_is_review_with_safe_pair_details(self):
        shared = " ".join(f"learningword{i}" for i in range(40))
        left = shared + " lefttopic uniqueleft"
        right = shared + " righttopic uniqueright"
        findings = compare_skills((skill("alpha", left), skill("beta", right)))
        review = [item for item in findings if item.rule_id == "DUP002"]
        self.assertEqual(len(review), 1)
        self.assertEqual(review[0].severity, "review")
        self.assertIn("alpha/SKILL.md", review[0].path)
        self.assertIn("beta/SKILL.md", review[0].message)
        self.assertIn("0.", review[0].message)

    def test_paraphrases_without_lexical_overlap_do_not_match(self):
        left = " " .join(f"alpha{i}" for i in range(40))
        right = " " .join(f"omega{i}" for i in range(40))
        self.assertEqual(compare_skills((skill("alpha", left), skill("beta", right))), ())

    def test_portuguese_text_and_minimum_token_threshold(self):
        portuguese = "O estudante prevê a resposta antes de receber a explicação."
        findings = compare_skills((skill("alpha", portuguese), skill("beta", portuguese)))
        self.assertEqual([item.rule_id for item in findings], ["DUP001"])
        short = "one two three four five six seven eight nine ten"
        self.assertEqual(compare_skills((skill("alpha", short), skill("beta", short + " extra"))), ())

    def test_pair_order_is_stable(self):
        body = "repeated words form an exact same instruction"
        findings = compare_skills((skill("charlie", body), skill("alpha", body), skill("bravo", body)))
        self.assertEqual([item.path for item in findings], [
            "alpha/SKILL.md", "alpha/SKILL.md", "bravo/SKILL.md",
        ])
        self.assertIn("bravo/SKILL.md", findings[0].message)
        self.assertIn("charlie/SKILL.md", findings[1].message)
        self.assertIn("charlie/SKILL.md", findings[2].message)


if __name__ == "__main__":
    unittest.main()
