# 03-哈希表

## 💡 核心结论

### 哈希表本质
- **原理**：通过哈希函数将key映射到数组索引，O(1)访问
- **性能**：平均O(1)查找/插入/删除，最坏O(n)
- **核心**：好的哈希函数 + 合适的冲突解决 = 高性能
- **负载因子**：α = n/m，α < 0.75性能良好，超过需扩容
- **应用**：缓存、去重、计数、索引

### 冲突解决
- **链地址法**：每个槽位存链表，简单但指针开销大
- **开放寻址**：线性探测/二次探测/双重哈希，缓存友好但聚集问题
- **选择**：链地址法更常用（Java HashMap、Python dict）

### 哈希函数要求
1. **确定性**：相同输入→相同输出
2. **均匀分布**：减少冲突
3. **快速计算**：保证O(1)
4. **雪崩效应**：输入微变化→输出巨变

### 性能关键
| 因素 | 影响 |
|------|------|
| 好的哈希函数 | 减少冲突 |
| 低负载因子 | 减少冲突 |
| 合理扩容 | 保持性能 |
| 冲突解决方法 | 最坏情况性能 |

## 🎯 哈希表原理

### 核心思想
通过哈希函数将key映射到数组索引，实现O(1)的查找、插入、删除。

```
key --[hash function]--> index --> value
"John" --> 哈希 --> 5 --> {name: "John", age: 30}
```

### 时间复杂度
| 操作 | 平均 | 最坏 |
|------|------|------|
| 查找 | O(1) | O(n) |
| 插入 | O(1) | O(n) |
| 删除 | O(1) | O(n) |

## 🔑 哈希函数

### 好的哈希函数特点
1. 确定性：相同输入产生相同输出
2. 快速计算
3. 均匀分布
4. 雪崩效应：输入微小变化导致输出巨大变化

### 常见哈希函数
```python
# 除法哈希
def hash_division(key, table_size):
    return key % table_size

# 乘法哈希
def hash_multiplication(key, table_size):
    A = 0.6180339887  # (√5 - 1) / 2
    return int(table_size * ((key * A) % 1))

# 字符串哈希
def hash_string(s, table_size):
    hash_val = 0
    for char in s:
        hash_val = (hash_val * 31 + ord(char)) % table_size
    return hash_val
```

## 💥 冲突解决

### 1. 链地址法（Chaining）
```
Index | Linked List
------|-------------
  0   | -> key1 -> key5
  1   | -> key2
  2   | (empty)
  3   | -> key3 -> key6 -> key8
  4   | -> key4
```

优点：
- 实现简单
- 对哈希函数要求低
- 负载因子可以>1

缺点：
- 额外指针开销
- 缓存性能差

### 2. 开放寻址法（Open Addressing）

#### 线性探测
```
hash(key) = h
探测序列: h, h+1, h+2, h+3, ...
```

优点：缓存友好
缺点：聚集问题

#### 二次探测
```
探测序列: h, h+1², h+2², h+3², ...
```

#### 双重哈希
```
h1(key) = key % m
h2(key) = 1 + (key % (m-1))
探测序列: h1, h1+h2, h1+2h2, h1+3h2, ...
```

## 📊 负载因子

```
负载因子 α = n / m
n: 已存储元素数
m: 哈希表大小

链地址法：α < 1.0 性能良好
开放寻址：α < 0.7 性能良好

扩容触发：α > 0.75（Java HashMap）
```

## 🔧 动态扩容

### 扩容策略
1. 创建新表（通常2倍大小）
2. 重新哈希所有元素（rehash）
3. 替换旧表

### Rehash过程
```python
def resize(self):
    old_table = self.table
    self.capacity *= 2
    self.table = [[] for _ in range(self.capacity)]
    self.size = 0
    
    for bucket in old_table:
        for key, value in bucket:
            self.insert(key, value)
```

## 💡 应用场景

### 缓存
- LRU缓存
- Redis
- Memcached

### 数据库索引
- Hash索引
- 快速查找

### 去重
- 统计不重复元素
- 集合运算

### 计数
- 词频统计
- 投票系统

## 📚 LeetCode练习

- [1. Two Sum](https://leetcode.com/problems/two-sum/)
- [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- [146. LRU Cache](https://leetcode.com/problems/lru-cache/)
- [387. First Unique Character](https://leetcode.com/problems/first-unique-character-in-a-string/)

