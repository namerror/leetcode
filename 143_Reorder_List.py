# Accepted. The common solution is slightly different from mine: people tend to find middle, reverse second half then merge
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from collections import deque

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        dq = deque()
        curr = head
        while curr:
            dq.append(curr)
            curr = curr.next

        head = dq.popleft()
        last = head
        while len(dq) > 0:
            tail = dq.pop()
            last.next = tail
            last = last.next
            if len(dq) == 0:
                break
            front = dq.popleft()
            last.next = front
            last = last.next
        
        last.next = None