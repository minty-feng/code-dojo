# 05-linked-list (链表)

LeetCode精选75题 - 链表专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 反转链表 | ⭐ | [206](https://leetcode.cn/problems/reverse-linked-list/) | [01-reverse-linked-list.py](./01-reverse-linked-list.py) | [01-reverse-linked-list.cpp](./01-reverse-linked-list.cpp) |
| 02 | 合并两个有序链表 | ⭐ | [21](https://leetcode.cn/problems/merge-two-sorted-lists/) | [02-merge-two-sorted-lists.py](./02-merge-two-sorted-lists.py) | [02-merge-two-sorted-lists.cpp](./02-merge-two-sorted-lists.cpp) |
| 03 | 环形链表 | ⭐ | [141](https://leetcode.cn/problems/linked-list-cycle/) | [03-linked-list-cycle.py](./03-linked-list-cycle.py) | [03-linked-list-cycle.cpp](./03-linked-list-cycle.cpp) |
| 04 | 环形链表II | ⭐⭐ | [142](https://leetcode.cn/problems/linked-list-cycle-ii/) | [04-linked-list-cycle-ii.py](./04-linked-list-cycle-ii.py) | [04-linked-list-cycle-ii.cpp](./04-linked-list-cycle-ii.cpp) |
| 05 | 相交链表 | ⭐ | [160](https://leetcode.cn/problems/intersection-of-two-linked-lists/) | [05-intersection-of-two-linked-lists.py](./05-intersection-of-two-linked-lists.py) | [05-intersection-of-two-linked-lists.cpp](./05-intersection-of-two-linked-lists.cpp) |
| 06 | 回文链表 | ⭐ | [234](https://leetcode.cn/problems/palindrome-linked-list/) | [06-palindrome-linked-list.py](./06-palindrome-linked-list.py) | [06-palindrome-linked-list.cpp](./06-palindrome-linked-list.cpp) |

## 🎯 核心技巧

### 双指针技巧
- **[环形链表](./03-linked-list-cycle.py)**：快慢指针检测环
- **[环形链表II](./04-linked-list-cycle-ii.py)**：Floyd判圈算法找环起点
- **[相交链表](./05-intersection-of-two-linked-lists.py)**：双指针走相同距离
- **[回文链表](./06-palindrome-linked-list.py)**：快慢指针找中点，反转后半部分

### 链表操作
- **[反转链表](./01-reverse-linked-list.py)**：迭代或递归反转
- **[合并两个有序链表](./02-merge-two-sorted-lists.py)**：归并排序思想

---

## 💡 解题模板

### 反转链表模板
```python
def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev
```

### 快慢指针模板
```python
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    
    return False
```

### 合并有序链表模板
```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    current.next = l1 or l2
    return dummy.next
```

---

## 📚 学习重点

1. **双指针**：快慢指针、同速指针的应用
2. **链表反转**：迭代和递归两种方法
3. **环检测**：Floyd判圈算法
4. **虚拟头节点**：简化边界处理
5. **链表合并**：归并排序思想
