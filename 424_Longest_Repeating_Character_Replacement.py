# Accepted, except I didn't realize I could comment out line 24: it's counterintuitive
'''
You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.
'''

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        max_count = 0
        char_count = {}
        i = 0 # left
        max_length = 0
        for j in range(len(s)):

            # update char count
            char_count[s[j]] = char_count[s[j]] + 1 if char_count.get(s[j]) else 1
            max_count = max(max_count, char_count[s[j]])

            if j-i+1 - max_count > k:
                # no solution, shrink
                char_count[s[i]] -= 1
                i += 1
                # max_count = max(char_count.values())
                # this above line is not necessary, as we don't overgrow or over shrink the list at any point

            max_length = max(j-i+1, max_length)

        return max_length