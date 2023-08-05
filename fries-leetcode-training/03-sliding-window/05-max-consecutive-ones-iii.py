"""
LeetCode 1004. 最大连续1的个数III
https://leetcode.cn/problems/max-consecutive-ones-iii/

给定一个二进制数组nums和一个整数k，最多可以把k个0变成1，返回仅包含1的最长（连续）子数组的长度。

滑动窗口

时间复杂度：O(n)
空间复杂度：O(1)
"""

def longest_ones(nums, k):
    """
    最大连续1的个数III - 滑动窗口法
    
    Args:
        nums: 二进制数组
        k: 最多可以翻转的0的个数
        
    Returns:
        最长连续1的长度
    """
    left = 0
    max_len = 0
    zero_count = 0
    
    for right in range(len(nums)):
        # 扩展窗口
        if nums[right] == 0:
            zero_count += 1
        
        # 收缩窗口
        while zero_count > k:
            if nums[left] == 0:
                zero_count -= 1
            left += 1
        
        # 更新结果
        max_len = max(max_len, right - left + 1)
    
    return max_len


def test_longest_ones():
    """测试函数"""
    # 测试用例1
    nums1, k1 = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2
    result1 = longest_ones(nums1, k1)
    print(f"测试1: {result1}")
    # 期望: 6
    
    # 测试用例2
    nums2, k2 = [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3
    result2 = longest_ones(nums2, k2)
    print(f"测试2: {result2}")
    # 期望: 10
    
    # 测试用例3
    nums3, k3 = [0, 0, 0, 1], 4
    result3 = longest_ones(nums3, k3)
    print(f"测试3: {result3}")
    # 期望: 4


if __name__ == "__main__":
    test_longest_ones()
