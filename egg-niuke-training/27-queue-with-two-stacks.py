"""
NC76 用两个栈实现队列
https://www.nowcoder.com/practice/54275ddae22f475981afa2244dd448c6

用两个栈来实现一个队列，完成队列的Push和Pop操作。

栈1用于入队，栈2用于出队

时间复杂度：Push O(1), Pop 摊还O(1)
空间复杂度：O(n)
"""

class QueueWithTwoStacks:
    def __init__(self):
        self.stack1 = []  # 用于入队
        self.stack2 = []  # 用于出队
    
    def push(self, node):
        """入队"""
        self.stack1.append(node)
    
    def pop(self):
        """出队"""
        if not self.stack2:
            # 将stack1的所有元素转移到stack2
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        
        if not self.stack2:
            return -1  # 队列为空
        
        return self.stack2.pop()

# 测试
if __name__ == "__main__":
    queue = QueueWithTwoStacks()
    
    # 测试
    queue.push(1)
    queue.push(2)
    queue.push(3)
    
    print(f"出队: {queue.pop()}")  # 1
    print(f"出队: {queue.pop()}")  # 2
    
    queue.push(4)
    print(f"出队: {queue.pop()}")  # 3
    print(f"出队: {queue.pop()}")  # 4

