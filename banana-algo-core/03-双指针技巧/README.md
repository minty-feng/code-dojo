# 03-双指针技巧

## 💡 核心结论

### 双指针本质
- **定义**：用两个指针遍历，降低时间复杂度
- **核心**：O(n²) → O(n)
- **类型**：对撞指针、快慢指针、滑动窗口
- **适用**：有序数组、链表、字符串
- **关键**：明确每个指针的含义和移动条件

### 三种模式
| 模式 | 特点 | 适用 | 复杂度 |
|------|------|------|--------|
| 对撞指针 | 两端向中间 | 有序数组、回文 | O(n) |
| 快慢指针 | 同向不同速 | 链表环、中点 | O(n) |
| 滑动窗口 | 维护区间 | 子串、子数组 | O(n) |

## 👈👉 对撞指针

### 两数之和II（有序数组）
```python
def two_sum(nums, target):
    left, right = 0, len(nums) - 1
    
    while left < right:
        sum_val = nums[left] + nums[right]
        if sum_val == target:
            return [left, right]
        elif sum_val < target:
            left += 1
        else:
            right -= 1
    
    return []
```

### 三数之和
```python
def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # 去重
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        while left < right:
            sum_val = nums[i] + nums[left] + nums[right]
            if sum_val == 0:
                result.append([nums[i], nums[left], nums[right]])
                # 去重
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif sum_val < 0:
                left += 1
            else:
                right -= 1
    
    return result
```

## 🐢🐰 快慢指针

### 环形链表
```python
def has_cycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False
```

### 链表中点
```python
def find_middle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
```

## 🪟 滑动窗口

### 最长无重复子串
```python
def length_of_longest_substring(s):
    char_set = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

### 滑动窗口模板
```python
def sliding_window(s):
    left = 0
    window = {}  # 维护窗口状态
    result = 0
    
    for right in range(len(s)):
        # 扩大窗口
        c = s[right]
        window[c] = window.get(c, 0) + 1
        
        # 缩小窗口
        while window不满足条件:
            d = s[left]
            left += 1
            window[d] -= 1
        
        # 更新结果
        result = max(result, right - left + 1)
    
    return result
```

## 📚 LeetCode练习

### 对撞指针
- [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [15. 3Sum](https://leetcode.com/problems/3sum/)
- [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

### 快慢指针
- [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)
- [876. Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)
- [202. Happy Number](https://leetcode.com/problems/happy-number/)

### 滑动窗口
- [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
- [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)
- [438. Find All Anagrams](https://leetcode.com/problems/find-all-anagrams-in-a-string/)

