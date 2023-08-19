/**
 * LeetCode 322. 零钱兑换
 * https://leetcode.cn/problems/coin-change/
 * 
 * 给你一个整数数组coins，表示不同面额的硬币；以及一个整数amount，表示总金额。
 * 计算并返回可以凑成总金额所需的最少的硬币个数。
 * 
 * 动态规划（完全背包）
 * 
 * 时间复杂度：O(amount * len(coins))
 * 空间复杂度：O(amount)
 */

class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        if (amount == 0) {
            return 0;
        }
        
        vector<int> dp(amount + 1, INT_MAX);
        dp[0] = 0;
        
        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                if (dp[i - coin] != INT_MAX) {
                    dp[i] = min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        
        return dp[amount] == INT_MAX ? -1 : dp[amount];
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>
using namespace std;

void testCoinChange() {
    Solution solution;
    
    vector<int> coins1 = {1, 3, 4};
    int amount1 = 6;
    int result1 = solution.coinChange(coins1, amount1);
    cout << "测试1 coins={1,3,4}, amount=6: " << result1 << endl;  // 期望: 2
    
    vector<int> coins2 = {2};
    int amount2 = 3;
    int result2 = solution.coinChange(coins2, amount2);
    cout << "测试2 coins={2}, amount=3: " << result2 << endl;  // 期望: -1
    
    vector<int> coins3 = {1};
    int amount3 = 0;
    int result3 = solution.coinChange(coins3, amount3);
    cout << "测试3 coins={1}, amount=0: " << result3 << endl;  // 期望: 0
}

int main() {
    testCoinChange();
    return 0;
}
