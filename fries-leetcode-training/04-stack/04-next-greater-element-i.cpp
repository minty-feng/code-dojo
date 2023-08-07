/**
 * LeetCode 496. 下一个更大元素I
 * https://leetcode.cn/problems/next-greater-element-i/
 * 
 * 给你两个没有重复元素的数组nums1和nums2，其中nums1是nums2的子集。
 * 请你找出nums1中每个元素在nums2中的下一个比其大的值。
 * 
 * 单调栈 + 哈希表
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <vector>
#include <stack>
#include <unordered_map>
using namespace std;

class Solution {
public:
    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
        unordered_map<int, int> next_greater;
        stack<int> st;
        
        for (int num : nums2) {
            while (!st.empty() && num > st.top()) {
                next_greater[st.top()] = num;
                st.pop();
            }
            st.push(num);
        }
        
        vector<int> result;
        for (int num : nums1) {
            result.push_back(next_greater.count(num) ? next_greater[num] : -1);
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
void testNextGreaterElement() {
    Solution solution;
    
    vector<int> nums1 = {4, 1, 2};
    vector<int> nums2 = {1, 3, 4, 2};
    vector<int> result = solution.nextGreaterElement(nums1, nums2);
    
    cout << "测试1: [";
    for (int i = 0; i < result.size(); i++) {
        cout << result[i];
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testNextGreaterElement();
    return 0;
}
