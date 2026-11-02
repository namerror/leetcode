# Accepted, solution O(len(nums1) + len(nums2)) with stack
'''
The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.

You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.

For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.

Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.


'''


from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:

        hashmap = {}
        stack = []
        for i in nums2:
            if i == nums2[0]:
                stack.append(i)
                hashmap[i] = -1
                continue
            while stack and i > stack[-1]:
                hashmap[stack.pop()] = i
            stack.append(i)
            hashmap[i] = -1

        results = []
        for j in nums1:
            results.append(hashmap[j])

        return results