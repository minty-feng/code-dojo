/**
 * LeetCode 567. 字符串的排列
 * https://leetcode.cn/problems/permutation-in-string/
 * 
 * 给你两个字符串s1和s2，写一个函数来判断s2是否包含s1的排列。
 * 换句话说，第一个字符串的排列之一是第二个字符串的子串。
 * 
 * 滑动窗口 + 哈希表
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <string>
#include <unordered_map>
using namespace std;

class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        if (s1.length() > s2.length()) {
            return false;
        }
        
        // 统计s1中每个字符的频次
        unordered_map<char, int> need;
        for (char c : s1) {
            need[c]++;
        }
        
        // 滑动窗口
        unordered_map<char, int> window;
        int left = 0;
        int valid = 0;
        
        for (int right = 0; right < s2.length(); right++) {
            char c = s2[right];
            
            // 扩展窗口
            if (need.count(c)) {
                window[c]++;
                if (window[c] == need[c]) {
                    valid++;
                }
            }
            
            // 收缩窗口
            while (right - left + 1 >= s1.length()) {
                if (valid == need.size()) {
                    return true;
                }
                
                char d = s2[left];
                left++;
                
                if (need.count(d)) {
                    if (window[d] == need[d]) {
                        valid--;
                    }
                    window[d]--;
                }
            }
        }
        
        return false;
    }
};

// 测试函数
#include <iostream>
void testCheckInclusion() {
    Solution solution;
    
    // 测试用例1
    string s1_1 = "ab", s2_1 = "eidbaooo";
    bool result1 = solution.checkInclusion(s1_1, s2_1);
    cout << "测试1: " << (result1 ? "True" : "False") << endl;
    
    // 测试用例2
    string s1_2 = "ab", s2_2 = "eidboaoo";
    bool result2 = solution.checkInclusion(s1_2, s2_2);
    cout << "测试2: " << (result2 ? "True" : "False") << endl;
    
    // 测试用例3
    string s1_3 = "adc", s2_3 = "dcda";
    bool result3 = solution.checkInclusion(s1_3, s2_3);
    cout << "测试3: " << (result3 ? "True" : "False") << endl;
}

int main() {
    testCheckInclusion();
    return 0;
}
