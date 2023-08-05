/**
 * LeetCode 3. 无重复字符的最长子串
 * https://leetcode.cn/problems/longest-substring-without-repeating-characters/
 * 
 * 给定一个字符串s，请你找出其中不含有重复字符的最长子串的长度。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(min(m,n))
 */

#include <iostream>
#include <string>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        if (s.empty()) return 0;
        
        unordered_set<char> charSet;
        int left = 0;
        int maxLength = 0;
        
        for (int right = 0; right < s.length(); right++) {
            // 如果右指针字符已存在，移动左指针
            while (charSet.count(s[right])) {
                charSet.erase(s[left]);
                left++;
            }
            
            // 添加右指针字符
            charSet.insert(s[right]);
            maxLength = max(maxLength, right - left + 1);
        }
        
        return maxLength;
    }
};

int main() {
    Solution solution;
    
    vector<string> testCases = {
        "abcabcbb",
        "bbbbb",
        "pwwkew",
        ""
    };
    
    for (const string& s : testCases) {
        int result = solution.lengthOfLongestSubstring(s);
        cout << "字符串: '" << s << "'" << endl;
        cout << "最长无重复子串长度: " << result << "\n" << endl;
    }
    
    return 0;
}

