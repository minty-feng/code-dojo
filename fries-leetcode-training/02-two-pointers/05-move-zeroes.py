"""
LeetCode 283. 移动零
https://leetcode.cn/problems/move-zeroes/

给定一个数组nums，编写一个函数将所有0移动到数组的末尾，同时保持非零元素的相对顺序。

双指针

时间复杂度：O(n)
空间复杂度：O(1)
"""

def move_zeroes(nums):
    """
    移动零 - 双指针法
    
    Args:
        nums: 整数数组
        
    Returns:
        None (原地修改)
    """
    slow = 0
    
    # 将所有非零元素移到前面
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1
    
    # 将剩余位置填充为0
    for i in range(slow, len(nums)):
        nums[i] = 0


def test_move_zeroes():
    """测试函数"""
    # 测试用例1
    nums1 = [0, 1, 0, 3, 12]
    move_zeroes(nums1)
    print(f"测试1: {nums1}")
    # 期望: [1, 3, 12, 0, 0]
    
    # 测试用例2
    nums2 = [0]
    move_zeroes(nums2)
    print(f"测试2: {nums2}")
    # 期望: [0]


if __name__ == "__main__":
    test_move_zeroes()
