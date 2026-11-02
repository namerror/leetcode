# Accepted. Took me a long time, not because of thinking of the solution
# But because I initialized the array with [[]]*n, which was the wrong way
# The difference is this doesn't create a list of separate empty lists,
# but a list where all elements point to the same list object, which is different from
# the standard (correct) way to initialize: [[] for _ in range(n)] 
'''
Given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of s.

Example 1:

    Input: s = "aab"
    Output: [["a","a","b"],["aa","b"]]

Example 2:

    Input: s = "a"
    Output: [["a"]]

Constraints:

    1 <= s.length <= 16
    s contains only lowercase English letters.
'''

from typing import List

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        M = [[] for _ in range(len(s))] # memorize the ways to partition ending at index i (0 to n-1)

        M[0] = [[s[0]]]
        print(M)
        for i in range(1, len(s)):
            # now ending at char i, search for all palindromes
            for x in range(0, i+1):
                candidate = s[x:i+1]
                if candidate[::-1] == candidate:
                    # is palindrome
                    if x == 0:
                        M[i].append([candidate])
                    else:
                        for ans in M[x-1]:
                            M[i].append(ans + [candidate])
        return M[len(s)-1]
