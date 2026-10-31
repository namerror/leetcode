# Accepted

'''
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

Example 1:

Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
Example 2:

Input: n = 1
Output: ["()"]
'''

class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        l = []
        # left, right means how many are left 
        def process(left, right, string:str):
            if left == 0:
                # append the rest
                l.append(''.join([string, ')'*right]))
                return 

            # we have to keep left <= right at all times
            if left == right:
                # no unclosed left paren
                new_string = ''.join([string, '('])
                process(left-1, right, new_string)
            else:
                string1 = ''.join([string, ')'])
                process(left, right-1, string1)
                string2 = ''.join([string, '('])
                process(left-1, right, string2)

        process(n, n, "")
        return l
            
                



        