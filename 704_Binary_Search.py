# Accepted

'''
Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.
'''

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        i = 0
        j = len(nums)-1

        while i <= j:
            mid = (i+j) // 2
            if target == nums[mid]:
                return mid
            elif target > nums[mid]:
                i = mid+1
            else:
                j = mid-1

        return -1

sol = Solution()

sol.search([-1,0,5], 2)