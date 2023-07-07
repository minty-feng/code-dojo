"""
NC60 数组中重复的数字
https://www.nowcoder.com/practice/6fe361ede7e54db1b84adc81d09d8524

在一个长度为n的数组里的所有数字都在0到n-1的范围内。
数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。
请找出数组中任意一个重复的数字。

解法1：哈希表 O(n) 空间O(n)
解法2：原地哈希 O(n) 空间O(1)
解法3：排序 O(nlogn) 空间O(1)

时间复杂度：O(n)
空间复杂度：O(1)
"""

def find_duplicate_hash(nums):
    """
    方法1：哈希表
    """
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
    return -1

def find_duplicate_inplace(nums):
    """
    方法2：原地哈希
    利用nums[i]应该放在索引为nums[i]的位置
    """
    for i in range(len(nums)):
        while nums[i] != i:
            # nums[i]应该放在索引nums[i]的位置
            if nums[i] == nums[nums[i]]:
                return nums[i]  # 找到重复
            
            # 交换到正确位置
            j = nums[i]
            nums[i], nums[j] = nums[j], nums[i]
    
    return -1

def find_duplicate_sort(nums):
    """
    方法3：排序
    """
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return nums[i]
    return -1

# 测试
if __name__ == "__main__":
    test_cases = [
        [2, 3, 1, 0, 2, 5, 3],
        [0, 1, 2, 3, 4, 5, 1],
        [1, 1, 1, 1, 1]
    ]
    
    for nums in test_cases:
        # 复制数组用于不同方法测试
        result1 = find_duplicate_hash(nums[:])
        result2 = find_duplicate_inplace(nums[:])
        result3 = find_duplicate_sort(nums[:])
        
        print(f"数组: {nums}")
        print(f"哈希表: {result1}")
        print(f"原地哈希: {result2}")
        print(f"排序: {result3}\n")

