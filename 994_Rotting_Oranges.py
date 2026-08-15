# Accepted, took quite long, edge cases are tricky
'''
You are given an m x n grid where each cell can have one of three values:

0 representing an empty cell,
1 representing a fresh orange, or
2 representing a rotten orange.
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
'''

from typing import List

from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rotten = deque()
        count = 0
        rot_count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != 0:
                    count += 1
                    if grid[i][j] == 2:
                        rotten.append((i, j))
                        rot_count += 1

        if rot_count == count:
            return 0
        if rot_count == 0 and count > 0:
            return -1

        def propagate(i, j, to_add) -> bool:
            nonlocal rot_count
            if i >= len(grid) or j >= len(grid[0]) or i < 0 or j < 0:
                return False
            if grid[i][j] == 1:
                grid[i][j] = 2
                to_add.append((i, j))
                rot_count += 1
                return True
            return False
        
        minutes = 0
        while len(rotten) > 0:
            to_add = []
            for (u, v) in rotten:
                left = propagate(u, v-1, to_add)
                right = propagate(u, v+1, to_add)
                up = propagate(u-1, v, to_add)
                down = propagate(u+1, v, to_add)
            minutes += 1
            rotten = to_add

        minutes -= 1
        if count != rot_count:
            return -1
        else:
            return minutes
                
        
                