# Accepted. Most difficult one yet. Failed to recognize that the bottleneck is the most frequent task.
'''
You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least n intervals between two tasks with the same label.

Return the minimum number of CPU intervals required to complete all tasks.
'''

from collections import defaultdict
from heapq import *

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        h = []
        counts = defaultdict(int)
        for t in tasks:
            counts[t] += 1

        for char, count in counts.items():
            heappush(h, -count)

        time = 0
        while h:

            temp = [] # temporary one to store all the tasks remaining
            wait_time = 0 

            while h and wait_time < n+1:
                popped = heappop(h)
                popped = popped + 1
                if popped < 0:
                    temp.append(popped)

                wait_time += 1

            for s in temp:
                heappush(h, s)

            if h and wait_time < n+1:
                wait_time = n+1 # a cycle is at least n+1 long except for the last cycle

            time += wait_time
            

        return time