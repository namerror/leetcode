# Accepted
"""
767. Reorganize String
Difficulty: Medium
https://leetcode.com/problems/reorganize-string/

Given a string s, rearrange the characters of s so that any two adjacent characters are not the same.

Return any possible rearrangement of s or return \"\" if not possible.

Example 1:

Input: s = \"aab\"
Output: \"aba\"

Example 2:

Input: s = \"aaab\"
Output: \"\"

Constraints:

- 1 <= s.length <= 500
- s consists of lowercase English letters.
"""

class Solution:
    def reorganizeString(self, s: str) -> str:
        mp = {}
        for c in s:
            if c not in mp:
                mp[c] = 0
            mp[c] += 1

        chars = []
        prev = "@"
        while len(mp) > 1:
            chosen = None
            max_v = 0
            for k,v in mp.items():
                if v > max_v and k != prev:
                    chosen = k
                    max_v = v
            prev = chosen
            chars.append(chosen)
            mp[chosen] -= 1
            if mp[chosen] == 0:
                mp.pop(chosen)

        last_char = list(mp.keys())[0]
        if mp[last_char] != 1:
            # not possible
            return ""

        chars.append(last_char)

        return ''.join(chars)
            
            
