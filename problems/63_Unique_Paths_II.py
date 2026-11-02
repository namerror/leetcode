# Accepted

'''
You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The testcases are generated so that the answer will be less than or equal to $2 * 10^9$.


'''

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        M = [[1] * n for _ in range(m)]

        M[0][0] = 0 if obstacleGrid[0][0] == 1 else 1
        for x in range(1, m):
            if obstacleGrid[x][0] == 1:
                M[x][0] = 0
            else:
                M[x][0] = M[x-1][0]
        
        for y in range(1, n):
            if obstacleGrid[0][y] == 1:
                M[0][y] = 0
            else:
                M[0][y] = M[0][y-1]

        for i in range(1, m):
            for j in range(1, n):
                if obstacleGrid[i][j] == 1: # obstacle
                    M[i][j] = 0
                else:
                    M[i][j] = M[i-1][j] + M[i][j-1]
        
        return M[m-1][n-1]