# Accepted
'''
Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.
'''

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        def helpersort(interval):
            return interval[0]

        sorted_intervals = sorted(intervals, key=helpersort)
        count = 0
        curr = sorted_intervals[0][1]
        for i in range(1, len(sorted_intervals)):
            if curr > sorted_intervals[i][0]:
                count += 1
                curr = min(curr, sorted_intervals[i][1])
            else:
                curr = sorted_intervals[i][1]

        return count