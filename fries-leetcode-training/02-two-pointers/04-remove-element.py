"""
LeetCode 27. 移除元素
https://leetcode.cn/problems/remove-element/

给你一个数组nums和一个值val，你需要原地移除所有数值等于val的元素，并返回移除后数组的新长度。

双指针

时间复杂度：O(n)
空间复杂度：O(1)
"""

def remove_element(nums, val):
    """
    移除元素 - 双指针法
    
    Args:
        nums: 整数数组
        val: 要移除的值
        
    Returns:
        移除后数组的新长度
    """
    slow = 0
    
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    
    return slow


def test_remove_element():
    """测试函数"""
    # 测试用例1
    nums1 = [3, 2, 2, 3]
    val1 = 3
    result1 = remove_element(nums1, val1)
    print(f"测试1: 长度={result1}, 数组={nums1[:result1]}")
    # 期望: 长度=2, 数组=[2,2]
    
    # 测试用例2
    nums2 = [0, 1, 2, 2, 3, 0, 4, 2]
    val2 = 2
    result2 = remove_element(nums2, val2)
    print(f"测试2: 长度={result2}, 数组={nums2[:result2]}")
    # 期望: 长度=5, 数组=[0,1,3,0,4]


if __name__ == "__main__":
    test_remove_element()
