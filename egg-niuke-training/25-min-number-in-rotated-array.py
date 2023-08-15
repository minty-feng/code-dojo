"""
NC88 旋转数组的最小数字
https://www.nowcoder.com/practice/9f3231a991af4f55b95579b44b7a01ba

把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。
输入一个非递减排序的数组的一个旋转，输出旋转数组的最小元素。

二分查找变形

时间复杂度：O(logn)
空间复杂度：O(1)
"""

def min_number_in_rotated_array(nums):
    """
    旋转数组的最小数字
    """
    if not nums:
        return -1
    
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            # 最小值在右半部分
            left = mid + 1
        elif nums[mid] < nums[right]:
            # 最小值在左半部分（包括mid）
            right = mid
        else:
            # nums[mid] == nums[right]，无法确定，right--
            right -= 1
    
    return nums[left]

# 测试
if __name__ == "__main__":
    test_cases = [
        [3, 4, 5, 1, 2],
        [2, 2, 2, 0, 1],
        [1, 0, 1, 1, 1],
        [1, 2, 3, 4, 5]
    ]
    
    for nums in test_cases:
        result = min_number_in_rotated_array(nums)
        print(f"数组 {nums} 的最小值: {result}")

