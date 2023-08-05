/**
 * LeetCode 76. 最小覆盖子串
 * https://leetcode.cn/problems/minimum-window-substring/
 * 
 * 给你一个字符串s、一个字符串t。返回s中涵盖t所有字符的最小子串。
 * 
 * 时间复杂度：O(|s| + |t|)
 * 空间复杂度：O(|s| + |t|)
 */

#include <iostream>
#include <string>
#include <unordered_map>
#include <climits>
using namespace std;

class Solution {
public:
    string minWindow(string s, string t) {
        if (s.empty() || t.empty() || s.length() < t.length()) {
            return "";
        }
        
        unordered_map<char, int> need;
        for (char c : t) {
            need[c]++;
        }
        
        int left = 0;
        int valid = 0;
        unordered_map<char, int> window;
        
        int start = 0;
        int minLen = INT_MAX;
        
        for (int right = 0; right < s.length(); right++) {
            char c = s[right];
            window[c]++;
            
            if (need.count(c) && window[c] == need[c]) {
                valid++;
            }
            
            while (valid == need.size()) {
                if (right - left + 1 < minLen) {
                    start = left;
                    minLen = right - left + 1;
                }
                
                char d = s[left];
                left++;
                
                if (need.count(d)) {
                    if (window[d] == need[d]) {
                        valid--;
                    }
                    window[d]--;
                }
            }
        }
        
        return minLen == INT_MAX ? "" : s.substr(start, minLen);
    }
};

int main() {
    Solution solution;
    vector<pair<string, string>> testCases = {
        {"ADOBECODEBANC", "ABC"},
        {"a", "a"},
        {"a", "aa"}
    };
    
    for (auto& testCase : testCases) {
        string s = testCase.first;
        string t = testCase.second;
        
        cout << "s: '" << s << "', t: '" << t << "'" << endl;
        
        string result = solution.minWindow(s, t);
        cout << "最小覆盖子串: '" << result << "'\n" << endl;
    }
    
    return 0;
}

