/**
 * LeetCode 287. 寻找重复数
 * https://leetcode.cn/problems/find-the-duplicate-number/
 * 
 * 给定一个包含n+1个整数的数组nums，其数字都在1到n之间，可知至少存在一个重复的整数。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        // 第一阶段：找到相遇点
        int slow = nums[0];
        int fast = nums[0];
        
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        
        // 第二阶段：找到环的入口
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        
        return slow;
    }
};

int main() {
    Solution solution;
    vector<vector<int>> testCases = {{1, 3, 4, 2, 2}, {3, 1, 3, 4, 2}, {1, 1}};
    
    for (auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        int result = solution.findDuplicate(nums);
        cout << "重复数: " << result << "\n" << endl;
    }
    
    return 0;
}

