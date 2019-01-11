# 01-数组与链表

## 💡 核心结论

### 数组
- **内存**：连续内存空间，固定大小或动态扩容
- **访问**：O(1)随机访问任意元素
- **插入删除**：O(n)需要移动元素，末尾操作O(1)
- **扩容**：通常2倍扩容，摊还复杂度O(1)
- **适用**：读多写少、需要随机访问

### 链表
- **内存**：离散内存空间，动态分配
- **访问**：O(n)只能顺序访问
- **插入删除**：O(1)已知位置直接操作，查找位置O(n)
- **无需扩容**：动态增长，无容量限制
- **适用**：频繁插入删除、不需随机访问

### 关键对比
| 特性 | 数组 | 链表 |
|------|------|------|
| 内存 | 连续 | 分散 |
| 访问 | O(1) | O(n) |
| 插入删除 | O(n) | O(1)* |
| 缓存友好 | ✅ | ❌ |
| 内存开销 | 低 | 高（额外指针） |

*已知位置

## 🎯 数组（Array）

### 特点
- 连续内存空间
- 支持随机访问 O(1)
- 插入删除 O(n)
- 固定大小（静态数组）或动态扩容（动态数组）

### 动态数组实现
- 初始容量
- 自动扩容（通常2倍）
- 缩容策略

### 时间复杂度
| 操作 | 平均 | 最坏 |
|------|------|------|
| 访问 | O(1) | O(1) |
| 查找 | O(n) | O(n) |
| 插入 | O(n) | O(n) |
| 删除 | O(n) | O(n) |
| 末尾插入 | O(1)* | O(n) |

*摊还复杂度

## 🔗 链表（Linked List）

### 单链表
```
head -> [data|next] -> [data|next] -> [data|next] -> null
```

特点：
- 单向遍历
- O(1)头部插入删除
- O(n)查找

### 双链表
```
null <- [prev|data|next] <-> [prev|data|next] <-> [prev|data|next] -> null
```

特点：
- 双向遍历
- O(1)头尾插入删除
- O(n)查找

### 循环链表
```
    ┌──────────────────────────┐
    ↓                          ↑
[data|next] -> [data|next] -> [data|next]
```

特点：
- 尾节点指向头节点
- 适合循环遍历

### 时间复杂度
| 操作 | 平均 | 最坏 |
|------|------|------|
| 访问 | O(n) | O(n) |
| 查找 | O(n) | O(n) |
| 插入（已知位置） | O(1) | O(1) |
| 删除（已知位置） | O(1) | O(1) |
| 插入（需查找） | O(n) | O(n) |
| 删除（需查找） | O(n) | O(n) |

## ⚖️ 数组 vs 链表

| 特性 | 数组 | 链表 |
|------|------|------|
| 内存 | 连续 | 分散 |
| 大小 | 固定或扩容 | 动态 |
| 访问 | O(1) 随机访问 | O(n) 顺序访问 |
| 插入删除 | O(n) | O(1) |
| 空间利用 | 紧凑 | 额外指针开销 |
| 缓存友好 | 是 | 否 |

## 🔧 应用场景

### 数组适用于
- 需要随机访问
- 数据量固定或变化不大
- 读多写少

### 链表适用于
- 频繁插入删除
- 不知道数据规模
- 不需要随机访问

## 💡 实战技巧

### 快慢指针
```python
# 找链表中点
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# 检测环
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### 反转链表
```python
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
```

### 合并有序链表
```python
def merge_lists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    
    while l1 and l2:
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    
    curr.next = l1 or l2
    return dummy.next
```

## 📚 LeetCode练习

### 数组
- [27. Remove Element](https://leetcode.com/problems/remove-element/)
- [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
- [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/)

### 链表
- [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)
- [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)
- [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)
- [876. Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)
- [234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)

## 🎯 实现要点

### Python实现
- 使用列表实现动态数组
- 自定义ListNode类
- 利用Python的垃圾回收

### C++实现
- 手动内存管理
- 使用指针和引用
- 注意内存泄漏
- 实现析构函数

## 📊 性能分析

### 数组扩容策略
```
容量翻倍：
初始: 4
扩容: 4 -> 8 -> 16 -> 32 -> 64
总拷贝: 4 + 8 + 16 + 32 = 60
插入64个元素，平均每次拷贝 < 1
摊还复杂度: O(1)
```

### 链表vs数组实测
```
操作10000次：
- 数组随机访问: 0.001s
- 链表顺序访问: 0.1s

- 数组末尾插入: 0.01s
- 链表头部插入: 0.005s

- 数组中间插入: 1s
- 链表已知位置插入: 0.001s
```

## 💡 最佳实践

1. **选择合适的数据结构**
   - 需要频繁随机访问 → 数组
   - 需要频繁插入删除 → 链表

2. **内存管理**
   - C++必须手动delete
   - Python自动垃圾回收
   - 注意循环引用

3. **边界条件**
   - 空链表
   - 单节点
   - 头尾操作

4. **代码优化**
   - 使用哨兵节点简化逻辑
   - 避免重复遍历
   - 注意指针空判断

