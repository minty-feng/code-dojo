/**
 * NC35 编辑距离
 * https://www.nowcoder.com/practice/05fed41805ae4394ab6607d0d745c8e4
 * 
 * 给定两个字符串word1和word2，计算出将word1转换成word2所使用的最少操作数。
 * 
 * 时间复杂度：O(m*n)
 * 空间复杂度：O(m*n)
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * 编辑距离 - 动态规划
     */
    int minDistance(string word1, string word2) {
        int m = word1.length(), n = word2.length();
        
        // dp[i][j]表示word1[0:i]转换为word2[0:j]的最小操作数
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        
        // 初始化
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }
        
        // 状态转移
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i-1] == word2[j-1]) {
                    dp[i][j] = dp[i-1][j-1];
                } else {
                    dp[i][j] = min({
                        dp[i-1][j] + 1,    // 删除
                        dp[i][j-1] + 1,    // 插入
                        dp[i-1][j-1] + 1   // 替换
                    });
                }
            }
        }
        
        return dp[m][n];
    }
    
    /**
     * 空间优化版本 O(n)
     */
    int minDistance_Optimized(string word1, string word2) {
        int m = word1.length(), n = word2.length();
        
        vector<int> prev(n + 1);
        for (int j = 0; j <= n; j++) {
            prev[j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            vector<int> curr(n + 1);
            curr[0] = i;
            
            for (int j = 1; j <= n; j++) {
                if (word1[i-1] == word2[j-1]) {
                    curr[j] = prev[j-1];
                } else {
                    curr[j] = min({prev[j], curr[j-1], prev[j-1]}) + 1;
                }
            }
            
            prev = curr;
        }
        
        return prev[n];
    }
};

int main() {
    Solution solution;
    
    vector<pair<string, string>> testCases = {
        {"horse", "ros"},
        {"intention", "execution"},
        {"", "a"},
        {"a", ""}
    };
    
    for (const auto& [word1, word2] : testCases) {
        int dist = solution.minDistance(word1, word2);
        cout << "'" << word1 << "' -> '" << word2 << "': 编辑距离 = " << dist << endl;
    }
    
    return 0;
}

