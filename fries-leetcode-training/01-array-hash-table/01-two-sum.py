"""
LeetCode 1. 两数之和
https://leetcode.cn/problems/two-sum/

给定一个整数数组nums和一个整数目标值target，请你在该数组中找出和为目标值target的那两个整数，并返回它们的数组下标。

哈希表解法

时间复杂度：O(n)
空间复杂度：O(n)
"""

def two_sum(nums, target):
    """
    两数之和 - 哈希表解法
    """
    hash_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in hash_map:
            return [hash_map[complement], i]
        
        hash_map[num] = i
    
    return []

def two_sum_brute_force(nums, target):
    """
    两数之和 - 暴力解法
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# 测试
if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9),
        ([3, 2, 4], 6),
        ([3, 3], 6)
    ]
    
    for nums, target in test_cases:
        result = two_sum(nums, target)
        print(f"数组: {nums}, 目标: {target}")
        print(f"结果: {result}")
        print(f"验证: {nums[result[0]]} + {nums[result[1]]} = {nums[result[0]] + nums[result[1]]}\n")

