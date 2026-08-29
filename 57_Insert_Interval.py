# Accepted
'''
You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi] represent the start and the end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] that represents the start and end of another interval.

Two intervals are considered overlapping if they share at least one point.

Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion.

Note that you don't need to modify intervals in-place. You can make a new array and return it.
'''

from collections import deque
from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        l = deque()

        while intervals and newInterval[1] <= intervals[-1][0]:
            if newInterval[1] == intervals[-1][0]:
                newInterval = [newInterval[0], intervals.pop()[1]]
                break
            l.appendleft(intervals.pop())

        l.appendleft(newInterval)

        # keep merging left
        while intervals and l[0][0] <= intervals[-1][1]:
            c = intervals.pop()
            l[0][0] = min(l[0][0], c[0])
            l[0][1] = max(l[0][1], c[1])
        # append back
        while l:
            intervals.append(l.popleft())

        return intervals