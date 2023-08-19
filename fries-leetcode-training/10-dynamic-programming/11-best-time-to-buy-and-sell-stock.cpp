/**
 * LeetCode 121. 买卖股票的最佳时机
 * https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/
 * 
 * 给定一个数组prices，它的第i个元素prices[i]表示一支给定股票第i天的价格。
 * 你只能选择某一天买入这只股票，并选择在未来的某一个不同的日子卖出该股票。
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
        
        int minPrice = prices[0];
        int maxProfit = 0;
        
        for (int i = 1; i < prices.size(); i++) {
            maxProfit = max(maxProfit, prices[i] - minPrice);
            minPrice = min(minPrice, prices[i]);
        }
        
        return maxProfit;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testMaxProfit() {
    Solution solution;
    
    vector<int> prices1 = {7, 1, 5, 3, 6, 4};
    int result1 = solution.maxProfit(prices1);
    cout << "测试1: " << result1 << endl;  // 期望: 5
    
    vector<int> prices2 = {7, 6, 4, 3, 1};
    int result2 = solution.maxProfit(prices2);
    cout << "测试2: " << result2 << endl;  // 期望: 0
    
    vector<int> prices3 = {1, 2};
    int result3 = solution.maxProfit(prices3);
    cout << "测试3: " << result3 << endl;  // 期望: 1
}

int main() {
    testMaxProfit();
    return 0;
}
