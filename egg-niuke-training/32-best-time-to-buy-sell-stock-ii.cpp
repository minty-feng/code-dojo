/**
 * NC104 买卖股票的最好时机(二)
 * https://www.nowcoder.com/practice/9e5e3c2603064829b0a0bbfca10594e9
 * 
 * 假设你有一个数组prices，长度为n，其中prices[i]是股票在第i天的价格。
 * 你可以多次买卖股票，但每次只能持有一只股票。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

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

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {7, 1, 5, 3, 6, 4},
        {1, 2, 3, 4, 5},
        {7, 6, 4, 3, 1},
        {1, 2, 1, 2}
    };
    
    for (auto& prices : testCases) {
        cout << "价格: ";
        for (int price : prices) cout << price << " ";
        cout << endl;
        
        int profit = solution.maxProfit(prices);
        cout << "最大收益: " << profit << "\n" << endl;
    }
    
    return 0;
}

