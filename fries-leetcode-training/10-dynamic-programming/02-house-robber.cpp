/**
 * LeetCode 198. 打家劫舍
 * https://leetcode.cn/problems/house-robber/
 * 
 * 你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，
 * 影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，
 * 如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
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
        
        // 空间优化版本
        int prev2 = nums[0];  // dp[i-2]
        int prev1 = max(nums[0], nums[1]);  // dp[i-1]
        
        for (int i = 2; i < nums.size(); i++) {
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
    
    vector<int> nums1 = {1, 2, 3, 1};
    int result1 = solution.rob(nums1);
    cout << "测试1 [1,2,3,1]: " << result1 << endl;  // 期望: 4
    
    vector<int> nums2 = {2, 7, 9, 3, 1};
    int result2 = solution.rob(nums2);
    cout << "测试2 [2,7,9,3,1]: " << result2 << endl;  // 期望: 12
}

int main() {
    testRob();
    return 0;
}
