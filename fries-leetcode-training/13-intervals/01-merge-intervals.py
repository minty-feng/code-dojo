"""
LeetCode 56. 合并区间
https://leetcode.cn/problems/merge-intervals/

以数组intervals表示若干个区间的集合，其中单个区间为intervals[i] = [starti, endi]。
请你合并所有重叠的区间，并返回一个不重叠的区间数组。

排序 + 贪心

时间复杂度：O(n log n)
空间复杂度：O(1)
"""

def merge_intervals(intervals):
    """
    合并区间 - 排序 + 贪心法
    
    Args:
        intervals: 区间数组
        
    Returns:
        合并后的区间数组
    """
    if not intervals:
        return []
    
    # 按开始时间排序
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        
        # 如果当前区间与最后一个区间重叠
        if current[0] <= last[1]:
            # 合并区间
            last[1] = max(last[1], current[1])
        else:
            # 不重叠，添加新区间
            merged.append(current)
    
    return merged


def test_merge_intervals():
    """测试函数"""
    # 测试用例1
    intervals1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
    result1 = merge_intervals(intervals1)
    print(f"测试1: {result1}")
    # 期望: [[1, 6], [8, 10], [15, 18]]
    
    # 测试用例2
    intervals2 = [[1, 4], [4, 5]]
    result2 = merge_intervals(intervals2)
    print(f"测试2: {result2}")
    # 期望: [[1, 5]]
    
    # 测试用例3
    intervals3 = [[1, 4], [0, 4]]
    result3 = merge_intervals(intervals3)
    print(f"测试3: {result3}")
    # 期望: [[0, 4]]


if __name__ == "__main__":
    test_merge_intervals()
