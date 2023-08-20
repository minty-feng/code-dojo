"""
NC120 滑动窗口最大值
https://www.nowcoder.com/practice/1624bc35a45c42c0bc17d17fa0cba788

给定一个数组和滑动窗口的大小，找出所有滑动窗口里数值的最大值。

双端队列（单调队列）

时间复杂度：O(n)
空间复杂度：O(k)
"""

from collections import deque

def max_in_windows(nums, size):
    """
    滑动窗口最大值
    """
    if not nums or size <= 0 or size > len(nums):
        return []
    
    result = []
    dq = deque()  # 存储索引
    
    for i in range(len(nums)):
        # 移除超出窗口的元素
        while dq and dq[0] <= i - size:
            dq.popleft()
        
        # 维护单调递减队列
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # 窗口形成后，记录最大值
        if i >= size - 1:
            result.append(nums[dq[0]])
    
    return result

# 测试
if __name__ == "__main__":
    nums = [2, 3, 4, 2, 6, 2, 5, 1]
    size = 3
    
    result = max_in_windows(nums, size)
    print(f"数组: {nums}")
    print(f"窗口大小: {size}")
    print(f"滑动窗口最大值: {result}")

