/**
 * LeetCode 123. 买卖股票的最佳时机III
 * https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/
 * 
 * 给定一个数组，它的第i个元素是一支给定的股票在第i天的价格。
 * 设计一个算法来计算你所能获取的最大利润。你最多可以完成两笔交易。
 * 
 * 动态规划
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
        
        // 第一次交易的状态
        int buy1 = -prices[0];   // 第一次买入
        int sell1 = 0;           // 第一次卖出
        
        // 第二次交易的状态
        int buy2 = -prices[0];   // 第二次买入
        int sell2 = 0;           // 第二次卖出
        
        for (int i = 1; i < prices.size(); i++) {
            // 更新第二次交易状态
            sell2 = max(sell2, buy2 + prices[i]);
            buy2 = max(buy2, sell1 - prices[i]);
            
            // 更新第一次交易状态
            sell1 = max(sell1, buy1 + prices[i]);
            buy1 = max(buy1, -prices[i]);
        }
        
        return sell2;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testMaxProfit() {
    Solution solution;
    
    vector<int> prices1 = {3, 3, 5, 0, 0, 3, 1, 4};
    int result1 = solution.maxProfit(prices1);
    cout << "测试1 [3,3,5,0,0,3,1,4]: " << result1 << endl;  // 期望: 6
    
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
