/**
 * LeetCode 53. 最大子数组和
 * https://leetcode.cn/problems/maximum-subarray/
 * 
 * 给你一个整数数组nums，请你找出一个具有最大和的连续子数组，返回其最大和。
 * 
 * Kadane算法
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        if (nums.empty()) {
            return 0;
        }
        
        int maxSum = nums[0];
        int currentSum = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            currentSum = max(nums[i], currentSum + nums[i]);
            maxSum = max(maxSum, currentSum);
        }
        
        return maxSum;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testMaxSubArray() {
    Solution solution;
    
    vector<int> nums1 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    int result1 = solution.maxSubArray(nums1);
    cout << "测试1: " << result1 << endl;  // 期望: 6
    
    vector<int> nums2 = {1};
    int result2 = solution.maxSubArray(nums2);
    cout << "测试2: " << result2 << endl;  // 期望: 1
    
    vector<int> nums3 = {5, 4, -1, 7, 8};
    int result3 = solution.maxSubArray(nums3);
    cout << "测试3: " << result3 << endl;  // 期望: 23
}

int main() {
    testMaxSubArray();
    return 0;
}
