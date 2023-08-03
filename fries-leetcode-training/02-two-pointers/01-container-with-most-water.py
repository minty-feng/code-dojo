"""
LeetCode 11. 盛最多水的容器
https://leetcode.cn/problems/container-with-most-water/

给定一个长度为n的整数数组height。有n条垂线，第i条线的两个端点是(i, 0)和(i, height[i])。
找出其中的两条线，使得它们与x轴共同构成的容器可以容纳最多的水。

双指针（对撞指针）

时间复杂度：O(n)
空间复杂度：O(1)
"""

def max_area(height):
    """
    盛最多水的容器 - 双指针
    """
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # 计算当前容器的面积
        width = right - left
        h = min(height[left], height[right])
        area = width * h
        max_water = max(max_water, area)
        
        # 移动较短的边
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, 8, 6, 2, 5, 4, 8, 3, 7],
        [1, 1],
        [4, 3, 2, 1, 4]
    ]
    
    for height in test_cases:
        result = max_area(height)
        print(f"高度数组: {height}")
        print(f"最大面积: {result}\n")

