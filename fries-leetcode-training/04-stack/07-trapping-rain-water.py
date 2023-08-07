"""
LeetCode 42. 接雨水
https://leetcode.cn/problems/trapping-rain-water/

给定n个非负整数表示每个宽度为1的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

单调栈

时间复杂度：O(n)
空间复杂度：O(n)
"""

def trap(height):
    """
    接雨水 - 单调栈法
    
    Args:
        height: 柱子高度列表
        
    Returns:
        能接的雨水总量
    """
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            width = i - stack[-1] - 1
            water_height = min(height[stack[-1]], h) - height[bottom]
            water += width * water_height
        stack.append(i)
    
    return water


def test_trap():
    """测试函数"""
    # 测试用例1
    height1 = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    result1 = trap(height1)
    print(f"测试1: {result1}")
    # 期望: 6
    
    # 测试用例2
    height2 = [4, 2, 0, 3, 2, 5]
    result2 = trap(height2)
    print(f"测试2: {result2}")
    # 期望: 9


if __name__ == "__main__":
    test_trap()
