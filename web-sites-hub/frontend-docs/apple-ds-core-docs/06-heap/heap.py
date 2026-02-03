"""
最大堆和最小堆实现
"""

class MaxHeap:
    """最大堆实现"""
    
    def __init__(self):
        self.heap = []
    
    def _parent(self, i):
        """父节点索引"""
        return (i - 1) // 2
    
    def _left_child(self, i):
        """左子节点索引"""
        return 2 * i + 1
    
    def _right_child(self, i):
        """右子节点索引"""
        return 2 * i + 2
    
    def _swap(self, i, j):
        """交换两个元素"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _swim(self, i):
        """上浮"""
        while i > 0 and self.heap[i] > self.heap[self._parent(i)]:
            self._swap(i, self._parent(i))
            i = self._parent(i)
    
    def _sink(self, i):
        """下沉"""
        max_index = i
        left = self._left_child(i)
        right = self._right_child(i)
        
        # 找出最大值的索引
        if left < len(self.heap) and self.heap[left] > self.heap[max_index]:
            max_index = left
        if right < len(self.heap) and self.heap[right] > self.heap[max_index]:
            max_index = right
        
        # 如果最大值不是当前节点，交换并继续下沉
        if max_index != i:
            self._swap(i, max_index)
            self._sink(max_index)
    
    def insert(self, val):
        """插入元素"""
        self.heap.append(val)
        self._swim(len(self.heap) - 1)
    
    def extract_max(self):
        """删除并返回最大值"""
        if not self.heap:
            raise IndexError('extract from empty heap')
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # 交换堆顶和末尾
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink(0)
        return max_val
    
    def peek(self):
        """查看最大值"""
        if not self.heap:
            raise IndexError('peek from empty heap')
        return self.heap[0]
    
    def size(self):
        """堆大小"""
        return len(self.heap)
    
    def is_empty(self):
        """是否为空"""
        return len(self.heap) == 0
    
    @staticmethod
    def heapify(arr):
        """建堆（O(n)）"""
        heap = MaxHeap()
        heap.heap = arr[:]
        
        # 从最后一个非叶子节点开始下沉
        for i in range((len(arr) - 2) // 2, -1, -1):
            heap._sink(i)
        
        return heap
    
    def __str__(self):
        return str(self.heap)


class MinHeap:
    """最小堆（只修改比较符号）"""
    
    def __init__(self):
        self.heap = []
    
    def _parent(self, i):
        return (i - 1) // 2
    
    def _left_child(self, i):
        return 2 * i + 1
    
    def _right_child(self, i):
        return 2 * i + 2
    
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _swim(self, i):
        while i > 0 and self.heap[i] < self.heap[self._parent(i)]:
            self._swap(i, self._parent(i))
            i = self._parent(i)
    
    def _sink(self, i):
        min_index = i
        left = self._left_child(i)
        right = self._right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left
        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right
        
        if min_index != i:
            self._swap(i, min_index)
            self._sink(min_index)
    
    def insert(self, val):
        self.heap.append(val)
        self._swim(len(self.heap) - 1)
    
    def extract_min(self):
        if not self.heap:
            raise IndexError('extract from empty heap')
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink(0)
        return min_val
    
    def peek(self):
        if not self.heap:
            raise IndexError('peek from empty heap')
        return self.heap[0]


def heap_sort(arr):
    """堆排序"""
    # 建立最大堆
    heap = MaxHeap.heapify(arr)
    
    # 依次取出最大值
    result = []
    while not heap.is_empty():
        result.append(heap.extract_max())
    
    return result[::-1]  # 反转得到升序


def top_k_largest(nums, k):
    """最大的K个元素（使用最小堆）"""
    if k >= len(nums):
        return nums
    
    heap = MinHeap()
    
    # 先放入K个元素
    for i in range(k):
        heap.insert(nums[i])
    
    # 遍历剩余元素
    for i in range(k, len(nums)):
        if nums[i] > heap.peek():
            heap.extract_min()
            heap.insert(nums[i])
    
    return heap.heap


def demo():
    """演示堆操作"""
    print("=== 最大堆演示 ===\n")
    
    heap = MaxHeap()
    
    # 插入
    values = [3, 1, 6, 5, 2, 4]
    print(f"插入: {values}")
    for val in values:
        heap.insert(val)
        print(f"插入 {val}: {heap}")
    
    print(f"\n堆顶（最大值）: {heap.peek()}")
    
    # 删除
    print("\n依次删除最大值:")
    while not heap.is_empty():
        print(f"删除: {heap.extract_max()}, 堆: {heap}")
    
    print("\n=== 建堆演示 ===\n")
    arr = [3, 1, 6, 5, 2, 4]
    print(f"原数组: {arr}")
    heap2 = MaxHeap.heapify(arr)
    print(f"建堆后: {heap2}")
    
    print("\n=== 堆排序演示 ===\n")
    arr = [3, 1, 6, 5, 2, 4]
    print(f"原数组: {arr}")
    sorted_arr = heap_sort(arr)
    print(f"排序后: {sorted_arr}")
    
    print("\n=== Top K问题 ===\n")
    nums = [3, 2, 1, 5, 6, 4]
    k = 3
    print(f"数组: {nums}")
    print(f"最大的{k}个元素: {top_k_largest(nums, k)}")


if __name__ == '__main__':
    demo()

