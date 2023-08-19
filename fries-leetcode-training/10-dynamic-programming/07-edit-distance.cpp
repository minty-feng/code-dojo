/**
 * LeetCode 72. 编辑距离
 * https://leetcode.cn/problems/edit-distance/
 * 
 * 给你两个单词word1和word2，请返回将word1转换成word2所使用的最少操作数。
 * 你可以对一个单词进行如下三种操作：
 * - 插入一个字符
 * - 删除一个字符
 * - 替换一个字符
 * 
 * 动态规划
 * 
 * 时间复杂度：O(m * n)
 * 空间复杂度：O(m * n)
 */

class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.length();
        int n = word2.length();
        
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        
        // 初始化边界条件
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;  // word1的前i个字符变成空字符串需要i次删除操作
        }
        
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;  // 空字符串变成word2的前j个字符需要j次插入操作
        }
        
        // 填充dp表
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i-1] == word2[j-1]) {
                    dp[i][j] = dp[i-1][j-1];  // 字符相同，不需要操作
                } else {
                    dp[i][j] = min({
                        dp[i-1][j] + 1,      // 删除word1[i-1]
                        dp[i][j-1] + 1,      // 插入word2[j-1]
                        dp[i-1][j-1] + 1     // 替换word1[i-1]为word2[j-1]
                    });
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

void testMinDistance() {
    Solution solution;
    
    string word1_1 = "horse", word2_1 = "ros";
    int result1 = solution.minDistance(word1_1, word2_1);
    cout << "测试1 '" << word1_1 << "' -> '" << word2_1 << "': " << result1 << endl;  // 期望: 3
    
    string word1_2 = "intention", word2_2 = "execution";
    int result2 = solution.minDistance(word1_2, word2_2);
    cout << "测试2 '" << word1_2 << "' -> '" << word2_2 << "': " << result2 << endl;  // 期望: 5
    
    string word1_3 = "", word2_3 = "a";
    int result3 = solution.minDistance(word1_3, word2_3);
    cout << "测试3 '" << word1_3 << "' -> '" << word2_3 << "': " << result3 << endl;  // 期望: 1
}

int main() {
    testMinDistance();
    return 0;
}
