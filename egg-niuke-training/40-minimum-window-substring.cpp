/**
 * NC143 最小覆盖子串
 * https://www.nowcoder.com/practice/c466d480d20c4c7c9d322d12ca7955ac
 * 
 * 给出两个字符串S和T，要求在O(n)的时间复杂度内在S中找出最短的包含T中所有字符的子串。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

class Solution {
public:
    string minWindow(string s, string t) {
        if (s.empty() || t.empty() || s.length() < t.length()) {
            return "";
        }
        
        // 统计t中每个字符的频次
        unordered_map<char, int> need;
        for (char c : t) {
            need[c]++;
        }
        
        // 滑动窗口
        int left = 0;
        int valid = 0;  // 窗口中满足条件的字符个数
        unordered_map<char, int> window;
        
        int start = 0;
        int minLen = INT_MAX;
        
        for (int right = 0; right < s.length(); right++) {
            char c = s[right];
            
            // 右移窗口
            if (need.count(c)) {
                window[c]++;
                if (window[c] == need[c]) {
                    valid++;
                }
            }
            
            // 收缩窗口
            while (valid == need.size()) {
                // 更新最小覆盖子串
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
    
    for (const auto& [s, t] : testCases) {
        string result = solution.minWindow(s, t);
        cout << "s='" << s << "', t='" << t << "'" << endl;
        cout << "最小覆盖子串: '" << result << "'\n" << endl;
    }
    
    return 0;
}

