# 09-DP进阶

## 💡 核心结论

### DP进阶问题特点
- **双串问题**：两个字符串/数组的DP
- **状态复杂**：需要多维状态表示
- **优化技巧**：降维、滚动数组、状态压缩
- **经典问题**：LCS、编辑距离、股票、打家劫舍变种

### 经典DP问题分类
| 类型 | 代表问题 | 状态 | 时间 |
|------|----------|------|------|
| 线性DP | LIS | dp[i] | O(n²) |
| 双串DP | LCS、编辑距离 | dp[i][j] | O(mn) |
| 区间DP | 最长回文子串 | dp[i][j] | O(n²) |
| 树形DP | 打家劫舍III | dp[node] | O(n) |
| 状态机DP | 股票问题 | dp[i][k][s] | O(nk) |

## 🎯 最长公共子序列（LCS）

### 问题
找两个字符串的最长公共子序列长度

### 状态定义
```
dp[i][j] = text1[0:i]和text2[0:j]的LCS长度
```

### 状态转移
```python
if text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

### 实现
```python
def longest_common_subsequence(text1, text2):
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

## ✏️ 编辑距离

### 问题
将word1转换为word2的最少操作数（插入、删除、替换）

### 状态定义
```
dp[i][j] = word1[0:i]转换为word2[0:j]的最少操作数
```

### 状态转移
```python
if word1[i-1] == word2[j-1]:
    dp[i][j] = dp[i-1][j-1]  # 不需要操作
else:
    dp[i][j] = 1 + min(
        dp[i-1][j],    # 删除
        dp[i][j-1],    # 插入
        dp[i-1][j-1]   # 替换
    )
```

### 实现
```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # 状态转移
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # 删除
                    dp[i][j-1],    # 插入
                    dp[i-1][j-1]   # 替换
                )
    
    return dp[m][n]
```

## 💰 股票问题系列

### 买卖一次
```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return max_profit
```

### 买卖多次
```python
def max_profit_unlimited(prices):
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit
```

### 买卖k次（通用解法）
```python
def max_profit_k(k, prices):
    if not prices:
        return 0
    
    n = len(prices)
    if k >= n // 2:
        return max_profit_unlimited(prices)
    
    # dp[i][k][0/1] = 第i天，最多k次交易，持有/不持有
    dp = [[[0, 0] for _ in range(k + 1)] for _ in range(n)]
    
    for i in range(n):
        for j in range(k, 0, -1):
            if i == 0:
                dp[i][j][0] = 0
                dp[i][j][1] = -prices[i]
            else:
                dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1] + prices[i])
                dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j-1][0] - prices[i])
    
    return dp[n-1][k][0]
```

## 🏠 打家劫舍变种

### 打家劫舍II（环形）
```python
def rob_circular(nums):
    if len(nums) == 1:
        return nums[0]
    
    def rob_range(nums, start, end):
        prev, curr = 0, 0
        for i in range(start, end):
            prev, curr = curr, max(curr, prev + nums[i])
        return curr
    
    # 分两种情况：偷第一个或不偷
    return max(
        rob_range(nums, 0, len(nums) - 1),  # 不偷最后一个
        rob_range(nums, 1, len(nums))       # 不偷第一个
    )
```

### 打家劫舍III（二叉树）
```python
def rob_tree(root):
    def dfs(node):
        if not node:
            return 0, 0
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # 偷当前节点
        rob_curr = node.val + left[1] + right[1]
        # 不偷当前节点
        not_rob = max(left) + max(right)
        
        return rob_curr, not_rob
    
    return max(dfs(root))
```

## 📚 LeetCode练习

### LCS变种
- [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/)
- [583. Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/)

### 编辑距离
- [72. Edit Distance](https://leetcode.com/problems/edit-distance/)
- [115. Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/)

### 股票问题
- [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
- [122. Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)
- [188. Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

### 打家劫舍
- [198. House Robber](https://leetcode.com/problems/house-robber/)
- [213. House Robber II](https://leetcode.com/problems/house-robber-ii/)
- [337. House Robber III](https://leetcode.com/problems/house-robber-iii/)


## 💻 完整代码实现

### Python 实现

```{literalinclude} dp_advanced.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} dp_advanced.cpp
:language: cpp
:linenos:
```

