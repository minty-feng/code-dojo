"""
LeetCode 152. 乘积最大子数组
https://leetcode.cn/problems/maximum-product-subarray/

给你一个整数数组nums，请你找出数组中乘积最大的连续子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。

动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_product(nums):
    """
    乘积最大子数组 - 动态规划
    """
    if not nums:
        return 0
    
    max_prod = min_prod = result = nums[0]
    
    for i in range(1, len(nums)):
        # 保存之前的值
        temp_max = max_prod
        
        # 更新最大值和最小值
        max_prod = max(nums[i], max_prod * nums[i], min_prod * nums[i])
        min_prod = min(nums[i], temp_max * nums[i], min_prod * nums[i])
        
        # 更新结果
        result = max(result, max_prod)
    
    return result

# 测试
if __name__ == "__main__":
    test_cases = [
        [2, 3, -2, 4],
        [-2, 0, -1],
        [-2, 3, -4],
        [0, 2]
    ]
    
    for nums in test_cases:
        result = max_product(nums)
        print(f"数组: {nums}")
        print(f"最大乘积: {result}\n")

