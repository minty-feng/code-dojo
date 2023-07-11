"""
NC19 最大子数组和
https://www.nowcoder.com/practice/459bd355da1549fa8a49e350bf3df484

输入一个长度为n的整型数组array，数组中的一个或连续多个整数组成一个子数组。
求所有子数组的和的最大值。

动态规划（Kadane算法）
dp[i] = max(dp[i-1] + nums[i], nums[i])

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_sub_array(nums):
    """
    最大子数组和 - 动态规划
    """
    if not nums:
        return 0
    
    max_sum = nums[0]
    current_sum = nums[0]
    
    for i in range(1, len(nums)):
        # 要么加上当前元素，要么重新开始
        current_sum = max(current_sum + nums[i], nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, -2, 3, 10, -4, 7, 2, -5],
        [-2, -1],
        [1, 2, 3, 4, 5]
    ]
    
    for nums in test_cases:
        result = max_sub_array(nums)
        print(f"数组 {nums}")
        print(f"最大子数组和: {result}\n")

