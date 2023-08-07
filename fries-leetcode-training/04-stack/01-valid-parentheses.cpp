/**
 * LeetCode 20. 有效的括号
 * https://leetcode.cn/problems/valid-parentheses/
 * 
 * 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串s，判断字符串是否有效。
 * 
 * 栈
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <string>
#include <stack>
#include <unordered_map>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        if (s.length() % 2 == 1) {
            return false;
        }
        
        stack<char> st;
        unordered_map<char, char> mapping = {
            {')', '('},
            {'}', '{'},
            {']', '['}
        };
        
        for (char c : s) {
            if (mapping.count(c)) {
                if (st.empty() || st.top() != mapping[c]) {
                    return false;
                }
                st.pop();
            } else {
                st.push(c);
            }
        }
        
        return st.empty();
    }
};

// 测试函数
#include <iostream>
void testIsValid() {
    Solution solution;
    
    // 测试用例1
    string s1 = "()";
    bool result1 = solution.isValid(s1);
    cout << "测试1: " << (result1 ? "True" : "False") << endl;
    
    // 测试用例2
    string s2 = "()[]{}";
    bool result2 = solution.isValid(s2);
    cout << "测试2: " << (result2 ? "True" : "False") << endl;
    
    // 测试用例3
    string s3 = "(]";
    bool result3 = solution.isValid(s3);
    cout << "测试3: " << (result3 ? "True" : "False") << endl;
}

int main() {
    testIsValid();
    return 0;
}
