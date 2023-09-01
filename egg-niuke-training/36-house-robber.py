"""
NC174 打家劫舍
https://www.nowcoder.com/practice/c5fbf7325fbd4c0ea3d0c3ea6bc6cc79

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金。
你不能偷窃相邻的房屋，问能够偷窃到的最高金额。

动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def rob(nums):
    """
    打家劫舍
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    # dp[i] = 偷到第i间房的最大金额
    prev2 = nums[0]  # dp[0]
    prev1 = max(nums[0], nums[1])  # dp[1]
    
    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = curr
    
    return prev1

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, 2, 3, 1],
        [2, 7, 9, 3, 1],
        [2, 1, 1, 2],
        [1]
    ]
    
    for nums in test_cases:
        result = rob(nums)
        print(f"房屋金额: {nums}")
        print(f"最大偷窃金额: {result}\n")

