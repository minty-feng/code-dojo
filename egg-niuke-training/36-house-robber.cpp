/**
 * NC174 打家劫舍
 * https://www.nowcoder.com/practice/c5fbf7325fbd4c0ea3d0c3ea6bc6cc79
 * 
 * 你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金。
 * 你不能偷窃相邻的房屋，问能够偷窃到的最高金额。
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
    int rob(vector<int>& nums) {
        if (nums.empty()) return 0;
        if (nums.size() == 1) return nums[0];
        
        int prev2 = nums[0];  // dp[0]
        int prev1 = max(nums[0], nums[1]);  // dp[1]
        
        for (int i = 2; i < nums.size(); i++) {
            int curr = max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = curr;
        }
        
        return prev1;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {1, 2, 3, 1},
        {2, 7, 9, 3, 1},
        {2, 1, 1, 2},
        {1}
    };
    
    for (auto& nums : testCases) {
        cout << "房屋金额: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        int result = solution.rob(nums);
        cout << "最大偷窃金额: " << result << "\n" << endl;
    }
    
    return 0;
}

