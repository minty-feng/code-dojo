"""
NC103 买卖股票的最好时机(一)
https://www.nowcoder.com/practice/64b4262d4e6d4f6181cd45446a5821ec

假设你有一个数组prices，长度为n，其中prices[i]是股票在第i天的价格。
请根据这个价格数组，返回买卖股票能获得的最大收益。

动态规划：记录最低价格和最大收益

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_profit(prices):
    """
    买卖股票的最好时机(一)
    """
    if not prices or len(prices) < 2:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        # 更新最低价格
        min_price = min(min_price, price)
        # 更新最大收益
        max_profit = max(max_profit, price - min_price)
    
    return max_profit

# 测试
if __name__ == "__main__":
    test_cases = [
        [7, 1, 5, 3, 6, 4],
        [7, 6, 4, 3, 1],
        [1, 2, 3, 4, 5],
        [2, 4, 1]
    ]
    
    for prices in test_cases:
        profit = max_profit(prices)
        print(f"价格: {prices}")
        print(f"最大收益: {profit}\n")

