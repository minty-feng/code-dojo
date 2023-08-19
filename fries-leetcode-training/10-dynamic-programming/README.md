# 10-dynamic-programming (动态规划)

LeetCode精选75题 - 动态规划专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 爬楼梯 | ⭐ | [70](https://leetcode.cn/problems/climbing-stairs/) | [01-climbing-stairs.py](./01-climbing-stairs.py) | [01-climbing-stairs.cpp](./01-climbing-stairs.cpp) |
| 02 | 打家劫舍 | ⭐⭐ | [198](https://leetcode.cn/problems/house-robber/) | [02-house-robber.py](./02-house-robber.py) | [02-house-robber.cpp](./02-house-robber.cpp) |
| 03 | 打家劫舍II | ⭐⭐ | [213](https://leetcode.cn/problems/house-robber-ii/) | [03-house-robber-ii.py](./03-house-robber-ii.py) | [03-house-robber-ii.cpp](./03-house-robber-ii.cpp) |
| 04 | 最长递增子序列 | ⭐⭐ | [300](https://leetcode.cn/problems/longest-increasing-subsequence/) | [04-longest-increasing-subsequence.py](./04-longest-increasing-subsequence.py) | [04-longest-increasing-subsequence.cpp](./04-longest-increasing-subsequence.cpp) |
| 05 | 零钱兑换 | ⭐⭐ | [322](https://leetcode.cn/problems/coin-change/) | [05-coin-change.py](./05-coin-change.py) | [05-coin-change.cpp](./05-coin-change.cpp) |
| 06 | 零钱兑换II | ⭐⭐ | [518](https://leetcode.cn/problems/coin-change-2/) | [06-coin-change-2.py](./06-coin-change-2.py) | [06-coin-change-2.cpp](./06-coin-change-2.cpp) |
| 07 | 编辑距离 | ⭐⭐⭐ | [72](https://leetcode.cn/problems/edit-distance/) | [07-edit-distance.py](./07-edit-distance.py) | [07-edit-distance.cpp](./07-edit-distance.cpp) |
| 08 | 最长公共子序列 | ⭐⭐ | [1143](https://leetcode.cn/problems/longest-common-subsequence/) | [08-longest-common-subsequence.py](./08-longest-common-subsequence.py) | [08-longest-common-subsequence.cpp](./08-longest-common-subsequence.cpp) |
| 09 | 乘积最大子数组 | ⭐⭐ | [152](https://leetcode.cn/problems/maximum-product-subarray/) | [09-maximum-product-subarray.py](./09-maximum-product-subarray.py) | [09-maximum-product-subarray.cpp](./09-maximum-product-subarray.cpp) |
| 10 | 最大子数组和 | ⭐ | [53](https://leetcode.cn/problems/maximum-subarray/) | [10-maximum-subarray.py](./10-maximum-subarray.py) | [10-maximum-subarray.cpp](./10-maximum-subarray.cpp) |
| 11 | 买卖股票的最佳时机 | ⭐ | [121](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/) | [11-best-time-to-buy-and-sell-stock.py](./11-best-time-to-buy-and-sell-stock.py) | [11-best-time-to-buy-and-sell-stock.cpp](./11-best-time-to-buy-and-sell-stock.cpp) |
| 12 | 买卖股票的最佳时机II | ⭐⭐ | [122](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/) | [12-best-time-to-buy-and-sell-stock-ii.py](./12-best-time-to-buy-and-sell-stock-ii.py) | [12-best-time-to-buy-and-sell-stock-ii.cpp](./12-best-time-to-buy-and-sell-stock-ii.cpp) |
| 13 | 买卖股票的最佳时机III | ⭐⭐⭐ | [123](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/) | [13-best-time-to-buy-and-sell-stock-iii.py](./13-best-time-to-buy-and-sell-stock-iii.py) | [13-best-time-to-buy-and-sell-stock-iii.cpp](./13-best-time-to-buy-and-sell-stock-iii.cpp) |

## 🎯 核心技巧

### 一维DP
- **[爬楼梯](./01-climbing-stairs.py)**：斐波那契数列
- **[打家劫舍](./02-house-robber.py)**：相邻不能选择
- **[打家劫舍II](./03-house-robber-ii.py)**：环形数组
- **[最长递增子序列](./04-longest-increasing-subsequence.py)**：LIS问题

### 背包问题
- **[零钱兑换](./05-coin-change.py)**：完全背包，最少硬币数
- **[零钱兑换II](./06-coin-change-2.py)**：完全背包，组合数

### 二维DP
- **[编辑距离](./07-edit-distance.py)**：字符串编辑
- **[最长公共子序列](./08-longest-common-subsequence.py)**：LCS问题

### 子数组问题
- **[乘积最大子数组](./09-maximum-product-subarray.py)**：考虑正负号
- **[最大子数组和](./10-maximum-subarray.py)**：Kadane算法

### 股票问题
- **[买卖股票的最佳时机](./11-best-time-to-buy-and-sell-stock.py)**：一次交易
- **[买卖股票的最佳时机II](./12-best-time-to-buy-and-sell-stock-ii.py)**：无限次交易
- **[买卖股票的最佳时机III](./13-best-time-to-buy-and-sell-stock-iii.py)**：最多两次交易

---

## 💡 解题模板

### 一维DP模板
```python
def dp_1d(nums):
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    
    for i in range(1, n):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    return dp[n-1]
```

### 二维DP模板
```python
def dp_2d(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### 背包问题模板
```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## 📚 学习重点

1. **状态定义**：明确dp[i]的含义
2. **状态转移**：找到状态间的关系
3. **边界条件**：初始化dp数组
4. **空间优化**：滚动数组技巧
5. **背包问题**：01背包、完全背包、多重背包
6. **股票问题**：状态机DP
