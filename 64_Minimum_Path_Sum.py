# Accepted

'''
Given a m x n grid filled with non-negative numbers, 
find a path from top left to bottom right, 
which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.

m == grid.length
n == grid[i].length
1 <= m, n <= 200
0 <= grid[i][j] <= 200
'''

class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        if m == 1 and n == 1:
            return grid[0][0]   
        M = [[0] * n for _ in range(m)]
        M[0][0] = grid[0][0]

        for x in range(1, n):
                M[0][x] = M[0][x-1] + grid[0][x]
        for y in range(1, m):
            M[y][0] = M[y-1][0] + grid[y][0]

        for i in range(1, m):
            for j in range(1, n):
                M[i][j] = min(M[i-1][j], M[i][j-1]) + grid[i][j]
        return M[m-1][n-1]