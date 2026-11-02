# Accepted
"""
36. Valid Sudoku
Difficulty: Medium
https://leetcode.com/problems/valid-sudoku/

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.

Note:

- A Sudoku board (partially filled) could be valid but is not necessarily solvable.
- Only the filled cells need to be validated according to the mentioned rules.

Example 1:

[Image: illustration] https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Sudoku-by-L2G-20050714.svg/250px-Sudoku-by-L2G-20050714.svg.png

Input: board =
[[\"5\",\"3\",\".\",\".\",\"7\",\".\",\".\",\".\",\".\"]
,[\"6\",\".\",\".\",\"1\",\"9\",\"5\",\".\",\".\",\".\"]
,[\".\",\"9\",\"8\",\".\",\".\",\".\",\".\",\"6\",\".\"]
,[\"8\",\".\",\".\",\".\",\"6\",\".\",\".\",\".\",\"3\"]
,[\"4\",\".\",\".\",\"8\",\".\",\"3\",\".\",\".\",\"1\"]
,[\"7\",\".\",\".\",\".\",\"2\",\".\",\".\",\".\",\"6\"]
,[\".\",\"6\",\".\",\".\",\".\",\".\",\"2\",\"8\",\".\"]
,[\".\",\".\",\".\",\"4\",\"1\",\"9\",\".\",\".\",\"5\"]
,[\".\",\".\",\".\",\".\",\"8\",\".\",\".\",\"7\",\"9\"]]
Output: true

Example 2:

Input: board =
[[\"8\",\"3\",\".\",\".\",\"7\",\".\",\".\",\".\",\".\"]
,[\"6\",\".\",\".\",\"1\",\"9\",\"5\",\".\",\".\",\".\"]
,[\".\",\"9\",\"8\",\".\",\".\",\".\",\".\",\"6\",\".\"]
,[\"8\",\".\",\".\",\".\",\"6\",\".\",\".\",\".\",\"3\"]
,[\"4\",\".\",\".\",\"8\",\".\",\"3\",\".\",\".\",\"1\"]
,[\"7\",\".\",\".\",\".\",\"2\",\".\",\".\",\".\",\"6\"]
,[\".\",\"6\",\".\",\".\",\".\",\".\",\"2\",\"8\",\".\"]
,[\".\",\".\",\".\",\"4\",\"1\",\"9\",\".\",\".\",\"5\"]
,[\".\",\".\",\".\",\".\",\"8\",\".\",\".\",\"7\",\"9\"]]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.

Constraints:

- board.length == 9
- board[i].length == 9
- board[i][j] is a digit 1-9 or '.'.
"""

class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        row_sets = [set() for _ in range(9)]
        col_sets = [set() for _ in range(9)]
        grid_sets = [set() for _ in range(9)]

        for i in range(9):
            for j in range(9):
                cur = board[i][j]
                if cur == ".":
                    continue
                grid_i = (i//3 * 3) + (j//3)
                
                if cur in row_sets[i] or cur in col_sets[j] or cur in grid_sets[grid_i]:
                    return False

                row_sets[i].add(cur)
                col_sets[j].add(cur)
                grid_sets[grid_i].add(cur)

        return True