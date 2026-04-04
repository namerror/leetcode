#!/usr/bin/env python3
"""
Update only the '## Index' section in README.md.

Rules:
- Only rewrite the '## Index' section slice (everything between '## Index' and the next '## ' header or EOF).
- Sort index bullet lines by ascending problem number.
- Update the 'Total count:' line to match the number of indexed bullet lines.
- Do not modify any other README sections or any other text outside that slice.
"""

from __future__ import annotations

import re
from pathlib import Path


README_PATH = Path("README.md")

# Matches the section header line itself.
INDEX_HEADER_RE = re.compile(r"(?m)^## Index[^\r\n]*\r?\n")
# Matches the next H2 header (used to find the end of the Index section).
NEXT_H2_RE = re.compile(r"(?m)^##\s+")

# A bullet line like: - [70. Climbing Stairs](70_Climbing_Stairs.py)
BULLET_RE = re.compile(r"^(\s*)-\s+\[(\d+)\.", re.ASCII)
_BULLET_START_RE = re.compile(r"-\s+\[\d+\.", re.ASCII)
TOTAL_COUNT_RE = re.compile(r"^(\s*)Total count:\s*.*$", re.ASCII)


def _detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _find_index_section_bounds(readme_text: str) -> tuple[int, int]:
    m = INDEX_HEADER_RE.search(readme_text)
    if not m:
        raise RuntimeError("Couldn't find a '## Index' section header in README.md")

    start = m.start()
    after_header_pos = m.end()

    m2 = NEXT_H2_RE.search(readme_text, pos=after_header_pos)
    end = m2.start() if m2 else len(readme_text)
    return start, end


def _update_index_section(section_text: str, newline: str) -> str:
    # Keep line endings, and only reshuffle bullet lines + rewrite the Total count line.
    raw_lines = section_text.splitlines(keepends=True)

    # Normalize any accidental bullet concatenation (e.g. "...py)- [1137....py)").
    # We only split when we see multiple bullet starts on the same physical line.
    lines: list[str] = []
    for raw in raw_lines:
        line_ending = "\r\n" if raw.endswith("\r\n") else ("\n" if raw.endswith("\n") else "")
        base = raw[:-len(line_ending)] if line_ending else raw
        starts = [m.start() for m in _BULLET_START_RE.finditer(base)]
        if len(starts) <= 1:
            lines.append(raw)
            continue

        for j, s in enumerate(starts):
            e = starts[j + 1] if j + 1 < len(starts) else len(base)
            chunk = base[s:e]
            # Give each extracted bullet its own line.
            lines.append(f"{chunk}{newline if j + 1 < len(starts) else line_ending or newline}")

    bullet_entries: list[tuple[int, str]] = []
    bullet_line_idxs: list[int] = []
    total_count_idx: int | None = None

    for i, line in enumerate(lines):
        if total_count_idx is None:
            if TOTAL_COUNT_RE.match(line.rstrip("\r\n")):
                total_count_idx = i

        m = BULLET_RE.match(line.rstrip("\r\n"))
        if not m:
            continue
        bullet_line_idxs.append(i)
        bullet_entries.append((int(m.group(2)), line))

    # Sort bullets numerically; keep the line text exactly as-is, just re-ordered.
    bullet_entries.sort(key=lambda t: t[0])
    sorted_bullet_lines: list[str] = []
    for _, line in bullet_entries:
        # Ensure each bullet occupies its own line even if the original file
        # was missing a terminal newline on a bullet line.
        if line.endswith("\n"):
            sorted_bullet_lines.append(line)
        else:
            sorted_bullet_lines.append(f"{line}{newline}")
    total_count = len(sorted_bullet_lines)

    # Update or insert "Total count:".
    inserted_at: int | None = None
    if total_count_idx is not None:
        old = lines[total_count_idx]
        line_ending = "\r\n" if old.endswith("\r\n") else ("\n" if old.endswith("\n") else "")
        indent_m = TOTAL_COUNT_RE.match(old.rstrip("\r\n"))
        indent = indent_m.group(1) if indent_m else ""
        lines[total_count_idx] = f"{indent}Total count: {total_count}{line_ending}"
    else:
        # Insert immediately after the header line.
        # We assume the first line in the section is the "## Index" header.
        insert_at = 1 if lines else 0
        inserted_at = insert_at
        lines.insert(insert_at, f"Total count: {total_count}{newline}")

    # Replace bullets in-place: remove all bullet lines and insert a single sorted block
    # at the position of the first bullet line (if any).
    if bullet_line_idxs:
        # If we inserted a line above the bullets, adjust indices accordingly.
        if inserted_at is not None:
            bullet_line_idxs = [idx + 1 if idx >= inserted_at else idx for idx in bullet_line_idxs]

        first = bullet_line_idxs[0]
        bullet_set = set(bullet_line_idxs)
        keep: list[str] = []
        for i, line in enumerate(lines):
            if i in bullet_set:
                continue
            keep.append(line)
        lines = keep

        # The indices changed after removals; re-find insertion point by counting how many
        # original lines (excluding removed bullets) were before `first`.
        removed_before_first = sum(1 for idx in bullet_line_idxs if idx < first)
        insert_pos = first - removed_before_first
        lines[insert_pos:insert_pos] = sorted_bullet_lines

    return "".join(lines)


def main() -> int:
    # Use newline="" so we preserve existing CRLF/LF in the untouched slices.
    with README_PATH.open("r", encoding="utf-8", newline="") as f:
        readme_text = f.read()
    newline = _detect_newline(readme_text)

    start, end = _find_index_section_bounds(readme_text)
    old_section = readme_text[start:end]
    new_section = _update_index_section(old_section, newline=newline)

    if new_section == old_section:
        return 0

    with README_PATH.open("w", encoding="utf-8", newline="") as f:
        f.write(readme_text[:start] + new_section + readme_text[end:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
