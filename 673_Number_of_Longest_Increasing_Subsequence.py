# Accepted, hard to do it right the first time
'''
Given an integer array nums, return the number of longest increasing subsequences.

Notice that the sequence has to be strictly increasing.

Example 1:

    Input: nums = [1,3,5,4,7]
    Output: 2
    Explanation: The two longest increasing subsequences are [1, 3, 4, 7] and [1, 3, 5, 7].

Example 2:

    Input: nums = [2,2,2,2,2]
    Output: 5
    Explanation: The length of the longest increasing subsequence is 1, and there are 5 increasing subsequences of length 1, so output 5.

Constraints:

    1 <= nums.length <= 2000
    -106 <= nums[i] <= 106
    The answer is guaranteed to fit inside a 32-bit integer.    
'''

class Solution:
    def findNumberOfLIS(self, nums: list[int]) -> int:
        M = [1] * len(nums)
        max_len = 1
        counts = [1] * len(nums) # stores the corresponding counts of length at i
        for i in range(1, len(nums)):
            j = 1
            while i-j >= 0:
                if nums[i-j] < nums[i]:
                    if M[i-j]+1 > M[i]:
                        # found candidate length
                        M[i] = M[i-j]+1
                        counts[i] = counts[i-j]
                    elif M[i-j]+1 == M[i]:
                        # found same max length, but different subsequence
                        counts[i] += counts[i-j]

                j += 1
            max_len = max(max_len, M[i])

        max_count = 0
        for x in range(len(nums)):
            if M[x] == max_len:
                max_count+= counts[x]

        return max_count

        

                
            