"""
哈希表实现（链地址法）
"""

class HashTable:
    """哈希表实现"""
    
    def __init__(self, capacity=16):
        """初始化
        
        Args:
            capacity: 初始容量
        """
        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(capacity)]
        self.load_factor_threshold = 0.75
    
    def _hash(self, key):
        """哈希函数
        
        Args:
            key: 键（支持字符串和整数）
            
        Returns:
            哈希值
        """
        if isinstance(key, str):
            hash_val = 0
            for char in key:
                hash_val = (hash_val * 31 + ord(char)) % self.capacity
            return hash_val
        else:
            return hash(key) % self.capacity
    
    def _resize(self):
        """扩容并重新哈希"""
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)
    
    def insert(self, key, value):
        """插入键值对
        
        Args:
            key: 键
            value: 值
        """
        # 检查是否需要扩容
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()
        
        index = self._hash(key)
        bucket = self.table[index]
        
        # 更新已存在的key
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # 插入新key
        bucket.append((key, value))
        self.size += 1
    
    def get(self, key):
        """获取值
        
        Args:
            key: 键
            
        Returns:
            值
            
        Raises:
            KeyError: 键不存在
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(f'Key {key} not found')
    
    def remove(self, key):
        """删除键值对
        
        Args:
            key: 键
            
        Raises:
            KeyError: 键不存在
        """
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return
        
        raise KeyError(f'Key {key} not found')
    
    def contains(self, key):
        """检查键是否存在
        
        Args:
            key: 键
            
        Returns:
            bool
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def keys(self):
        """返回所有键"""
        result = []
        for bucket in self.table:
            for k, v in bucket:
                result.append(k)
        return result
    
    def values(self):
        """返回所有值"""
        result = []
        for bucket in self.table:
            for k, v in bucket:
                result.append(v)
        return result
    
    def items(self):
        """返回所有键值对"""
        result = []
        for bucket in self.table:
            for item in bucket:
                result.append(item)
        return result
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        items = [f"{k}: {v}" for k, v in self.items()]
        return "{" + ", ".join(items) + "}"


def demo():
    """演示哈希表的使用"""
    print("=== 哈希表演示 ===\n")
    
    ht = HashTable(4)
    
    # 插入
    print("插入键值对:")
    ht.insert("apple", 5)
    print(f"  apple: 5")
    ht.insert("banana", 3)
    print(f"  banana: 3")
    ht.insert("orange", 7)
    print(f"  orange: 7")
    
    print(f"\n哈希表: {ht}")
    print(f"大小: {len(ht)}, 容量: {ht.capacity}\n")
    
    # 查找
    print(f"查找 'apple': {ht.get('apple')}")
    print(f"包含 'grape': {ht.contains('grape')}\n")
    
    # 更新
    print("更新 'apple' 为 10")
    ht.insert("apple", 10)
    print(f"哈希表: {ht}\n")
    
    # 继续插入触发扩容
    print("继续插入触发扩容:")
    ht.insert("grape", 8)
    ht.insert("melon", 6)
    print(f"哈希表: {ht}")
    print(f"大小: {len(ht)}, 容量: {ht.capacity}\n")
    
    # 删除
    print("删除 'banana'")
    ht.remove("banana")
    print(f"哈希表: {ht}\n")
    
    # 遍历
    print("所有键:", ht.keys())
    print("所有值:", ht.values())


if __name__ == '__main__':
    demo()

