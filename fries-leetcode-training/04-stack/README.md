# 04-stack (栈)

LeetCode精选75题 - 栈专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 有效的括号 | ⭐ | [20](https://leetcode.cn/problems/valid-parentheses/) | [01-valid-parentheses.py](./01-valid-parentheses.py) | [01-valid-parentheses.cpp](./01-valid-parentheses.cpp) |
| 02 | 最小栈 | ⭐ | [155](https://leetcode.cn/problems/min-stack/) | [02-min-stack.py](./02-min-stack.py) | [02-min-stack.cpp](./02-min-stack.cpp) |
| 03 | 每日温度 | ⭐⭐ | [739](https://leetcode.cn/problems/daily-temperatures/) | [03-daily-temperatures.py](./03-daily-temperatures.py) | [03-daily-temperatures.cpp](./03-daily-temperatures.cpp) |
| 04 | 下一个更大元素I | ⭐ | [496](https://leetcode.cn/problems/next-greater-element-i/) | [04-next-greater-element-i.py](./04-next-greater-element-i.py) | [04-next-greater-element-i.cpp](./04-next-greater-element-i.cpp) |
| 05 | 下一个更大元素II | ⭐⭐ | [503](https://leetcode.cn/problems/next-greater-element-ii/) | [05-next-greater-element-ii.py](./05-next-greater-element-ii.py) | [05-next-greater-element-ii.cpp](./05-next-greater-element-ii.cpp) |
| 06 | 柱状图中最大的矩形 | ⭐⭐⭐ | [84](https://leetcode.cn/problems/largest-rectangle-in-histogram/) | [06-largest-rectangle-in-histogram.py](./06-largest-rectangle-in-histogram.py) | [06-largest-rectangle-in-histogram.cpp](./06-largest-rectangle-in-histogram.cpp) |
| 07 | 接雨水 | ⭐⭐⭐ | [42](https://leetcode.cn/problems/trapping-rain-water/) | [07-trapping-rain-water.py](./07-trapping-rain-water.py) | [07-trapping-rain-water.cpp](./07-trapping-rain-water.cpp) |

## 🎯 核心技巧

### 单调栈
- **[每日温度](./03-daily-temperatures.py)**：维护递减栈，找下一个更大元素
- **[下一个更大元素I](./04-next-greater-element-i.py)**：单调栈 + 哈希表
- **[下一个更大元素II](./05-next-greater-element-ii.py)**：循环数组，栈中存储索引
- **[柱状图中最大的矩形](./06-largest-rectangle-in-histogram.py)**：维护递增栈，计算面积

### 栈的基本应用
- **[有效的括号](./01-valid-parentheses.py)**：栈的经典应用，匹配问题
- **[最小栈](./02-min-stack.py)**：辅助栈维护最小值
- **[接雨水](./07-trapping-rain-water.py)**：单调栈或双指针

---

## 💡 解题模板

### 单调栈模板
```python
def monotonic_stack(nums):
    stack = []
    result = []
    
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            index = stack.pop()
            result[index] = num
        stack.append(i)
    
    return result
```

### 有效括号模板
```python
def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack
```

### 接雨水模板
```python
def trap(height):
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            width = i - stack[-1] - 1
            water_height = min(height[stack[-1]], h) - height[bottom]
            water += width * water_height
        stack.append(i)
    
    return water
```

---

## 📚 学习重点

1. **单调栈**：维护栈内元素单调性，解决"下一个更大/更小元素"问题
2. **栈的基本操作**：入栈、出栈、查看栈顶
3. **辅助栈**：用额外空间优化某些操作
4. **循环数组**：通过取模或重复数组处理循环问题
