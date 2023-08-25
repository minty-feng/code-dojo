# 13-intervals (区间)

LeetCode精选75题 - 区间专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 合并区间 | ⭐⭐ | [56](https://leetcode.cn/problems/merge-intervals/) | [01-merge-intervals.py](./01-merge-intervals.py) | [01-merge-intervals.cpp](./01-merge-intervals.cpp) |
| 02 | 插入区间 | ⭐⭐ | [57](https://leetcode.cn/problems/insert-interval/) | [02-insert-interval.py](./02-insert-interval.py) | [02-insert-interval.cpp](./02-insert-interval.cpp) |
| 03 | 会议室 | ⭐ | [252](https://leetcode.cn/problems/meeting-rooms/) | [03-meeting-rooms.py](./03-meeting-rooms.py) | [03-meeting-rooms.cpp](./03-meeting-rooms.cpp) |
| 04 | 会议室II | ⭐⭐ | [253](https://leetcode.cn/problems/meeting-rooms-ii/) | [04-meeting-rooms-ii.py](./04-meeting-rooms-ii.py) | [04-meeting-rooms-ii.cpp](./04-meeting-rooms-ii.cpp) |

## 🎯 核心技巧

### 区间合并
- **[合并区间](./01-merge-intervals.py)**：按开始时间排序，合并重叠区间
- **[插入区间](./02-insert-interval.py)**：插入新区间并合并

### 会议室问题
- **[会议室](./03-meeting-rooms.py)**：检测区间是否重叠
- **[会议室II](./04-meeting-rooms-ii.py)**：最小会议室数量

---

## 💡 解题模板

### 区间合并模板
```python
def merge_intervals(intervals):
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    
    return merged
```

### 会议室II模板
```python
def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    
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
```

---

## 📚 学习重点

1. **区间排序**：按开始时间或结束时间排序
2. **重叠检测**：判断两个区间是否重叠
3. **贪心策略**：区间问题的贪心选择
4. **扫描线算法**：处理区间重叠问题
