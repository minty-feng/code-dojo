/**
 * LeetCode 199. 二叉树的右视图
 * https://leetcode.cn/problems/binary-tree-right-side-view/
 * 
 * 给定一个二叉树的根节点root，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。
 * 
 * BFS层序遍历
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(w) w为树的最大宽度
 */

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int> result;
        if (!root) {
            return result;
        }
        
        queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty()) {
            int level_size = q.size();
            
            for (int i = 0; i < level_size; i++) {
                TreeNode* node = q.front();
                q.pop();
                
                // 如果是当前层的最后一个节点，加入结果
                if (i == level_size - 1) {
                    result.push_back(node->val);
                }
                
                if (node->left) {
                    q.push(node->left);
                }
                if (node->right) {
                    q.push(node->right);
                }
            }
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

void testRightSideView() {
    Solution solution;
    
    // 创建测试二叉树: [1,2,3,null,5,null,4]
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->right = new TreeNode(5);
    root->right->right = new TreeNode(4);
    
    vector<int> result = solution.rightSideView(root);
    
    cout << "右视图: [";
    for (int i = 0; i < result.size(); i++) {
        cout << result[i];
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;  // 期望: [1,3,4]
}

int main() {
    testRightSideView();
    return 0;
}
