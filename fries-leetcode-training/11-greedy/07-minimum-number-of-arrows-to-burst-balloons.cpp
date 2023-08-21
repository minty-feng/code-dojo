/**
 * LeetCode 452. 用最少数量的箭引爆气球
 * https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/
 * 
 * 有一些球形气球贴在一堵用XY平面表示的墙上。墙上的气球用一个二维数组points表示，
 * 其中points[i] = [xstart, xend]表示水平直径在xstart和xend之间的气球。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int findMinArrowShots(vector<vector<int>>& points) {
        if (points.empty()) {
            return 0;
        }
        
        // 按结束位置排序
        sort(points.begin(), points.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[1] < b[1];
        });
        
        int arrows = 1;
        int end = points[0][1];
        
        for (int i = 1; i < points.size(); i++) {
            // 如果当前气球的开始位置大于上一支箭的结束位置
            if (points[i][0] > end) {
                arrows++;
                end = points[i][1];
            }
        }
        
        return arrows;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testFindMinArrowShots() {
    Solution solution;
    
    vector<vector<int>> points1 = {{10, 16}, {2, 8}, {1, 6}, {7, 12}};
    int result1 = solution.findMinArrowShots(points1);
    cout << "测试1 {{10,16},{2,8},{1,6},{7,12}}: " << result1 << endl;  // 期望: 2
    
    vector<vector<int>> points2 = {{1, 2}, {3, 4}, {5, 6}, {7, 8}};
    int result2 = solution.findMinArrowShots(points2);
    cout << "测试2 {{1,2},{3,4},{5,6},{7,8}}: " << result2 << endl;  // 期望: 4
    
    vector<vector<int>> points3 = {{1, 2}, {2, 3}, {3, 4}, {4, 5}};
    int result3 = solution.findMinArrowShots(points3);
    cout << "测试3 {{1,2},{2,3},{3,4},{4,5}}: " << result3 << endl;  // 期望: 2
}

int main() {
    testFindMinArrowShots();
    return 0;
}
