# 06-贪心算法

## 💡 核心结论

### 贪心本质
- **定义**：每步选择当前最优，期望全局最优
- **关键**：局部最优 → 全局最优（需要证明）
- **vs DP**：贪心不回头，DP考虑所有可能
- **难点**：如何证明贪心策略正确
- **应用**：区间调度、哈夫曼编码、最小生成树

### 贪心 vs 动态规划
| 特性 | 贪心 | 动态规划 |
|------|------|----------|
| 决策 | 当前最优 | 全局最优 |
| 回溯 | 不回溯 | 可回溯 |
| 子问题 | 无重叠 | 有重叠 |
| 时间 | 通常O(n log n) | O(n²)或更高 |
| 正确性 | 需要证明 | 一定正确 |

### 贪心策略
1. **排序**：按某种规则排序后贪心选择
2. **优先队列**：每次选择最优元素
3. **局部最优**：证明局部最优能导致全局最优

### 经典问题
- **区间调度**：按结束时间排序
- **跳跃游戏**：维护最远距离
- **加油站**：从能到达最远的开始
- **分配问题**：排序后贪心分配

## 🎯 经典贪心问题

### 1. 区间调度
```python
def interval_scheduling(intervals):
    """最多不重叠区间数"""
    if not intervals:
        return 0
    
    # 按结束时间排序
    intervals.sort(key=lambda x: x[1])
    
    count = 1
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] >= end:
            count += 1
            end = intervals[i][1]
    
    return count
```

### 2. 跳跃游戏
```python
def can_jump(nums):
    """能否跳到最后"""
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True

def jump(nums):
    """最少跳跃次数"""
    jumps = 0
    curr_end = 0
    max_reach = 0
    
    for i in range(len(nums) - 1):
        max_reach = max(max_reach, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = max_reach
    
    return jumps
```

### 3. 分配饼干
```python
def find_content_children(g, s):
    """g:孩子胃口 s:饼干大小"""
    g.sort()
    s.sort()
    
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    
    return child
```

## 📚 LeetCode练习

- [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
- [55. Jump Game](https://leetcode.com/problems/jump-game/)
- [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/)
- [455. Assign Cookies](https://leetcode.com/problems/assign-cookies/)
- [122. Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)


## 💻 完整代码实现

### Python 实现

```{literalinclude} greedy.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} greedy.cpp
:language: cpp
:linenos:
```

