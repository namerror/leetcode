# Accepted
# This one was insanely hard for me, implementation wise
# It's important to acknowledge the optimal starting position of the intervals
# It's also difficult to model the sum across a few intervals
# the right approach I think is a sliding window, but the start and end of it is conditioned 
# to be on the start and end of the intervals
"""
3413. Maximum Coins From K Consecutive Bags
Difficulty: Medium
https://leetcode.com/problems/maximum-coins-from-k-consecutive-bags/

There are an infinite amount of bags on a number line, one bag for each coordinate. Some of these bags contain coins.

You are given a 2D array coins, where coins[i] = [l_(i), r_(i), c_(i)] denotes that every bag from l_(i) to r_(i) contains c_(i) coins.

The segments that coins contain are non-overlapping.

You are also given an integer k.

Return the maximum amount of coins you can obtain by collecting k consecutive bags.

Example 1:

Input: coins = [[8,10,1],[1,3,2],[5,6,4]], k = 4

Output: 10

Explanation:

Selecting bags at positions [3, 4, 5, 6] gives the maximum number of coins: 2 + 0 + 4 + 4 = 10.

Example 2:

Input: coins = [[1,10,3]], k = 2

Output: 6

Explanation:

Selecting bags at positions [1, 2] gives the maximum number of coins: 3 + 3 = 6.

Constraints:

- 1 <= coins.length <= 10^(5)
- 1 <= k <= 10^(9)
- coins[i] == [l_(i), r_(i), c_(i)]
- 1 <= l_(i) <= r_(i) <= 10^(9)
- 1 <= c_(i) <= 1000
- The given segments are non-overlapping.
"""
from typing import List

class Solution:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        coins = sorted(coins, key=lambda i: i[0])
        
        max_coins = 0
        start = coins[0][0]
        l_i = 0 # left index: start is at least smaller than the end of interval i
        end = start + k - 1 
        r_i = 0 # right index: end at most larger than the start of interval i
        total = 0
        # do the first range first: start at coins[0][0]
        while r_i+1 <= len(coins)-1:
            if coins[r_i+1][0] > end:
                break
            total += coins[r_i][2] * (coins[r_i][1]-coins[r_i][0]+1)
            r_i += 1
        if end >= coins[r_i][1]:
            total += coins[r_i][2] * (coins[r_i][1]-coins[r_i][0]+1)
        else:
            total += coins[r_i][2] * (end - coins[r_i][0]+1)

        # now the first interval is checked:  we may continue moving

        while end < coins[-1][1]:
            max_coins = max(max_coins, total)

            # we'll decide the smaller next step
            # either move end to the next end or start to the next start

            # option 1: align start with the next start
            next_start = (
                coins[l_i][0] if start < coins[l_i][0]
                else coins[l_i+1][0] if l_i+1 < len(coins)
                else float("inf")
            )
            diff1 = next_start-start

            # option 2: align end with next end
            next_end = coins[r_i][1] if end < coins[r_i][1] else coins[r_i+1][1]
            diff2 = next_end - end

            shift = min(diff1, diff2)

            # we know it will differ by at most one interval on both sides
            # just need to update l_i, r_i, start, end and total
            new_start = start + shift
            new_end = end + shift
            if new_start > coins[l_i][1]:
                # start has left the current interval
                # so we need to deduct all the coins from that range
                total -= (coins[l_i][1] - start+1) * coins[l_i][2]
                l_i+=1 
            else:
                if start >= coins[l_i][0]:
                    total -= shift * coins[l_i][2]

            if r_i + 1 < len(coins) and new_end >= coins[r_i + 1][0]:
                total += (new_end - coins[r_i + 1][0] + 1) * coins[r_i + 1][2]
                r_i += 1
            elif end < coins[r_i][1]:
                total += shift * coins[r_i][2]

            start = new_start
            end = new_end

        return max(max_coins, total)