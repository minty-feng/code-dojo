/**
 * 背包问题实现
 */

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 0-1背包（二维DP）
int knapsack01(const vector<int>& weights, const vector<int>& values, int capacity) {
    int n = weights.size();
    vector<vector<int>> dp(n + 1, vector<int>(capacity + 1, 0));
    
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= capacity; j++) {
            if (j < weights[i-1]) {
                dp[i][j] = dp[i-1][j];
            } else {
                dp[i][j] = max(
                    dp[i-1][j],
                    dp[i-1][j - weights[i-1]] + values[i-1]
                );
            }
        }
    }
    
    return dp[n][capacity];
}

// 0-1背包（一维优化）
int knapsack01Optimized(const vector<int>& weights, const vector<int>& values, int capacity) {
    vector<int> dp(capacity + 1, 0);
    
    for (int i = 0; i < weights.size(); i++) {
        // 逆序遍历
        for (int j = capacity; j >= weights[i]; j--) {
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i]);
        }
    }
    
    return dp[capacity];
}

// 完全背包
int knapsackComplete(const vector<int>& weights, const vector<int>& values, int capacity) {
    vector<int> dp(capacity + 1, 0);
    
    for (int i = 0; i < weights.size(); i++) {
        // 正序遍历
        for (int j = weights[i]; j <= capacity; j++) {
            dp[j] = max(dp[j], dp[j - weights[i]] + values[i]);
        }
    }
    
    return dp[capacity];
}

// 零钱兑换（完全背包）
int coinChange(const vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;
    
    for (int coin : coins) {
        for (int j = coin; j <= amount; j++) {
            if (dp[j - coin] != INT_MAX) {
                dp[j] = min(dp[j], dp[j - coin] + 1);
            }
        }
    }
    
    return dp[amount] == INT_MAX ? -1 : dp[amount];
}

// 零钱兑换II（方案数）
int coinChangeWays(const vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, 0);
    dp[0] = 1;
    
    for (int coin : coins) {
        for (int j = coin; j <= amount; j++) {
            dp[j] += dp[j - coin];
        }
    }
    
    return dp[amount];
}

// 分割等和子集
bool canPartition(const vector<int>& nums) {
    int sum = 0;
    for (int num : nums) sum += num;
    
    if (sum % 2) return false;
    
    int target = sum / 2;
    vector<bool> dp(target + 1, false);
    dp[0] = true;
    
    for (int num : nums) {
        for (int j = target; j >= num; j--) {
            dp[j] = dp[j] || dp[j - num];
        }
    }
    
    return dp[target];
}

int main() {
    cout << "=== 背包问题演示 ===" << endl << endl;
    
    // 0-1背包
    vector<int> weights = {2, 3, 4, 5};
    vector<int> values = {3, 4, 5, 6};
    int capacity = 8;
    
    cout << "0-1背包:" << endl;
    cout << "  重量: [2,3,4,5]" << endl;
    cout << "  价值: [3,4,5,6]" << endl;
    cout << "  容量: 8" << endl;
    cout << "  最大价值: " << knapsack01(weights, values, capacity) << endl;
    cout << "  最大价值（优化）: " << knapsack01Optimized(weights, values, capacity) << endl << endl;
    
    // 完全背包
    cout << "完全背包:" << endl;
    cout << "  最大价值: " << knapsackComplete(weights, values, capacity) << endl << endl;
    
    // 零钱兑换
    vector<int> coins = {1, 2, 5};
    int amount = 11;
    cout << "零钱兑换:" << endl;
    cout << "  硬币: [1,2,5], 金额: 11" << endl;
    cout << "  最少硬币数: " << coinChange(coins, amount) << endl;
    cout << "  方案数: " << coinChangeWays(coins, amount) << endl << endl;
    
    // 分割等和子集
    vector<int> nums = {1, 5, 11, 5};
    cout << "分割等和子集 [1,5,11,5]:" << endl;
    cout << "  能否分割: " << (canPartition(nums) ? "是" : "否") << endl;
    
    return 0;
}

