/**
 * LeetCode 84. 柱状图中最大的矩形
 * https://leetcode.cn/problems/largest-rectangle-in-histogram/
 * 
 * 给定n个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为1。
 * 求在该柱状图中，能够勾勒出来的矩形的最大面积。
 * 
 * 单调栈
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> st;
        int max_area = 0;
        
        for (int i = 0; i < heights.size(); i++) {
            while (!st.empty() && heights[i] < heights[st.top()]) {
                int h = heights[st.top()];
                st.pop();
                int width = st.empty() ? i : i - st.top() - 1;
                max_area = max(max_area, h * width);
            }
            st.push(i);
        }
        
        while (!st.empty()) {
            int h = heights[st.top()];
            st.pop();
            int width = st.empty() ? heights.size() : heights.size() - st.top() - 1;
            max_area = max(max_area, h * width);
        }
        
        return max_area;
    }
};

// 测试函数
#include <iostream>
void testLargestRectangleArea() {
    Solution solution;
    
    vector<int> heights = {2, 1, 5, 6, 2, 3};
    int result = solution.largestRectangleArea(heights);
    
    cout << "测试1: " << result << endl;  // 期望: 10
}

int main() {
    testLargestRectangleArea();
    return 0;
}
