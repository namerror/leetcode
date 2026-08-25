# Accepted

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        last = None
        curr = head
        while curr is not None:
            next = curr.next
            curr.next = last
            last = curr
            curr = next

        return last