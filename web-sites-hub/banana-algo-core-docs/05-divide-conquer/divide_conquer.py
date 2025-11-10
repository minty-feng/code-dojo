"""
分治算法实现
"""

# ========== 快速选择（第K大元素） ==========

def quick_select(nums, k):
    """找第k大元素（平均O(n)）"""
    if not nums:
        return None
    
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x > pivot]
    mid = [x for x in nums if x == pivot]
    right = [x for x in nums if x < pivot]
    
    if k <= len(left):
        return quick_select(left, k)
    elif k <= len(left) + len(mid):
        return mid[0]
    else:
        return quick_select(right, k - len(left) - len(mid))


# ========== 归并排序 ==========

def merge_sort(arr):
    """归并排序"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left, right):
    """合并两个有序数组"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ========== 计算逆序对 ==========

def merge_count(arr):
    """归并排序同时计算逆序对"""
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_count = merge_count(arr[:mid])
    right, right_count = merge_count(arr[mid:])
    
    merged, merge_count_val = merge_and_count(left, right)
    
    return merged, left_count + right_count + merge_count_val


def merge_and_count(left, right):
    """合并并计算跨越两部分的逆序对"""
    result = []
    count = 0
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            count += len(left) - i  # 逆序对数
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result, count


def count_inversions(arr):
    """计算逆序对数量"""
    _, count = merge_count(arr)
    return count


# ========== 最大子数组和（分治） ==========

def max_subarray_divide_conquer(nums, left, right):
    """分治法求最大子数组和"""
    if left == right:
        return nums[left]
    
    mid = (left + right) // 2
    
    # 左半部分最大
    left_max = max_subarray_divide_conquer(nums, left, mid)
    # 右半部分最大
    right_max = max_subarray_divide_conquer(nums, mid + 1, right)
    # 跨中点最大
    cross_max = max_crossing_sum(nums, left, mid, right)
    
    return max(left_max, right_max, cross_max)


def max_crossing_sum(nums, left, mid, right):
    """计算跨越中点的最大子数组和"""
    # 左边最大
    left_sum = float('-inf')
    curr_sum = 0
    for i in range(mid, left - 1, -1):
        curr_sum += nums[i]
        left_sum = max(left_sum, curr_sum)
    
    # 右边最大
    right_sum = float('-inf')
    curr_sum = 0
    for i in range(mid + 1, right + 1):
        curr_sum += nums[i]
        right_sum = max(right_sum, curr_sum)
    
    return left_sum + right_sum


def demo():
    """演示分治算法"""
    print("=== 分治算法演示 ===\n")
    
    # 快速选择
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    print(f"第{k}大元素 {nums}:")
    print(f"  结果: {quick_select(nums, k)}\n")
    
    # 归并排序
    arr = [5, 2, 8, 1, 9, 3]
    print(f"归并排序 {arr}:")
    print(f"  结果: {merge_sort(arr)}\n")
    
    # 逆序对
    arr = [8, 4, 2, 1]
    print(f"逆序对 {arr}:")
    print(f"  数量: {count_inversions(arr)}\n")
    
    # 最大子数组和（分治）
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"最大子数组和 {nums}:")
    result = max_subarray_divide_conquer(nums, 0, len(nums) - 1)
    print(f"  结果: {result}")


if __name__ == '__main__':
    demo()

