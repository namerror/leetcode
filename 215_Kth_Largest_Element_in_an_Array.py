# Accepted. Optimal solution exists (quickselect), but for me heap is easier
'''
Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?
'''
from heapq import *
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heapify(nums)
        while len(nums)-k > 0:
            heappop(nums)

        return heappop(nums)