/**
 * NC120 滑动窗口最大值
 * https://www.nowcoder.com/practice/1624bc35a45c42c0bc17d17fa0cba788
 * 
 * 给定一个数组和滑动窗口的大小，找出所有滑动窗口里数值的最大值。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(k)
 */

#include <iostream>
#include <vector>
#include <deque>
using namespace std;

class Solution {
public:
    vector<int> maxInWindows(vector<int>& nums, int size) {
        vector<int> result;
        if (nums.empty() || size <= 0 || size > nums.size()) {
            return result;
        }
        
        deque<int> dq;  // 存储索引
        
        for (int i = 0; i < nums.size(); i++) {
            // 移除超出窗口的元素
            while (!dq.empty() && dq.front() <= i - size) {
                dq.pop_front();
            }
            
            // 维护单调递减队列
            while (!dq.empty() && nums[dq.back()] <= nums[i]) {
                dq.pop_back();
            }
            
            dq.push_back(i);
            
            // 窗口形成后，记录最大值
            if (i >= size - 1) {
                result.push_back(nums[dq.front()]);
            }
        }
        
        return result;
    }
};

int main() {
    Solution solution;
    
    vector<int> nums = {2, 3, 4, 2, 6, 2, 5, 1};
    int size = 3;
    
    cout << "数组: ";
    for (int num : nums) cout << num << " ";
    cout << endl;
    cout << "窗口大小: " << size << endl;
    
    vector<int> result = solution.maxInWindows(nums, size);
    
    cout << "滑动窗口最大值: ";
    for (int val : result) cout << val << " ";
    cout << endl;
    
    return 0;
}

