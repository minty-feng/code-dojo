/**
 * LeetCode 213. 打家劫舍II
 * https://leetcode.cn/problems/house-robber-ii/
 * 
 * 你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。
 * 这个地方所有的房屋都围成一圈，这意味着第一个房屋和最后一个房屋是紧挨着的。
 * 
 * 动态规划
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int rob(vector<int>& nums) {
        if (nums.empty()) {
            return 0;
        }
        
        if (nums.size() == 1) {
            return nums[0];
        }
        
        if (nums.size() == 2) {
            return max(nums[0], nums[1]);
        }
        
        // 情况1：不偷第一个房子
        int case1 = robLinear(nums, 1, nums.size() - 1);
        
        // 情况2：不偷最后一个房子
        int case2 = robLinear(nums, 0, nums.size() - 2);
        
        return max(case1, case2);
    }
    
private:
    int robLinear(vector<int>& nums, int start, int end) {
        int prev2 = nums[start];
        int prev1 = max(nums[start], nums[start + 1]);
        
        for (int i = start + 2; i <= end; i++) {
            int current = max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testRob() {
    Solution solution;
    
    vector<int> nums1 = {2, 3, 2};
    int result1 = solution.rob(nums1);
    cout << "测试1 [2,3,2]: " << result1 << endl;  // 期望: 3
    
    vector<int> nums2 = {1, 2, 3, 1};
    int result2 = solution.rob(nums2);
    cout << "测试2 [1,2,3,1]: " << result2 << endl;  // 期望: 4
}

int main() {
    testRob();
    return 0;
}
