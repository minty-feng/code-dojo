"""
NC91 最长递增子序列
https://www.nowcoder.com/practice/9cf027bf54714ad889d4f30ff0ae5481

给定一个长度为n的数组，找出其中最长严格递增子序列的长度。

解法1：动态规划 O(n^2)
解法2：动态规划+二分查找 O(nlogn)

时间复杂度：O(nlogn)
空间复杂度：O(n)
"""

import bisect

def length_of_lis_dp(nums):
    """
    方法1：动态规划
    dp[i]表示以nums[i]结尾的最长递增子序列长度
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

def length_of_lis_binary(nums):
    """
    方法2：动态规划+二分查找
    tails[i]表示长度为i+1的递增子序列的最小尾部元素
    """
    if not nums:
        return 0
    
    tails = []
    
    for num in nums:
        # 二分查找插入位置
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)

# 测试
if __name__ == "__main__":
    test_cases = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 3, 2, 3],
        [7, 7, 7, 7, 7]
    ]
    
    for nums in test_cases:
        print(f"数组: {nums}")
        print(f"DP法: {length_of_lis_dp(nums)}")
        print(f"二分法: {length_of_lis_binary(nums)}\n")

