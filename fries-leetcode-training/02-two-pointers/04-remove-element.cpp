/**
 * LeetCode 27. 移除元素
 * https://leetcode.cn/problems/remove-element/
 * 
 * 给你一个数组nums和一个值val，你需要原地移除所有数值等于val的元素，并返回移除后数组的新长度。
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
    int removeElement(vector<int>& nums, int val) {
        int slow = 0;
        
        for (int fast = 0; fast < nums.size(); fast++) {
            if (nums[fast] != val) {
                nums[slow] = nums[fast];
                slow++;
            }
        }
        
        return slow;
    }
};

// 测试函数
#include <iostream>
void testRemoveElement() {
    Solution solution;
    
    // 测试用例1
    vector<int> nums1 = {3, 2, 2, 3};
    int val1 = 3;
    int result1 = solution.removeElement(nums1, val1);
    cout << "测试1: 长度=" << result1 << ", 数组=[";
    for (int i = 0; i < result1; i++) {
        cout << nums1[i];
        if (i < result1 - 1) cout << ",";
    }
    cout << "]" << endl;
    
    // 测试用例2
    vector<int> nums2 = {0, 1, 2, 2, 3, 0, 4, 2};
    int val2 = 2;
    int result2 = solution.removeElement(nums2, val2);
    cout << "测试2: 长度=" << result2 << ", 数组=[";
    for (int i = 0; i < result2; i++) {
        cout << nums2[i];
        if (i < result2 - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testRemoveElement();
    return 0;
}
