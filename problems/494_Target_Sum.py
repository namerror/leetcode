# Accepted

'''
You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers.

For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1 and concatenate them to build the expression "+2-1".
Return the number of different expressions that you can build, which evaluates to target.
'''

from collections import defaultdict

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        M = []
        for _ in range(len(nums)):
            M.append(defaultdict(int))
        M[0][nums[0]] += 1
        M[0][-nums[0]] += 1
        for i in range(1, len(nums)):
            for k, v in M[i-1].items():
                M[i][k+nums[i]] += v
                M[i][k-nums[i]] += v

        return M[-1][target]