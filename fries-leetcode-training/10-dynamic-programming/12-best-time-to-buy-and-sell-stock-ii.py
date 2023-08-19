"""
LeetCode 122. 买卖股票的最佳时机II
https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/

给你一个整数数组prices，其中prices[i]表示某支股票第i天的价格。
在每一天，你可以决定是否购买和/或出售股票。你在任何时候最多只能持有一股股票。

贪心/动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_profit(prices):
    """
    买卖股票的最佳时机II - 贪心法
    
    Args:
        prices: 股票价格数组
        
    Returns:
        最大利润
    """
    if not prices or len(prices) < 2:
        return 0
    
    profit = 0
    
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    
    return profit


def max_profit_dp(prices):
    """
    买卖股票的最佳时机II - 动态规划法
    
    Args:
        prices: 股票价格数组
        
    Returns:
        最大利润
    """
    if not prices or len(prices) < 2:
        return 0
    
    # dp[i][0] 表示第i天不持有股票的最大利润
    # dp[i][1] 表示第i天持有股票的最大利润
    hold = -prices[0]  # 持有股票
    not_hold = 0       # 不持有股票
    
    for i in range(1, len(prices)):
        # 今天不持有股票 = max(昨天不持有, 昨天持有今天卖出)
        not_hold = max(not_hold, hold + prices[i])
        
        # 今天持有股票 = max(昨天持有, 昨天不持有今天买入)
        hold = max(hold, not_hold - prices[i])
    
    return not_hold


def max_profit_dp_2d(prices):
    """
    买卖股票的最佳时机II - 二维DP法
    
    Args:
        prices: 股票价格数组
        
    Returns:
        最大利润
    """
    if not prices or len(prices) < 2:
        return 0
    
    n = len(prices)
    dp = [[0, 0] for _ in range(n)]
    
    dp[0][0] = 0          # 不持有股票
    dp[0][1] = -prices[0]  # 持有股票
    
    for i in range(1, n):
        dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
        dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])
    
    return dp[n-1][0]


def test_max_profit():
    """测试函数"""
    # 测试用例1
    prices1 = [7, 1, 5, 3, 6, 4]
    result1 = max_profit(prices1)
    result1_dp = max_profit_dp(prices1)
    result1_2d = max_profit_dp_2d(prices1)
    print(f"测试1 {prices1}: Greedy={result1}, DP={result1_dp}, 2D={result1_2d}")  # 期望: 7
    
    # 测试用例2
    prices2 = [1, 2, 3, 4, 5]
    result2 = max_profit(prices2)
    result2_dp = max_profit_dp(prices2)
    result2_2d = max_profit_dp_2d(prices2)
    print(f"测试2 {prices2}: Greedy={result2}, DP={result2_dp}, 2D={result2_2d}")  # 期望: 4
    
    # 测试用例3
    prices3 = [7, 6, 4, 3, 1]
    result3 = max_profit(prices3)
    result3_dp = max_profit_dp(prices3)
    result3_2d = max_profit_dp_2d(prices3)
    print(f"测试3 {prices3}: Greedy={result3}, DP={result3_dp}, 2D={result3_2d}")  # 期望: 0


if __name__ == "__main__":
    test_max_profit()
