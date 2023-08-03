/**
 * LeetCode 11. 盛最多水的容器
 * https://leetcode.cn/problems/container-with-most-water/
 * 
 * 给定一个长度为n的整数数组height。找出其中的两条线，使得它们与x轴共同构成的容器可以容纳最多的水。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxArea(vector<int>& height) {
        int left = 0, right = height.size() - 1;
        int maxWater = 0;
        
        while (left < right) {
            // 计算当前容器的面积
            int width = right - left;
            int h = min(height[left], height[right]);
            int area = width * h;
            maxWater = max(maxWater, area);
            
            // 移动较短的边
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        
        return maxWater;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {1, 8, 6, 2, 5, 4, 8, 3, 7},
        {1, 1},
        {4, 3, 2, 1, 4}
    };
    
    for (auto& height : testCases) {
        cout << "高度数组: ";
        for (int h : height) cout << h << " ";
        cout << endl;
        
        int result = solution.maxArea(height);
        cout << "最大面积: " << result << "\n" << endl;
    }
    
    return 0;
}

