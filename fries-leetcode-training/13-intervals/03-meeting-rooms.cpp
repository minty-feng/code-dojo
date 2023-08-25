/**
 * LeetCode 252. 会议室
 * https://leetcode.cn/problems/meeting-rooms/
 * 
 * 给定一个会议时间安排的数组intervals，每个会议时间都会包括开始和结束的时间intervals[i] = [starti, endi]，
 * 请你判断一个人是否能够参加这里面的全部会议。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    bool canAttendMeetings(vector<vector<int>>& intervals) {
        if (intervals.empty() || intervals.size() <= 1) {
            return true;
        }
        
        // 按开始时间排序
        sort(intervals.begin(), intervals.end(), 
             [](const vector<int>& a, const vector<int>& b) {
                 return a[0] < b[0];
             });
        
        // 检查是否有重叠
        for (int i = 1; i < intervals.size(); i++) {
            if (intervals[i][0] < intervals[i-1][1]) {
                return false;
            }
        }
        
        return true;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testCanAttendMeetings() {
    Solution solution;
    
    vector<vector<int>> intervals1 = {{0, 30}, {5, 10}, {15, 20}};
    bool result1 = solution.canAttendMeetings(intervals1);
    cout << "测试1 {{0,30},{5,10},{15,20}}: " << (result1 ? "True" : "False") << endl;  // 期望: False
    
    vector<vector<int>> intervals2 = {{7, 10}, {2, 4}};
    bool result2 = solution.canAttendMeetings(intervals2);
    cout << "测试2 {{7,10},{2,4}}: " << (result2 ? "True" : "False") << endl;  // 期望: True
    
    vector<vector<int>> intervals3 = {{1, 4}, {4, 5}};
    bool result3 = solution.canAttendMeetings(intervals3);
    cout << "测试3 {{1,4},{4,5}}: " << (result3 ? "True" : "False") << endl;  // 期望: True
}

int main() {
    testCanAttendMeetings();
    return 0;
}
