/**
 * LeetCode 45. 跳跃游戏II
 * https://leetcode.cn/problems/jump-game-ii/
 * 
 * 给你一个非负整数数组nums，你最初位于数组的第一个位置。
 * 数组中的每个元素代表你在该位置可以跳跃的最大长度。
 * 你的目标是使用最少的跳跃次数到达数组的最后一个位置。
 * 
 * 贪心
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int jump(vector<int>& nums) {
        if (nums.size() <= 1) {
            return 0;
        }
        
        int jumps = 0;
        int currentEnd = 0;
        int farthest = 0;
        
        for (int i = 0; i < nums.size() - 1; i++) {
            farthest = max(farthest, i + nums[i]);
            
            if (i == currentEnd) {
                jumps++;
                currentEnd = farthest;
                
                if (currentEnd >= nums.size() - 1) {
                    break;
                }
            }
        }
        
        return jumps;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testJump() {
    Solution solution;
    
    vector<int> nums1 = {2, 3, 1, 1, 4};
    int result1 = solution.jump(nums1);
    cout << "测试1 [2,3,1,1,4]: " << result1 << endl;  // 期望: 2
    
    vector<int> nums2 = {2, 3, 0, 1, 4};
    int result2 = solution.jump(nums2);
    cout << "测试2 [2,3,0,1,4]: " << result2 << endl;  // 期望: 2
    
    vector<int> nums3 = {1, 2, 3};
    int result3 = solution.jump(nums3);
    cout << "测试3 [1,2,3]: " << result3 << endl;  // 期望: 2
}

int main() {
    testJump();
    return 0;
}
