/**
 * LeetCode 283. 移动零
 * https://leetcode.cn/problems/move-zeroes/
 * 
 * 给定一个数组nums，编写一个函数将所有0移动到数组的末尾，同时保持非零元素的相对顺序。
 * 
 * 双指针
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <vector>
using namespace std;

class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int slow = 0;
        
        // 将所有非零元素移到前面
        for (int fast = 0; fast < nums.size(); fast++) {
            if (nums[fast] != 0) {
                nums[slow] = nums[fast];
                slow++;
            }
        }
        
        // 将剩余位置填充为0
        for (int i = slow; i < nums.size(); i++) {
            nums[i] = 0;
        }
    }
};

// 测试函数
#include <iostream>
void testMoveZeroes() {
    Solution solution;
    
    // 测试用例1
    vector<int> nums1 = {0, 1, 0, 3, 12};
    solution.moveZeroes(nums1);
    cout << "测试1: [";
    for (int i = 0; i < nums1.size(); i++) {
        cout << nums1[i];
        if (i < nums1.size() - 1) cout << ",";
    }
    cout << "]" << endl;
    
    // 测试用例2
    vector<int> nums2 = {0};
    solution.moveZeroes(nums2);
    cout << "测试2: [";
    for (int i = 0; i < nums2.size(); i++) {
        cout << nums2[i];
        if (i < nums2.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testMoveZeroes();
    return 0;
}
