"""
LeetCode 84. 柱状图中最大的矩形
https://leetcode.cn/problems/largest-rectangle-in-histogram/

给定n个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为1。
求在该柱状图中，能够勾勒出来的矩形的最大面积。

单调栈

时间复杂度：O(n)
空间复杂度：O(n)
"""

def largest_rectangle_area(heights):
    """
    柱状图中最大的矩形 - 单调栈法
    
    Args:
        heights: 柱子高度列表
        
    Returns:
        最大矩形面积
    """
    stack = []
    max_area = 0
    
    for i, height in enumerate(heights):
        while stack and height < heights[stack[-1]]:
            h = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * width)
        stack.append(i)
    
    # 处理栈中剩余元素
    while stack:
        h = heights[stack.pop()]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, h * width)
    
    return max_area


def test_largest_rectangle_area():
    """测试函数"""
    # 测试用例1
    heights1 = [2, 1, 5, 6, 2, 3]
    result1 = largest_rectangle_area(heights1)
    print(f"测试1: {result1}")
    # 期望: 10


if __name__ == "__main__":
    test_largest_rectangle_area()
