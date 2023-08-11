/**
 * LeetCode 106. 从中序与后序遍历序列构造二叉树
 * https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/
 * 
 * 给定两个整数数组inorder和postorder，其中inorder是二叉树的中序遍历，postorder是同一棵树的后序遍历，
 * 请构造并返回这颗二叉树。
 * 
 * 递归构建
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
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
    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        if (inorder.empty() || postorder.empty()) {
            return nullptr;
        }
        
        // 创建中序遍历的索引映射
        unordered_map<int, int> inorder_map;
        for (int i = 0; i < inorder.size(); i++) {
            inorder_map[inorder[i]] = i;
        }
        
        int postorder_idx = postorder.size() - 1;
        return buildTreeHelper(inorder, inorder_map, postorder, postorder_idx, 0, inorder.size() - 1);
    }
    
private:
    TreeNode* buildTreeHelper(vector<int>& inorder, unordered_map<int, int>& inorder_map,
                              vector<int>& postorder, int& postorder_idx, int left, int right) {
        if (left > right) {
            return nullptr;
        }
        
        // 选择postorder_idx位置的元素作为根节点
        int root_val = postorder[postorder_idx--];
        TreeNode* root = new TreeNode(root_val);
        
        // 在中序遍历中找到根节点的位置
        int root_index = inorder_map[root_val];
        
        // 先构建右子树，再构建左子树（因为后序遍历是左右根）
        root->right = buildTreeHelper(inorder, inorder_map, postorder, postorder_idx, root_index + 1, right);
        root->left = buildTreeHelper(inorder, inorder_map, postorder, postorder_idx, left, root_index - 1);
        
        return root;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

void testBuildTree() {
    Solution solution;
    
    vector<int> inorder = {9, 3, 15, 20, 7};
    vector<int> postorder = {9, 15, 7, 20, 3};
    
    TreeNode* root = solution.buildTree(inorder, postorder);
    
    // 验证构造的树
    cout << "构造的树根节点值: " << root->val << endl;
    cout << "左子树根节点值: " << (root->left ? to_string(root->left->val) : "null") << endl;
    cout << "右子树根节点值: " << (root->right ? to_string(root->right->val) : "null") << endl;
}

int main() {
    testBuildTree();
    return 0;
}
