"""
LeetCode 16. 最接近的三数之和
https://leetcode.cn/problems/3sum-closest/

给你一个长度为n的整数数组nums和一个目标值target。请你从nums中选出三个整数，使它们的和与target最接近。

双指针

时间复杂度：O(n^2)
空间复杂度：O(1)
"""

def three_sum_closest(nums, target):
    """
    最接近的三数之和 - 双指针
    """
    nums.sort()
    n = len(nums)
    closest_sum = float('inf')
    
    for i in range(n - 2):
        left, right = i + 1, n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            # 更新最接近的和
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return target  # 找到完全匹配
    
    return closest_sum

# 测试
if __name__ == "__main__":
    test_cases = [
        ([-1, 2, 1, -4], 1),
        ([0, 0, 0], 1),
        ([1, 1, 1, 0], -100)
    ]
    
    for nums, target in test_cases:
        result = three_sum_closest(nums, target)
        print(f"数组: {nums}, 目标: {target}")
        print(f"最接近的三数之和: {result}\n")

