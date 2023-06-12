/**
 * NC79 二叉搜索树与双向链表
 * https://www.nowcoder.com/practice/947f6eb80d944a84850b0538bf0ec3a5
 * 
 * 输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的双向链表。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(h)
 */

#include <iostream>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    TreeNode* Convert(TreeNode* root) {
        if (!root) return nullptr;
        
        inorder(root);
        return head;
    }

private:
    TreeNode* prev = nullptr;
    TreeNode* head = nullptr;
    
    void inorder(TreeNode* node) {
        if (!node) return;
        
        // 左子树
        inorder(node->left);
        
        // 处理当前节点
        if (prev) {
            prev->right = node;
            node->left = prev;
        } else {
            head = node;  // 记录头节点
        }
        prev = node;
        
        // 右子树
        inorder(node->right);
    }
};

int main() {
    // 创建BST
    TreeNode* root = new TreeNode(4);
    root->left = new TreeNode(2);
    root->right = new TreeNode(6);
    root->left->left = new TreeNode(1);
    root->left->right = new TreeNode(3);
    root->right->left = new TreeNode(5);
    root->right->right = new TreeNode(7);
    
    Solution solution;
    TreeNode* head = solution.Convert(root);
    
    // 打印双向链表
    cout << "正向遍历: ";
    TreeNode* curr = head;
    TreeNode* tail = nullptr;
    while (curr) {
        cout << curr->val << " ";
        if (!curr->right) tail = curr;
        curr = curr->right;
    }
    
    cout << "\n反向遍历: ";
    curr = tail;
    while (curr) {
        cout << curr->val << " ";
        curr = curr->left;
    }
    cout << endl;
    
    return 0;
}

