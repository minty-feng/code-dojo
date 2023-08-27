"""
NC41 最长无重复子数组
https://www.nowcoder.com/practice/b56799ebfd684fb394bd315e89324fb4

给定一个数组arr，返回arr的最长无重复元素子数组的长度。

滑动窗口 + 哈希表

时间复杂度：O(n)
空间复杂度：O(n)
"""

def max_length(arr):
    """
    最长无重复子数组
    """
    if not arr:
        return 0
    
    char_map = {}
    left = 0
    max_len = 0
    
    for right in range(len(arr)):
        if arr[right] in char_map and char_map[arr[right]] >= left:
            # 更新左边界
            left = char_map[arr[right]] + 1
        
        char_map[arr[right]] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len

# 测试
if __name__ == "__main__":
    test_cases = [
        [2, 3, 4, 5],
        [2, 2, 3, 4, 3],
        [1, 2, 3, 1, 2, 3, 2, 2],
        [1, 1, 1, 1]
    ]
    
    for arr in test_cases:
        result = max_length(arr)
        print(f"数组: {arr}")
        print(f"最长无重复子数组长度: {result}\n")

