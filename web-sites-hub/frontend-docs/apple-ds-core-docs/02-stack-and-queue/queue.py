"""
队列的实现：循环队列和链式队列
"""

class CircularQueue:
    """循环队列（基于数组）"""
    
    def __init__(self, capacity=5):
        self._data = [None] * (capacity + 1)  # 多一个位置区分满和空
        self._front = 0
        self._rear = 0
        self._capacity = capacity + 1
    
    def enqueue(self, val):
        """入队"""
        if self.is_full():
            raise OverflowError('Queue is full')
        self._data[self._rear] = val
        self._rear = (self._rear + 1) % self._capacity
    
    def dequeue(self):
        """出队"""
        if self.is_empty():
            raise IndexError('dequeue from empty queue')
        val = self._data[self._front]
        self._front = (self._front + 1) % self._capacity
        return val
    
    def front(self):
        """查看队首"""
        if self.is_empty():
            raise IndexError('front from empty queue')
        return self._data[self._front]
    
    def is_empty(self):
        """是否为空"""
        return self._front == self._rear
    
    def is_full(self):
        """是否已满"""
        return (self._rear + 1) % self._capacity == self._front
    
    def size(self):
        """队列大小"""
        return (self._rear - self._front + self._capacity) % self._capacity
    
    def __str__(self):
        if self.is_empty():
            return "Queue([])"
        items = []
        i = self._front
        while i != self._rear:
            items.append(self._data[i])
            i = (i + 1) % self._capacity
        return f"Queue({items})"


class LinkedQueue:
    """链式队列"""
    
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next
    
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
    
    def enqueue(self, val):
        """入队"""
        new_node = self.Node(val)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1
    
    def dequeue(self):
        """出队"""
        if self.is_empty():
            raise IndexError('dequeue from empty queue')
        val = self._head.val
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return val
    
    def front(self):
        """查看队首"""
        if self.is_empty():
            raise IndexError('front from empty queue')
        return self._head.val
    
    def is_empty(self):
        return self._size == 0
    
    def size(self):
        return self._size


# 双端队列
class Deque:
    """双端队列"""
    
    def __init__(self):
        self._data = []
    
    def add_front(self, val):
        """前端添加"""
        self._data.insert(0, val)
    
    def add_rear(self, val):
        """后端添加"""
        self._data.append(val)
    
    def remove_front(self):
        """前端删除"""
        if self.is_empty():
            raise IndexError('remove from empty deque')
        return self._data.pop(0)
    
    def remove_rear(self):
        """后端删除"""
        if self.is_empty():
            raise IndexError('remove from empty deque')
        return self._data.pop()
    
    def is_empty(self):
        return len(self._data) == 0


if __name__ == '__main__':
    print("=== 循环队列演示 ===\n")
    queue = CircularQueue(5)
    
    print("入队: 1, 2, 3")
    for i in range(1, 4):
        queue.enqueue(i)
        print(f"enqueue({i}): {queue}")
    
    print(f"\nfront(): {queue.front()}")
    print(f"size(): {queue.size()}")
    
    print(f"\ndequeue(): {queue.dequeue()}")
    print(f"队列: {queue}")
    
    print(f"\n入队: 4, 5")
    queue.enqueue(4)
    queue.enqueue(5)
    print(f"队列: {queue}")

