/**
 * LeetCode 49. 字母异位词分组
 * https://leetcode.cn/problems/group-anagrams/
 * 
 * 给你一个字符串数组，请你将字母异位词组合在一起。
 * 
 * 时间复杂度：O(nklogk)
 * 空间复杂度：O(nk)
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> groups;
        
        for (const string& s : strs) {
            string key = s;
            sort(key.begin(), key.end());
            groups[key].push_back(s);
        }
        
        vector<vector<string>> result;
        for (const auto& pair : groups) {
            result.push_back(pair.second);
        }
        
        return result;
    }
};

int main() {
    Solution solution;
    
    vector<vector<string>> testCases = {
        {"eat", "tea", "tan", "ate", "nat", "bat"},
        {""},
        {"a"}
    };
    
    for (auto& strs : testCases) {
        cout << "输入: [";
        for (size_t i = 0; i < strs.size(); i++) {
            cout << "\"" << strs[i] << "\"";
            if (i < strs.size() - 1) cout << ", ";
        }
        cout << "]" << endl;
        
        vector<vector<string>> result = solution.groupAnagrams(strs);
        
        cout << "分组结果:" << endl;
        for (const auto& group : result) {
            cout << "  [";
            for (size_t i = 0; i < group.size(); i++) {
                cout << "\"" << group[i] << "\"";
                if (i < group.size() - 1) cout << ", ";
            }
            cout << "]" << endl;
        }
        cout << endl;
    }
    
    return 0;
}

