/**
 * LeetCode 739. 每日温度
 * https://leetcode.cn/problems/daily-temperatures/
 * 
 * 请根据每日气温列表temperatures，重新生成一个列表，要求对于每一天，
 * 你都要计算这一天之后第一个更高温度出现在几天后。
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
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> result(n, 0);
        stack<int> st;  // 存储索引
        
        for (int i = 0; i < n; i++) {
            while (!st.empty() && temperatures[i] > temperatures[st.top()]) {
                int index = st.top();
                st.pop();
                result[index] = i - index;
            }
            st.push(i);
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
void testDailyTemperatures() {
    Solution solution;
    
    vector<int> temperatures1 = {73, 74, 75, 71, 69, 72, 76, 73};
    vector<int> result1 = solution.dailyTemperatures(temperatures1);
    
    cout << "测试1: [";
    for (int i = 0; i < result1.size(); i++) {
        cout << result1[i];
        if (i < result1.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testDailyTemperatures();
    return 0;
}
