/**
 * LeetCode 55. 跳跃游戏
 * https://leetcode.cn/problems/jump-game/
 * 
 * 给定一个非负整数数组nums，你最初位于数组的第一个下标。
 * 数组中的每个元素代表你在该位置可以跳跃的最大长度。
 * 判断你是否能够到达最后一个下标。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    bool canJump(vector<int>& nums) {
        int max_reach = 0;
        
        for (int i = 0; i < nums.size(); i++) {
            if (i > max_reach) {
                return false;
            }
            max_reach = max(max_reach, i + nums[i]);
        }
        
        return true;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testCanJump() {
    Solution solution;
    
    vector<int> nums1 = {2, 3, 1, 1, 4};
    bool result1 = solution.canJump(nums1);
    cout << "测试1 [2,3,1,1,4]: " << (result1 ? "True" : "False") << endl;  // 期望: True
    
    vector<int> nums2 = {3, 2, 1, 0, 4};
    bool result2 = solution.canJump(nums2);
    cout << "测试2 [3,2,1,0,4]: " << (result2 ? "True" : "False") << endl;  // 期望: False
}

int main() {
    testCanJump();
    return 0;
}
