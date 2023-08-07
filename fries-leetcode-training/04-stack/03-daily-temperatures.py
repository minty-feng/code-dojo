"""
LeetCode 739. 每日温度
https://leetcode.cn/problems/daily-temperatures/

请根据每日气温列表temperatures，重新生成一个列表，要求对于每一天，你都要计算这一天之后第一个更高温度出现在几天后。

单调栈

时间复杂度：O(n)
空间复杂度：O(n)
"""

def daily_temperatures(temperatures):
    """
    每日温度 - 单调栈法
    
    Args:
        temperatures: 温度列表
        
    Returns:
        等待天数的列表
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # 存储索引
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            index = stack.pop()
            result[index] = i - index
        stack.append(i)
    
    return result


def test_daily_temperatures():
    """测试函数"""
    # 测试用例1
    temperatures1 = [73, 74, 75, 71, 69, 72, 76, 73]
    result1 = daily_temperatures(temperatures1)
    print(f"测试1: {result1}")
    # 期望: [1, 1, 4, 2, 1, 1, 0, 0]
    
    # 测试用例2
    temperatures2 = [30, 40, 50, 60]
    result2 = daily_temperatures(temperatures2)
    print(f"测试2: {result2}")
    # 期望: [1, 1, 1, 0]


if __name__ == "__main__":
    test_daily_temperatures()
