"""
LeetCode 252. 会议室
https://leetcode.cn/problems/meeting-rooms/

给定一个会议时间安排的数组intervals，每个会议时间都会包括开始和结束的时间intervals[i] = [starti, endi]，
请你判断一个人是否能够参加这里面的全部会议。

贪心

时间复杂度：O(n log n)
空间复杂度：O(1)
"""

def can_attend_meetings(intervals):
    """
    会议室 - 贪心法
    
    Args:
        intervals: 会议时间数组
        
    Returns:
        是否能够参加全部会议
    """
    if not intervals or len(intervals) <= 1:
        return True
    
    # 按开始时间排序
    intervals.sort(key=lambda x: x[0])
    
    # 检查是否有重叠
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    
    return True


def can_attend_meetings_brute_force(intervals):
    """
    会议室 - 暴力法
    
    Args:
        intervals: 会议时间数组
        
    Returns:
        是否能够参加全部会议
    """
    if not intervals or len(intervals) <= 1:
        return True
    
    # 检查每对区间是否重叠
    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            if intervals_overlap(intervals[i], intervals[j]):
                return False
    
    return True


def intervals_overlap(interval1, interval2):
    """
    判断两个区间是否重叠
    
    Args:
        interval1: 第一个区间
        interval2: 第二个区间
        
    Returns:
        是否重叠
    """
    return not (interval1[1] <= interval2[0] or interval2[1] <= interval1[0])


def test_can_attend_meetings():
    """测试函数"""
    # 测试用例1
    intervals1 = [[0, 30], [5, 10], [15, 20]]
    result1 = can_attend_meetings(intervals1)
    result1_bf = can_attend_meetings_brute_force(intervals1)
    print(f"测试1 {intervals1}: Greedy={result1}, BF={result1_bf}")  # 期望: False
    
    # 测试用例2
    intervals2 = [[7, 10], [2, 4]]
    result2 = can_attend_meetings(intervals2)
    result2_bf = can_attend_meetings_brute_force(intervals2)
    print(f"测试2 {intervals2}: Greedy={result2}, BF={result2_bf}")  # 期望: True
    
    # 测试用例3
    intervals3 = [[1, 4], [4, 5]]
    result3 = can_attend_meetings(intervals3)
    result3_bf = can_attend_meetings_brute_force(intervals3)
    print(f"测试3 {intervals3}: Greedy={result3}, BF={result3_bf}")  # 期望: True


if __name__ == "__main__":
    test_can_attend_meetings()
