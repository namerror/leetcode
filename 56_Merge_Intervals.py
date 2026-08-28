# Accepted. Below is my first try implementation, optimal but unnecessarily complicated
# The cleaner version would just compare the last popped element's end with the current element's start and end to determine whether to merge

'''
Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
'''

from collections import deque
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:

        def order(ints: List[int]):
            return ints[0]
        
        s_intervals = deque(sorted(intervals, key=order))
        out = []
        while len(s_intervals) >= 2:
            # check if overlap at all
            if s_intervals[0][1] < s_intervals[1][0]:
                # done with the first interval
                out.append(s_intervals.popleft())
            elif s_intervals[0][1] >= s_intervals[1][1]:
                # merge the second one into the first
                lower = s_intervals[0][0]
                upper = s_intervals[0][1]
                s_intervals.popleft()
                s_intervals.popleft()
                s_intervals.appendleft([lower, upper])
            elif s_intervals[0][1] >= s_intervals[1][0]:
                lower = s_intervals.popleft()[0]
                upper = s_intervals.popleft()[1]
                s_intervals.appendleft([lower, upper])

        out.append(s_intervals.pop())

        return out