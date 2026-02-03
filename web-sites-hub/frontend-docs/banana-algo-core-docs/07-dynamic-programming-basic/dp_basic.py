"""
动态规划基础问题实现
"""

# ========== 1. 斐波那契数列 ==========

def fib_recursive(n):
    """递归：O(2^n)"""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_memo(n, memo=None):
    """记忆化递归：O(n)"""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_dp(n):
    """DP数组：O(n)"""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_optimized(n):
    """空间优化：O(1)"""
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


# ========== 2. 爬楼梯 ==========

def climb_stairs(n):
    """一次爬1或2级，n级有多少种方法"""
    if n <= 1:
        return 1
    prev, curr = 1, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


# ========== 3. 打家劫舍 ==========

def rob(nums):
    """不能偷相邻房屋"""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev, curr = 0, 0
    for num in nums:
        prev, curr = curr, max(curr, prev + num)
    return curr


# ========== 4. 最大子数组和 ==========

def max_sub_array(nums):
    """Kadane算法：O(n)"""
    max_sum = nums[0]
    curr_sum = nums[0]
    
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    
    return max_sum


# ========== 5. 最长递增子序列 ==========

def length_of_lis(nums):
    """O(n²)解法"""
    if not nums:
        return 0
    
    dp = [1] * len(nums)
    
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def length_of_lis_optimized(nums):
    """二分优化：O(n log n)"""
    if not nums:
        return 0
    
    tails = []  # tails[i]表示长度为i+1的LIS的最小末尾元素
    
    for num in nums:
        # 二分查找插入位置
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    
    return len(tails)


# ========== 6. 零钱兑换 ==========

def coin_change(coins, amount):
    """最少硬币数"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


# ========== 7. 不同路径 ==========

def unique_paths(m, n):
    """m×n网格，从左上到右下有多少路径"""
    dp = [[0] * n for _ in range(m)]
    
    # 初始化第一行和第一列
    for i in range(m):
        dp[i][0] = 1
    for j in range(n):
        dp[0][j] = 1
    
    # 状态转移
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[m - 1][n - 1]


def unique_paths_optimized(m, n):
    """空间优化：O(n)"""
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    
    return dp[n - 1]


# ========== 8. 最小路径和 ==========

def min_path_sum(grid):
    """网格中从左上到右下的最小路径和"""
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    
    # 初始化
    dp[0][0] = grid[0][0]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    
    # 状态转移
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]
    
    return dp[m - 1][n - 1]


def demo():
    """演示DP算法"""
    print("=== 动态规划基础演示 ===\n")
    
    # 斐波那契
    n = 10
    print(f"斐波那契第{n}项:")
    print(f"  递归: {fib_recursive(n)}")
    print(f"  记忆化: {fib_memo(n)}")
    print(f"  DP: {fib_dp(n)}")
    print(f"  优化: {fib_optimized(n)}\n")
    
    # 爬楼梯
    n = 5
    print(f"爬{n}级楼梯的方法数: {climb_stairs(n)}\n")
    
    # 打家劫舍
    nums = [2, 7, 9, 3, 1]
    print(f"打家劫舍 {nums}: {rob(nums)}\n")
    
    # 最大子数组和
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"最大子数组和 {nums}: {max_sub_array(nums)}\n")
    
    # LIS
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"最长递增子序列 {nums}: {length_of_lis(nums)}\n")
    
    # 零钱兑换
    coins, amount = [1, 2, 5], 11
    print(f"零钱兑换 coins={coins}, amount={amount}: {coin_change(coins, amount)}\n")
    
    # 不同路径
    m, n = 3, 7
    print(f"网格 {m}×{n} 不同路径数: {unique_paths(m, n)}")


if __name__ == '__main__':
    demo()

