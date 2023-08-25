/**
 * LeetCode 56. 合并区间
 * https://leetcode.cn/problems/merge-intervals/
 * 
 * 以数组intervals表示若干个区间的集合，其中单个区间为intervals[i] = [starti, endi]。
 * 请你合并所有重叠的区间，并返回一个不重叠的区间数组。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        if (intervals.empty()) {
            return {};
        }
        
        // 按开始时间排序
        sort(intervals.begin(), intervals.end(), 
             [](const vector<int>& a, const vector<int>& b) {
                 return a[0] < b[0];
             });
        
        vector<vector<int>> merged;
        merged.push_back(intervals[0]);
        
        for (int i = 1; i < intervals.size(); i++) {
            vector<int>& last = merged.back();
            vector<int>& current = intervals[i];
            
            if (current[0] <= last[1]) {
                // 重叠，合并区间
                last[1] = max(last[1], current[1]);
            } else {
                // 不重叠，添加新区间
                merged.push_back(current);
            }
        }
        
        return merged;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testMerge() {
    Solution solution;
    
    vector<vector<int>> intervals1 = {{1, 3}, {2, 6}, {8, 10}, {15, 18}};
    vector<vector<int>> result1 = solution.merge(intervals1);
    cout << "测试1 {{1,3},{2,6},{8,10},{15,18}}: ";
    for (const auto& interval : result1) {
        cout << "[" << interval[0] << "," << interval[1] << "] ";
    }
    cout << endl;  // 期望: [1,6] [8,10] [15,18]
    
    vector<vector<int>> intervals2 = {{1, 4}, {4, 5}};
    vector<vector<int>> result2 = solution.merge(intervals2);
    cout << "测试2 {{1,4},{4,5}}: ";
    for (const auto& interval : result2) {
        cout << "[" << interval[0] << "," << interval[1] << "] ";
    }
    cout << endl;  // 期望: [1,5]
}

int main() {
    testMerge();
    return 0;
}
