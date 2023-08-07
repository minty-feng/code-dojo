/**
 * LeetCode 42. 接雨水
 * https://leetcode.cn/problems/trapping-rain-water/
 * 
 * 给定n个非负整数表示每个宽度为1的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
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
    int trap(vector<int>& height) {
        stack<int> st;
        int water = 0;
        
        for (int i = 0; i < height.size(); i++) {
            while (!st.empty() && height[i] > height[st.top()]) {
                int bottom = st.top();
                st.pop();
                
                if (st.empty()) {
                    break;
                }
                
                int width = i - st.top() - 1;
                int water_height = min(height[st.top()], height[i]) - height[bottom];
                water += width * water_height;
            }
            st.push(i);
        }
        
        return water;
    }
};

// 测试函数
#include <iostream>
void testTrap() {
    Solution solution;
    
    vector<int> height1 = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
    int result1 = solution.trap(height1);
    cout << "测试1: " << result1 << endl;  // 期望: 6
    
    vector<int> height2 = {4, 2, 0, 3, 2, 5};
    int result2 = solution.trap(height2);
    cout << "测试2: " << result2 << endl;  // 期望: 9
}

int main() {
    testTrap();
    return 0;
}
