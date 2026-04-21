#!/usr/bin/env python3
"""
Refresh the README's generated LeetCode dashboard and index.
"""

from __future__ import annotations

from pathlib import Path
import re

from leetcode_progress import ProgressResult, sync_progress_assets_and_block


README_PATH = Path("README.md")
DASHBOARD_START = "<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_START -->"
DASHBOARD_END = "<!-- AUTO-GENERATED:LEETCODE_DASHBOARD_END -->"
INDEX_HEADER_RE = re.compile(r"(?m)^## Index[^\r\n]*\r?\n")
NEXT_H2_RE = re.compile(r"(?m)^##\s+")


def _detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _find_index_section_bounds(readme_text: str) -> tuple[int, int]:
    match = INDEX_HEADER_RE.search(readme_text)
    if not match:
        raise RuntimeError("Couldn't find a '## Index' section header in README.md")

    start = match.start()
    next_match = NEXT_H2_RE.search(readme_text, pos=match.end())
    end = next_match.start() if next_match else len(readme_text)
    return start, end


def _render_index_section(progress: ProgressResult, newline: str) -> str:
    lines = ["## Index", f"Total count: {len(progress.entries)}"]
    for entry in progress.entries:
        bullet = f"- [{entry.question_frontend_id}. {entry.display_title}]({entry.file_name})"
        if entry.problem_url:
            bullet += f" ([LeetCode]({entry.problem_url}))"
        lines.append(bullet)
    return newline.join(lines) + newline


def _replace_index_section(readme_text: str, index_section: str) -> str:
    start, end = _find_index_section_bounds(readme_text)
    return readme_text[:start] + index_section + readme_text[end:]


def _upsert_dashboard_block(readme_text: str, dashboard_markdown: str, newline: str) -> str:
    block = dashboard_markdown.rstrip("\r\n")
    start_idx = readme_text.find(DASHBOARD_START)
    end_idx = readme_text.find(DASHBOARD_END)

    if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
        end_idx += len(DASHBOARD_END)
        prefix = readme_text[:start_idx].rstrip("\r\n")
        suffix = readme_text[end_idx:].lstrip("\r\n")
        return prefix + newline * 2 + block + newline * 2 + suffix

    index_start, _ = _find_index_section_bounds(readme_text)
    prefix = readme_text[:index_start].rstrip("\r\n")
    suffix = readme_text[index_start:].lstrip("\r\n")
    return prefix + newline * 2 + block + newline * 2 + suffix


def sync_readme(repo_root: Path = Path("."), readme_path: Path = README_PATH) -> bool:
    with readme_path.open("r", encoding="utf-8", newline="") as readme_file:
        readme_text = readme_file.read()

    newline = _detect_newline(readme_text)
    progress = sync_progress_assets_and_block(repo_root, readme_text)
    with_dashboard = _upsert_dashboard_block(readme_text, progress.dashboard_markdown, newline)
    new_index_section = _render_index_section(progress, newline)
    updated_readme = _replace_index_section(with_dashboard, new_index_section)

    if updated_readme == readme_text:
        return False

    with readme_path.open("w", encoding="utf-8", newline="") as readme_file:
        readme_file.write(updated_readme)
    return True


def main() -> int:
    sync_readme()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
