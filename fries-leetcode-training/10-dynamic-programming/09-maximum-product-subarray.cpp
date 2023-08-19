/**
 * LeetCode 152. 乘积最大子数组
 * https://leetcode.cn/problems/maximum-product-subarray/
 * 
 * 给你一个整数数组nums，请你找出数组中乘积最大的连续子数组，并返回该子数组的乘积。
 * 
 * 动态规划
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int maxProduct(vector<int>& nums) {
        if (nums.empty()) {
            return 0;
        }
        
        // 维护最大值和最小值
        int maxProd = nums[0];
        int minProd = nums[0];
        int result = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            // 如果当前数是负数，交换最大值和最小值
            if (nums[i] < 0) {
                swap(maxProd, minProd);
            }
            
            // 更新最大值和最小值
            maxProd = max(nums[i], maxProd * nums[i]);
            minProd = min(nums[i], minProd * nums[i]);
            
            // 更新结果
            result = max(result, maxProd);
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testMaxProduct() {
    Solution solution;
    
    vector<int> nums1 = {2, 3, -2, 4};
    int result1 = solution.maxProduct(nums1);
    cout << "测试1 [2,3,-2,4]: " << result1 << endl;  // 期望: 6
    
    vector<int> nums2 = {-2, 0, -1};
    int result2 = solution.maxProduct(nums2);
    cout << "测试2 [-2,0,-1]: " << result2 << endl;  // 期望: 0
    
    vector<int> nums3 = {-2, 3, -4};
    int result3 = solution.maxProduct(nums3);
    cout << "测试3 [-2,3,-4]: " << result3 << endl;  // 期望: 24
}

int main() {
    testMaxProduct();
    return 0;
}
