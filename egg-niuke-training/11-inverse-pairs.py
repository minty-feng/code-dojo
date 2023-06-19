"""
NC117 数组中的逆序对
https://www.nowcoder.com/practice/96bd6684e04a44eb80e6a68efc0ec6c5

在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。
输入一个数组，求出这个数组中的逆序对的总数。

解法：归并排序
在归并排序的过程中统计逆序对

时间复杂度：O(nlogn)
空间复杂度：O(n)
"""

def inverse_pairs(nums):
    """
    归并排序统计逆序对
    """
    def merge_sort(arr, left, right):
        if left >= right:
            return 0
        
        mid = (left + right) // 2
        count = merge_sort(arr, left, mid) + merge_sort(arr, mid + 1, right)
        
        # 合并并统计逆序对
        i, j = left, mid + 1
        temp = []
        
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp.append(arr[i])
                i += 1
            else:
                # arr[i] > arr[j]，则[i, mid]都大于arr[j]
                temp.append(arr[j])
                count += mid - i + 1
                j += 1
        
        temp.extend(arr[i:mid+1])
        temp.extend(arr[j:right+1])
        
        # 复制回原数组
        arr[left:right+1] = temp
        
        return count
    
    return merge_sort(nums, 0, len(nums) - 1) % 1000000007

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, 2, 3, 4, 5, 6, 7, 0],
        [7, 5, 6, 4],
        [1, 2, 3]
    ]
    
    for nums in test_cases:
        count = inverse_pairs(nums[:])
        print(f"数组 {nums} 的逆序对数: {count}")

