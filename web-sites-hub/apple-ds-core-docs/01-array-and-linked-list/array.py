"""
动态数组实现
支持自动扩容和缩容
"""

class DynamicArray:
    """动态数组实现"""
    
    def __init__(self, capacity=4):
        """初始化
        
        Args:
            capacity: 初始容量
        """
        self._data = [None] * capacity
        self._size = 0
        self._capacity = capacity
    
    def __len__(self):
        """返回元素个数"""
        return self._size
    
    def __getitem__(self, index):
        """获取索引位置的元素
        
        Args:
            index: 索引
            
        Returns:
            元素值
            
        Raises:
            IndexError: 索引越界
        """
        if not 0 <= index < self._size:
            raise IndexError('Index out of range')
        return self._data[index]
    
    def __setitem__(self, index, value):
        """设置索引位置的元素
        
        Args:
            index: 索引
            value: 新值
            
        Raises:
            IndexError: 索引越界
        """
        if not 0 <= index < self._size:
            raise IndexError('Index out of range')
        self._data[index] = value
    
    def append(self, value):
        """在末尾添加元素
        
        Args:
            value: 要添加的元素
        """
        if self._size == self._capacity:
            self._resize(2 * self._capacity)  # 扩容2倍
        self._data[self._size] = value
        self._size += 1
    
    def insert(self, index, value):
        """在指定位置插入元素
        
        Args:
            index: 插入位置
            value: 要插入的元素
            
        Raises:
            IndexError: 索引越界
        """
        if not 0 <= index <= self._size:
            raise IndexError('Index out of range')
        
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        
        # 后移元素
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        
        self._data[index] = value
        self._size += 1
    
    def remove(self, value):
        """删除第一个匹配的元素
        
        Args:
            value: 要删除的元素
            
        Raises:
            ValueError: 元素不存在
        """
        for i in range(self._size):
            if self._data[i] == value:
                self.pop(i)
                return
        raise ValueError(f'{value} not in array')
    
    def pop(self, index=None):
        """删除并返回指定位置的元素
        
        Args:
            index: 索引，默认为末尾
            
        Returns:
            被删除的元素
            
        Raises:
            IndexError: 索引越界或数组为空
        """
        if self._size == 0:
            raise IndexError('pop from empty array')
        
        if index is None:
            index = self._size - 1
        
        if not 0 <= index < self._size:
            raise IndexError('Index out of range')
        
        value = self._data[index]
        
        # 前移元素
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        
        self._data[self._size - 1] = None
        self._size -= 1
        
        # 缩容：当元素数量为容量的1/4时，缩容为1/2
        if self._size > 0 and self._size == self._capacity // 4:
            self._resize(self._capacity // 2)
        
        return value
    
    def _resize(self, new_capacity):
        """调整容量
        
        Args:
            new_capacity: 新容量
        """
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
    
    def index(self, value):
        """查找元素的索引
        
        Args:
            value: 要查找的元素
            
        Returns:
            元素索引
            
        Raises:
            ValueError: 元素不存在
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError(f'{value} not in array')
    
    def is_empty(self):
        """判断数组是否为空"""
        return self._size == 0
    
    def clear(self):
        """清空数组"""
        self._data = [None] * 4
        self._size = 0
        self._capacity = 4
    
    def __str__(self):
        """字符串表示"""
        return '[' + ', '.join(str(self._data[i]) for i in range(self._size)) + ']'
    
    def __repr__(self):
        """调试表示"""
        return f'DynamicArray({list(self._data[i] for i in range(self._size))})'


def demo():
    """演示动态数组的使用"""
    print("=== 动态数组演示 ===\n")
    
    # 创建数组
    arr = DynamicArray()
    print(f"创建空数组: {arr}")
    print(f"容量: {arr._capacity}, 大小: {len(arr)}\n")
    
    # 添加元素
    print("添加元素: 1, 2, 3, 4, 5")
    for i in range(1, 6):
        arr.append(i)
    print(f"数组: {arr}")
    print(f"容量: {arr._capacity}, 大小: {len(arr)}\n")
    
    # 继续添加触发扩容
    print("继续添加元素: 6, 7, 8")
    for i in range(6, 9):
        arr.append(i)
    print(f"数组: {arr}")
    print(f"容量: {arr._capacity}, 大小: {len(arr)}\n")
    
    # 访问元素
    print(f"访问索引2: {arr[2]}")
    print(f"修改索引2为99")
    arr[2] = 99
    print(f"数组: {arr}\n")
    
    # 插入元素
    print("在索引0插入100")
    arr.insert(0, 100)
    print(f"数组: {arr}\n")
    
    # 删除元素
    print("删除末尾元素")
    removed = arr.pop()
    print(f"删除的元素: {removed}")
    print(f"数组: {arr}\n")
    
    # 查找元素
    print(f"查找元素99的索引: {arr.index(99)}\n")
    
    # 删除多个元素触发缩容
    print("删除多个元素...")
    for _ in range(5):
        arr.pop()
    print(f"数组: {arr}")
    print(f"容量: {arr._capacity}, 大小: {len(arr)}")


if __name__ == '__main__':
    demo()

