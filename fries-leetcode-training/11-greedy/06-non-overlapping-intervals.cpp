/**
 * LeetCode 435. 无重叠区间
 * https://leetcode.cn/problems/non-overlapping-intervals/
 * 
 * 给定一个区间的集合intervals，其中intervals[i] = [starti, endi]。
 * 返回需要移除区间的最小数量，使剩余区间互不重叠。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        if (intervals.empty()) {
            return 0;
        }
        
        // 按结束时间排序
        sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[1] < b[1];
        });
        
        int count = 0;
        int end = intervals[0][1];
        
        for (int i = 1; i < intervals.size(); i++) {
            if (intervals[i][0] < end) {
                count++;
            } else {
                end = intervals[i][1];
            }
        }
        
        return count;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testEraseOverlapIntervals() {
    Solution solution;
    
    vector<vector<int>> intervals1 = {{1, 2}, {2, 3}, {3, 4}, {1, 3}};
    int result1 = solution.eraseOverlapIntervals(intervals1);
    cout << "测试1 {{1,2},{2,3},{3,4},{1,3}}: " << result1 << endl;  // 期望: 1
    
    vector<vector<int>> intervals2 = {{1, 2}, {1, 2}, {1, 2}};
    int result2 = solution.eraseOverlapIntervals(intervals2);
    cout << "测试2 {{1,2},{1,2},{1,2}}: " << result2 << endl;  // 期望: 2
    
    vector<vector<int>> intervals3 = {{1, 2}, {2, 3}};
    int result3 = solution.eraseOverlapIntervals(intervals3);
    cout << "测试3 {{1,2},{2,3}}: " << result3 << endl;  // 期望: 0
}

int main() {
    testEraseOverlapIntervals();
    return 0;
}
