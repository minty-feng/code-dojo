/**
 * 动态规划基础问题实现
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

// 斐波那契数列
int fib(int n) {
    if (n <= 1) return n;
    
    int prev = 0, curr = 1;
    for (int i = 2; i <= n; i++) {
        int temp = curr;
        curr = prev + curr;
        prev = temp;
    }
    return curr;
}

// 爬楼梯
int climbStairs(int n) {
    if (n <= 1) return 1;
    
    int prev = 1, curr = 1;
    for (int i = 2; i <= n; i++) {
        int temp = curr;
        curr = prev + curr;
        prev = temp;
    }
    return curr;
}

// 打家劫舍
int rob(const vector<int>& nums) {
    if (nums.empty()) return 0;
    if (nums.size() == 1) return nums[0];
    
    int prev = 0, curr = 0;
    for (int num : nums) {
        int temp = curr;
        curr = max(curr, prev + num);
        prev = temp;
    }
    return curr;
}

// 最大子数组和
int maxSubArray(const vector<int>& nums) {
    int maxSum = nums[0];
    int currSum = nums[0];
    
    for (int i = 1; i < nums.size(); i++) {
        currSum = max(nums[i], currSum + nums[i]);
        maxSum = max(maxSum, currSum);
    }
    
    return maxSum;
}

// 最长递增子序列
int lengthOfLIS(const vector<int>& nums) {
    if (nums.empty()) return 0;
    
    vector<int> dp(nums.size(), 1);
    
    for (int i = 0; i < nums.size(); i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }
    
    return *max_element(dp.begin(), dp.end());
}

// 零钱兑换
int coinChange(const vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;
    
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (i >= coin && dp[i - coin] != INT_MAX) {
                dp[i] = min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    
    return dp[amount] == INT_MAX ? -1 : dp[amount];
}

// 不同路径
int uniquePaths(int m, int n) {
    vector<int> dp(n, 1);
    
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[j] += dp[j - 1];
        }
    }
    
    return dp[n - 1];
}

int main() {
    cout << "=== 动态规划基础演示 ===" << endl << endl;
    
    // 斐波那契
    int n = 10;
    cout << "斐波那契第" << n << "项: " << fib(n) << endl << endl;
    
    // 爬楼梯
    n = 5;
    cout << "爬" << n << "级楼梯的方法数: " << climbStairs(n) << endl << endl;
    
    // 打家劫舍
    vector<int> nums = {2, 7, 9, 3, 1};
    cout << "打家劫舍 [2,7,9,3,1]: " << rob(nums) << endl << endl;
    
    // 最大子数组和
    vector<int> nums2 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    cout << "最大子数组和: " << maxSubArray(nums2) << endl << endl;
    
    // LIS
    vector<int> nums3 = {10, 9, 2, 5, 3, 7, 101, 18};
    cout << "最长递增子序列长度: " << lengthOfLIS(nums3) << endl << endl;
    
    // 零钱兑换
    vector<int> coins = {1, 2, 5};
    int amount = 11;
    cout << "零钱兑换 coins=[1,2,5], amount=11: " 
         << coinChange(coins, amount) << endl << endl;
    
    // 不同路径
    cout << "网格 3×7 不同路径数: " << uniquePaths(3, 7) << endl;
    
    return 0;
}

