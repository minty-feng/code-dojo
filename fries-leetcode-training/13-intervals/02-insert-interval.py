"""
LeetCode 57. 插入区间
https://leetcode.cn/problems/insert-interval/

给你一个无重叠的，按照区间起始端点排序的区间列表。
在列表中插入一个新的区间，你需要确保列表中的区间仍然有序且不重叠。

贪心

时间复杂度：O(n)
空间复杂度：O(1)
"""

def insert(intervals, new_interval):
    """
    插入区间 - 贪心法
    
    Args:
        intervals: 无重叠的区间列表
        new_interval: 要插入的新区间
        
    Returns:
        插入后的区间列表
    """
    result = []
    i = 0
    
    # 添加所有在新区间之前的区间
    while i < len(intervals) and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # 合并重叠的区间
    while i < len(intervals) and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    
    result.append(new_interval)
    
    # 添加剩余的区间
    while i < len(intervals):
        result.append(intervals[i])
        i += 1
    
    return result


def insert_merge(intervals, new_interval):
    """
    插入区间 - 合并法
    
    Args:
        intervals: 无重叠的区间列表
        new_interval: 要插入的新区间
        
    Returns:
        插入后的区间列表
    """
    # 将新区间添加到列表中
    intervals.append(new_interval)
    
    # 按开始时间排序
    intervals.sort(key=lambda x: x[0])
    
    # 合并重叠区间
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    
    return merged


def test_insert():
    """测试函数"""
    # 测试用例1
    intervals1 = [[1, 3], [6, 9]]
    new_interval1 = [2, 5]
    result1 = insert(intervals1, new_interval1)
    result1_merge = insert_merge(intervals1[:], new_interval1)
    print(f"测试1 intervals={intervals1}, new_interval={new_interval1}: {result1}")  # 期望: [[1,5],[6,9]]
    print(f"测试1 merge方法: {result1_merge}")
    
    # 测试用例2
    intervals2 = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
    new_interval2 = [4, 8]
    result2 = insert(intervals2, new_interval2)
    result2_merge = insert_merge(intervals2[:], new_interval2)
    print(f"测试2 intervals={intervals2}, new_interval={new_interval2}: {result2}")  # 期望: [[1,2],[3,10],[12,16]]
    print(f"测试2 merge方法: {result2_merge}")
    
    # 测试用例3
    intervals3 = []
    new_interval3 = [5, 7]
    result3 = insert(intervals3, new_interval3)
    result3_merge = insert_merge(intervals3[:], new_interval3)
    print(f"测试3 intervals={intervals3}, new_interval={new_interval3}: {result3}")  # 期望: [[5,7]]
    print(f"测试3 merge方法: {result3_merge}")


if __name__ == "__main__":
    test_insert()
