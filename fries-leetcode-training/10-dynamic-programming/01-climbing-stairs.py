"""
LeetCode 70. 爬楼梯
https://leetcode.cn/problems/climbing-stairs/

假设你正在爬楼梯。需要n阶你才能到达楼顶。
每次你可以爬1或2个台阶。你有多少种不同的方法可以爬到楼顶呢？

动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def climb_stairs(n):
    """
    爬楼梯 - 动态规划法
    
    Args:
        n: 楼梯阶数
        
    Returns:
        爬到楼顶的方法数
    """
    if n <= 2:
        return n
    
    # 空间优化版本
    prev2 = 1  # dp[i-2]
    prev1 = 2  # dp[i-1]
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


def climb_stairs_dp(n):
    """
    爬楼梯 - 标准动态规划法
    
    Args:
        n: 楼梯阶数
        
    Returns:
        爬到楼顶的方法数
    """
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def test_climb_stairs():
    """测试函数"""
    # 测试用例1
    n1 = 2
    result1 = climb_stairs(n1)
    print(f"测试1 n=2: {result1}")  # 期望: 2
    
    # 测试用例2
    n2 = 3
    result2 = climb_stairs(n2)
    print(f"测试2 n=3: {result2}")  # 期望: 3
    
    # 测试用例3
    n3 = 5
    result3 = climb_stairs(n3)
    print(f"测试3 n=5: {result3}")  # 期望: 8


if __name__ == "__main__":
    test_climb_stairs()
