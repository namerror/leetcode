# Accepted, Difficult to notice binary search at first sight
'''
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.
'''

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        i = 1
        j = max(piles)

        def calcHours(k):
            hours = 0
            for x in piles:
                hours += -(-x//k)
            return hours

        min_k = j
        while i <= j:
            mid = (i+j)//2
            hours = calcHours(mid)
            if hours <= h:
                min_k = min(min_k, mid)
                j = mid-1
            if hours > h:
                i = mid+1

        return min_k
            