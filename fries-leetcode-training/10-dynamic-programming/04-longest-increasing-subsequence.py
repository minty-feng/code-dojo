"""
LeetCode 300. 最长递增子序列
https://leetcode.cn/problems/longest-increasing-subsequence/

给你一个整数数组nums，找到其中最长严格递增子序列的长度。

动态规划 + 二分搜索

时间复杂度：O(n log n)
空间复杂度：O(n)
"""

def length_of_lis(nums):
    """
    最长递增子序列 - 动态规划法
    
    Args:
        nums: 整数数组
        
    Returns:
        最长递增子序列的长度
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def length_of_lis_binary_search(nums):
    """
    最长递增子序列 - 二分搜索法
    
    Args:
        nums: 整数数组
        
    Returns:
        最长递增子序列的长度
    """
    if not nums:
        return 0
    
    tails = []
    
    for num in nums:
        left, right = 0, len(tails)
        
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    
    return len(tails)


def test_length_of_lis():
    """测试函数"""
    # 测试用例1
    nums1 = [10, 9, 2, 5, 3, 7, 101, 18]
    result1 = length_of_lis(nums1)
    result1_bs = length_of_lis_binary_search(nums1)
    print(f"测试1 [10,9,2,5,3,7,101,18]: DP={result1}, BS={result1_bs}")  # 期望: 4
    
    # 测试用例2
    nums2 = [0, 1, 0, 3, 2, 3]
    result2 = length_of_lis(nums2)
    result2_bs = length_of_lis_binary_search(nums2)
    print(f"测试2 [0,1,0,3,2,3]: DP={result2}, BS={result2_bs}")  # 期望: 4
    
    # 测试用例3
    nums3 = [7, 7, 7, 7, 7, 7, 7]
    result3 = length_of_lis(nums3)
    result3_bs = length_of_lis_binary_search(nums3)
    print(f"测试3 [7,7,7,7,7,7,7]: DP={result3}, BS={result3_bs}")  # 期望: 1


if __name__ == "__main__":
    test_length_of_lis()
