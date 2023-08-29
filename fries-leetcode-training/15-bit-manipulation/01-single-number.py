"""
LeetCode 136. 只出现一次的数字
https://leetcode.cn/problems/single-number/

给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现两次。
找出那个只出现了一次的元素。

位运算（异或）

时间复杂度：O(n)
空间复杂度：O(1)
"""

def single_number(nums):
    """
    只出现一次的数字 - 异或法
    
    Args:
        nums: 非空整数数组
        
    Returns:
        只出现一次的数字
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_hash(nums):
    """
    只出现一次的数字 - 哈希表法
    
    Args:
        nums: 非空整数数组
        
    Returns:
        只出现一次的数字
    """
    from collections import Counter
    count = Counter(nums)
    
    for num, freq in count.items():
        if freq == 1:
            return num


def test_single_number():
    """测试函数"""
    # 测试用例1
    nums1 = [2, 2, 1]
    result1 = single_number(nums1)
    print(f"测试1 [2,2,1]: {result1}")  # 期望: 1
    
    # 测试用例2
    nums2 = [4, 1, 2, 1, 2]
    result2 = single_number(nums2)
    print(f"测试2 [4,1,2,1,2]: {result2}")  # 期望: 4
    
    # 测试用例3
    nums3 = [1]
    result3 = single_number(nums3)
    print(f"测试3 [1]: {result3}")  # 期望: 1
    
    # 验证异或性质
    print("\n异或性质验证:")
    print(f"a ^ a = 0: {5 ^ 5}")  # 期望: 0
    print(f"a ^ 0 = a: {5 ^ 0}")  # 期望: 5
    print(f"a ^ b ^ a = b: {5 ^ 3 ^ 5}")  # 期望: 3


if __name__ == "__main__":
    test_single_number()
