"""
NC181 完全背包问题
https://www.nowcoder.com/practice/237ae40ea1e84d8980c1d5666d741e0

有n个物品和一个容量为v的背包，每个物品有重量w[i]和价值v[i]。
每个物品可以选择无限次，问能装下的最大价值。

动态规划

时间复杂度：O(n*v)
空间复杂度：O(v)
"""

def knapsack_complete(weights, values, capacity):
    """
    完全背包问题
    """
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0
    
    # dp[i]表示容量为i时的最大价值
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # 从小到大遍历，允许重复使用
        for j in range(weights[i], capacity + 1):
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i])
    
    return dp[capacity]

# 测试
if __name__ == "__main__":
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    
    result = knapsack_complete(weights, values, capacity)
    print(f"物品重量: {weights}")
    print(f"物品价值: {values}")
    print(f"背包容量: {capacity}")
    print(f"最大价值: {result}")

