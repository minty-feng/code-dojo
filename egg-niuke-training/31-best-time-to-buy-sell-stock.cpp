/**
 * NC103 买卖股票的最好时机(一)
 * https://www.nowcoder.com/practice/64b4262d4e6d4f6181cd45446a5821ec
 * 
 * 假设你有一个数组prices，长度为n，其中prices[i]是股票在第i天的价格。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        if (prices.empty() || prices.size() < 2) {
            return 0;
        }
        
        int minPrice = prices[0];
        int maxProfit = 0;
        
        for (int i = 1; i < prices.size(); i++) {
            // 更新最低价格
            minPrice = min(minPrice, prices[i]);
            // 更新最大收益
            maxProfit = max(maxProfit, prices[i] - minPrice);
        }
        
        return maxProfit;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {7, 1, 5, 3, 6, 4},
        {7, 6, 4, 3, 1},
        {1, 2, 3, 4, 5},
        {2, 4, 1}
    };
    
    for (const auto& prices : testCases) {
        cout << "价格: ";
        for (int price : prices) cout << price << " ";
        cout << endl;
        
        int profit = solution.maxProfit(const_cast<vector<int>&>(prices));
        cout << "最大收益: " << profit << "\n" << endl;
    }
    
    return 0;
}

