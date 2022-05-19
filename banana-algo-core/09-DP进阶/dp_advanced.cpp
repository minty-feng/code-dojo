/**
 * DP进阶问题实现
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>

using namespace std;

// 最长公共子序列
int longestCommonSubsequence(const string& text1, const string& text2) {
    int m = text1.length(), n = text2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
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

// 编辑距离
int minDistance(const string& word1, const string& word2) {
    int m = word1.length(), n = word2.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1[i-1] == word2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + min({
                    dp[i-1][j],    // 删除
                    dp[i][j-1],    // 插入
                    dp[i-1][j-1]   // 替换
                });
            }
        }
    }
    
    return dp[m][n];
}

// 最长回文子串
string longestPalindrome(const string& s) {
    int n = s.length();
    if (n == 0) return "";
    
    vector<vector<bool>> dp(n, vector<bool>(n, false));
    int start = 0, maxLen = 1;
    
    for (int i = 0; i < n; i++) {
        dp[i][i] = true;
    }
    
    for (int i = 0; i < n - 1; i++) {
        if (s[i] == s[i+1]) {
            dp[i][i+1] = true;
            start = i;
            maxLen = 2;
        }
    }
    
    for (int len = 3; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;
            if (s[i] == s[j] && dp[i+1][j-1]) {
                dp[i][j] = true;
                start = i;
                maxLen = len;
            }
        }
    }
    
    return s.substr(start, maxLen);
}

// 买卖股票（一次）
int maxProfitOne(const vector<int>& prices) {
    int minPrice = INT_MAX;
    int maxProfit = 0;
    
    for (int price : prices) {
        minPrice = min(minPrice, price);
        maxProfit = max(maxProfit, price - minPrice);
    }
    
    return maxProfit;
}

// 买卖股票（无限次）
int maxProfitUnlimited(const vector<int>& prices) {
    int profit = 0;
    
    for (int i = 1; i < prices.size(); i++) {
        if (prices[i] > prices[i-1]) {
            profit += prices[i] - prices[i-1];
        }
    }
    
    return profit;
}

// 买卖股票（k次）
int maxProfitK(int k, const vector<int>& prices) {
    if (prices.empty()) return 0;
    
    int n = prices.size();
    if (k >= n / 2) {
        return maxProfitUnlimited(prices);
    }
    
    // dp[i][j][0/1] = 第i天，最多j次交易，不持有/持有
    vector<vector<vector<int>>> dp(n, 
        vector<vector<int>>(k + 1, vector<int>(2, 0)));
    
    for (int i = 0; i < n; i++) {
        for (int j = k; j >= 1; j--) {
            if (i == 0) {
                dp[i][j][0] = 0;
                dp[i][j][1] = -prices[i];
            } else {
                dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1] + prices[i]);
                dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j-1][0] - prices[i]);
            }
        }
    }
    
    return dp[n-1][k][0];
}

// 最长递增子序列（二分优化）
int lengthOfLIS(const vector<int>& nums) {
    if (nums.empty()) return 0;
    
    vector<int> tails;
    
    for (int num : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), num);
        if (it == tails.end()) {
            tails.push_back(num);
        } else {
            *it = num;
        }
    }
    
    return tails.size();
}

int main() {
    cout << "=== DP进阶演示 ===" << endl << endl;
    
    // LCS
    string text1 = "abcde", text2 = "ace";
    cout << "最长公共子序列 '" << text1 << "' 和 '" << text2 << "':" << endl;
    cout << "  长度: " << longestCommonSubsequence(text1, text2) << endl << endl;
    
    // 编辑距离
    string word1 = "horse", word2 = "ros";
    cout << "编辑距离 '" << word1 << "' -> '" << word2 << "':" << endl;
    cout << "  最少操作: " << minDistance(word1, word2) << endl << endl;
    
    // 最长回文
    string s = "babad";
    cout << "最长回文子串 '" << s << "':" << endl;
    cout << "  结果: " << longestPalindrome(s) << endl << endl;
    
    // 股票
    vector<int> prices = {7,1,5,3,6,4};
    cout << "股票问题 [7,1,5,3,6,4]:" << endl;
    cout << "  买卖一次: " << maxProfitOne(prices) << endl;
    cout << "  买卖多次: " << maxProfitUnlimited(prices) << endl;
    cout << "  最多2次: " << maxProfitK(2, prices) << endl << endl;
    
    // LIS
    vector<int> nums = {10, 9, 2, 5, 3, 7, 101, 18};
    cout << "最长递增子序列 [10,9,2,5,3,7,101,18]:" << endl;
    cout << "  长度: " << lengthOfLIS(nums) << endl;
    
    return 0;
}

