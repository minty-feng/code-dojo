"""
LeetCode 155. 最小栈
https://leetcode.cn/problems/min-stack/

设计一个支持push，pop，top操作，并能在常数时间内检索到最小元素的栈。

辅助栈

时间复杂度：O(1) 所有操作
空间复杂度：O(n)
"""

class MinStack:
    """
    最小栈 - 辅助栈法
    """
    
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        """
        入栈
        
        Args:
            val: 要入栈的值
        """
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self):
        """
        出栈
        """
        if not self.stack:
            return
        
        val = self.stack.pop()
        if self.min_stack and val == self.min_stack[-1]:
            self.min_stack.pop()
    
    def top(self):
        """
        获取栈顶元素
        
        Returns:
            栈顶元素
        """
        return self.stack[-1] if self.stack else None
    
    def get_min(self):
        """
        获取最小元素
        
        Returns:
            最小元素
        """
        return self.min_stack[-1] if self.min_stack else None


def test_min_stack():
    """测试函数"""
    min_stack = MinStack()
    
    # 测试用例
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    
    print(f"最小元素: {min_stack.get_min()}")  # 期望: -3
    
    min_stack.pop()
    print(f"栈顶元素: {min_stack.top()}")      # 期望: 0
    print(f"最小元素: {min_stack.get_min()}")  # 期望: -2


if __name__ == "__main__":
    test_min_stack()
