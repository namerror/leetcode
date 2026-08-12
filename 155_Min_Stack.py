# Accepted, note that bit shift needs to be in parentheses as - takes precedence over <<
'''
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:

MinStack() initializes the stack object.
void push(int value) pushes the element value onto the stack.
void pop() removes the element on the top of the stack.
int top() gets the top element of the stack.
int getMin() retrieves the minimum element in the stack.
You must implement a solution with O(1) time complexity for each function.
'''

class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = [(0b1 << 31) - 1]

    def push(self, value: int) -> None:
        self.stack.append(value)
        if value <= self.min_stack[-1]:
            self.min_stack.append(value)


    def pop(self) -> None:
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        del self.stack[-1]

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(value)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()