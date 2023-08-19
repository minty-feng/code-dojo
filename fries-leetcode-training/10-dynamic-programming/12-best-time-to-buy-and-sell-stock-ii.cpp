/**
 * LeetCode 122. 买卖股票的最佳时机II
 * https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/
 * 
 * 给你一个整数数组prices，其中prices[i]表示某支股票第i天的价格。
 * 在每一天，你可以决定是否购买和/或出售股票。你在任何时候最多只能持有一股股票。
 * 
 * 贪心/动态规划
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        if (prices.empty() || prices.size() < 2) {
            return 0;
        }
        
        int profit = 0;
        
        for (int i = 1; i < prices.size(); i++) {
            if (prices[i] > prices[i-1]) {
                profit += prices[i] - prices[i-1];
            }
        }
        
        return profit;
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testMaxProfit() {
    Solution solution;
    
    vector<int> prices1 = {7, 1, 5, 3, 6, 4};
    int result1 = solution.maxProfit(prices1);
    cout << "测试1 [7,1,5,3,6,4]: " << result1 << endl;  // 期望: 7
    
    vector<int> prices2 = {1, 2, 3, 4, 5};
    int result2 = solution.maxProfit(prices2);
    cout << "测试2 [1,2,3,4,5]: " << result2 << endl;  // 期望: 4
    
    vector<int> prices3 = {7, 6, 4, 3, 1};
    int result3 = solution.maxProfit(prices3);
    cout << "测试3 [7,6,4,3,1]: " << result3 << endl;  // 期望: 0
}

int main() {
    testMaxProfit();
    return 0;
}
