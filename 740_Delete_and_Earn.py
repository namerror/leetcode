# Accepted

class Solution:
    def deleteAndEarn(self, nums: list[int]) -> int:
        mx = 0
        for i in nums:
            mx = max(i, mx)
        array = [0] * mx

        for i in nums:
            array[i-1] += i

        M = [0] * mx
        M[0] = array[0]
        if mx==1:
            return array[0]

        M[1] = max(array[0], array[1])
        for j in range(2, mx):
            M[j] = max(array[j]+M[j-2],M[j-1])

        return M[mx-1]



