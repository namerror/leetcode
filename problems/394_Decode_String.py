"""
394. Decode String
Difficulty: Medium
https://leetcode.com/problems/decode-string/

Given an encoded string, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.

You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4].

The test cases are generated so that the length of the output will never exceed 10^(5).

Example 1:

Input: s = \"3[a]2[bc]\"
Output: \"aaabcbc\"

Example 2:

Input: s = \"3[a2[c]]\"
Output: \"accaccacc\"

Example 3:

Input: s = \"2[abc]3[cd]ef\"
Output: \"abcabccdcdcdef\"

Constraints:

- 1 <= s.length <= 30
- s consists of lowercase English letters, digits, and square brackets '[]'.
- s is guaranteed to be a valid input.
- All the integers in s are in the range [1, 300].
"""

from collections import defaultdict
from curses.ascii import isdigit

class Solution:
    def decodeString(self, s: str) -> str:
        d = defaultdict(str)
        stack = []
        res = ''
        for i, c in enumerate(s):
            if c == '[':
                stack.append(i+1) # keeps track of current bracket start
            elif c == ']':
                r = stack[-1]-2
                multiplier = ""
                while s[r].isdigit():
                    multiplier = s[r] + multiplier
                    r -= 1
                cur_s = d[stack[-1]] * int(multiplier)
                stack.pop()
                # the last bracket
                if not stack:
                    res += cur_s
                else:
                    d[stack[-1]] += cur_s
            else:
                if c.isalpha():
                    if not stack:
                        res += c
                    else:
                        d[stack[-1]] += c

        return res
            
