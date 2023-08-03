# 02-two-pointers (双指针)

LeetCode精选75题 - 双指针专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 盛最多水的容器 | ⭐⭐ | [11](https://leetcode.cn/problems/container-with-most-water/) | [01-container-with-most-water.py](./01-container-with-most-water.py) | [01-container-with-most-water.cpp](./01-container-with-most-water.cpp) |
| 02 | 最接近的三数之和 | ⭐⭐ | [16](https://leetcode.cn/problems/3sum-closest/) | [02-three-sum-closest.py](./02-three-sum-closest.py) | [02-three-sum-closest.cpp](./02-three-sum-closest.cpp) |
| 03 | 删除排序数组中的重复项 | ⭐ | [26](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/) | [03-remove-duplicates.py](./03-remove-duplicates.py) | [03-remove-duplicates.cpp](./03-remove-duplicates.cpp) |
| 04 | 移除元素 | ⭐ | [27](https://leetcode.cn/problems/remove-element/) | [04-remove-element.py](./04-remove-element.py) | [04-remove-element.cpp](./04-remove-element.cpp) |
| 05 | 移动零 | ⭐ | [283](https://leetcode.cn/problems/move-zeroes/) | [05-move-zeroes.py](./05-move-zeroes.py) | [05-move-zeroes.cpp](./05-move-zeroes.cpp) |
| 06 | 颜色分类 | ⭐⭐ | [75](https://leetcode.cn/problems/sort-colors/) | [06-sort-colors.py](./06-sort-colors.py) | [06-sort-colors.cpp](./06-sort-colors.cpp) |

## 🎯 核心技巧

### 对撞指针
- **[盛最多水的容器](./01-container-with-most-water.py)**：从两端向中间移动，贪心选择
- **[最接近的三数之和](./02-three-sum-closest.py)**：固定一个数，双指针找最接近目标的两数

### 快慢指针
- **[删除重复项](./03-remove-duplicates.py)**：慢指针记录位置，快指针遍历
- **[移除元素](./04-remove-element.py)**：原地删除，双指针覆盖
- **[移动零](./05-move-zeroes.py)**：将非零元素前移，剩余位置填零

### 三指针
- **[颜色分类](./06-sort-colors.py)**：三指针分区（荷兰国旗问题）

---

## 💡 解题模板

### 对撞指针模板
```python
def two_pointers(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        # 根据条件移动指针
        if condition:
            left += 1
        else:
            right -= 1
    
    return result
```

### 快慢指针模板
```python
def fast_slow_pointers(nums):
    slow = 0
    
    for fast in range(len(nums)):
        if condition:
            nums[slow] = nums[fast]
            slow += 1
    
    return slow
```

### 三指针模板
```python
def three_pointers(nums):
    left = 0
    right = len(nums) - 1
    current = 0
    
    while current <= right:
        if nums[current] == 0:
            nums[left], nums[current] = nums[current], nums[left]
            left += 1
            current += 1
        elif nums[current] == 2:
            nums[right], nums[current] = nums[current], nums[right]
            right -= 1
        else:
            current += 1
```

---

## 📚 学习重点

1. **对撞指针**：有序数组的经典技巧，从两端向中间移动
2. **快慢指针**：原地修改数组，一个记录位置一个遍历
3. **三指针**：多分区问题，如荷兰国旗问题
4. **贪心思想**：在双指针中经常用到贪心策略
