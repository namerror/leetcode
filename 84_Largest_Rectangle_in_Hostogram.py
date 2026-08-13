# Accepted, somewhat overcomplicated, but asymptotically optimal O(n)
'''
Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
'''

from typing import List

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        asc_stack = []
        dsc_stack = []
        widths = [1] * len(heights)

        for i in range(len(heights)):
            while asc_stack and heights[asc_stack[-1]] > heights[i]:
                widths[asc_stack[-1]] += i - asc_stack[-1] - 1
                asc_stack.pop() # remove every higher one and record its right-extended width
            asc_stack.append(i)

            j = len(heights)-i-1

            # we should have recorded each of their right extended width. Now left side

            while dsc_stack and heights[dsc_stack[-1]] > heights[j]:
                widths[dsc_stack[-1]] += dsc_stack[-1] - j - 1
                dsc_stack.pop()
            dsc_stack.append(j)

        while asc_stack:
            # clean up left overs
            widths[asc_stack[-1]] += len(heights)-1-asc_stack[-1]
            asc_stack.pop()
        while dsc_stack:
            widths[dsc_stack[-1]] += dsc_stack[-1]
            dsc_stack.pop()

        mx = 0
        for k in range(len(heights)):
            mx = max(widths[k] * heights[k], mx)

        return mx