# Accepted
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        stack = []
        curr = head
        while curr:
            stack.append(curr)
            curr = curr.next
        if 1 < n < len(stack):
            stack[len(stack)-n].next = None
            stack[len(stack)-n-1].next = stack[len(stack)-n+1]
        elif n == len(stack):
            t = head
            head = head.next
            t.next = None
        elif n == 1:
            # tail
            stack[len(stack)-2].next = None
        return head