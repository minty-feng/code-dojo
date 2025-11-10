# 08-背包问题

## 💡 核心结论

### 背包问题本质
- **定义**：在容量限制下，选择物品使价值最大
- **核心**：动态规划的经典应用
- **关键**：每个物品选或不选，累积最优解
- **难点**：状态定义、空间优化
- **应用**：资源分配、项目选择、切割问题

### 三种背包对比
| 类型 | 特点 | 状态转移 | 遍历顺序 |
|------|------|----------|----------|
| 0-1背包 | 每个物品最多1个 | max(不选, 选) | 逆序 |
| 完全背包 | 每个物品无限个 | max(不选, 选) | 正序 |
| 多重背包 | 每个物品k个 | 二进制优化 | - |

### 0-1背包核心
```
状态：dp[i][j] = 前i个物品，容量j的最大价值
转移：dp[i][j] = max(
    dp[i-1][j],              # 不选第i个
    dp[i-1][j-w[i]] + v[i]   # 选第i个
)
空间优化：一维数组，逆序遍历
```

### 完全背包核心
```
状态：dp[i][j] = 前i种物品，容量j的最大价值  
转移：dp[i][j] = max(
    dp[i-1][j],          # 不选第i种
    dp[i][j-w[i]] + v[i] # 选第i种（注意是dp[i]不是dp[i-1]）
)
空间优化：一维数组，正序遍历
```

## 🎯 0-1背包

### 二维DP
```python
def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(capacity + 1):
            if j < weights[i-1]:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(
                    dp[i-1][j],
                    dp[i-1][j - weights[i-1]] + values[i-1]
                )
    
    return dp[n][capacity]
```

### 一维DP（空间优化）
```python
def knapsack_01_optimized(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # 逆序遍历（避免物品被重复选择）
        for j in range(capacity, weights[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[capacity]
```

## 🔄 完全背包

### 一维DP
```python
def knapsack_complete(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # 正序遍历（允许物品被重复选择）
        for j in range(weights[i], capacity + 1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[capacity]
```

## 🎁 多重背包

### 二进制优化
```python
def knapsack_multiple(weights, values, counts, capacity):
    # 转换为0-1背包
    new_weights = []
    new_values = []
    
    for i in range(len(weights)):
        k = 1
        while k <= counts[i]:
            new_weights.append(weights[i] * k)
            new_values.append(values[i] * k)
            counts[i] -= k
            k *= 2
        if counts[i] > 0:
            new_weights.append(weights[i] * counts[i])
            new_values.append(values[i] * counts[i])
    
    return knapsack_01_optimized(new_weights, new_values, capacity)
```

## 🎯 背包变种

### 1. 恰好装满
```python
# 初始化
dp = [-inf] * (capacity + 1)
dp[0] = 0  # 容量0价值0
```

### 2. 求方案数
```python
# 状态：dp[i] = 容量i的方案数
dp[j] += dp[j - weight[i]]  # 累加方案数
```

### 3. 求具体方案
```python
# 记录选择
choice = [[False] * (capacity + 1) for _ in range(n + 1)]

# 回溯方案
result = []
j = capacity
for i in range(n, 0, -1):
    if choice[i][j]:
        result.append(i - 1)
        j -= weights[i - 1]
```

## 📚 LeetCode练习

### 0-1背包
- [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)
- [474. Ones and Zeroes](https://leetcode.com/problems/ones-and-zeroes/)
- [494. Target Sum](https://leetcode.com/problems/target-sum/)

### 完全背包
- [322. Coin Change](https://leetcode.com/problems/coin-change/)
- [518. Coin Change 2](https://leetcode.com/problems/coin-change-2/)
- [279. Perfect Squares](https://leetcode.com/problems/perfect-squares/)

## 💡 解题模板

### 0-1背包模板
```python
dp = [0] * (capacity + 1)
for i in range(n):
    for j in range(capacity, weights[i] - 1, -1):
        dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
return dp[capacity]
```

### 完全背包模板
```python
dp = [0] * (capacity + 1)
for i in range(n):
    for j in range(weights[i], capacity + 1):
        dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
return dp[capacity]
```

## 🎯 关键区别

**0-1背包 vs 完全背包唯一区别**：
- 0-1：`for j in range(capacity, w-1, -1)` 逆序
- 完全：`for j in range(w, capacity+1)` 正序

**为什么？**
- 逆序：保证每个物品只用一次
- 正序：允许物品重复使用


## 💻 完整代码实现

### Python 实现

```{literalinclude} knapsack.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} knapsack.cpp
:language: cpp
:linenos:
```

