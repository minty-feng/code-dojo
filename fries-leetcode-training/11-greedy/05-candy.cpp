/**
 * LeetCode 135. 分发糖果
 * https://leetcode.cn/problems/candy/
 * 
 * n个孩子站成一排。给你一个整数数组ratings表示每个孩子的评分。
 * 你需要按照以下要求，给这些孩子分发糖果：
 * - 每个孩子至少分得1个糖果
 * - 相邻的孩子中，评分高的孩子必须获得更多的糖果
 * 
 * 贪心
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> candies(n, 1);
        
        // 从左到右遍历，确保右边评分高的孩子糖果更多
        for (int i = 1; i < n; i++) {
            if (ratings[i] > ratings[i-1]) {
                candies[i] = candies[i-1] + 1;
            }
        }
        
        // 从右到左遍历，确保左边评分高的孩子糖果更多
        for (int i = n-2; i >= 0; i--) {
            if (ratings[i] > ratings[i+1]) {
                candies[i] = max(candies[i], candies[i+1] + 1);
            }
        }
        
        int total = 0;
        for (int candy : candies) {
            total += candy;
        }
        
        return total;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testCandy() {
    Solution solution;
    
    vector<int> ratings1 = {1, 0, 2};
    int result1 = solution.candy(ratings1);
    cout << "测试1 [1,0,2]: " << result1 << endl;  // 期望: 5
    
    vector<int> ratings2 = {1, 2, 2};
    int result2 = solution.candy(ratings2);
    cout << "测试2 [1,2,2]: " << result2 << endl;  // 期望: 4
    
    vector<int> ratings3 = {1, 3, 2, 2, 1};
    int result3 = solution.candy(ratings3);
    cout << "测试3 [1,3,2,2,1]: " << result3 << endl;  // 期望: 7
}

int main() {
    testCandy();
    return 0;
}
