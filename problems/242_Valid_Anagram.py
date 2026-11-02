# Accepted

'''
Given two strings s and t, return true if t is an anagram of s, and false otherwise.
'''

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        d1 = {}
        d2 = {}
        for c in s:
            d1[c] = d1.get(c, 0) + 1
        for c in t:
            d2[c] = d2.get(c, 0) + 1

        return d1 == d2