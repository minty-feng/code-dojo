# 07-动态规划基础

## 💡 核心结论

### 动态规划本质
- **定义**：将复杂问题分解为重叠子问题，存储子问题解避免重复计算
- **核心**：最优子结构 + 重叠子问题 = 动态规划
- **vs递归**：递归重复计算，DP记忆化存储
- **vs贪心**：贪心局部最优，DP考虑所有可能
- **关键**：找状态、写方程、定边界、优化空间

### DP三要素（必须明确）
1. **状态定义**：dp[i]表示什么？
2. **状态转移方程**：dp[i]如何由之前的状态得到？
3. **初始状态**：dp[0]或dp[i][0]是什么？

### 解题步骤
1. **暴力递归**：写出递归解法
2. **记忆化**：加memo避免重复计算
3. **自底向上**：改为DP数组
4. **空间优化**：滚动数组或变量

### DP vs 其他
| 方法 | 适用 | 时间 | 空间 |
|------|------|------|------|
| 暴力 | 数据小 | 指数级 | O(1) |
| 贪心 | 局部最优=全局 | O(n) | O(1) |
| DP | 重叠子问题 | O(n)~O(n³) | O(n)~O(n²) |

## 🎯 经典问题

### 1. 斐波那契数列

#### 递归（指数时间）
```python
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
# 时间：O(2^n) 重复计算
```

#### 记忆化递归
```python
def fib(n, memo={}):
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
# 时间：O(n) 空间：O(n)
```

#### DP数组
```python
def fib(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
# 时间：O(n) 空间：O(n)
```

#### 空间优化
```python
def fib(n):
    if n <= 1: return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
# 时间：O(n) 空间：O(1)
```

### 2. 爬楼梯
```
一次爬1或2级，n级有多少种方法？

状态：dp[i] = 到第i级的方法数
转移：dp[i] = dp[i-1] + dp[i-2]
初始：dp[0]=1, dp[1]=1
```

```python
def climbStairs(n):
    if n <= 1: return 1
    prev, curr = 1, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

### 3. 打家劫舍
```
不能偷相邻房屋，求最大金额

状态：dp[i] = 前i个房屋能偷的最大金额
转移：dp[i] = max(dp[i-1], dp[i-2] + nums[i])
       不偷第i个     偷第i个
```

```python
def rob(nums):
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    
    prev, curr = 0, 0
    for num in nums:
        prev, curr = curr, max(curr, prev + num)
    return curr
```

### 4. 最大子数组和（Kadane算法）
```
状态：dp[i] = 以nums[i]结尾的最大子数组和
转移：dp[i] = max(nums[i], dp[i-1] + nums[i])
```

```python
def maxSubArray(nums):
    max_sum = nums[0]
    curr_sum = nums[0]
    
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    
    return max_sum
```

### 5. 最长递增子序列（LIS）
```
状态：dp[i] = 以nums[i]结尾的最长递增子序列长度
转移：dp[i] = max(dp[j] + 1) for j < i if nums[j] < nums[i]
时间：O(n²)
```

```python
def lengthOfLIS(nums):
    if not nums: return 0
    dp = [1] * len(nums)
    
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

## 🎯 DP解题套路

### 一维DP
```python
# 模板
dp = [0] * (n + 1)
dp[0] = initial_value

for i in range(1, n + 1):
    dp[i] = f(dp[i-1], dp[i-2], ...)

return dp[n]
```

### 二维DP
```python
# 模板
dp = [[0] * (m + 1) for _ in range(n + 1)]

# 初始化
for i in range(n + 1):
    dp[i][0] = ...
for j in range(m + 1):
    dp[0][j] = ...

# 状态转移
for i in range(1, n + 1):
    for j in range(1, m + 1):
        dp[i][j] = f(dp[i-1][j], dp[i][j-1], ...)

return dp[n][m]
```

## 📚 LeetCode练习

### 入门
- [509. Fibonacci Number](https://leetcode.com/problems/fibonacci-number/)
- [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)
- [198. House Robber](https://leetcode.com/problems/house-robber/)

### 进阶
- [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)
- [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)
- [322. Coin Change](https://leetcode.com/problems/coin-change/)
- [62. Unique Paths](https://leetcode.com/problems/unique-paths/)

## 💡 优化技巧

### 1. 空间优化
```python
# 只依赖前一个状态
dp[i] = f(dp[i-1])
# 优化为一个变量

# 只依赖前两个状态
dp[i] = f(dp[i-1], dp[i-2])
# 优化为两个变量

# 只依赖上一行
dp[i][j] = f(dp[i-1][j], dp[i][j-1])
# 优化为一维数组
```

### 2. 降维技巧
```python
# 二维改一维
for i in range(n):
    for j in range(m):
        dp[i][j] = f(dp[i-1][j], dp[i][j-1])

# 优化为
dp = [0] * m
for i in range(n):
    for j in range(m):
        dp[j] = f(dp[j], dp[j-1])
```

## 🎯 思维导图

```
动态规划
├── 线性DP
│   ├── 单串：爬楼梯、打家劫舍、最大子数组
│   └── 双串：最长公共子序列、编辑距离
├── 区间DP
│   ├── 最长回文子串
│   └── 戳气球
├── 背包DP
│   ├── 0-1背包
│   ├── 完全背包
│   └── 多重背包
└── 状态机DP
    ├── 股票问题
    └── 打家劫舍II
```

## 💡 学习建议

1. **从简单开始**：斐波那契→爬楼梯→打家劫舍
2. **画表理解**：手动模拟DP过程
3. **总结模板**：相同类型问题用相同套路
4. **优化意识**：能否降维？能否滚动数组？
5. **大量练习**：至少50道DP题

### 学习顺序
1. 理解递归解法
2. 加memo优化
3. 改为DP数组
4. 优化空间
5. 总结模板

