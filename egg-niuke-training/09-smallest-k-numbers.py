"""
NC119 最小的K个数
https://www.nowcoder.com/practice/6a296eb82cf844ca8539b57c23e6e9bf

给定一个长度为 n 的可能有重复值的数组，找出其中不去重的最小的 k 个数。

解法1：堆（推荐）
解法2：快速选择
解法3：排序

时间复杂度：O(nlogk) - 堆
空间复杂度：O(k)
"""

import heapq

def get_least_numbers_heap(arr, k):
    """
    方法1：大顶堆
    维护大小为k的大顶堆
    """
    if k == 0 or not arr:
        return []
    
    # Python的heapq是小顶堆，用负数模拟大顶堆
    heap = []
    
    for num in arr:
        if len(heap) < k:
            heapq.heappush(heap, -num)
        elif -heap[0] > num:
            heapq.heapreplace(heap, -num)
    
    return sorted([-x for x in heap])

def get_least_numbers_quickselect(arr, k):
    """
    方法2：快速选择
    """
    if k == 0 or not arr:
        return []
    
    def partition(left, right):
        pivot = arr[right]
        i = left
        for j in range(left, right):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[right] = arr[right], arr[i]
        return i
    
    def quickselect(left, right, k):
        if left == right:
            return
        
        pos = partition(left, right)
        
        if pos == k:
            return
        elif pos < k:
            quickselect(pos + 1, right, k)
        else:
            quickselect(left, pos - 1, k)
    
    quickselect(0, len(arr) - 1, k)
    return sorted(arr[:k])

# 测试
if __name__ == "__main__":
    arr = [4, 5, 1, 6, 2, 7, 3, 8]
    k = 4
    
    print(f"数组: {arr}")
    print(f"最小的{k}个数: {get_least_numbers_heap(arr[:], k)}")
    print(f"快速选择: {get_least_numbers_quickselect(arr[:], k)}")

