"""
经典排序算法实现
"""

def bubble_sort(arr):
    """冒泡排序：O(n²)
    重复遍历，相邻元素逆序则交换
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # 优化：一轮没交换则已有序
            break
    return arr


def selection_sort(arr):
    """选择排序：O(n²)
    每次选择最小元素放到已排序部分末尾
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    """插入排序：O(n²)
    将元素插入到已排序部分的正确位置
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    """归并排序：O(n log n)
    分治策略：分割→递归排序→合并
    """
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


def quick_sort(arr):
    """快速排序：O(n log n)平均
    选择pivot，分区，递归
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr, low=0, high=None):
    """原地快速排序"""
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)
    
    return arr


def partition(arr, low, high):
    """分区函数"""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def heap_sort(arr):
    """堆排序：O(n log n)
    建最大堆，反复取堆顶
    """
    n = len(arr)
    
    # 建堆
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # 排序
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr


def heapify(arr, n, i):
    """堆调整"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def counting_sort(arr):
    """计数排序：O(n + k)
    适用于整数，范围不大
    """
    if not arr:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    range_size = max_val - min_val + 1
    count = [0] * range_size
    
    # 计数
    for num in arr:
        count[num - min_val] += 1
    
    # 累加
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # 输出
    output = [0] * len(arr)
    for num in reversed(arr):  # 逆序保证稳定性
        index = count[num - min_val] - 1
        output[index] = num
        count[num - min_val] -= 1
    
    return output


def test_sorting_algorithms():
    """测试所有排序算法"""
    import random
    import time
    
    test_cases = [
        ([5, 2, 8, 1, 9], "小规模随机"),
        ([1, 2, 3, 4, 5], "已排序"),
        ([5, 4, 3, 2, 1], "逆序"),
        ([3, 3, 2, 1, 2], "重复元素"),
        (list(range(1000, 0, -1)), "大规模逆序")
    ]
    
    algorithms = [
        ("冒泡排序", bubble_sort),
        ("选择排序", selection_sort),
        ("插入排序", insertion_sort),
        ("归并排序", merge_sort),
        ("快速排序", quick_sort),
        ("原地快排", lambda arr: quick_sort_inplace(arr.copy())),
        ("堆排序", heap_sort),
        ("计数排序", counting_sort)
    ]
    
    print("=== 排序算法测试 ===\n")
    
    for arr, desc in test_cases[:4]:  # 跳过大规模测试
        print(f"测试用例: {desc}")
        print(f"原数组: {arr[:10]}{'...' if len(arr) > 10 else ''}")
        
        for name, func in algorithms:
            test_arr = arr.copy()
            start = time.time()
            result = func(test_arr)
            elapsed = time.time() - start
            
            is_sorted = result == sorted(arr)
            status = "✅" if is_sorted else "❌"
            print(f"{status} {name:12s}: {elapsed*1000:.3f}ms")
        
        print()


if __name__ == '__main__':
    test_sorting_algorithms()

