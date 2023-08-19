"""
LeetCode 53. 最大子数组和
https://leetcode.cn/problems/maximum-subarray/

给你一个整数数组nums，请你找出一个具有最大和的连续子数组，返回其最大和。

Kadane算法

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_subarray(nums):
    """
    最大子数组和 - Kadane算法
    
    Args:
        nums: 整数数组
        
    Returns:
        最大子数组和
    """
    if not nums:
        return 0
    
    max_sum = current_sum = nums[0]
    
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum


def max_subarray_dp(nums):
    """
    最大子数组和 - 动态规划法
    
    Args:
        nums: 整数数组
        
    Returns:
        最大子数组和
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    max_sum = nums[0]
    
    for i in range(1, n):
        dp[i] = max(nums[i], dp[i-1] + nums[i])
        max_sum = max(max_sum, dp[i])
    
    return max_sum


def test_max_subarray():
    """测试函数"""
    # 测试用例1
    nums1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    result1 = max_subarray(nums1)
    print(f"测试1: {result1}")  # 期望: 6
    
    # 测试用例2
    nums2 = [1]
    result2 = max_subarray(nums2)
    print(f"测试2: {result2}")  # 期望: 1
    
    # 测试用例3
    nums3 = [5, 4, -1, 7, 8]
    result3 = max_subarray(nums3)
    print(f"测试3: {result3}")  # 期望: 23


if __name__ == "__main__":
    test_max_subarray()
