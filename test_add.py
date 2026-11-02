from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import add


def question(number=36, snippet=None):
    return {
        "questionFrontendId": str(number),
        "title": "Valid Sudoku",
        "titleSlug": "valid-sudoku",
        "difficulty": "Medium",
        "content": '<p>Check the board.</p><ol><li>First rule</li></ol>'
                   '<pre>Input: [1, 2]\n  Output: true</pre>'
                   '<p>Constraints: n &lt;= 10<sup>5</sup></p>'
                   '<img src="/diagram.png" alt="Board">',
        "codeSnippets": [{"langSlug": "python3", "code": snippet or
                          'class Solution:\n    def isValidSudoku(self, board: List[List[str]]) -> bool:\n        '}],
    }


class TemplateTests(unittest.TestCase):
    def test_render_preserves_description_and_exact_starter(self):
        q = question()
        filename, content = add.render_template(q)
        self.assertEqual(filename, "36_Valid_Sudoku.py")
        self.assertTrue(content.endswith(q["codeSnippets"][0]["code"]))
        for expected in ("Medium", "1. First rule", "Input: [1, 2]\n  Output: true",
                         "Constraints: n <= 10^(5)", "https://leetcode.com/diagram.png"):
            self.assertIn(expected, content)

    def test_multi_method_snippet_and_safe_docstring(self):
        snippet = '# Definition for a Node.\nclass Thing:\n    def __init__(self):\n        \n    def get(self):\n        '
        q = question(snippet=snippet)
        q["title"] = 'Thing: A/B?'
        q["content"] = '<p>Use """ and \\n literally.</p>'
        filename, content = add.render_template(q)
        self.assertEqual(filename, "36_Thing_AB.py")
        # Evaluate just the docstring to check that its escaping preserves text.
        header = content[:content.index('\n\n# Definition')]
        self.assertIn('Use """ and \\n literally.', eval(header))
        self.assertTrue(content.endswith(snippet))

    def test_missing_content_or_snippet(self):
        for field, value in (("content", None), ("codeSnippets", [])):
            q = question()
            q[field] = value
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                add.render_template(q)

    def test_create_and_skip_existing_even_empty_or_different_title(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            root = Path(directory)
            client = Mock()
            client.fetch_question.return_value = question()
            path = add.add_problem(36, root, client)
            original = path.read_bytes()
            client.reset_mock()
            self.assertIsNone(add.add_problem(36, root, client))
            self.assertEqual(path.read_bytes(), original)
            client.fetch_question.assert_not_called()
            path.unlink()
            (root / "36_Old_Title.py").touch()
            self.assertIsNone(add.add_problem(36, root, client))
            client.fetch_question.assert_not_called()

    def test_collision_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            root = Path(directory)
            def fetch(number):
                (root / "36_Valid_Sudoku.py").write_text("existing")
                return question()
            client = Mock()
            client.fetch_question.side_effect = fetch
            self.assertIsNone(add.add_problem(36, root, client))
            self.assertEqual((root / "36_Valid_Sudoku.py").read_text(), "existing")

    def test_fetch_error_creates_no_file(self):
        with tempfile.TemporaryDirectory() as directory:
            client = Mock()
            client.fetch_question.side_effect = RuntimeError("network failure")
            with self.assertRaises(RuntimeError):
                add.add_problem(36, Path(directory), client)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_cli_arguments_and_failure(self):
        for args in ([], ["0"], ["-1"], ["abc"], ["1", "2"]):
            with self.subTest(args=args), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                add.main(args)
        with patch.object(add, "add_problem", side_effect=RuntimeError("unavailable")), redirect_stderr(io.StringIO()) as err:
            self.assertEqual(add.main(["36"]), 1)
            self.assertIn("unavailable", err.getvalue())


class ClientTests(unittest.TestCase):
    def make_client(self, rows, detail):
        responses = []
        for payload in ({"data": {"problemsetQuestionList": {"data": rows}}}, detail):
            response = Mock()
            response.__enter__ = Mock(return_value=response)
            response.__exit__ = Mock(return_value=False)
            response.read.return_value = json.dumps(payload).encode()
            responses.append(response)
        opener = Mock(side_effect=responses)
        return add.TemplateClient(urlopen_func=opener), opener

    def test_exact_id_match_and_detail_query(self):
        rows = [question(136), question(36)]
        client, opener = self.make_client(rows, {"data": {"question": question()}})
        self.assertEqual(client.fetch_question(36), question())
        body = json.loads(opener.call_args.args[0].data)
        self.assertEqual(body["variables"], {"titleSlug": "valid-sudoku"})
        self.assertIn("codeSnippets", body["query"])

    def test_not_found_mismatched_detail_and_graphql_error(self):
        for rows, detail in (([question(136)], {}),
                             ([question()], {"data": {"question": question(136)}}),
                             ([question()], {"errors": [{"message": "blocked"}]})):
            client, _ = self.make_client(rows, detail)
            with self.subTest(detail=detail), self.assertRaises(RuntimeError):
                client.fetch_question(36)


if __name__ == "__main__":
    unittest.main()
