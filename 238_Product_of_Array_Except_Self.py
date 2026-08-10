# Accepted
'''
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.
'''

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        pre = [0] * len(nums)
        suf = [0] * len(nums)
        pre[0] = 1
        suf[len(nums)-1] = 1
        for i in range(1, len(pre)):
            pre[i] = pre[i-1] * nums[i-1]
        for j in range(1, len(nums)):
            suf[len(nums)-1-j] = suf[len(nums)-j] * nums[len(nums)-j]
        M = []
        for n in range(len(nums)):
            M.append(pre[n]*suf[n])

        return M