# Accepted, although less clean, it is asymptotically optimal
'''
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.
'''

class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        sorted_nums = sorted(nums)
        k = len(nums)-1
        ans = []
        while k >= 2:
            target = 0-sorted_nums[k]
            i = 0
            j = k - 1
            while i < j:
                if sorted_nums[i]+sorted_nums[j] == target:
                    ans.append([sorted_nums[i], sorted_nums[j], sorted_nums[k]])
                    while i < j and sorted_nums[i] == sorted_nums[i+1]:
                        i += 1
                    i+=1
                elif sorted_nums[i]+sorted_nums[j] < target:
                    while i < j and sorted_nums[i] == sorted_nums[i+1]:
                        i += 1
                    i+=1

                else:
                    while i < j and sorted_nums[j] == sorted_nums[j-1]:
                        j -= 1
                    j-=1

            while k >= 2 and sorted_nums[k] == sorted_nums[k-1]:
                k-=1 

            k -= 1
        return ans