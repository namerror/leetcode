# Accepted, I haven't done DP for a while so got stuck for a bit
'''
Given an integer array nums, find the subarray with the largest sum, and return its sum.
'''

from typing import nums

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        M = [0] * len(nums) # stores the largest sum sub array ending at i
        M[0] = nums[0]
        mx = nums[0]
        for i in range(1, len(nums)):
            M[i] = max(M[i-1]+nums[i], nums[i])
            mx = max(mx, M[i])

        return mx
            
