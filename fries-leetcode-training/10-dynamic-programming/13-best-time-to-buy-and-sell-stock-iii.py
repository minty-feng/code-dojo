"""
LeetCode 123. 买卖股票的最佳时机III
https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/

给定一个数组，它的第i个元素是一支给定的股票在第i天的价格。
设计一个算法来计算你所能获取的最大利润。你最多可以完成两笔交易。

动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_profit(prices):
    """
    买卖股票的最佳时机III - 动态规划法
    
    Args:
        prices: 股票价格数组
        
    Returns:
        最大利润
    """
    if not prices or len(prices) < 2:
        return 0
    
    # 第一次交易的状态
    buy1 = -prices[0]   # 第一次买入
    sell1 = 0           # 第一次卖出
    
    # 第二次交易的状态
    buy2 = -prices[0]   # 第二次买入
    sell2 = 0           # 第二次卖出
    
    for i in range(1, len(prices)):
        # 更新第二次交易状态
        sell2 = max(sell2, buy2 + prices[i])
        buy2 = max(buy2, sell1 - prices[i])
        
        # 更新第一次交易状态
        sell1 = max(sell1, buy1 + prices[i])
        buy1 = max(buy1, -prices[i])
    
    return sell2


def max_profit_dp(prices):
    """
    买卖股票的最佳时机III - 标准动态规划法
    
    Args:
        prices: 股票价格数组
        
    Returns:
        最大利润
    """
    if not prices or len(prices) < 2:
        return 0
    
    n = len(prices)
    # dp[i][j][k] 表示第i天，进行了j次交易，当前状态为k的最大利润
    # k=0: 未持有股票, k=1: 持有股票
    dp = [[[0, 0] for _ in range(3)] for _ in range(n)]
    
    # 初始化
    dp[0][0][0] = 0
    dp[0][0][1] = -prices[0]
    dp[0][1][0] = float('-inf')
    dp[0][1][1] = float('-inf')
    dp[0][2][0] = float('-inf')
    dp[0][2][1] = float('-inf')
    
    for i in range(1, n):
        for j in range(3):
            if j == 0:
                # 没有进行过交易
                dp[i][j][0] = dp[i-1][j][0]
                dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j][0] - prices[i])
            else:
                # 进行过交易
                dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j-1][1] + prices[i])
                dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j][0] - prices[i])
    
    return max(dp[n-1][0][0], dp[n-1][1][0], dp[n-1][2][0])


def test_max_profit():
    """测试函数"""
    # 测试用例1
    prices1 = [3, 3, 5, 0, 0, 3, 1, 4]
    result1 = max_profit(prices1)
    result1_dp = max_profit_dp(prices1)
    print(f"测试1 {prices1}: Opt={result1}, DP={result1_dp}")  # 期望: 6
    
    # 测试用例2
    prices2 = [1, 2, 3, 4, 5]
    result2 = max_profit(prices2)
    result2_dp = max_profit_dp(prices2)
    print(f"测试2 {prices2}: Opt={result2}, DP={result2_dp}")  # 期望: 4
    
    # 测试用例3
    prices3 = [7, 6, 4, 3, 1]
    result3 = max_profit(prices3)
    result3_dp = max_profit_dp(prices3)
    print(f"测试3 {prices3}: Opt={result3}, DP={result3_dp}")  # 期望: 0
    
    # 测试用例4
    prices4 = [1]
    result4 = max_profit(prices4)
    result4_dp = max_profit_dp(prices4)
    print(f"测试4 {prices4}: Opt={result4}, DP={result4_dp}")  # 期望: 0


if __name__ == "__main__":
    test_max_profit()
