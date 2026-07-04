# Accepted

'''
Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.
'''

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        d = {}
        for i in range(len(nums)):
            if d.get(nums[i]) is not None:
                return True
            d[nums[i]] = 1

        return False