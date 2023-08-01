"""
LeetCode 128. 最长连续序列
https://leetcode.cn/problems/longest-consecutive-sequence/

给定一个未排序的整数数组nums，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

哈希表

时间复杂度：O(n)
空间复杂度：O(n)
"""

def longest_consecutive(nums):
    """
    最长连续序列 - 哈希表
    """
    if not nums:
        return 0
    
    num_set = set(nums)
    max_length = 0
    
    for num in num_set:
        # 只从序列的起始位置开始计算
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            # 计算连续序列长度
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            max_length = max(max_length, current_length)
    
    return max_length

# 测试
if __name__ == "__main__":
    test_cases = [
        [100, 4, 200, 1, 3, 2],
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],
        [1, 2, 0, 1]
    ]
    
    for nums in test_cases:
        result = longest_consecutive(nums)
        print(f"数组: {nums}")
        print(f"最长连续序列长度: {result}\n")

