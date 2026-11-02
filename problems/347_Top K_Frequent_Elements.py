# Accepted, O(n) solution exists
'''
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
'''

from heapq import *
from collections import defaultdict

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        mp = defaultdict(int)

        for n in nums:
            mp[n] += 1

        heap = []

        for key, value in mp.items():
            heappush(heap, (-value, key))

        out = []
        for i in range(k):
            out.append(heappop(heap)[1])

        return out

                

        
        
        