"""
LeetCode 198. 打家劫舍
https://leetcode.cn/problems/house-robber/

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，
影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，
如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def rob(nums):
    """
    打家劫舍 - 动态规划法
    
    Args:
        nums: 每间房屋的现金数量
        
    Returns:
        能偷窃到的最高金额
    """
    if not nums:
        return 0
    
    if len(nums) == 1:
        return nums[0]
    
    # 空间优化版本
    prev2 = nums[0]  # dp[i-2]
    prev1 = max(nums[0], nums[1])  # dp[i-1]
    
    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = current
    
    return prev1


def rob_dp(nums):
    """
    打家劫舍 - 标准动态规划法
    
    Args:
        nums: 每间房屋的现金数量
        
    Returns:
        能偷窃到的最高金额
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    
    if n > 1:
        dp[1] = max(nums[0], nums[1])
    
    for i in range(2, n):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    return dp[n-1]


def test_rob():
    """测试函数"""
    # 测试用例1
    nums1 = [1, 2, 3, 1]
    result1 = rob(nums1)
    print(f"测试1 [1,2,3,1]: {result1}")  # 期望: 4
    
    # 测试用例2
    nums2 = [2, 7, 9, 3, 1]
    result2 = rob(nums2)
    print(f"测试2 [2,7,9,3,1]: {result2}")  # 期望: 12
    
    # 测试用例3
    nums3 = [2, 1, 1, 2]
    result3 = rob(nums3)
    print(f"测试3 [2,1,1,2]: {result3}")  # 期望: 4


if __name__ == "__main__":
    test_rob()
