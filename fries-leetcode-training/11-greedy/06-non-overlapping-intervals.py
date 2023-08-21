"""
LeetCode 435. 无重叠区间
https://leetcode.cn/problems/non-overlapping-intervals/

给定一个区间的集合intervals，其中intervals[i] = [starti, endi]。
返回需要移除区间的最小数量，使剩余区间互不重叠。

贪心

时间复杂度：O(n log n)
空间复杂度：O(1)
"""

def erase_overlap_intervals(intervals):
    """
    无重叠区间 - 贪心法
    
    Args:
        intervals: 区间集合
        
    Returns:
        需要移除区间的最小数量
    """
    if not intervals:
        return 0
    
    # 按结束时间排序
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            count += 1
        else:
            end = intervals[i][1]
    
    return count


def test_erase_overlap_intervals():
    """测试函数"""
    # 测试用例1
    intervals1 = [[1, 2], [2, 3], [3, 4], [1, 3]]
    result1 = erase_overlap_intervals(intervals1)
    print(f"测试1: {result1}")  # 期望: 1
    
    # 测试用例2
    intervals2 = [[1, 2], [1, 2], [1, 2]]
    result2 = erase_overlap_intervals(intervals2)
    print(f"测试2: {result2}")  # 期望: 2


if __name__ == "__main__":
    test_erase_overlap_intervals()
