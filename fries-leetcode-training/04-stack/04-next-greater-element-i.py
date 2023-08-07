"""
LeetCode 496. 下一个更大元素I
https://leetcode.cn/problems/next-greater-element-i/

给你两个没有重复元素的数组nums1和nums2，其中nums1是nums2的子集。
请你找出nums1中每个元素在nums2中的下一个比其大的值。

单调栈 + 哈希表

时间复杂度：O(n)
空间复杂度：O(n)
"""

def next_greater_element(nums1, nums2):
    """
    下一个更大元素I - 单调栈法
    
    Args:
        nums1: 子集数组
        nums2: 父集数组
        
    Returns:
        下一个更大元素的列表
    """
    # 用单调栈找到nums2中每个元素的下一个更大元素
    next_greater = {}
    stack = []
    
    for num in nums2:
        while stack and num > stack[-1]:
            next_greater[stack.pop()] = num
        stack.append(num)
    
    # 为nums1中的每个元素查找结果
    result = []
    for num in nums1:
        result.append(next_greater.get(num, -1))
    
    return result


def test_next_greater_element():
    """测试函数"""
    # 测试用例1
    nums1_1 = [4, 1, 2]
    nums2_1 = [1, 3, 4, 2]
    result1 = next_greater_element(nums1_1, nums2_1)
    print(f"测试1: {result1}")
    # 期望: [-1, 3, -1]


if __name__ == "__main__":
    test_next_greater_element()
