# Accepted, very subtle, once you see the important property you'd know
# It's also very subtle about the order of your operations
'''
Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:

Input: nums = [1,1,1], k = 2
Output: 2
Example 2:

Input: nums = [1,2,3], k = 3
Output: 2

'''
from collections import defaultdict
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        sum_to_freq = defaultdict(int)
        sums = 0
        count = 0
        sum_to_freq[0] = 1
        for i in range(len(nums)):
            sums += nums[i]
            target = sums - k
            count += sum_to_freq[target]
            sum_to_freq[sums] += 1
        return count
        