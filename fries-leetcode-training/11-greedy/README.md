# 11-greedy (贪心)

LeetCode精选75题 - 贪心专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 买卖股票的最佳时机 | ⭐ | [121](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/) | [01-best-time-to-buy-and-sell-stock.py](./01-best-time-to-buy-and-sell-stock.py) | [01-best-time-to-buy-and-sell-stock.cpp](./01-best-time-to-buy-and-sell-stock.cpp) |
| 02 | 跳跃游戏 | ⭐⭐ | [55](https://leetcode.cn/problems/jump-game/) | [02-jump-game.py](./02-jump-game.py) | [02-jump-game.cpp](./02-jump-game.cpp) |
| 03 | 跳跃游戏II | ⭐⭐ | [45](https://leetcode.cn/problems/jump-game-ii/) | [03-jump-game-ii.py](./03-jump-game-ii.py) | [03-jump-game-ii.cpp](./03-jump-game-ii.cpp) |
| 04 | 加油站 | ⭐⭐ | [134](https://leetcode.cn/problems/gas-station/) | [04-gas-station.py](./04-gas-station.py) | [04-gas-station.cpp](./04-gas-station.cpp) |
| 05 | 分发糖果 | ⭐⭐⭐ | [135](https://leetcode.cn/problems/candy/) | [05-candy.py](./05-candy.py) | [05-candy.cpp](./05-candy.cpp) |
| 06 | 无重叠区间 | ⭐⭐ | [435](https://leetcode.cn/problems/non-overlapping-intervals/) | [06-non-overlapping-intervals.py](./06-non-overlapping-intervals.py) | [06-non-overlapping-intervals.cpp](./06-non-overlapping-intervals.cpp) |
| 07 | 用最少数量的箭引爆气球 | ⭐⭐ | [452](https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/) | [07-minimum-number-of-arrows-to-burst-balloons.py](./07-minimum-number-of-arrows-to-burst-balloons.py) | [07-minimum-number-of-arrows-to-burst-balloons.cpp](./07-minimum-number-of-arrows-to-burst-balloons.cpp) |

## 🎯 核心技巧

### 区间问题
- **[无重叠区间](./06-non-overlapping-intervals.py)**：按结束时间排序
- **[用最少数量的箭引爆气球](./07-minimum-number-of-arrows-to-burst-balloons.py)**：区间重叠问题

### 跳跃问题
- **[跳跃游戏](./02-jump-game.py)**：维护最远可达距离
- **[跳跃游戏II](./03-jump-game-ii.py)**：贪心选择最远跳跃

### 其他贪心
- **[买卖股票的最佳时机](./01-best-time-to-buy-and-sell-stock.py)**：维护最低价格
- **[加油站](./04-gas-station.py)**：总油量 >= 总消耗
- **[分发糖果](./05-candy.py)**：左右两次遍历

---

## 💡 解题模板

### 区间贪心模板
```python
def interval_scheduling(intervals):
    intervals.sort(key=lambda x: x[1])  # 按结束时间排序
    
    count = 0
    end = float('-inf')
    
    for start, finish in intervals:
        if start >= end:
            count += 1
            end = finish
    
    return count
```

### 跳跃游戏模板
```python
def can_jump(nums):
    max_reach = 0
    
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    
    return True
```

---

## 📚 学习重点

1. **贪心策略**：局部最优导致全局最优
2. **区间问题**：排序 + 贪心选择
3. **跳跃问题**：维护最远可达距离
4. **证明贪心**：理解为什么贪心策略正确
