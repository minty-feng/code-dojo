/**
 * LeetCode 57. 插入区间
 * https://leetcode.cn/problems/insert-interval/
 * 
 * 给你一个无重叠的，按照区间起始端点排序的区间列表。
 * 在列表中插入一个新的区间，你需要确保列表中的区间仍然有序且不重叠。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> result;
        int i = 0;
        
        // 添加所有在新区间之前的区间
        while (i < intervals.size() && intervals[i][1] < newInterval[0]) {
            result.push_back(intervals[i]);
            i++;
        }
        
        // 合并重叠的区间
        while (i < intervals.size() && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = min(newInterval[0], intervals[i][0]);
            newInterval[1] = max(newInterval[1], intervals[i][1]);
            i++;
        }
        
        result.push_back(newInterval);
        
        // 添加剩余的区间
        while (i < intervals.size()) {
            result.push_back(intervals[i]);
            i++;
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testInsert() {
    Solution solution;
    
    vector<vector<int>> intervals1 = {{1, 3}, {6, 9}};
    vector<int> newInterval1 = {2, 5};
    vector<vector<int>> result1 = solution.insert(intervals1, newInterval1);
    cout << "测试1 intervals={{1,3},{6,9}}, newInterval={2,5}: ";
    for (const auto& interval : result1) {
        cout << "[" << interval[0] << "," << interval[1] << "] ";
    }
    cout << endl;  // 期望: [1,5] [6,9]
    
    vector<vector<int>> intervals2 = {{1, 2}, {3, 5}, {6, 7}, {8, 10}, {12, 16}};
    vector<int> newInterval2 = {4, 8};
    vector<vector<int>> result2 = solution.insert(intervals2, newInterval2);
    cout << "测试2 intervals={{1,2},{3,5},{6,7},{8,10},{12,16}}, newInterval={4,8}: ";
    for (const auto& interval : result2) {
        cout << "[" << interval[0] << "," << interval[1] << "] ";
    }
    cout << endl;  // 期望: [1,2] [3,10] [12,16]
}

int main() {
    testInsert();
    return 0;
}
