/**
 * LeetCode 300. 最长递增子序列
 * https://leetcode.cn/problems/longest-increasing-subsequence/
 * 
 * 给你一个整数数组nums，找到其中最长严格递增子序列的长度。
 * 
 * 动态规划 + 二分搜索
 * 
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(n)
 */

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        if (nums.empty()) {
            return 0;
        }
        
        vector<int> tails;
        
        for (int num : nums) {
            int left = 0, right = tails.size();
            
            while (left < right) {
                int mid = left + (right - left) / 2;
                if (tails[mid] < num) {
                    left = mid + 1;
                } else {
                    right = mid;
                }
            }
            
            if (left == tails.size()) {
                tails.push_back(num);
            } else {
                tails[left] = num;
            }
        }
        
        return tails.size();
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testLengthOfLIS() {
    Solution solution;
    
    vector<int> nums1 = {10, 9, 2, 5, 3, 7, 101, 18};
    int result1 = solution.lengthOfLIS(nums1);
    cout << "测试1: " << result1 << endl;  // 期望: 4
    
    vector<int> nums2 = {0, 1, 0, 3, 2, 3};
    int result2 = solution.lengthOfLIS(nums2);
    cout << "测试2: " << result2 << endl;  // 期望: 4
    
    vector<int> nums3 = {7, 7, 7, 7, 7, 7, 7};
    int result3 = solution.lengthOfLIS(nums3);
    cout << "测试3: " << result3 << endl;  // 期望: 1
}

int main() {
    testLengthOfLIS();
    return 0;
}
