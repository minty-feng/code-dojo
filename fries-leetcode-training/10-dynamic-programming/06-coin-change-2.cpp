/**
 * LeetCode 518. 零钱兑换II
 * https://leetcode.cn/problems/coin-change-2/
 * 
 * 给你一个整数数组coins表示不同面额的硬币，另给一个整数amount表示总金额。
 * 请你计算并返回可以凑成总金额的硬币组合数。
 * 
 * 动态规划（完全背包）
 * 
 * 时间复杂度：O(amount * len(coins))
 * 空间复杂度：O(amount)
 */

class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<int> dp(amount + 1, 0);
        dp[0] = 1;  // 金额为0时有一种组合（不选任何硬币）
        
        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                dp[i] += dp[i - coin];
            }
        }
        
        return dp[amount];
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testChange() {
    Solution solution;
    
    vector<int> coins1 = {1, 2, 5};
    int amount1 = 5;
    int result1 = solution.change(amount1, coins1);
    cout << "测试1 amount=5, coins={1,2,5}: " << result1 << endl;  // 期望: 4
    
    vector<int> coins2 = {2};
    int amount2 = 3;
    int result2 = solution.change(amount2, coins2);
    cout << "测试2 amount=3, coins={2}: " << result2 << endl;  // 期望: 0
    
    vector<int> coins3 = {10};
    int amount3 = 10;
    int result3 = solution.change(amount3, coins3);
    cout << "测试3 amount=10, coins={10}: " << result3 << endl;  // 期望: 1
}

int main() {
    testChange();
    return 0;
}
