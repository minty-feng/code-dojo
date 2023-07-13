"""
NC68 跳台阶
https://www.nowcoder.com/practice/8c82a5b80378478f9484d87d1c5f12a4

一只青蛙一次可以跳上1级台阶，也可以跳上2级。
求该青蛙跳上一个 n 级的台阶总共有多少种跳法。

动态规划/斐波那契数列
dp[i] = dp[i-1] + dp[i-2]

时间复杂度：O(n)
空间复杂度：O(1)
"""

def jump_floor(n):
    """
    跳台阶 - 动态规划
    """
    if n <= 2:
        return n
    
    # dp[i] = 跳到第i级台阶的方法数
    prev2 = 1  # n=1
    prev1 = 2  # n=2
    
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    
    return prev1

def jump_floor_recursive(n):
    """
    跳台阶 - 递归（会超时）
    """
    if n <= 2:
        return n
    return jump_floor_recursive(n-1) + jump_floor_recursive(n-2)

# 测试
if __name__ == "__main__":
    for n in range(1, 11):
        result = jump_floor(n)
        print(f"n={n}: {result}种跳法")

