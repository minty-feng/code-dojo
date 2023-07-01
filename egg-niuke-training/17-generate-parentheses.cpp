/**
 * NC137 括号生成
 * https://www.nowcoder.com/practice/c9addb265cdf4cdd92c092c655d164ca
 * 
 * 给出n对括号，请编写一个函数来生成所有的由n对括号组成的合法组合。
 * 
 * 时间复杂度：O(4^n / sqrt(n))
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    /**
     * 生成所有合法括号组合 - 回溯法
     */
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        backtrack(result, "", 0, 0, n);
        return result;
    }

private:
    void backtrack(vector<string>& result, string path, int left, int right, int n) {
        // 终止条件
        if (path.length() == 2 * n) {
            result.push_back(path);
            return;
        }
        
        // 添加左括号
        if (left < n) {
            backtrack(result, path + '(', left + 1, right, n);
        }
        
        // 添加右括号
        if (right < left) {
            backtrack(result, path + ')', left, right + 1, n);
        }
    }
};

int main() {
    Solution solution;
    
    for (int n = 1; n <= 4; n++) {
        vector<string> result = solution.generateParenthesis(n);
        
        cout << "n=" << n << ":" << endl;
        for (const string& s : result) {
            cout << "  " << s << endl;
        }
        cout << "共 " << result.size() << " 种组合\n" << endl;
    }
    
    return 0;
}

