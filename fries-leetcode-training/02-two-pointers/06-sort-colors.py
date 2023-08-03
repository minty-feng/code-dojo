"""
LeetCode 75. 颜色分类
https://leetcode.cn/problems/sort-colors/

给定一个包含红色、白色和蓝色，一共n个元素的数组，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

三指针（荷兰国旗问题）

时间复杂度：O(n)
空间复杂度：O(1)
"""

def sort_colors(nums):
    """
    颜色分类 - 三指针法（荷兰国旗问题）
    
    Args:
        nums: 包含0,1,2的数组
        
    Returns:
        None (原地修改)
    """
    left = 0  # 0的右边界
    right = len(nums) - 1  # 2的左边界
    current = 0  # 当前指针
    
    while current <= right:
        if nums[current] == 0:
            # 交换到左边界
            nums[left], nums[current] = nums[current], nums[left]
            left += 1
            current += 1
        elif nums[current] == 2:
            # 交换到右边界
            nums[right], nums[current] = nums[current], nums[right]
            right -= 1
            # current不增加，因为交换过来的元素需要重新检查
        else:
            # nums[current] == 1，直接跳过
            current += 1


def test_sort_colors():
    """测试函数"""
    # 测试用例1
    nums1 = [2, 0, 2, 1, 1, 0]
    sort_colors(nums1)
    print(f"测试1: {nums1}")
    # 期望: [0, 0, 1, 1, 2, 2]
    
    # 测试用例2
    nums2 = [2, 0, 1]
    sort_colors(nums2)
    print(f"测试2: {nums2}")
    # 期望: [0, 1, 2]
    
    # 测试用例3
    nums3 = [0]
    sort_colors(nums3)
    print(f"测试3: {nums3}")
    # 期望: [0]


if __name__ == "__main__":
    test_sort_colors()
