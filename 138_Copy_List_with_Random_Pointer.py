# Accepted, two while loops is cleaner but I spent time trying to do in one pass
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        curr = head
        if head is None:
            return None
        
        h = {}
        while curr:
            h[curr] = Node(curr.val)
            curr = curr.next

        curr = head
        while curr:
            h[curr].next = h.get(curr.next, None)
            h[curr].random = h.get(curr.random, None)
            curr = curr.next
        
        return h[head]