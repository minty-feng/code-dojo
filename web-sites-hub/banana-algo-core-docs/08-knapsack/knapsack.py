"""
背包问题实现
"""

# ========== 0-1背包 ==========

def knapsack_01(weights, values, capacity):
    """0-1背包（二维DP）"""
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


def knapsack_01_optimized(weights, values, capacity):
    """0-1背包（一维DP优化）"""
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # 逆序遍历
        for j in range(capacity, weights[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[capacity]


# ========== 完全背包 ==========

def knapsack_complete(weights, values, capacity):
    """完全背包（物品可重复选择）"""
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # 正序遍历
        for j in range(weights[i], capacity + 1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[capacity]


# ========== 多重背包 ==========

def knapsack_multiple(weights, values, counts, capacity):
    """多重背包（每个物品有数量限制）"""
    # 二进制优化：转换为0-1背包
    new_weights = []
    new_values = []
    
    for i in range(len(weights)):
        count = counts[i]
        k = 1
        while k <= count:
            new_weights.append(weights[i] * k)
            new_values.append(values[i] * k)
            count -= k
            k *= 2
        if count > 0:
            new_weights.append(weights[i] * count)
            new_values.append(values[i] * count)
    
    return knapsack_01_optimized(new_weights, new_values, capacity)


# ========== 应用：分割等和子集 ==========

def can_partition(nums):
    """判断能否分割成两个和相等的子集"""
    total = sum(nums)
    if total % 2:
        return False
    
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    
    return dp[target]


# ========== 应用：零钱兑换 ==========

def coin_change(coins, amount):
    """最少硬币数（完全背包）"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] = min(dp[j], dp[j - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins, amount):
    """组成金额的方案数（完全背包）"""
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] += dp[j - coin]
    
    return dp[amount]


def demo():
    """演示背包问题"""
    print("=== 背包问题演示 ===\n")
    
    # 0-1背包
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    
    print(f"0-1背包:")
    print(f"  重量: {weights}")
    print(f"  价值: {values}")
    print(f"  容量: {capacity}")
    print(f"  最大价值: {knapsack_01(weights, values, capacity)}")
    print(f"  最大价值（优化）: {knapsack_01_optimized(weights, values, capacity)}\n")
    
    # 完全背包
    print(f"完全背包:")
    print(f"  最大价值: {knapsack_complete(weights, values, capacity)}\n")
    
    # 多重背包
    counts = [1, 2, 3, 1]
    print(f"多重背包:")
    print(f"  数量: {counts}")
    print(f"  最大价值: {knapsack_multiple(weights, values, counts, capacity)}\n")
    
    # 分割等和子集
    nums = [1, 5, 11, 5]
    print(f"分割等和子集 {nums}:")
    print(f"  能否分割: {can_partition(nums)}\n")
    
    # 零钱兑换
    coins, amount = [1, 2, 5], 11
    print(f"零钱兑换:")
    print(f"  硬币: {coins}, 金额: {amount}")
    print(f"  最少硬币数: {coin_change(coins, amount)}")
    print(f"  方案数: {coin_change_ways(coins, amount)}")


if __name__ == '__main__':
    demo()

