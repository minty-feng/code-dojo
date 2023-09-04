/**
 * NC6 二叉树中和为某一值的路径
 * https://www.nowcoder.com/practice/b736e784e3e34731af99065031301bca
 * 
 * 输入一颗二叉树的根节点root和一个整数expectNumber，找出二叉树中结点值的和为expectNumber的所有路径。
 * 
 * 时间复杂度：O(n^2)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    vector<vector<int>> FindPath(TreeNode* root, int expectNumber) {
        vector<vector<int>> result;
        if (!root) return result;
        
        vector<int> path;
        dfs(root, expectNumber, path, result);
        return result;
    }

private:
    void dfs(TreeNode* node, int remaining, vector<int>& path, vector<vector<int>>& result) {
        if (!node) return;
        
        // 添加当前节点
        path.push_back(node->val);
        remaining -= node->val;
        
        // 叶子节点且和为target
        if (!node->left && !node->right && remaining == 0) {
            result.push_back(path);
        }
        
        // 递归左右子树
        dfs(node->left, remaining, path, result);
        dfs(node->right, remaining, path, result);
        
        // 回溯
        path.pop_back();
    }
};

int main() {
    TreeNode* root = new TreeNode(10);
    root->left = new TreeNode(5);
    root->right = new TreeNode(12);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(7);
    
    int target = 22;
    Solution solution;
    vector<vector<int>> result = solution.FindPath(root, target);
    
    cout << "和为" << target << "的路径:" << endl;
    for (const auto& path : result) {
        cout << "[";
        for (size_t i = 0; i < path.size(); i++) {
            cout << path[i];
            if (i < path.size() - 1) cout << ", ";
        }
        cout << "]" << endl;
    }
    
    return 0;
}

