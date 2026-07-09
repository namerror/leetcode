# Accepted
'''
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.
'''

class Solution:
    def isPalindrome(self, s: str) -> bool:
        t="".join(c for c in s if c.isalnum()).lower()
        l = 0
        r = len(t)-1
        while (l<r):
            if t[l] != t[r]:
                return False
            l+=1
            r-=1
        return True
        