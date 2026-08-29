# Accepted
'''
You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.
'''

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        i = 0
        j = 0

        while i <= j:
            j = max(i + nums[i], j)
            if j >= len(nums) - 1:
                return True
            i += 1

        return False
