# Accepted, took a long time
"""
1004. Max Consecutive Ones III
Difficulty: Medium
https://leetcode.com/problems/max-consecutive-ones-iii/

Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.

Example 1:

Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

Example 2:

Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

Constraints:

- 1 <= nums.length <= 10^(5)
- nums[i] is either 0 or 1.
- 0 <= k <= nums.length
"""

from collections import deque

class Solution:
    def longestOnes(self, nums: list[int], k: int) -> int:
        intervals = []

        i = 0
        while True:
            while i < len(nums) and nums[i] == 0:
                i += 1
            if i == len(nums):
                break
            j = i

            while j < len(nums) and nums[j] == 1:
                j += 1
            j -= 1

            intervals.append([i, j])

            i = j+1
        print(intervals)
        # intervals like [1, 3], [5, 7], [10, 11], [13, 13]
        if not intervals:
            return min(k, len(nums))

        if len(intervals) == 1:
            return min(k+intervals[0][1]-intervals[0][0]+1, len(nums))

        l = 0
        r = 0
        
        max_window = intervals[r][1] - intervals[l][0] + 1
        remain = k
        while r < len(intervals)-1:
            gap = intervals[r+1][0] - intervals[r][1] - 1
            if gap <= remain:
                # fill the gap and extend window
                r += 1
                max_window = max(max_window, intervals[r][1] - intervals[l][0]+1)
                remain -= gap
            else:
                # it can't reach the next interval, we reset and start new
                # first evaluate current interval
                max_window = max(max_window, intervals[r][1]-intervals[l][0]+1+remain)
                # discard the leftmost interval
                if l < r:
                    remain += intervals[l+1][0] - intervals[l][1] - 1
                else:
                    r += 1 # move right index if left has to move
                l += 1

        # to this point, the right has reached the end 
        # now we flip any zeroes around if we have remaining ones
        left_end = intervals[l-1][1]+1 if l > 0 else 0
        right_end = len(nums)-1
        window = min(intervals[r][1]-intervals[l][0]+1+remain, right_end-left_end+1)
        max_window = max(window, max_window)
        
        return max_window