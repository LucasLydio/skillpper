from pathlib import Path
import tempfile
import unittest

from scripts.update_skill_votes import (
    dashboard_data,
    parse_skill_marker,
    read_skill_metadata,
    render_ranking,
    thumbs_up_count,
    vote_body,
)


class SkillVotesTests(unittest.TestCase):
    def test_vote_body_contains_parseable_marker(self):
        body = vote_body("design-craft")
        self.assertEqual(parse_skill_marker(body), "design-craft")

    def test_render_ranking_sorts_by_votes_then_name(self):
        skills = {
            "study-quiz": "Quiz helper",
            "design-craft": "Design helper",
            "technical-talk-research": "Research helper",
        }
        discussions = {
            "study-quiz": {
                "url": "https://github.com/example/repo/discussions/2",
                "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 7}}],
            },
            "design-craft": {
                "url": "https://github.com/example/repo/discussions/1",
                "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 7}}],
            },
        }

        ranking = render_ranking(skills, discussions, "Skill Votes")

        self.assertLess(ranking.index("[design-craft]"), ranking.index("[study-quiz]"))
        self.assertLess(ranking.index("[study-quiz]"), ranking.index("[technical-talk-research]"))
        self.assertIn("| 1 | [design-craft](./design-craft/SKILL.md) | 7 | [Vote](", ranking)
        self.assertIn("| 3 | [technical-talk-research](./technical-talk-research/SKILL.md) | 0 | Not created yet |", ranking)

    def test_thumbs_up_count_ignores_other_reactions(self):
        discussion = {
            "reactionGroups": [
                {"content": "HEART", "users": {"totalCount": 10}},
                {"content": "THUMBS_UP", "users": {"totalCount": 3}},
            ]
        }
        self.assertEqual(thumbs_up_count(discussion), 3)
        self.assertEqual(thumbs_up_count(None), 0)

    def test_dashboard_data_includes_repository_totals_and_ranks(self):
        data = dashboard_data(
            {"alpha": "First skill", "beta": "Second skill"},
            {
                "beta": {
                    "url": "https://github.com/example/repo/discussions/2",
                    "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 2}}],
                }
            },
            "Skill Votes",
            "example/repo",
        )

        self.assertEqual(data["repository"], "example/repo")
        self.assertEqual(data["total_skills"], 2)
        self.assertEqual(data["total_votes"], 2)
        self.assertEqual(data["skills"][0]["skill"], "beta")
        self.assertEqual(data["skills"][0]["rank"], 1)

    def test_read_skill_metadata_discovers_root_skills(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "alpha"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: alpha\ndescription: Test\n---\n", encoding="utf-8")
            nested = root / "nested" / "ignored"
            nested.mkdir(parents=True)
            (nested / "SKILL.md").write_text("---\nname: ignored\ndescription: Nope\n---\n", encoding="utf-8")

            self.assertEqual(read_skill_metadata(root), {"alpha": "Test"})


if __name__ == "__main__":
    unittest.main()
