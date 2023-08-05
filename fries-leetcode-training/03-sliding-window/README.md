# 03-sliding-window (滑动窗口)

LeetCode精选75题 - 滑动窗口专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 无重复字符的最长子串 | ⭐⭐ | [3](https://leetcode.cn/problems/longest-substring-without-repeating-characters/) | [01-longest-substring-without-repeating.py](./01-longest-substring-without-repeating.py) | [01-longest-substring-without-repeating.cpp](./01-longest-substring-without-repeating.cpp) |
| 02 | 最小覆盖子串 | ⭐⭐⭐ | [76](https://leetcode.cn/problems/minimum-window-substring/) | [02-minimum-window-substring.py](./02-minimum-window-substring.py) | [02-minimum-window-substring.cpp](./02-minimum-window-substring.cpp) |
| 03 | 找到字符串中所有字母异位词 | ⭐⭐ | [438](https://leetcode.cn/problems/find-all-anagrams-in-a-string/) | [03-find-all-anagrams.py](./03-find-all-anagrams.py) | [03-find-all-anagrams.cpp](./03-find-all-anagrams.cpp) |
| 04 | 字符串的排列 | ⭐⭐ | [567](https://leetcode.cn/problems/permutation-in-string/) | [04-permutation-in-string.py](./04-permutation-in-string.py) | [04-permutation-in-string.cpp](./04-permutation-in-string.cpp) |
| 05 | 最大连续1的个数III | ⭐⭐ | [1004](https://leetcode.cn/problems/max-consecutive-ones-iii/) | [05-max-consecutive-ones-iii.py](./05-max-consecutive-ones-iii.py) | [05-max-consecutive-ones-iii.cpp](./05-max-consecutive-ones-iii.cpp) |
| 06 | 水果成篮 | ⭐⭐ | [904](https://leetcode.cn/problems/fruit-into-baskets/) | [06-fruit-into-baskets.py](./06-fruit-into-baskets.py) | [06-fruit-into-baskets.cpp](./06-fruit-into-baskets.cpp) |

## 🎯 核心技巧

### 固定窗口
- **[字符串的排列](./04-permutation-in-string.py)**：窗口大小固定为模式串长度
- **[找到所有字母异位词](./03-find-all-anagrams.py)**：窗口大小固定为目标串长度

### 可变窗口
- **[无重复字符的最长子串](./01-longest-substring-without-repeating.py)**：右指针扩展，左指针收缩
- **[最小覆盖子串](./02-minimum-window-substring.py)**：维护窗口内字符频次
- **[最大连续1的个数III](./05-max-consecutive-ones-iii.py)**：最多翻转k个0
- **[水果成篮](./06-fruit-into-baskets.py)**：最多包含2种水果类型

### 双指针模板
```python
def sliding_window(s):
    left = 0
    for right in range(len(s)):
        # 扩展窗口
        window.add(s[right])
        
        # 收缩窗口
        while condition:
            window.remove(s[left])
            left += 1
        
        # 更新结果
        update_result()
```

---

## 💡 解题模板

### 无重复字符模板
```python
def longest_substring(s):
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

### 最小覆盖子串模板
```python
def min_window(s, t):
    need = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
    
    left = 0
    valid = 0
    window = {}
    
    start = 0
    min_len = float('inf')
    
    for right in range(len(s)):
        c = s[right]
        if c in need:
            window[c] = window.get(c, 0) + 1
            if window[c] == need[c]:
                valid += 1
        
        while valid == len(need):
            if right - left + 1 < min_len:
                start = left
                min_len = right - left + 1
            
            d = s[left]
            left += 1
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1
    
    return s[start:start + min_len] if min_len != float('inf') else ""
```

---

## 📚 学习重点

1. **窗口维护**：左右指针的移动策略
2. **条件判断**：何时扩展，何时收缩
3. **状态更新**：窗口内数据的维护
4. **结果记录**：最优解的保存
