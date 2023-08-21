"""
LeetCode 452. 用最少数量的箭引爆气球
https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/

有一些球形气球贴在一堵用XY平面表示的墙上。墙上的气球用一个二维数组points表示，
其中points[i] = [xstart, xend]表示水平直径在xstart和xend之间的气球。

贪心

时间复杂度：O(n log n)
空间复杂度：O(1)
"""

def find_min_arrow_shots(points):
    """
    用最少数量的箭引爆气球 - 贪心法
    
    Args:
        points: 气球坐标数组
        
    Returns:
        最少需要的箭数
    """
    if not points:
        return 0
    
    # 按结束位置排序
    points.sort(key=lambda x: x[1])
    
    arrows = 1
    end = points[0][1]
    
    for i in range(1, len(points)):
        # 如果当前气球的开始位置大于上一支箭的结束位置
        if points[i][0] > end:
            arrows += 1
            end = points[i][1]
    
    return arrows


def test_find_min_arrow_shots():
    """测试函数"""
    # 测试用例1
    points1 = [[10, 16], [2, 8], [1, 6], [7, 12]]
    result1 = find_min_arrow_shots(points1)
    print(f"测试1 {points1}: {result1}")  # 期望: 2
    
    # 测试用例2
    points2 = [[1, 2], [3, 4], [5, 6], [7, 8]]
    result2 = find_min_arrow_shots(points2)
    print(f"测试2 {points2}: {result2}")  # 期望: 4
    
    # 测试用例3
    points3 = [[1, 2], [2, 3], [3, 4], [4, 5]]
    result3 = find_min_arrow_shots(points3)
    print(f"测试3 {points3}: {result3}")  # 期望: 2


if __name__ == "__main__":
    test_find_min_arrow_shots()
