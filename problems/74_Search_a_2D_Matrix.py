# Accepted
'''
You are given an m x n integer matrix matrix with the following two properties:

Each row is sorted in non-decreasing order.
The first integer of each row is greater than the last integer of the previous row.
Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.
'''

from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        i = 0
        j = len(matrix) * len(matrix[0]) - 1
        def get_element(index):
            row = index // len(matrix[0])
            col = index - row * len(matrix[0])
            return matrix[row][col]
            
        while i <= j:
            mid = (i + j) // 2
            x = get_element(mid)
            if x == target:
                return True
            elif x > target:
                j = mid-1
            else:
                i = mid+1

        return False
