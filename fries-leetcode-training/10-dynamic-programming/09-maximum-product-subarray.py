"""
LeetCode 152. 乘积最大子数组
https://leetcode.cn/problems/maximum-product-subarray/

给你一个整数数组nums，请你找出数组中乘积最大的连续子数组，并返回该子数组的乘积。

动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_product(nums):
    """
    乘积最大子数组 - 动态规划法
    
    Args:
        nums: 整数数组
        
    Returns:
        乘积最大的连续子数组的乘积
    """
    if not nums:
        return 0
    
    # 维护最大值和最小值
    max_prod = min_prod = result = nums[0]
    
    for i in range(1, len(nums)):
        # 如果当前数是负数，交换最大值和最小值
        if nums[i] < 0:
            max_prod, min_prod = min_prod, max_prod
        
        # 更新最大值和最小值
        max_prod = max(nums[i], max_prod * nums[i])
        min_prod = min(nums[i], min_prod * nums[i])
        
        # 更新结果
        result = max(result, max_prod)
    
    return result


def max_product_dp(nums):
    """
    乘积最大子数组 - 标准动态规划法
    
    Args:
        nums: 整数数组
        
    Returns:
        乘积最大的连续子数组的乘积
    """
    if not nums:
        return 0
    
    n = len(nums)
    # dp_max[i] 表示以nums[i]结尾的最大乘积
    # dp_min[i] 表示以nums[i]结尾的最小乘积
    dp_max = [0] * n
    dp_min = [0] * n
    
    dp_max[0] = dp_min[0] = nums[0]
    result = nums[0]
    
    for i in range(1, n):
        if nums[i] >= 0:
            dp_max[i] = max(nums[i], dp_max[i-1] * nums[i])
            dp_min[i] = min(nums[i], dp_min[i-1] * nums[i])
        else:
            dp_max[i] = max(nums[i], dp_min[i-1] * nums[i])
            dp_min[i] = min(nums[i], dp_max[i-1] * nums[i])
        
        result = max(result, dp_max[i])
    
    return result


def test_max_product():
    """测试函数"""
    # 测试用例1
    nums1 = [2, 3, -2, 4]
    result1 = max_product(nums1)
    result1_dp = max_product_dp(nums1)
    print(f"测试1 [2,3,-2,4]: Opt={result1}, DP={result1_dp}")  # 期望: 6
    
    # 测试用例2
    nums2 = [-2, 0, -1]
    result2 = max_product(nums2)
    result2_dp = max_product_dp(nums2)
    print(f"测试2 [-2,0,-1]: Opt={result2}, DP={result2_dp}")  # 期望: 0
    
    # 测试用例3
    nums3 = [-2, 3, -4]
    result3 = max_product(nums3)
    result3_dp = max_product_dp(nums3)
    print(f"测试3 [-2,3,-4]: Opt={result3}, DP={result3_dp}")  # 期望: 24
    
    # 测试用例4
    nums4 = [0, 2]
    result4 = max_product(nums4)
    result4_dp = max_product_dp(nums4)
    print(f"测试4 [0,2]: Opt={result4}, DP={result4_dp}")  # 期望: 2


if __name__ == "__main__":
    test_max_product()
