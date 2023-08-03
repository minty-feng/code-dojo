/**
 * LeetCode 26. 删除排序数组中的重复项
 * https://leetcode.cn/problems/remove-duplicates-from-sorted-array/
 * 
 * 给你一个升序排列的数组nums，请你原地删除重复出现的元素，使每个元素只出现一次。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        int slow = 0;
        
        for (int fast = 1; fast < nums.size(); fast++) {
            if (nums[fast] != nums[slow]) {
                slow++;
                nums[slow] = nums[fast];
            }
        }
        
        return slow + 1;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {1, 1, 2},
        {0, 0, 1, 1, 1, 2, 2, 3, 3, 4},
        {1, 2, 3},
        {1}
    };
    
    for (auto& nums : testCases) {
        vector<int> original = nums;
        int length = solution.removeDuplicates(nums);
        
        cout << "原数组: ";
        for (int num : original) cout << num << " ";
        cout << endl;
        
        cout << "去重后长度: " << length << endl;
        
        cout << "去重后数组: ";
        for (int i = 0; i < length; i++) {
            cout << nums[i] << " ";
        }
        cout << "\n" << endl;
    }
    
    return 0;
}

