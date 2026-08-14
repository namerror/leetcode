# Accepted. Uses recursive DFS instead of the canonical BFS with deque, but still optimal 
'''
Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).
'''

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        l = []
        def nextLevel(root: Optional[TreeNode], level):
            if root is None:
                return
            if len(l)-1 < level:
                l.append([])
            l[level].append(root.val)
            nextLevel(root.left, level+1)
            nextLevel(root.right, level+1)

        nextLevel(root, 0)

        return l