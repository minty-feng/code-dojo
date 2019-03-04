"""
栈的实现：数组栈和链式栈
"""

class ArrayStack:
    """基于数组的栈"""
    
    def __init__(self):
        self._data = []
    
    def push(self, val):
        """入栈"""
        self._data.append(val)
    
    def pop(self):
        """出栈"""
        if self.is_empty():
            raise IndexError('pop from empty stack')
        return self._data.pop()
    
    def peek(self):
        """查看栈顶"""
        if self.is_empty():
            raise IndexError('peek from empty stack')
        return self._data[-1]
    
    def is_empty(self):
        """是否为空"""
        return len(self._data) == 0
    
    def size(self):
        """栈大小"""
        return len(self._data)
    
    def __str__(self):
        return f"Stack({self._data})"


class LinkedStack:
    """基于链表的栈"""
    
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next
    
    def __init__(self):
        self._top = None
        self._size = 0
    
    def push(self, val):
        """入栈"""
        self._top = self.Node(val, self._top)
        self._size += 1
    
    def pop(self):
        """出栈"""
        if self.is_empty():
            raise IndexError('pop from empty stack')
        val = self._top.val
        self._top = self._top.next
        self._size -= 1
        return val
    
    def peek(self):
        """查看栈顶"""
        if self.is_empty():
            raise IndexError('peek from empty stack')
        return self._top.val
    
    def is_empty(self):
        return self._size == 0
    
    def size(self):
        return self._size


if __name__ == '__main__':
    print("=== 数组栈演示 ===\n")
    stack = ArrayStack()
    
    for i in range(1, 4):
        stack.push(i)
        print(f"push({i}): {stack}")
    
    print(f"\npeek(): {stack.peek()}")
    
    while not stack.is_empty():
        print(f"pop(): {stack.pop()}")
    
    print(f"\n栈是否为空: {stack.is_empty()}")

