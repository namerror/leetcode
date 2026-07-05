# Accepted. For this problem, the more optimal solution is by just identifying the start of a sequence: when n-1 exists, it's not at the beginning; else, that's the start and we do a while loop to go all the way to the end to count max counts. This could work because by converting the list to a set, it's O(1) time to identify whether some element is in the set, so it's guarenteed that the start identified is correct. However, I used the following method, because I thought the previous one might not be strictly O(n)

'''
Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.
'''

class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        d = {}
        mx = 0
        for n in nums:
            if n in d:
                continue
            d[n] = [n, n] # default
            if n-1 in d:
                d[n][0] = d[n-1][0] # mark start
            if n+1 in d:
                d[n][1] = d[n+1][1] # mark end
            d[d[n][0]][1] = d[n][1]
            d[d[n][1]][0] = d[n][0]
            mx = max(mx, d[d[n][1]][1]-d[d[n][0]][0]+1)
        return mx