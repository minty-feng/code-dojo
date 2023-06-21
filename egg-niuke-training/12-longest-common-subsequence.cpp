/**
 * NC127 最长公共子序列(二)
 * https://www.nowcoder.com/practice/6d29638c85bb4ffd80c020fe244baf11
 * 
 * 给定两个字符串str1和str2，输出两个字符串的最长公共子序列。
 * 
 * 时间复杂度：O(n*m)
 * 空间复杂度：O(n*m)
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * 最长公共子序列
     */
    string LCS(string s1, string s2) {
        int m = s1.length(), n = s2.length();
        
        // dp[i][j]表示s1[0:i]和s2[0:j]的LCS长度
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        
        // 填充dp表
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1[i-1] == s2[j-1]) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                } else {
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        
        // 回溯构造LCS
        if (dp[m][n] == 0) {
            return "-1";
        }
        
        string lcs;
        int i = m, j = n;
        while (i > 0 && j > 0) {
            if (s1[i-1] == s2[j-1]) {
                lcs += s1[i-1];
                i--;
                j--;
            } else if (dp[i-1][j] > dp[i][j-1]) {
                i--;
            } else {
                j--;
            }
        }
        
        reverse(lcs.begin(), lcs.end());
        return lcs;
    }
};

int main() {
    Solution solution;
    
    vector<pair<string, string>> testCases = {
        {"1A2C3D4B56", "B1D23A456A"},
        {"abc", "def"},
        {"abc", "abc"}
    };
    
    for (const auto& tc : testCases) {
        string result = solution.LCS(tc.first, tc.second);
        cout << "s1=" << tc.first << ", s2=" << tc.second << endl;
        cout << "LCS=" << result << endl << endl;
    }
    
    return 0;
}

