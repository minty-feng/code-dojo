/**
 * NC68 0-1背包问题
 * https://www.nowcoder.com/practice/2820ea076d144b30806e72de5ce5a4c
 * 
 * 有n个物品和一个容量为v的背包，每个物品有重量w[i]和价值v[i]。
 * 每个物品只能选择一次，问能装下的最大价值。
 * 
 * 时间复杂度：O(n*v)
 * 空间复杂度：O(v)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int knapsack(vector<int>& weights, vector<int>& values, int capacity) {
        int n = weights.size();
        if (n == 0 || capacity == 0) {
            return 0;
        }
        
        // dp[i]表示容量为i时的最大价值
        vector<int> dp(capacity + 1, 0);
        
        for (int i = 0; i < n; i++) {
            // 从大到小遍历，避免重复使用
            for (int j = capacity; j >= weights[i]; j--) {
                dp[j] = max(dp[j], dp[j - weights[i]] + values[i]);
            }
        }
        
        return dp[capacity];
    }
};

int main() {
    Solution solution;
    
    vector<int> weights = {2, 3, 4, 5};
    vector<int> values = {3, 4, 5, 6};
    int capacity = 8;
    
    cout << "物品重量: ";
    for (int w : weights) cout << w << " ";
    cout << endl;
    
    cout << "物品价值: ";
    for (int v : values) cout << v << " ";
    cout << endl;
    
    cout << "背包容量: " << capacity << endl;
    
    int result = solution.knapsack(weights, values, capacity);
    cout << "最大价值: " << result << endl;
    
    return 0;
}

