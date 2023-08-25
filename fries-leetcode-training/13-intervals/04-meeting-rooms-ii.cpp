/**
 * LeetCode 253. 会议室II
 * https://leetcode.cn/problems/meeting-rooms-ii/
 * 
 * 给你一个会议时间安排的数组intervals，每个会议时间都会包括开始和结束的时间intervals[i] = [starti, endi]，
 * 返回所需会议室的最小数量。
 * 
 * 贪心/扫描线
 * 
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(n)
 */

class Solution {
public:
    int minMeetingRooms(vector<vector<int>>& intervals) {
        if (intervals.empty()) {
            return 0;
        }
        
        // 提取开始和结束时间
        vector<int> startTimes, endTimes;
        for (const auto& interval : intervals) {
            startTimes.push_back(interval[0]);
            endTimes.push_back(interval[1]);
        }
        
        sort(startTimes.begin(), startTimes.end());
        sort(endTimes.begin(), endTimes.end());
        
        int startPtr = 0, endPtr = 0;
        int rooms = 0;
        
        while (startPtr < intervals.size()) {
            if (startTimes[startPtr] >= endTimes[endPtr]) {
                rooms--;
                endPtr++;
            }
            
            rooms++;
            startPtr++;
        }
        
        return rooms;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testMinMeetingRooms() {
    Solution solution;
    
    vector<vector<int>> intervals1 = {{0, 30}, {5, 10}, {15, 20}};
    int result1 = solution.minMeetingRooms(intervals1);
    cout << "测试1 {{0,30},{5,10},{15,20}}: " << result1 << endl;  // 期望: 2
    
    vector<vector<int>> intervals2 = {{7, 10}, {2, 4}};
    int result2 = solution.minMeetingRooms(intervals2);
    cout << "测试2 {{7,10},{2,4}}: " << result2 << endl;  // 期望: 1
    
    vector<vector<int>> intervals3 = {{1, 4}, {2, 3}, {3, 6}};
    int result3 = solution.minMeetingRooms(intervals3);
    cout << "测试3 {{1,4},{2,3},{3,6}}: " << result3 << endl;  // 期望: 2
}

int main() {
    testMinMeetingRooms();
    return 0;
}
