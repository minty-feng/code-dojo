"""
LeetCode 253. 会议室II
https://leetcode.cn/problems/meeting-rooms-ii/

给你一个会议时间安排的数组intervals，每个会议时间都会包括开始和结束的时间intervals[i] = [starti, endi]，
返回所需会议室的最小数量。

贪心/扫描线

时间复杂度：O(n log n)
空间复杂度：O(n)
"""

def min_meeting_rooms(intervals):
    """
    会议室II - 扫描线法
    
    Args:
        intervals: 会议时间数组
        
    Returns:
        最小会议室数量
    """
    if not intervals:
        return 0
    
    # 提取开始和结束时间
    start_times = sorted([interval[0] for interval in intervals])
    end_times = sorted([interval[1] for interval in intervals])
    
    start_ptr = end_ptr = 0
    rooms = 0
    
    while start_ptr < len(intervals):
        if start_times[start_ptr] >= end_times[end_ptr]:
            rooms -= 1
            end_ptr += 1
        
        rooms += 1
        start_ptr += 1
    
    return rooms


def min_meeting_rooms_heap(intervals):
    """
    会议室II - 堆法
    
    Args:
        intervals: 会议时间数组
        
    Returns:
        最小会议室数量
    """
    if not intervals:
        return 0
    
    import heapq
    
    # 按开始时间排序
    intervals.sort(key=lambda x: x[0])
    
    # 使用最小堆存储结束时间
    heap = []
    
    for interval in intervals:
        start, end = interval
        
        # 如果当前会议开始时，有会议室已经结束
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        
        # 将当前会议的结束时间加入堆
        heapq.heappush(heap, end)
    
    return len(heap)


def min_meeting_rooms_events(intervals):
    """
    会议室II - 事件法
    
    Args:
        intervals: 会议时间数组
        
    Returns:
        最小会议室数量
    """
    if not intervals:
        return 0
    
    events = []
    
    # 创建事件：开始时间+1，结束时间-1
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    
    # 按时间排序
    events.sort()
    
    rooms = 0
    max_rooms = 0
    
    for time, delta in events:
        rooms += delta
        max_rooms = max(max_rooms, rooms)
    
    return max_rooms


def test_min_meeting_rooms():
    """测试函数"""
    # 测试用例1
    intervals1 = [[0, 30], [5, 10], [15, 20]]
    result1 = min_meeting_rooms(intervals1)
    result1_heap = min_meeting_rooms_heap(intervals1)
    result1_events = min_meeting_rooms_events(intervals1)
    print(f"测试1 {intervals1}: Scan={result1}, Heap={result1_heap}, Events={result1_events}")  # 期望: 2
    
    # 测试用例2
    intervals2 = [[7, 10], [2, 4]]
    result2 = min_meeting_rooms(intervals2)
    result2_heap = min_meeting_rooms_heap(intervals2)
    result2_events = min_meeting_rooms_events(intervals2)
    print(f"测试2 {intervals2}: Scan={result2}, Heap={result2_heap}, Events={result2_events}")  # 期望: 1
    
    # 测试用例3
    intervals3 = [[1, 4], [2, 3], [3, 6]]
    result3 = min_meeting_rooms(intervals3)
    result3_heap = min_meeting_rooms_heap(intervals3)
    result3_events = min_meeting_rooms_events(intervals3)
    print(f"测试3 {intervals3}: Scan={result3}, Heap={result3_heap}, Events={result3_events}")  # 期望: 2


if __name__ == "__main__":
    test_min_meeting_rooms()
