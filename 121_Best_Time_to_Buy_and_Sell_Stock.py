# Accepted
'''
You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
'''

from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        cheapest = prices[0]
        p = 0
        mp = p
        for i in range(1, len(prices)):
            cheapest = min(cheapest, prices[i-1])
            mp = max(mp, prices[i]-cheapest)
        return mp