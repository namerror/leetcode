#!/usr/bin/env python3
"""Create an official Python 3 LeetCode starter in this repository."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urljoin

from leetcode_progress import LeetCodeMetadataClient, PROBLEMS_DIR


REPO_ROOT = Path(__file__).resolve().parent
QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    difficulty
    content
    codeSnippets { langSlug code }
  }
}
""".strip()


class DescriptionParser(HTMLParser):
    """Render problem HTML without losing preformatted examples or exponents."""

    def __init__(self, source_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source_url = source_url
        self.parts: list[str] = []
        self.lists: list[int | None] = []
        self.pre = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"p", "div", "pre", "ul", "ol", "blockquote"}:
            self.parts.append("\n\n")
        if tag in {"ul", "ol"}:
            self.lists.append(0 if tag == "ol" else None)
        elif tag == "li":
            marker = "- "
            if self.lists and self.lists[-1] is not None:
                self.lists[-1] += 1
                marker = f"{self.lists[-1]}. "
            self.parts.append("\n" + "  " * max(0, len(self.lists) - 1) + marker)
        elif tag == "br":
            self.parts.append("\n")
        elif tag == "pre":
            self.pre = True
        elif tag in {"sup", "sub"}:
            self.parts.append("^(" if tag == "sup" else "_(")
        elif tag == "img" and attributes.get("src"):
            self.parts.append(
                f"\n[Image: {attributes.get('alt') or 'illustration'}] "
                + urljoin(self.source_url, attributes["src"])
                + "\n"
            )

    def handle_endtag(self, tag: str) -> None:
        if tag in {"sup", "sub"}:
            self.parts.append(")")
        if tag in {"p", "div", "pre", "ul", "ol", "blockquote"}:
            self.parts.append("\n\n")
        if tag in {"ul", "ol"} and self.lists:
            self.lists.pop()
        if tag == "pre":
            self.pre = False

    def handle_data(self, data: str) -> None:
        data = data.replace("\xa0", " ")
        self.parts.append(data if self.pre else re.sub(r"\s+", " ", data))

    def render(self, html: str) -> str:
        self.feed(html)
        self.close()
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        return re.sub(r"\n(?:[ \t]*\n){2,}", "\n\n", text).strip()


class TemplateClient(LeetCodeMetadataClient):
    def fetch_question(self, number: int) -> dict:
        matches = self.search_problems(str(number))
        metadata = next((p for p in matches if p.question_frontend_id == number), None)
        if metadata is None:
            raise RuntimeError(f"LeetCode problem {number} was not found.")
        payload = self._graphql_request(QUESTION_QUERY, {"titleSlug": metadata.title_slug})
        question = (payload.get("data") or {}).get("question")
        if not isinstance(question, dict) or str(question.get("questionFrontendId")) != str(number):
            raise RuntimeError("LeetCode returned missing or mismatched question data.")
        return question


def render_template(question: dict) -> tuple[str, str]:
    for field in ("title", "titleSlug", "difficulty", "content"):
        if not isinstance(question.get(field), str) or not question[field].strip():
            raise RuntimeError(f"LeetCode did not provide {field}; the problem may require login or Premium.")
    snippets = question.get("codeSnippets") or []
    snippet = next(
        (s.get("code") for s in snippets if isinstance(s, dict) and s.get("langSlug") == "python3"),
        None,
    )
    if not isinstance(snippet, str) or not snippet.strip():
        raise RuntimeError("LeetCode did not provide a Python 3 starter snippet.")
    title = re.sub(r"[^\w\s-]", "", question["title"])
    title = re.sub(r"\s+", "_", title.strip())
    if not title:
        raise RuntimeError("LeetCode returned an unusable problem title.")
    filename = f"{int(question['questionFrontendId'])}_{title}.py"
    source_url = f"https://leetcode.com/problems/{question['titleSlug']}/"
    description = DescriptionParser(source_url).render(question["content"])
    header = (
        f"{question['questionFrontendId']}. {question['title']}\n"
        f"Difficulty: {question['difficulty']}\n{source_url}\n\n{description}"
    )
    # Escape only the docstring; the official starter remains byte-for-byte intact.
    header = header.replace("\\", "\\\\").replace('"', '\\"')
    return filename, f'"""\n{header}\n"""\n\n' + snippet


def add_problem(number: int, repo_root: Path, client: TemplateClient | None = None) -> Path | None:
    problems_dir = repo_root / PROBLEMS_DIR
    existing = next((p for p in problems_dir.glob(f"{number}_*.py") if p.is_file()), None)
    if existing is not None:
        print(f"Skipped: {existing.name} already exists.")
        return None
    question = (client or TemplateClient()).fetch_question(number)
    filename, content = render_template(question)
    problems_dir.mkdir(parents=True, exist_ok=True)
    destination = problems_dir / filename
    try:
        with destination.open("x", encoding="utf-8", newline="") as output:
            output.write(content)
    except FileExistsError:
        print(f"Skipped: {destination.name} already exists.")
        return None
    except OSError:
        # Remove an incomplete new file if writing failed after exclusive creation.
        if 'output' in locals():
            destination.unlink(missing_ok=True)
        raise
    print(f"Created: {destination}")
    return destination


def positive_number(value: str) -> int:
    if not re.fullmatch(r"[0-9]+", value) or int(value) < 1:
        raise argparse.ArgumentTypeError("provide a positive LeetCode problem number")
    return int(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, prog="add")
    parser.add_argument("number", type=positive_number, help="LeetCode problem number (e.g. 36)")
    args = parser.parse_args(argv)
    try:
        add_problem(args.number, REPO_ROOT)
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(f"add: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
