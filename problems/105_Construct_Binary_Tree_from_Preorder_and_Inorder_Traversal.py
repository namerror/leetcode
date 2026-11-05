# Accepted, not optimal

"""
105. Construct Binary Tree from Preorder and Inorder Traversal
Difficulty: Medium
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

Example 1:

[Image: illustration] https://assets.leetcode.com/uploads/2021/02/19/tree.jpg

Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]

Example 2:

Input: preorder = [-1], inorder = [-1]
Output: [-1]

Constraints:

- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values.
- Each value of inorder also appears in preorder.
- preorder is guaranteed to be the preorder traversal of the tree.
- inorder is guaranteed to be the inorder traversal of the tree.
"""

# Definition for a binary tree node.
from lark import Tree


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> TreeNode | None:
        if not preorder:
            return None
        if len(preorder) == 1:
            return TreeNode(preorder[0])
        
        # find root
        root = preorder[0]

        lefti = righti = leftp = rightp = None
        # split left and right components from inorder
        for i in range(len(inorder)):
            if inorder[i] == root:
                lefti = inorder[:i]
                righti = inorder[i+1:]
                break

        # extract the corresponding preorder lists
        leftp = preorder[1:len(lefti)+1]
        rightp = preorder[len(lefti)+1:]

        # left node
        return TreeNode(root, self.buildTree(leftp, lefti), self.buildTree(rightp, righti))