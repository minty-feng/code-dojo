/**
 * LeetCode 152. 乘积最大子数组
 * https://leetcode.cn/problems/maximum-product-subarray/
 * 
 * 给你一个整数数组nums，请你找出数组中乘积最大的连续子数组。
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
    int maxProduct(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        int maxProd = nums[0];
        int minProd = nums[0];
        int result = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            int tempMax = maxProd;
            maxProd = max({nums[i], maxProd * nums[i], minProd * nums[i]});
            minProd = min({nums[i], tempMax * nums[i], minProd * nums[i]});
            result = max(result, maxProd);
        }
        
        return result;
    }
};

int main() {
    Solution solution;
    vector<vector<int>> testCases = {{2, 3, -2, 4}, {-2, 0, -1}};
    
    for (auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << "\n最大乘积: " << solution.maxProduct(nums) << "\n" << endl;
    }
    return 0;
}
