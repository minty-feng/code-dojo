/**
 * LeetCode 75. 颜色分类
 * https://leetcode.cn/problems/sort-colors/
 * 
 * 给定一个包含红色、白色和蓝色，一共n个元素的数组，原地对它们进行排序，
 * 使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。
 * 
 * 三指针（荷兰国旗问题）
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <vector>
using namespace std;

class Solution {
public:
    void sortColors(vector<int>& nums) {
        int left = 0;      // 0的右边界
        int right = nums.size() - 1;  // 2的左边界
        int current = 0;    // 当前指针
        
        while (current <= right) {
            if (nums[current] == 0) {
                // 交换到左边界
                swap(nums[left], nums[current]);
                left++;
                current++;
            } else if (nums[current] == 2) {
                // 交换到右边界
                swap(nums[right], nums[current]);
                right--;
                // current不增加，因为交换过来的元素需要重新检查
            } else {
                // nums[current] == 1，直接跳过
                current++;
            }
        }
    }
};

// 测试函数
#include <iostream>
void testSortColors() {
    Solution solution;
    
    // 测试用例1
    vector<int> nums1 = {2, 0, 2, 1, 1, 0};
    solution.sortColors(nums1);
    cout << "测试1: [";
    for (int i = 0; i < nums1.size(); i++) {
        cout << nums1[i];
        if (i < nums1.size() - 1) cout << ",";
    }
    cout << "]" << endl;
    
    // 测试用例2
    vector<int> nums2 = {2, 0, 1};
    solution.sortColors(nums2);
    cout << "测试2: [";
    for (int i = 0; i < nums2.size(); i++) {
        cout << nums2[i];
        if (i < nums2.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testSortColors();
    return 0;
}
