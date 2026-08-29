# Accepted. My first solution was very complex. It took me a long time to think of the optimal approach.
'''
You are given a string s. We want to partition the string into as many parts as possible so that each letter appears in at most one part. For example, the string "ababcc" can be partitioned into ["abab", "cc"], but partitions such as ["aba", "bcc"] or ["ab", "ab", "cc"] are invalid.

Note that the partition is done so that after concatenating all the parts in order, the resultant string should be s.

Return a list of integers representing the size of these parts.
'''

class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        end_table = {}

        for i in range(len(s)):
            end_table[s[i]] = i

        end = 0
        res = []
        start = 0
        for j in range(len(s)):
            if end_table[s[j]] > end:
                end = end_table[s[j]]
            elif j == end:
                length = end - start + 1
                res.append(length)
                start = j + 1
                end = j + 1
        return res