/**
 * LeetCode 1004. 最大连续1的个数III
 * https://leetcode.cn/problems/max-consecutive-ones-iii/
 * 
 * 给定一个二进制数组nums和一个整数k，最多可以把k个0变成1，返回仅包含1的最长（连续）子数组的长度。
 * 
 * 滑动窗口
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <vector>
using namespace std;

class Solution {
public:
    int longestOnes(vector<int>& nums, int k) {
        int left = 0;
        int max_len = 0;
        int zero_count = 0;
        
        for (int right = 0; right < nums.size(); right++) {
            // 扩展窗口
            if (nums[right] == 0) {
                zero_count++;
            }
            
            // 收缩窗口
            while (zero_count > k) {
                if (nums[left] == 0) {
                    zero_count--;
                }
                left++;
            }
            
            // 更新结果
            max_len = max(max_len, right - left + 1);
        }
        
        return max_len;
    }
};

// 测试函数
#include <iostream>
void testLongestOnes() {
    Solution solution;
    
    // 测试用例1
    vector<int> nums1 = {1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0};
    int k1 = 2;
    int result1 = solution.longestOnes(nums1, k1);
    cout << "测试1: " << result1 << endl;
    
    // 测试用例2
    vector<int> nums2 = {0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1};
    int k2 = 3;
    int result2 = solution.longestOnes(nums2, k2);
    cout << "测试2: " << result2 << endl;
    
    // 测试用例3
    vector<int> nums3 = {0, 0, 0, 1};
    int k3 = 4;
    int result3 = solution.longestOnes(nums3, k3);
    cout << "测试3: " << result3 << endl;
}

int main() {
    testLongestOnes();
    return 0;
}
