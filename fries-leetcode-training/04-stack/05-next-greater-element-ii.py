"""
LeetCode 503. 下一个更大元素II
https://leetcode.cn/problems/next-greater-element-ii/

给定一个循环数组nums，返回nums中每个元素的下一个更大元素。

单调栈 + 循环数组

时间复杂度：O(n)
空间复杂度：O(n)
"""

def next_greater_elements(nums):
    """
    下一个更大元素II - 单调栈法
    
    Args:
        nums: 循环数组
        
    Returns:
        下一个更大元素的列表
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # 存储索引
    
    # 遍历两遍数组来处理循环
    for i in range(2 * n):
        while stack and nums[i % n] > nums[stack[-1]]:
            index = stack.pop()
            result[index] = nums[i % n]
        stack.append(i % n)
    
    return result


def test_next_greater_elements():
    """测试函数"""
    # 测试用例1
    nums1 = [1, 2, 1]
    result1 = next_greater_elements(nums1)
    print(f"测试1: {result1}")
    # 期望: [2, -1, 2]


if __name__ == "__main__":
    test_next_greater_elements()
