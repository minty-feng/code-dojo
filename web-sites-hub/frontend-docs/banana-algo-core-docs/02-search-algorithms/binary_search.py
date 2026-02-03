"""
二分查找及变种
"""

def binary_search(arr, target):
    """基本二分查找"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def left_bound(arr, target):
    """查找左边界（第一个>=target的位置）"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left


def right_bound(arr, target):
    """查找右边界（最后一个<=target的位置）"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left - 1


def search_range(arr, target):
    """查找target的起始和结束位置"""
    left = left_bound(arr, target)
    right = right_bound(arr, target)
    
    if left >= len(arr) or arr[left] != target:
        return [-1, -1]
    
    return [left, right]


# ========== 应用 ==========

def my_sqrt(x):
    """求平方根（整数部分）"""
    if x < 2:
        return x
    
    left, right = 1, x // 2
    
    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return right


def search_rotated(nums, target):
    """旋转数组中查找"""
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # 判断哪一半是有序的
        if nums[left] <= nums[mid]:
            # 左半有序
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # 右半有序
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


def find_peak_element(nums):
    """找峰值元素"""
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    
    return left


def demo():
    """演示二分查找"""
    print("=== 二分查找演示 ===\n")
    
    arr = [1, 2, 2, 2, 3, 4, 5, 5, 6]
    target = 2
    
    print(f"数组: {arr}")
    print(f"目标: {target}\n")
    
    print(f"基本查找: {binary_search(arr, target)}")
    print(f"左边界: {left_bound(arr, target)}")
    print(f"右边界: {right_bound(arr, target)}")
    print(f"查找范围: {search_range(arr, target)}\n")
    
    # 平方根
    x = 8
    print(f"sqrt({x}) = {my_sqrt(x)}\n")
    
    # 旋转数组
    rotated = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    print(f"旋转数组: {rotated}")
    print(f"查找 {target}: {search_rotated(rotated, target)}\n")
    
    # 峰值
    nums = [1, 2, 3, 1]
    print(f"数组: {nums}")
    print(f"峰值索引: {find_peak_element(nums)}")


if __name__ == '__main__':
    demo()

