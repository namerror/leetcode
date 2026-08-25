# Accepted
'''
Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.
'''

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        char_t = {}
        missing_char = set()
        for a in t:
            char_t[a] = char_t.get(a, 0) + 1
            missing_char.add(a)

        i = 0
        min_s = ""
        for j in range(len(s)):
            if s[j] in char_t:
                char_t[s[j]] -= 1
                if char_t[s[j]] == 0:
                    missing_char.remove(s[j]) # satisfies requirement

                    if len(missing_char) == 0:
                        while i <= j:
                            # everything is present, shrink left side
                            if s[i] in char_t:
                                if char_t[s[i]] == 0:
                                    if j+1-i < len(min_s) or min_s=="":
                                        min_s = s[i:j+1]
                                    missing_char.add(s[i])
                                    char_t[s[i]] += 1
                                    i+=1
                                    break
                                else:
                                    char_t[s[i]] += 1
                            i += 1
        return min_s

solution = Solution()
solution.minWindow("ADOBECODEBANC", "ABC")


