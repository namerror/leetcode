# Accepted
'''
iven an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.
'''

from typing import List

class Solution:

    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        res.append([])

        for n in nums:
            temp = res.copy()
            for r in temp:
                res.append(r + [n])

        return res
