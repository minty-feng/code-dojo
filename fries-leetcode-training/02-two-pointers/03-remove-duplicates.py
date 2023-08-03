"""
LeetCode 26. 删除排序数组中的重复项
https://leetcode.cn/problems/remove-duplicates-from-sorted-array/

给你一个升序排列的数组nums，请你原地删除重复出现的元素，使每个元素只出现一次，返回删除后数组的新长度。

快慢指针

时间复杂度：O(n)
空间复杂度：O(1)
"""

def remove_duplicates(nums):
    """
    删除排序数组中的重复项 - 快慢指针
    """
    if not nums:
        return 0
    
    slow = 0
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, 1, 2],
        [0, 0, 1, 1, 1, 2, 2, 3, 3, 4],
        [1, 2, 3],
        [1]
    ]
    
    for nums in test_cases:
        original = nums[:]
        length = remove_duplicates(nums)
        print(f"原数组: {original}")
        print(f"去重后长度: {length}")
        print(f"去重后数组: {nums[:length]}\n")

