/**
 * LeetCode 438. 找到字符串中所有字母异位词
 * https://leetcode.cn/problems/find-all-anagrams-in-a-string/
 * 
 * 给定两个字符串s和p，找到s中所有p的字母异位词的子串，返回这些子串的起始索引。
 * 
 * 时间复杂度：O(|s| + |p|)
 * 空间复杂度：O(|s| + |p|)
 */

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        if (s.length() < p.length()) {
            return {};
        }
        
        unordered_map<char, int> need;
        for (char c : p) {
            need[c]++;
        }
        
        int left = 0;
        int valid = 0;
        unordered_map<char, int> window;
        vector<int> result;
        
        for (int right = 0; right < s.length(); right++) {
            char c = s[right];
            window[c]++;
            
            if (need.count(c) && window[c] == need[c]) {
                valid++;
            }
            
            while (right - left + 1 >= p.length()) {
                if (valid == need.size()) {
                    result.push_back(left);
                }
                
                char d = s[left];
                left++;
                
                if (need.count(d)) {
                    if (window[d] == need[d]) {
                        valid--;
                    }
                    window[d]--;
                }
            }
        }
        
        return result;
    }
};

int main() {
    Solution solution;
    vector<pair<string, string>> testCases = {
        {"cbaebabacd", "abc"},
        {"abab", "ab"},
        {"baa", "aa"}
    };
    
    for (auto& testCase : testCases) {
        string s = testCase.first;
        string p = testCase.second;
        
        cout << "s: '" << s << "', p: '" << p << "'" << endl;
        
        vector<int> result = solution.findAnagrams(s, p);
        cout << "字母异位词起始索引: ";
        for (int idx : result) cout << idx << " ";
        cout << "\n" << endl;
    }
    
    return 0;
}

