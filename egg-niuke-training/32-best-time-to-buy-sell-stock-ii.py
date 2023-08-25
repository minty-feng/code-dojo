"""
NC104 买卖股票的最好时机(二)
https://www.nowcoder.com/practice/9e5e3c2603064829b0a0bbfca10594e9

假设你有一个数组prices，长度为n，其中prices[i]是股票在第i天的价格。
你可以多次买卖股票，但每次只能持有一只股票。

贪心算法：只要第二天价格更高就买卖

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_profit_multiple_transactions(prices):
    """
    买卖股票的最好时机(二) - 多次交易
    """
    if not prices or len(prices) < 2:
        return 0
    
    profit = 0
    
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    
    return profit

# 测试
if __name__ == "__main__":
    test_cases = [
        [7, 1, 5, 3, 6, 4],
        [1, 2, 3, 4, 5],
        [7, 6, 4, 3, 1],
        [1, 2, 1, 2]
    ]
    
    for prices in test_cases:
        profit = max_profit_multiple_transactions(prices)
        print(f"价格: {prices}")
        print(f"最大收益: {profit}\n")

