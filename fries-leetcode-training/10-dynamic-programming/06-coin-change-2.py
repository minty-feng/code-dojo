"""
LeetCode 518. 零钱兑换II
https://leetcode.cn/problems/coin-change-2/

给你一个整数数组coins表示不同面额的硬币，另给一个整数amount表示总金额。
请你计算并返回可以凑成总金额的硬币组合数。

动态规划（完全背包）

时间复杂度：O(amount * len(coins))
空间复杂度：O(amount)
"""

def change(amount, coins):
    """
    零钱兑换II - 动态规划法
    
    Args:
        amount: 目标金额
        coins: 硬币面额数组
        
    Returns:
        可以凑成总金额的硬币组合数
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # 金额为0时有一种组合（不选任何硬币）
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]


def change_2d(amount, coins):
    """
    零钱兑换II - 二维DP法
    
    Args:
        amount: 目标金额
        coins: 硬币面额数组
        
    Returns:
        可以凑成总金额的硬币组合数
    """
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n + 1)]
    
    # 初始化：金额为0时有一种组合
    for i in range(n + 1):
        dp[i][0] = 1
    
    for i in range(1, n + 1):
        for j in range(amount + 1):
            # 不使用第i-1个硬币
            dp[i][j] = dp[i-1][j]
            
            # 使用第i-1个硬币
            if j >= coins[i-1]:
                dp[i][j] += dp[i][j - coins[i-1]]
    
    return dp[n][amount]


def test_change():
    """测试函数"""
    # 测试用例1
    amount1 = 5
    coins1 = [1, 2, 5]
    result1 = change(amount1, coins1)
    result1_2d = change_2d(amount1, coins1)
    print(f"测试1 amount={amount1}, coins={coins1}: 1D={result1}, 2D={result1_2d}")  # 期望: 4
    
    # 测试用例2
    amount2 = 3
    coins2 = [2]
    result2 = change(amount2, coins2)
    result2_2d = change_2d(amount2, coins2)
    print(f"测试2 amount={amount2}, coins={coins2}: 1D={result2}, 2D={result2_2d}")  # 期望: 0
    
    # 测试用例3
    amount3 = 10
    coins3 = [10]
    result3 = change(amount3, coins3)
    result3_2d = change_2d(amount3, coins3)
    print(f"测试3 amount={amount3}, coins={coins3}: 1D={result3}, 2D={result3_2d}")  # 期望: 1


if __name__ == "__main__":
    test_change()
