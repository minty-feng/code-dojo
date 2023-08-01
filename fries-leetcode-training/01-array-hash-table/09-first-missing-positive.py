"""
LeetCode 41. 缺失的第一个正数
https://leetcode.cn/problems/first-missing-positive/

给你一个未排序的整数数组nums，请你找出其中没有出现的最小的正整数。

原地哈希

时间复杂度：O(n)
空间复杂度：O(1)
"""

def first_missing_positive(nums):
    """
    缺失的第一个正数 - 原地哈希
    """
    n = len(nums)
    
    # 将数组中的数映射到1-n的位置
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            nums[nums[i] - 1], nums[i] = nums[i], nums[nums[i] - 1]
    
    # 找到第一个位置不正确的数
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    
    return n + 1

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, 2, 0],
        [3, 4, -1, 1],
        [7, 8, 9, 11, 12]
    ]
    
    for nums in test_cases:
        result = first_missing_positive(nums[:])
        print(f"数组: {nums}")
        print(f"缺失的第一个正数: {result}\n")

