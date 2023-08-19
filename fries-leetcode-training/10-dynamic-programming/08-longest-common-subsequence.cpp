/**
 * LeetCode 1143. 最长公共子序列
 * https://leetcode.cn/problems/longest-common-subsequence/
 * 
 * 给定两个字符串text1和text2，返回这两个字符串的最长公共子序列的长度。
 * 如果不存在公共子序列，返回0。
 * 
 * 动态规划
 * 
 * 时间复杂度：O(m * n)
 * 空间复杂度：O(m * n)
 */

class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.length();
        int n = text2.length();
        
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        
        // 填充dp表
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1[i-1] == text2[j-1]) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                } else {
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        
        return dp[m][n];
    }
};

// 测试函数
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

void testLongestCommonSubsequence() {
    Solution solution;
    
    string text1_1 = "abcde", text2_1 = "ace";
    int result1 = solution.longestCommonSubsequence(text1_1, text2_1);
    cout << "测试1 '" << text1_1 << "' & '" << text2_1 << "': " << result1 << endl;  // 期望: 3
    
    string text1_2 = "abc", text2_2 = "abc";
    int result2 = solution.longestCommonSubsequence(text1_2, text2_2);
    cout << "测试2 '" << text1_2 << "' & '" << text2_2 << "': " << result2 << endl;  // 期望: 3
    
    string text1_3 = "abc", text2_3 = "def";
    int result3 = solution.longestCommonSubsequence(text1_3, text2_3);
    cout << "测试3 '" << text1_3 << "' & '" << text2_3 << "': " << result3 << endl;  // 期望: 0
}

int main() {
    testLongestCommonSubsequence();
    return 0;
}
