/**
 * NC17 最长回文子串
 * https://www.nowcoder.com/practice/b4525d1d84934cf280439aeecc36f4af
 * 
 * 对于长度为n的一个字符串A，找到一个最长的回文子串。
 * 
 * 时间复杂度：O(n^2)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    /**
     * 方法1：中心扩展法
     */
    string longestPalindrome_Center(string s) {
        if (s.empty()) return "";
        
        int start = 0, maxLen = 1;
        
        for (int i = 0; i < s.length(); i++) {
            // 奇数长度回文
            auto [left1, right1] = expandAroundCenter(s, i, i);
            // 偶数长度回文
            auto [left2, right2] = expandAroundCenter(s, i, i + 1);
            
            // 选择更长的
            if (right1 - left1 + 1 > maxLen) {
                start = left1;
                maxLen = right1 - left1 + 1;
            }
            if (right2 - left2 + 1 > maxLen) {
                start = left2;
                maxLen = right2 - left2 + 1;
            }
        }
        
        return s.substr(start, maxLen);
    }
    
    /**
     * 方法2：动态规划
     */
    string longestPalindrome_DP(string s) {
        if (s.empty()) return "";
        
        int n = s.length();
        vector<vector<bool>> dp(n, vector<bool>(n, false));
        int start = 0, maxLen = 1;
        
        // 单个字符都是回文
        for (int i = 0; i < n; i++) {
            dp[i][i] = true;
        }
        
        // 枚举子串长度
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i <= n - len; i++) {
                int j = i + len - 1;
                
                if (s[i] == s[j]) {
                    if (len == 2) {
                        dp[i][j] = true;
                    } else {
                        dp[i][j] = dp[i+1][j-1];
                    }
                }
                
                if (dp[i][j] && len > maxLen) {
                    start = i;
                    maxLen = len;
                }
            }
        }
        
        return s.substr(start, maxLen);
    }

private:
    pair<int, int> expandAroundCenter(const string& s, int left, int right) {
        while (left >= 0 && right < s.length() && s[left] == s[right]) {
            left--;
            right++;
        }
        return {left + 1, right - 1};
    }
};

int main() {
    Solution solution;
    
    vector<string> testCases = {"babad", "cbbd", "a", "ac"};
    
    for (const string& s : testCases) {
        cout << "字符串: " << s << endl;
        cout << "中心扩展: " << solution.longestPalindrome_Center(s) << endl;
        cout << "动态规划: " << solution.longestPalindrome_DP(s) << endl << endl;
    }
    
    return 0;
}

