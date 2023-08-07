/**
 * LeetCode 503. 下一个更大元素II
 * https://leetcode.cn/problems/next-greater-element-ii/
 * 
 * 给定一个循环数组nums，返回nums中每个元素的下一个更大元素。
 * 
 * 单调栈 + 循环数组
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, -1);
        stack<int> st;  // 存储索引
        
        for (int i = 0; i < 2 * n; i++) {
            while (!st.empty() && nums[i % n] > nums[st.top()]) {
                int index = st.top();
                st.pop();
                result[index] = nums[i % n];
            }
            st.push(i % n);
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
void testNextGreaterElements() {
    Solution solution;
    
    vector<int> nums = {1, 2, 1};
    vector<int> result = solution.nextGreaterElements(nums);
    
    cout << "测试1: [";
    for (int i = 0; i < result.size(); i++) {
        cout << result[i];
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testNextGreaterElements();
    return 0;
}
