'''
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

The left subtree of a node contains only nodes with keys strictly less than the node's key.
The right subtree of a node contains only nodes with keys strictly greater than the node's key.
Both the left and right subtrees must also be binary search trees.
'''

from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        last = None
        def traverse(root) -> bool:
            nonlocal last
            if root is None:
                return True
            
            if not traverse(root.left):
                return False
            if last is not None and last >= root.val:
                return False
            last = root.val

            return traverse(root.right)

        return traverse(root)

