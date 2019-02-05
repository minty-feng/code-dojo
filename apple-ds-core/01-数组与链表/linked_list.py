"""
单链表和双链表实现
"""

class ListNode:
    """链表节点"""
    
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __str__(self):
        return str(self.val)


class LinkedList:
    """单链表实现"""
    
    def __init__(self):
        """初始化"""
        self._head = None
        self._size = 0
    
    def __len__(self):
        """返回链表长度"""
        return self._size
    
    def is_empty(self):
        """判断是否为空"""
        return self._size == 0
    
    def prepend(self, val):
        """在头部添加节点
        
        Args:
            val: 节点值
        """
        new_node = ListNode(val, self._head)
        self._head = new_node
        self._size += 1
    
    def append(self, val):
        """在尾部添加节点
        
        Args:
            val: 节点值
        """
        if self._head is None:
            self._head = ListNode(val)
        else:
            curr = self._head
            while curr.next:
                curr = curr.next
            curr.next = ListNode(val)
        self._size += 1
    
    def insert(self, index, val):
        """在指定位置插入节点
        
        Args:
            index: 插入位置
            val: 节点值
            
        Raises:
            IndexError: 索引越界
        """
        if not 0 <= index <= self._size:
            raise IndexError('Index out of range')
        
        if index == 0:
            self.prepend(val)
            return
        
        curr = self._head
        for _ in range(index - 1):
            curr = curr.next
        
        curr.next = ListNode(val, curr.next)
        self._size += 1
    
    def remove(self, val):
        """删除第一个匹配的节点
        
        Args:
            val: 要删除的值
            
        Raises:
            ValueError: 值不存在
        """
        if self._head is None:
            raise ValueError(f'{val} not in list')
        
        # 删除头节点
        if self._head.val == val:
            self._head = self._head.next
            self._size -= 1
            return
        
        # 删除其他节点
        curr = self._head
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                self._size -= 1
                return
            curr = curr.next
        
        raise ValueError(f'{val} not in list')
    
    def pop(self, index=None):
        """删除并返回指定位置的节点值
        
        Args:
            index: 索引，默认为尾部
            
        Returns:
            节点值
            
        Raises:
            IndexError: 索引越界或链表为空
        """
        if self._head is None:
            raise IndexError('pop from empty list')
        
        if index is None:
            index = self._size - 1
        
        if not 0 <= index < self._size:
            raise IndexError('Index out of range')
        
        # 删除头节点
        if index == 0:
            val = self._head.val
            self._head = self._head.next
            self._size -= 1
            return val
        
        # 删除其他节点
        curr = self._head
        for _ in range(index - 1):
            curr = curr.next
        
        val = curr.next.val
        curr.next = curr.next.next
        self._size -= 1
        return val
    
    def find(self, val):
        """查找值的索引
        
        Args:
            val: 要查找的值
            
        Returns:
            索引
            
        Raises:
            ValueError: 值不存在
        """
        curr = self._head
        index = 0
        while curr:
            if curr.val == val:
                return index
            curr = curr.next
            index += 1
        raise ValueError(f'{val} not in list')
    
    def reverse(self):
        """反转链表"""
        prev = None
        curr = self._head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self._head = prev
    
    def to_list(self):
        """转换为Python列表"""
        result = []
        curr = self._head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result
    
    def __str__(self):
        """字符串表示"""
        return ' -> '.join(str(val) for val in self.to_list()) + ' -> None'


# 双链表节点
class DListNode:
    """双链表节点"""
    
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    """双链表实现"""
    
    def __init__(self):
        """初始化"""
        self._head = None
        self._tail = None
        self._size = 0
    
    def __len__(self):
        """返回链表长度"""
        return self._size
    
    def is_empty(self):
        """判断是否为空"""
        return self._size == 0
    
    def prepend(self, val):
        """在头部添加节点"""
        new_node = DListNode(val, None, self._head)
        if self._head is None:
            self._head = self._tail = new_node
        else:
            self._head.prev = new_node
            self._head = new_node
        self._size += 1
    
    def append(self, val):
        """在尾部添加节点"""
        new_node = DListNode(val, self._tail, None)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1
    
    def pop_front(self):
        """删除并返回头节点值"""
        if self._head is None:
            raise IndexError('pop from empty list')
        
        val = self._head.val
        self._head = self._head.next
        if self._head:
            self._head.prev = None
        else:
            self._tail = None
        self._size -= 1
        return val
    
    def pop_back(self):
        """删除并返回尾节点值"""
        if self._tail is None:
            raise IndexError('pop from empty list')
        
        val = self._tail.val
        self._tail = self._tail.prev
        if self._tail:
            self._tail.next = None
        else:
            self._head = None
        self._size -= 1
        return val
    
    def to_list(self):
        """转换为Python列表"""
        result = []
        curr = self._head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result
    
    def __str__(self):
        """字符串表示"""
        return ' <-> '.join(str(val) for val in self.to_list())


def demo():
    """演示链表的使用"""
    print("=== 单链表演示 ===\n")
    
    # 创建链表
    ll = LinkedList()
    print(f"创建空链表: {ll}\n")
    
    # 添加元素
    print("尾部添加: 1, 2, 3")
    for i in range(1, 4):
        ll.append(i)
    print(f"链表: {ll}\n")
    
    # 头部添加
    print("头部添加: 0")
    ll.prepend(0)
    print(f"链表: {ll}\n")
    
    # 插入
    print("在索引2插入99")
    ll.insert(2, 99)
    print(f"链表: {ll}\n")
    
    # 查找
    print(f"查找99的索引: {ll.find(99)}\n")
    
    # 删除
    print("删除元素99")
    ll.remove(99)
    print(f"链表: {ll}\n")
    
    # 反转
    print("反转链表")
    ll.reverse()
    print(f"链表: {ll}\n")
    
    print("\n=== 双链表演示 ===\n")
    
    # 创建双链表
    dll = DoublyLinkedList()
    print(f"创建空双链表\n")
    
    # 添加元素
    print("尾部添加: 1, 2, 3")
    for i in range(1, 4):
        dll.append(i)
    print(f"双链表: {dll}\n")
    
    # 头部添加
    print("头部添加: 0")
    dll.prepend(0)
    print(f"双链表: {dll}\n")
    
    # 头部删除
    print(f"头部删除: {dll.pop_front()}")
    print(f"双链表: {dll}\n")
    
    # 尾部删除
    print(f"尾部删除: {dll.pop_back()}")
    print(f"双链表: {dll}")


if __name__ == '__main__':
    demo()

