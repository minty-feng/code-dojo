"""
LeetCode 121. 买卖股票的最佳时机
https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/

给定一个数组prices，它的第i个元素prices[i]表示一支给定股票第i天的价格。
你只能选择某一天买入这只股票，并选择在未来的某一个不同的日子卖出该股票。

贪心/动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_profit(prices):
    """
    买卖股票的最佳时机 - 贪心法
    
    Args:
        prices: 股票价格数组
        
    Returns:
        最大利润
    """
    if not prices or len(prices) < 2:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        max_profit = max(max_profit, price - min_price)
        min_price = min(min_price, price)
    
    return max_profit


def test_max_profit():
    """测试函数"""
    # 测试用例1
    prices1 = [7, 1, 5, 3, 6, 4]
    result1 = max_profit(prices1)
    print(f"测试1 [7,1,5,3,6,4]: {result1}")  # 期望: 5
    
    # 测试用例2
    prices2 = [7, 6, 4, 3, 1]
    result2 = max_profit(prices2)
    print(f"测试2 [7,6,4,3,1]: {result2}")  # 期望: 0
    
    # 测试用例3
    prices3 = [1, 2]
    result3 = max_profit(prices3)
    print(f"测试3 [1,2]: {result3}")  # 期望: 1


if __name__ == "__main__":
    test_max_profit()
