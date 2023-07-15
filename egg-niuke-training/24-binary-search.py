"""
NC7 二分查找
https://www.nowcoder.com/practice/d3df40bd23594118b57554129cadf47b

请实现无重复数字的升序数组的二分查找。

时间复杂度：O(logn)
空间复杂度：O(1)
"""

def binary_search(nums, target):
    """
    二分查找
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def binary_search_recursive(nums, target):
    """
    二分查找 - 递归版本
    """
    def search(left, right):
        if left > right:
            return -1
        
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return search(mid + 1, right)
        else:
            return search(left, mid - 1)
    
    return search(0, len(nums) - 1)

# 测试
if __name__ == "__main__":
    nums = [1, 3, 5, 7, 9, 11, 13, 15]
    
    for target in [7, 10, 1, 15]:
        result = binary_search(nums, target)
        print(f"查找 {target}: 索引 {result}")

