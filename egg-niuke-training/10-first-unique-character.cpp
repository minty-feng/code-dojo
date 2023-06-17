/**
 * 第一个只出现一次的字符
 * 
 * 在一个长度为 n 字符串中找到第一个只出现一次的字符,并返回它的位置。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

class Solution {
public:
    /**
     * 找到第一个只出现一次的字符
     */
    int FirstUniqChar(string s) {
        // 统计频次
        unordered_map<char, int> charCount;
        for (char ch : s) {
            charCount[ch]++;
        }
        
        // 找第一个频次为1的
        for (int i = 0; i < s.length(); i++) {
            if (charCount[s[i]] == 1) {
                return i;
            }
        }
        
        return -1;
    }
    
    /**
     * 使用数组代替哈希表（只有小写字母的情况）
     */
    int FirstUniqChar_Array(string s) {
        int count[26] = {0};
        
        // 统计频次
        for (char ch : s) {
            count[ch - 'a']++;
        }
        
        // 找第一个频次为1的
        for (int i = 0; i < s.length(); i++) {
            if (count[s[i] - 'a'] == 1) {
                return i;
            }
        }
        
        return -1;
    }
};

int main() {
    Solution solution;
    
    vector<string> testCases = {
        "leetcode",
        "loveleetcode",
        "aabb",
        "abcdefg"
    };
    
    for (const string& s : testCases) {
        int result = solution.FirstUniqChar(s);
        cout << "字符串 '" << s << "' 的第一个唯一字符位置: " << result;
        if (result != -1) {
            cout << " (字符: '" << s[result] << "')";
        }
        cout << endl;
    }
    
    return 0;
}

