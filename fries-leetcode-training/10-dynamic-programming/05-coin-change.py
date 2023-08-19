"""
LeetCode 322. 零钱兑换
https://leetcode.cn/problems/coin-change/

给你一个整数数组coins，表示不同面额的硬币；以及一个整数amount，表示总金额。
计算并返回可以凑成总金额所需的最少的硬币个数。

动态规划（完全背包）

时间复杂度：O(amount * len(coins))
空间复杂度：O(amount)
"""

def coin_change(coins, amount):
    """
    零钱兑换 - 动态规划法
    
    Args:
        coins: 硬币面额数组
        amount: 目标金额
        
    Returns:
        最少硬币个数，无法凑成则返回-1
    """
    if amount == 0:
        return 0
    
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_bfs(coins, amount):
    """
    零钱兑换 - BFS法
    
    Args:
        coins: 硬币面额数组
        amount: 目标金额
        
    Returns:
        最少硬币个数，无法凑成则返回-1
    """
    if amount == 0:
        return 0
    
    from collections import deque
    
    queue = deque([(0, 0)])  # (current_amount, steps)
    visited = {0}
    
    while queue:
        current_amount, steps = queue.popleft()
        
        for coin in coins:
            next_amount = current_amount + coin
            
            if next_amount == amount:
                return steps + 1
            
            if next_amount < amount and next_amount not in visited:
                visited.add(next_amount)
                queue.append((next_amount, steps + 1))
    
    return -1


def test_coin_change():
    """测试函数"""
    # 测试用例1
    coins1 = [1, 3, 4]
    amount1 = 6
    result1 = coin_change(coins1, amount1)
    result1_bfs = coin_change_bfs(coins1, amount1)
    print(f"测试1 coins={coins1}, amount={amount1}: DP={result1}, BFS={result1_bfs}")  # 期望: 2
    
    # 测试用例2
    coins2 = [2]
    amount2 = 3
    result2 = coin_change(coins2, amount2)
    result2_bfs = coin_change_bfs(coins2, amount2)
    print(f"测试2 coins={coins2}, amount={amount2}: DP={result2}, BFS={result2_bfs}")  # 期望: -1
    
    # 测试用例3
    coins3 = [1]
    amount3 = 0
    result3 = coin_change(coins3, amount3)
    result3_bfs = coin_change_bfs(coins3, amount3)
    print(f"测试3 coins={coins3}, amount={amount3}: DP={result3}, BFS={result3_bfs}")  # 期望: 0


if __name__ == "__main__":
    test_coin_change()
