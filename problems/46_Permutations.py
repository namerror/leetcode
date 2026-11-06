# Accepted
"""
46. Permutations
Difficulty: Medium
https://leetcode.com/problems/permutations/

Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.

Example 1:

Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Example 2:

Input: nums = [0,1]
Output: [[0,1],[1,0]]

Example 3:

Input: nums = [1]
Output: [[1]]

Constraints:

- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.
"""

class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        out = []
        # choose one from each
        if len(nums) == 1:
            return [[nums[0]]]
        for n in nums:
            new = nums.copy()
            new.remove(n)
            result = self.permute(nums=new)
            for r in result:
                out.append([n] + r)
        return out