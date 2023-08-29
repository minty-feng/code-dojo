/**
 * LeetCode 136. 只出现一次的数字
 * https://leetcode.cn/problems/single-number/
 * 
 * 给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现两次。
 * 找出那个只出现了一次的元素。
 * 
 * 位运算
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int result = 0;
        
        for (int num : nums) {
            result ^= num;
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testSingleNumber() {
    Solution solution;
    
    vector<int> nums1 = {2, 2, 1};
    int result1 = solution.singleNumber(nums1);
    cout << "测试1 [2,2,1]: " << result1 << endl;  // 期望: 1
    
    vector<int> nums2 = {4, 1, 2, 1, 2};
    int result2 = solution.singleNumber(nums2);
    cout << "测试2 [4,1,2,1,2]: " << result2 << endl;  // 期望: 4
    
    vector<int> nums3 = {1};
    int result3 = solution.singleNumber(nums3);
    cout << "测试3 [1]: " << result3 << endl;  // 期望: 1
}

int main() {
    testSingleNumber();
    return 0;
}
