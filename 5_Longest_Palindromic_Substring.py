# Accepted

'''Given a string s, return the longest palindromic substring in s.

Example 1:

    Input: s = "babad"
    Output: "bab"
    Explanation: "aba" is also a valid answer.

Example 2:

    Input: s = "cbbd"
    Output: "bb"

Constraints:

    1 <= s.length <= 1000
    s consist of only digits and English letters.
'''

class Solution:
    def longestPalindrome(self, s: str) -> str:
        max_len = 1
        max_str = s[0]
        for n in range(0, len(s)-1):
            cur_len = 1
            l = n-1
            r = n+1
            while (l >= 0 and r < len(s)):
                if s[l] == s[r]:
                    cur_len += 2
                    l = l-1
                    r = r+1
                else:
                    break

            if max_len < cur_len:
                max_str = s[l+1: r]
                max_len = cur_len

            cur_len = 0
            l = n
            r = n+1

            while (l >= 0 and r < len(s)):
                if s[l] == s[r]:
                    cur_len += 2
                    l -= 1
                    r += 1
                else:
                    break
            if max_len < cur_len:
                max_str = s[l+1: r]
                max_len = cur_len

        return max_str  
            

