# Accepted

'''
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.


'''
from collections import defaultdict, deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:

        hashmap = defaultdict(int)
        childmap = defaultdict(set)
        
        order = []
        for pair in prerequisites:
            hashmap[pair[0]] += 1
            childmap[pair[1]].add(pair[0]) 

        queue = deque()

        for n in range(0, numCourses):
            if hashmap[n] == 0:
                queue.append(n)

        while queue:
            cur = queue.popleft()
            for child in childmap[cur]:
                hashmap[child] -= 1
                if hashmap[child] == 0:
                    queue.append(child)

            order.append(cur)

        if len(order) != numCourses:
            return []

        return order

        