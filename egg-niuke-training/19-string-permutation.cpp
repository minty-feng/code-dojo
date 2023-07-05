/**
 * NC61 字符串的排列
 * https://www.nowcoder.com/practice/fe6b651b66ae47d7acce78ffdd9a96c7
 * 
 * 输入一个长度为 n 字符串，打印出该字符串中字符的所有排列。
 * 
 * 时间复杂度：O(n*n!)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<string> Permutation(string s) {
        vector<string> result;
        sort(s.begin(), s.end());  // 排序便于去重
        vector<bool> used(s.length(), false);
        string path;
        
        backtrack(s, path, used, result);
        return result;
    }

private:
    void backtrack(const string& s, string& path, vector<bool>& used, vector<string>& result) {
        if (path.length() == s.length()) {
            result.push_back(path);
            return;
        }
        
        for (int i = 0; i < s.length(); i++) {
            // 已使用过
            if (used[i]) continue;
            
            // 去重
            if (i > 0 && s[i] == s[i-1] && !used[i-1]) continue;
            
            // 做选择
            path += s[i];
            used[i] = true;
            
            // 递归
            backtrack(s, path, used, result);
            
            // 撤销选择
            path.pop_back();
            used[i] = false;
        }
    }
};

int main() {
    Solution solution;
    
    vector<string> testCases = {"abc", "abb", "aab"};
    
    for (const string& s : testCases) {
        vector<string> result = solution.Permutation(s);
        
        cout << "'" << s << "' 的排列:" << endl;
        for (const string& perm : result) {
            cout << "  " << perm << endl;
        }
        cout << "共 " << result.size() << " 种\n" << endl;
    }
    
    return 0;
}

