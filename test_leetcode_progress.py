from __future__ import annotations

import tempfile
from pathlib import Path
import unittest
from unittest import mock

import Markdown_formatter
from leetcode_progress import (
    LeetCodeMetadataClient,
    ProblemEntry,
    ProblemMetadata,
    ProgressResult,
    TopicTag,
    count_difficulties,
    count_topics,
    discover_solution_entries,
    render_difficulty_pie_svg,
    render_topic_bar_svg,
    resolve_problem_entries,
    save_cache,
    sync_progress_assets_and_block,
)


class FakeClient:
    def __init__(self, responses: dict[str, object]) -> None:
        self.responses = responses

    def search_problems(self, search_keywords: str):
        response = self.responses.get(search_keywords, [])
        if isinstance(response, Exception):
            raise response
        return response


def make_metadata(
    problem_id: int,
    title: str,
    slug: str,
    difficulty: str,
    topics: list[tuple[str, str]],
) -> ProblemMetadata:
    return ProblemMetadata(
        question_frontend_id=problem_id,
        title=title,
        title_slug=slug,
        difficulty=difficulty,
        topic_tags=tuple(TopicTag(name=name, slug=topic_slug) for name, topic_slug in topics),
    )


class DiscoveryTests(unittest.TestCase):
    def test_discover_solution_entries_sorts_numeric_and_prefers_readme_titles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            (repo_root / "70_Climbing_Stairs.py").write_text("# ok\n", encoding="utf-8")
            (repo_root / "2_Add_Two_Numbers.py").write_text("# ok\n", encoding="utf-8")
            (repo_root / "notes.py").write_text("# ignore\n", encoding="utf-8")
            readme_text = "\n".join(
                [
                    "## Index",
                    "Total count: 2",
                    "- [70. Climbing Stairs](70_Climbing_Stairs.py)",
                    "- [2. Add Two Numbers](2_Add_Two_Numbers.py)",
                ]
            )

            entries = discover_solution_entries(repo_root, readme_text)

            self.assertEqual([entry.question_frontend_id for entry in entries], [2, 70])
            self.assertEqual(entries[0].fallback_title, "Add Two Numbers")
            self.assertEqual(entries[1].fallback_title, "Climbing Stairs")


class ResolutionTests(unittest.TestCase):
    def test_resolve_problem_entries_uses_exact_id_match(self) -> None:
        entry = ProblemEntry(509, "509_Fibonacci_Number.py", "Fibonacci Number")
        expected = make_metadata(
            509,
            "Fibonacci Number",
            "fibonacci-number",
            "Easy",
            [("Math", "math"), ("Dynamic Programming", "dynamic-programming")],
        )
        client = FakeClient({"509": [expected]})

        resolved = resolve_problem_entries([entry], cache={}, client=client)

        self.assertEqual(resolved[0].metadata, expected)
        self.assertEqual(resolved[0].display_title, "Fibonacci Number")
        self.assertEqual(resolved[0].problem_url, "https://leetcode.com/problems/fibonacci-number/")

    def test_resolve_problem_entries_falls_back_to_exact_title_and_unresolved(self) -> None:
        exact_title_match = make_metadata(
            1137,
            "N-th Tribonacci Number",
            "n-th-tribonacci-number",
            "Easy",
            [("Dynamic Programming", "dynamic-programming"), ("Math", "math")],
        )
        resolved_title_entry = ProblemEntry(1137, "1137_Nth_Tribonacci_Number.py", "N-th Tribonacci Number")
        unresolved_entry = ProblemEntry(9999, "9999_Missing_Problem.py", "Missing Problem")
        client = FakeClient(
            {
                "1137": [],
                "N-th Tribonacci Number": [exact_title_match],
                "9999": [],
                "Missing Problem": [],
            }
        )

        resolved = resolve_problem_entries(
            [resolved_title_entry, unresolved_entry],
            cache={},
            client=client,
        )

        self.assertEqual(resolved[0].metadata, exact_title_match)
        self.assertIsNone(resolved[1].metadata)
        self.assertEqual(resolved[1].display_title, "Missing Problem")

    def test_sync_progress_uses_cache_when_live_fetch_fails(self) -> None:
        cached = make_metadata(
            746,
            "Min Cost Climbing Stairs",
            "min-cost-climbing-stairs",
            "Easy",
            [("Array", "array"), ("Dynamic Programming", "dynamic-programming")],
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            (repo_root / "README.md").write_text(
                "## Index\nTotal count: 1\n- [746. Min Cost Climbing Stairs](746_Min_Cost_Climbing_Stairs.py)\n",
                encoding="utf-8",
            )
            (repo_root / "746_Min_Cost_Climbing_Stairs.py").write_text("# ok\n", encoding="utf-8")
            cache_dir = repo_root / "generated/leetcode"
            cache_dir.mkdir(parents=True, exist_ok=True)
            save_cache(cache_dir / "metadata_cache.json", {746: cached})

            progress = sync_progress_assets_and_block(
                repo_root,
                (repo_root / "README.md").read_text(encoding="utf-8"),
                client=FakeClient({"746": RuntimeError("offline")}),
            )

            self.assertEqual(progress.entries[0].metadata, cached)
            self.assertIn("Solved 1 problems. Easy: 1, Medium: 0, Hard: 0.", progress.dashboard_markdown)
            self.assertNotIn("Unresolved metadata", progress.dashboard_markdown)
            self.assertTrue((repo_root / progress.difficulty_chart_path).exists())
            self.assertTrue((repo_root / progress.topic_chart_path).exists())


class RenderingTests(unittest.TestCase):
    def test_svg_renderers_include_expected_content(self) -> None:
        difficulty_svg = render_difficulty_pie_svg({"Easy": 2, "Medium": 1, "Hard": 0})
        topic_svg = render_topic_bar_svg(
            [
                (TopicTag("Dynamic Programming", "dynamic-programming"), 3),
                (TopicTag("Math", "math"), 2),
            ]
        )

        self.assertIn("Solved by difficulty", difficulty_svg)
        self.assertIn("Easy: 2", difficulty_svg)
        self.assertIn("Dynamic Programming", topic_svg)
        self.assertIn(">3<", topic_svg)

    def test_count_helpers_sort_topics_and_difficulties(self) -> None:
        fibonacci = make_metadata(
            509,
            "Fibonacci Number",
            "fibonacci-number",
            "Easy",
            [("Math", "math"), ("Dynamic Programming", "dynamic-programming")],
        )
        robber = make_metadata(
            198,
            "House Robber",
            "house-robber",
            "Medium",
            [("Array", "array"), ("Dynamic Programming", "dynamic-programming")],
        )
        entries = [
            ProblemEntry(509, "509_Fibonacci_Number.py", "Fibonacci Number", fibonacci, "resolved"),
            ProblemEntry(198, "198_House_Robber.py", "House Robber", robber, "resolved"),
        ]

        self.assertEqual(count_difficulties(entries), {"Easy": 1, "Medium": 1, "Hard": 0})
        self.assertEqual(
            [(topic.name, count) for topic, count in count_topics(entries)],
            [("Dynamic Programming", 2), ("Array", 1), ("Math", 1)],
        )


class FormatterTests(unittest.TestCase):
    def test_upsert_dashboard_block_places_block_before_index(self) -> None:
        readme = "# Title\n\nIntro text.\n\n## Index\nTotal count: 0\n"
        dashboard = (
            "<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_START -->\n"
            "## Progress\n"
            "Solved 0 problems.\n"
            "<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_END -->\n"
        )

        updated = Markdown_formatter._upsert_dashboard_block(readme, dashboard, "\n")

        self.assertLess(updated.index("## Progress"), updated.index("## Index"))
        self.assertEqual(updated.count("AUTO-GENERATED:LEETCODE_DASHBOARD_START"), 1)

    def test_render_index_section_includes_canonical_links(self) -> None:
        progress = ProgressResult(
            entries=[
                ProblemEntry(
                    62,
                    "62_Unique_Paths.py",
                    "Unique Paths",
                    make_metadata(62, "Unique Paths", "unique-paths", "Medium", [("Math", "math")]),
                    "resolved",
                ),
                ProblemEntry(9999, "9999_Unresolved.py", "Unresolved", None, None),
            ],
            dashboard_markdown="dashboard\n",
            difficulty_chart_path="generated/leetcode/difficulty_breakdown.svg",
            topic_chart_path="generated/leetcode/topic_coverage.svg",
            cache_path="generated/leetcode/metadata_cache.json",
        )

        section = Markdown_formatter._render_index_section(progress, "\n")

        self.assertIn(
            "- [62. Unique Paths](62_Unique_Paths.py) ([LeetCode](https://leetcode.com/problems/unique-paths/))",
            section,
        )
        self.assertIn("- [9999. Unresolved](9999_Unresolved.py)", section)

    def test_sync_readme_is_idempotent(self) -> None:
        fake_progress = ProgressResult(
            entries=[
                ProblemEntry(
                    70,
                    "70_Climbing_Stairs.py",
                    "Climbing Stairs",
                    make_metadata(70, "Climbing Stairs", "climbing-stairs", "Easy", [("Math", "math")]),
                    "resolved",
                )
            ],
            dashboard_markdown=(
                "<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_START -->\n"
                "## Progress\n"
                "Solved 1 problems. Easy: 1, Medium: 0, Hard: 0.\n"
                "\n"
                "![Difficulty breakdown](generated/leetcode/difficulty_breakdown.svg)\n"
                "\n"
                "## Topics\n"
                "![Topic coverage](generated/leetcode/topic_coverage.svg)\n"
                "\n"
                "| Topic | Solved |\n"
                "| --- | ---: |\n"
                "| [Math](https://leetcode.com/tag/math/) | 1 |\n"
                "<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_END -->\n"
            ),
            difficulty_chart_path="generated/leetcode/difficulty_breakdown.svg",
            topic_chart_path="generated/leetcode/topic_coverage.svg",
            cache_path="generated/leetcode/metadata_cache.json",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            readme_path = repo_root / "README.md"
            readme_path.write_text(
                "# Title\n\nIntro text.\n\n## Index\nTotal count: 0\n",
                encoding="utf-8",
            )
            with mock.patch.object(
                Markdown_formatter,
                "sync_progress_assets_and_block",
                return_value=fake_progress,
            ):
                first_changed = Markdown_formatter.sync_readme(repo_root=repo_root, readme_path=readme_path)
                second_changed = Markdown_formatter.sync_readme(repo_root=repo_root, readme_path=readme_path)

            content = readme_path.read_text(encoding="utf-8")
            self.assertTrue(first_changed)
            self.assertFalse(second_changed)
            self.assertEqual(content.count("AUTO-GENERATED:LEETCODE_DASHBOARD_START"), 1)
            self.assertEqual(content.count("## Index"), 1)


class ClientTests(unittest.TestCase):
    def test_client_parses_graphql_payload(self) -> None:
        payload = {
            "data": {
                "problemsetQuestionList": {
                    "data": [
                        {
                            "questionFrontendId": "509",
                            "title": "Fibonacci Number",
                            "titleSlug": "fibonacci-number",
                            "difficulty": "Easy",
                            "topicTags": [{"name": "Math", "slug": "math"}],
                        }
                    ]
                }
            }
        }
        client = LeetCodeMetadataClient()
        with mock.patch.object(client, "_graphql_request", return_value=payload):
            results = client.search_problems("509")

        self.assertEqual(results[0].question_frontend_id, 509)
        self.assertEqual(results[0].topic_tags[0].slug, "math")


if __name__ == "__main__":
    unittest.main()
