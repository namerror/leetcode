#!/usr/bin/env python3
"""
Build LeetCode progress assets and README dashboard content.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from html import escape
import json
import math
from pathlib import Path
import re
from typing import Callable
from urllib import error, request


GRAPHQL_URL = "https://leetcode.com/graphql"
SOLUTION_FILE_RE = re.compile(r"^(?P<id>\d+)_(?P<name>.+)\.py$", re.ASCII)
README_BULLET_RE = re.compile(r"^\s*-\s+\[(\d+)\.\s+([^\]]+)\]", re.MULTILINE)
DASHBOARD_DIR = Path("generated/leetcode")
CACHE_FILENAME = "metadata_cache.json"
DIFFICULTY_SVG_FILENAME = "difficulty_breakdown.svg"
TOPIC_SVG_FILENAME = "topic_coverage.svg"
QUESTION_LIST_CATEGORY = "all-code-essentials"
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard")
DIFFICULTY_COLORS = {
    "Easy": "#4caf50",
    "Medium": "#ff9800",
    "Hard": "#f44336",
}

QUESTION_SEARCH_QUERY = """
query search($categorySlug: String, $skip: Int, $limit: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    skip: $skip
    limit: $limit
    filters: $filters
  ) {
    totalNum
    data {
      questionFrontendId
      title
      titleSlug
      difficulty
      topicTags {
        name
        slug
      }
    }
  }
}
""".strip()


@dataclass(frozen=True)
class TopicTag:
    name: str
    slug: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "slug": self.slug}


@dataclass(frozen=True)
class ProblemMetadata:
    question_frontend_id: int
    title: str
    title_slug: str
    difficulty: str
    topic_tags: tuple[TopicTag, ...]

    @property
    def problem_url(self) -> str:
        return f"https://leetcode.com/problems/{self.title_slug}/"

    def to_dict(self) -> dict[str, object]:
        return {
            "question_frontend_id": self.question_frontend_id,
            "title": self.title,
            "title_slug": self.title_slug,
            "difficulty": self.difficulty,
            "topic_tags": [topic.to_dict() for topic in self.topic_tags],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ProblemMetadata":
        raw_topics = data.get("topic_tags", [])
        topic_tags = tuple(
            TopicTag(name=str(topic["name"]), slug=str(topic["slug"]))
            for topic in raw_topics
            if isinstance(topic, dict) and "name" in topic and "slug" in topic
        )
        return cls(
            question_frontend_id=int(data["question_frontend_id"]),
            title=str(data["title"]),
            title_slug=str(data["title_slug"]),
            difficulty=str(data["difficulty"]),
            topic_tags=topic_tags,
        )


@dataclass(frozen=True)
class ProblemEntry:
    question_frontend_id: int
    file_name: str
    fallback_title: str
    metadata: ProblemMetadata | None = None
    metadata_source: str | None = None

    @property
    def display_title(self) -> str:
        return self.metadata.title if self.metadata else self.fallback_title

    @property
    def problem_url(self) -> str | None:
        return self.metadata.problem_url if self.metadata else None

    @property
    def is_resolved(self) -> bool:
        return self.metadata is not None


@dataclass(frozen=True)
class ProgressResult:
    entries: list[ProblemEntry]
    dashboard_markdown: str
    difficulty_chart_path: str
    topic_chart_path: str
    cache_path: str


class LeetCodeMetadataClient:
    def __init__(
        self,
        *,
        timeout_seconds: float = 15.0,
        urlopen_func: Callable[..., object] | None = None,
    ) -> None:
        self._timeout_seconds = timeout_seconds
        self._urlopen = urlopen_func or request.urlopen
        self._live_fetch_enabled = True

    def search_problems(self, search_keywords: str) -> list[ProblemMetadata]:
        if not self._live_fetch_enabled:
            return []

        variables = {
            "categorySlug": QUESTION_LIST_CATEGORY,
            "skip": 0,
            "limit": 10,
            "filters": {"searchKeywords": search_keywords},
        }
        try:
            payload = self._graphql_request(QUESTION_SEARCH_QUERY, variables)
        except (OSError, error.URLError, TimeoutError, ValueError) as exc:
            self._live_fetch_enabled = False
            raise RuntimeError(f"LeetCode request failed: {exc}") from exc

        problemset = payload.get("data", {}).get("problemsetQuestionList", {})
        rows = problemset.get("data", [])
        if not isinstance(rows, list):
            return []
        return [self._metadata_from_node(node) for node in rows if isinstance(node, dict)]

    def _graphql_request(self, query: str, variables: dict[str, object]) -> dict[str, object]:
        body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
        http_request = request.Request(
            GRAPHQL_URL,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Referer": "https://leetcode.com/problemset/",
                "User-Agent": "leetcode-progress-script/1.0",
            },
            method="POST",
        )
        with self._urlopen(http_request, timeout=self._timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if payload.get("errors"):
            raise RuntimeError(f"LeetCode GraphQL returned errors: {payload['errors']}")
        return payload

    @staticmethod
    def _metadata_from_node(node: dict[str, object]) -> ProblemMetadata:
        topics = tuple(
            TopicTag(name=str(topic["name"]), slug=str(topic["slug"]))
            for topic in node.get("topicTags", [])
            if isinstance(topic, dict) and "name" in topic and "slug" in topic
        )
        return ProblemMetadata(
            question_frontend_id=int(node["questionFrontendId"]),
            title=str(node["title"]),
            title_slug=str(node["titleSlug"]),
            difficulty=str(node["difficulty"]),
            topic_tags=topics,
        )


def discover_solution_entries(repo_root: Path, readme_text: str = "") -> list[ProblemEntry]:
    readme_titles = parse_readme_titles(readme_text)
    entries: list[ProblemEntry] = []
    for path in sorted(repo_root.iterdir(), key=lambda item: item.name):
        match = SOLUTION_FILE_RE.match(path.name)
        if not match:
            continue
        frontend_id = int(match.group("id"))
        fallback_title = readme_titles.get(frontend_id, _title_from_filename(match.group("name")))
        entries.append(
            ProblemEntry(
                question_frontend_id=frontend_id,
                file_name=path.name,
                fallback_title=fallback_title,
            )
        )
    entries.sort(key=lambda entry: entry.question_frontend_id)
    return entries


def parse_readme_titles(readme_text: str) -> dict[int, str]:
    titles: dict[int, str] = {}
    for match in README_BULLET_RE.finditer(readme_text):
        titles[int(match.group(1))] = match.group(2).strip()
    return titles


def sync_progress_assets_and_block(
    repo_root: Path,
    readme_text: str,
    *,
    client: LeetCodeMetadataClient | None = None,
) -> ProgressResult:
    entries = discover_solution_entries(repo_root, readme_text)
    output_dir = repo_root / DASHBOARD_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_path = output_dir / CACHE_FILENAME
    cache = load_cache(cache_path)
    metadata_client = client or LeetCodeMetadataClient()
    resolved_entries = resolve_problem_entries(
        entries,
        cache=cache,
        client=metadata_client,
    )
    save_cache(cache_path, cache)

    difficulty_counts = count_difficulties(resolved_entries)
    topic_counts = count_topics(resolved_entries)
    difficulty_chart_path = output_dir / DIFFICULTY_SVG_FILENAME
    topic_chart_path = output_dir / TOPIC_SVG_FILENAME
    difficulty_chart_path.write_text(render_difficulty_pie_svg(difficulty_counts), encoding="utf-8")
    topic_chart_path.write_text(render_topic_bar_svg(topic_counts[:10]), encoding="utf-8")
    dashboard_markdown = render_dashboard_markdown(
        resolved_entries,
        difficulty_counts=difficulty_counts,
        topic_counts=topic_counts,
        difficulty_chart_path=difficulty_chart_path.relative_to(repo_root).as_posix(),
        topic_chart_path=topic_chart_path.relative_to(repo_root).as_posix(),
    )
    return ProgressResult(
        entries=resolved_entries,
        dashboard_markdown=dashboard_markdown,
        difficulty_chart_path=difficulty_chart_path.relative_to(repo_root).as_posix(),
        topic_chart_path=topic_chart_path.relative_to(repo_root).as_posix(),
        cache_path=cache_path.relative_to(repo_root).as_posix(),
    )


def load_cache(cache_path: Path) -> dict[int, ProblemMetadata]:
    if not cache_path.exists():
        return {}
    raw_data = json.loads(cache_path.read_text(encoding="utf-8"))
    problems = raw_data.get("problems", {})
    cache: dict[int, ProblemMetadata] = {}
    if not isinstance(problems, dict):
        return cache
    for key, value in problems.items():
        if not isinstance(value, dict):
            continue
        try:
            cache[int(key)] = ProblemMetadata.from_dict(value)
        except (KeyError, TypeError, ValueError):
            continue
    return cache


def save_cache(cache_path: Path, cache: dict[int, ProblemMetadata]) -> None:
    serialized = {
        "problems": {
            str(problem_id): metadata.to_dict()
            for problem_id, metadata in sorted(cache.items())
        }
    }
    cache_path.write_text(json.dumps(serialized, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_problem_entries(
    entries: list[ProblemEntry],
    *,
    cache: dict[int, ProblemMetadata],
    client: LeetCodeMetadataClient,
) -> list[ProblemEntry]:
    resolved_entries: list[ProblemEntry] = []
    cache_title_map = {metadata.title.casefold(): metadata for metadata in cache.values()}

    for entry in entries:
        metadata = _resolve_entry_metadata(entry, cache=cache, cache_title_map=cache_title_map, client=client)
        if metadata is None:
            resolved_entries.append(entry)
            continue

        cache[metadata.question_frontend_id] = metadata
        cache_title_map[metadata.title.casefold()] = metadata
        resolved_entries.append(
            replace(
                entry,
                metadata=metadata,
                metadata_source="resolved",
            )
        )

    return resolved_entries


def _resolve_entry_metadata(
    entry: ProblemEntry,
    *,
    cache: dict[int, ProblemMetadata],
    cache_title_map: dict[str, ProblemMetadata],
    client: LeetCodeMetadataClient,
) -> ProblemMetadata | None:
    try:
        search_results = client.search_problems(str(entry.question_frontend_id))
    except RuntimeError:
        search_results = []

    for metadata in search_results:
        if metadata.question_frontend_id == entry.question_frontend_id:
            return metadata

    cached = cache.get(entry.question_frontend_id)
    if cached:
        return cached

    exact_titles = []
    for candidate in (entry.fallback_title, _title_from_filename(Path(entry.file_name).stem.split("_", 1)[1])):
        candidate = candidate.strip()
        if candidate and candidate not in exact_titles:
            exact_titles.append(candidate)

    for title in exact_titles:
        cached_by_title = cache_title_map.get(title.casefold())
        if cached_by_title:
            return cached_by_title

    for title in exact_titles:
        try:
            search_results = client.search_problems(title)
        except RuntimeError:
            break
        for metadata in search_results:
            if metadata.title.casefold() == title.casefold():
                return metadata

    return None


def count_difficulties(entries: list[ProblemEntry]) -> dict[str, int]:
    counts = {difficulty: 0 for difficulty in DIFFICULTY_ORDER}
    for entry in entries:
        if not entry.metadata:
            continue
        if entry.metadata.difficulty in counts:
            counts[entry.metadata.difficulty] += 1
    return counts


def count_topics(entries: list[ProblemEntry]) -> list[tuple[TopicTag, int]]:
    counter: Counter[tuple[str, str]] = Counter()
    for entry in entries:
        if not entry.metadata:
            continue
        for topic in entry.metadata.topic_tags:
            counter[(topic.name, topic.slug)] += 1
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0][0].casefold()))
    return [(TopicTag(name=name, slug=slug), count) for (name, slug), count in ranked]


def render_dashboard_markdown(
    entries: list[ProblemEntry],
    *,
    difficulty_counts: dict[str, int],
    topic_counts: list[tuple[TopicTag, int]],
    difficulty_chart_path: str,
    topic_chart_path: str,
) -> str:
    total = len(entries)
    unresolved_ids = [str(entry.question_frontend_id) for entry in entries if not entry.is_resolved]
    lines = [
        "<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_START -->",
        "## Progress",
        (
            f"Solved {total} problems. "
            f"Easy: {difficulty_counts['Easy']}, "
            f"Medium: {difficulty_counts['Medium']}, "
            f"Hard: {difficulty_counts['Hard']}."
        ),
        "",
        f"![Difficulty breakdown]({difficulty_chart_path})",
        "",
        "## Topics",
        f"![Topic coverage]({topic_chart_path})",
        "",
    ]

    if topic_counts:
        lines.extend(
            [
                "| Topic | Solved |",
                "| --- | ---: |",
            ]
        )
        for topic, count in topic_counts:
            topic_url = f"https://leetcode.com/tag/{topic.slug}/"
            lines.append(f"| [{topic.name}]({topic_url}) | {count} |")
    else:
        lines.append("No topic metadata available yet.")

    if unresolved_ids:
        lines.extend(
            [
                "",
                f"Unresolved metadata for problem ids: {', '.join(unresolved_ids)}.",
            ]
        )

    lines.append("<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_END -->")
    return "\n".join(lines) + "\n"


def render_difficulty_pie_svg(counts: dict[str, int]) -> str:
    width = 420
    height = 280
    cx = 130
    cy = 140
    radius = 90
    total = sum(counts.values())
    if total == 0:
        return _render_empty_svg(width, height, "No resolved difficulty data yet")

    slices: list[str] = []
    start_angle = -math.pi / 2
    for difficulty in DIFFICULTY_ORDER:
        count = counts[difficulty]
        if count <= 0:
            continue
        fraction = count / total
        sweep_angle = fraction * math.tau
        if count == total:
            slices.append(
                f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{DIFFICULTY_COLORS[difficulty]}" />'
            )
        else:
            end_angle = start_angle + sweep_angle
            slices.append(
                (
                    f'<path d="{_describe_wedge(cx, cy, radius, start_angle, end_angle)}" '
                    f'fill="{DIFFICULTY_COLORS[difficulty]}" stroke="#ffffff" stroke-width="2" />'
                )
            )
            start_angle = end_angle

    legend_lines: list[str] = []
    legend_x = 255
    legend_y = 92
    for index, difficulty in enumerate(DIFFICULTY_ORDER):
        y = legend_y + index * 36
        legend_lines.append(
            f'<rect x="{legend_x}" y="{y}" width="18" height="18" '
            f'fill="{DIFFICULTY_COLORS[difficulty]}" rx="4" />'
        )
        legend_lines.append(
            f'<text x="{legend_x + 28}" y="{y + 14}" font-size="14" fill="#1f2933">'
            f'{escape(difficulty)}: {counts[difficulty]}</text>'
        )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="LeetCode difficulty breakdown">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="16" />',
            *slices,
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#ffffff" stroke-width="2" />',
            '<text x="24" y="30" font-size="18" font-weight="700" fill="#1f2933">Solved by difficulty</text>',
            f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="26" font-weight="700" fill="#1f2933">{total}</text>',
            f'<text x="{cx}" y="{cy + 28}" text-anchor="middle" font-size="13" fill="#52606d">resolved</text>',
            *legend_lines,
            "</svg>",
            "",
        ]
    )


def render_topic_bar_svg(topic_counts: list[tuple[TopicTag, int]]) -> str:
    width = 760
    row_height = 34
    top_padding = 60
    left_label_width = 220
    right_padding = 36
    bottom_padding = 30
    chart_width = width - left_label_width - right_padding - 40

    if not topic_counts:
        return _render_empty_svg(width, 180, "No resolved topic data yet")

    height = top_padding + len(topic_counts) * row_height + bottom_padding
    max_count = max(count for _, count in topic_counts)
    bars: list[str] = []
    for index, (topic, count) in enumerate(topic_counts):
        y = top_padding + index * row_height
        bar_width = 0 if max_count == 0 else int((count / max_count) * chart_width)
        bars.append(
            f'<text x="20" y="{y + 18}" font-size="13" fill="#1f2933">{escape(topic.name)}</text>'
        )
        bars.append(
            f'<rect x="{left_label_width}" y="{y + 4}" width="{chart_width}" height="18" fill="#e5e7eb" rx="6" />'
        )
        bars.append(
            f'<rect x="{left_label_width}" y="{y + 4}" width="{bar_width}" height="18" fill="#2563eb" rx="6" />'
        )
        bars.append(
            f'<text x="{left_label_width + bar_width + 8}" y="{y + 18}" font-size="13" fill="#1f2933">{count}</text>'
        )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="LeetCode topic coverage">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="16" />',
            '<text x="20" y="30" font-size="18" font-weight="700" fill="#1f2933">Top topic coverage</text>',
            '<text x="20" y="48" font-size="12" fill="#52606d">Top 10 topics by solved problem count</text>',
            *bars,
            "</svg>",
            "",
        ]
    )


def _render_empty_svg(width: int, height: int, message: str) -> str:
    safe_message = escape(message)
    inner_width = max(width - 32, 0)
    inner_height = max(height - 32, 0)
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{safe_message}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="16" />',
            f'<rect x="16" y="16" width="{inner_width}" height="{inner_height}" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="6 6" rx="12" />',
            f'<text x="{width / 2}" y="{height / 2}" text-anchor="middle" font-size="16" fill="#52606d">{safe_message}</text>',
            "</svg>",
            "",
        ]
    )


def _describe_wedge(cx: int, cy: int, radius: int, start_angle: float, end_angle: float) -> str:
    start_x, start_y = _polar_to_cartesian(cx, cy, radius, start_angle)
    end_x, end_y = _polar_to_cartesian(cx, cy, radius, end_angle)
    large_arc = 1 if end_angle - start_angle > math.pi else 0
    return (
        f"M {cx:.2f} {cy:.2f} "
        f"L {start_x:.2f} {start_y:.2f} "
        f"A {radius} {radius} 0 {large_arc} 1 {end_x:.2f} {end_y:.2f} Z"
    )


def _polar_to_cartesian(cx: int, cy: int, radius: int, angle: float) -> tuple[float, float]:
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def _title_from_filename(raw_name: str) -> str:
    return raw_name.replace("_", " ").strip()
