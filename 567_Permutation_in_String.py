'''
Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.

In other words, return true if one of s1's permutations is the substring of s2.
'''

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        c_s1 = {}
        for c in s1:
            if c in c_s1:
                c_s1[c] += 1
            else:
                c_s1[c] = 1

        i = 0
        for j in range(len(s2)):
            if c_s1.get(s2[j], 0) == 0:
                c_s1[s2[j]] = -1
                while c_s1[s2[j]] < 0:
                    c_s1[s2[i]] += 1
                    i += 1
            else:
                c_s1[s2[j]] -= 1

            if len(set(c_s1.values())) == 1:
                if 0 in c_s1.values():
                    return True

        return False