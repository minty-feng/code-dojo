/**
 * NC52 有效括号序列
 * https://www.nowcoder.com/practice/37548e94a270412c8b9fb85643c8ccc2
 * 
 * 给出一个仅包含字符'(',')','{','}','['和']',的字符串，判断是否是合法的括号序列。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <string>
#include <stack>
#include <unordered_map>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        if (s.empty()) return true;
        
        stack<char> st;
        unordered_map<char, char> mapping = {
            {')', '('},
            {'}', '{'},
            {']', '['}
        };
        
        for (char c : s) {
            if (mapping.count(c)) {
                // 右括号
                if (st.empty() || st.top() != mapping[c]) {
                    return false;
                }
                st.pop();
            } else {
                // 左括号
                st.push(c);
            }
        }
        
        return st.empty();
    }
};

int main() {
    Solution solution;
    
    vector<string> testCases = {
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[]}",
        ""
    };
    
    for (const string& s : testCases) {
        bool result = solution.isValid(s);
        cout << "'" << s << "' 是否有效: " << (result ? "是" : "否") << endl;
    }
    
    return 0;
}

