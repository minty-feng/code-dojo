/**
 * NC14 二叉树的锯齿形层序遍历
 * https://www.nowcoder.com/practice/91b69814117f4e8097390d107d2efbe0
 * 
 * 给定一个二叉树，返回该二叉树层序遍历的结果，从左往右，下一层从右往左。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (!root) return result;
        
        queue<TreeNode*> q;
        q.push(root);
        int level = 0;
        
        while (!q.empty()) {
            int levelSize = q.size();
            vector<int> levelNodes;
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode* node = q.front();
                q.pop();
                levelNodes.push_back(node->val);
                
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            
            // 奇数层反转
            if (level % 2 == 1) {
                reverse(levelNodes.begin(), levelNodes.end());
            }
            
            result.push_back(levelNodes);
            level++;
        }
        
        return result;
    }
};

int main() {
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    
    Solution solution;
    vector<vector<int>> result = solution.zigzagLevelOrder(root);
    
    cout << "锯齿形层序遍历:" << endl;
    for (const auto& level : result) {
        cout << "[";
        for (size_t i = 0; i < level.size(); i++) {
            cout << level[i];
            if (i < level.size() - 1) cout << ", ";
        }
        cout << "]" << endl;
    }
    
    return 0;
}

