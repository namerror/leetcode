# Accepted, note edge cases
'''
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.
'''
from collections import deque
from typing import *

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        in_degree = [0] * numCourses
        nodes: Dict[int, List[int]] = {}
        for p in prerequisites:
            if p[1] in nodes:
                nodes[p[1]].append(p[0])
            else:
                nodes[p[1]] = [p[0]]
            in_degree[p[0]] += 1

        queue = deque()
        for i in range(len(in_degree)):
            if in_degree[i] == 0:
                queue.append(i) # store 0-in-degree nodes

        removed_count = 0
        while len(queue) > 0:
            x = queue.pop()
            removed_count += 1
            if x not in nodes:
                continue
            for y in nodes.get(x):
                in_degree[y] -= 1
                if in_degree[y] == 0:
                    queue.appendleft(y) # add new node with no incoming edges

        if removed_count == numCourses:
            return True
        else:
            return False
        