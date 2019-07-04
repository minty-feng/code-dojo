/**
 * 二叉树实现和遍历
 */

#include <iostream>
#include <vector>
#include <stack>
#include <queue>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};


class BinaryTree {
public:
    TreeNode* root;
    
    BinaryTree() : root(nullptr) {}
    
    // ========== 递归遍历 ==========
    
    void preorder(TreeNode* node, std::vector<int>& result) {
        if (!node) return;
        result.push_back(node->val);
        preorder(node->left, result);
        preorder(node->right, result);
    }
    
    void inorder(TreeNode* node, std::vector<int>& result) {
        if (!node) return;
        inorder(node->left, result);
        result.push_back(node->val);
        inorder(node->right, result);
    }
    
    void postorder(TreeNode* node, std::vector<int>& result) {
        if (!node) return;
        postorder(node->left, result);
        postorder(node->right, result);
        result.push_back(node->val);
    }
    
    // ========== 迭代遍历 ==========
    
    std::vector<int> preorderIterative(TreeNode* root) {
        std::vector<int> result;
        if (!root) return result;
        
        std::stack<TreeNode*> st;
        st.push(root);
        
        while (!st.empty()) {
            TreeNode* node = st.top();
            st.pop();
            result.push_back(node->val);
            
            if (node->right) st.push(node->right);
            if (node->left) st.push(node->left);
        }
        
        return result;
    }
    
    std::vector<int> inorderIterative(TreeNode* root) {
        std::vector<int> result;
        std::stack<TreeNode*> st;
        TreeNode* curr = root;
        
        while (curr || !st.empty()) {
            while (curr) {
                st.push(curr);
                curr = curr->left;
            }
            curr = st.top();
            st.pop();
            result.push_back(curr->val);
            curr = curr->right;
        }
        
        return result;
    }
    
    std::vector<int> levelorder(TreeNode* root) {
        std::vector<int> result;
        if (!root) return result;
        
        std::queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            result.push_back(node->val);
            
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        
        return result;
    }
    
    // ========== 树的性质 ==========
    
    int height(TreeNode* node) {
        if (!node) return 0;
        return 1 + std::max(height(node->left), height(node->right));
    }
    
    int countNodes(TreeNode* node) {
        if (!node) return 0;
        return 1 + countNodes(node->left) + countNodes(node->right);
    }
    
    void mirror(TreeNode* node) {
        if (!node) return;
        std::swap(node->left, node->right);
        mirror(node->left);
        mirror(node->right);
    }
    
    // ========== 打印 ==========
    
    void printVector(const std::vector<int>& vec) {
        std::cout << "[";
        for (size_t i = 0; i < vec.size(); i++) {
            std::cout << vec[i];
            if (i < vec.size() - 1) std::cout << ", ";
        }
        std::cout << "]" << std::endl;
    }
    
    ~BinaryTree() {
        deleteTree(root);
    }
    
    void deleteTree(TreeNode* node) {
        if (node) {
            deleteTree(node->left);
            deleteTree(node->right);
            delete node;
        }
    }
};


int main() {
    std::cout << "=== 二叉树演示 ===" << std::endl << std::endl;
    
    // 构建树
    //       1
    //      / \
    //     2   3
    //    / \
    //   4   5
    
    BinaryTree tree;
    tree.root = new TreeNode(1);
    tree.root->left = new TreeNode(2);
    tree.root->right = new TreeNode(3);
    tree.root->left->left = new TreeNode(4);
    tree.root->left->right = new TreeNode(5);
    
    // 遍历
    std::vector<int> result;
    
    tree.preorder(tree.root, result);
    std::cout << "前序遍历（递归）: ";
    tree.printVector(result);
    
    std::cout << "前序遍历（迭代）: ";
    tree.printVector(tree.preorderIterative(tree.root));
    std::cout << std::endl;
    
    result.clear();
    tree.inorder(tree.root, result);
    std::cout << "中序遍历（递归）: ";
    tree.printVector(result);
    
    std::cout << "中序遍历（迭代）: ";
    tree.printVector(tree.inorderIterative(tree.root));
    std::cout << std::endl;
    
    result.clear();
    tree.postorder(tree.root, result);
    std::cout << "后序遍历（递归）: ";
    tree.printVector(result);
    std::cout << std::endl;
    
    std::cout << "层序遍历: ";
    tree.printVector(tree.levelorder(tree.root));
    std::cout << std::endl;
    
    // 性质
    std::cout << "树的高度: " << tree.height(tree.root) << std::endl;
    std::cout << "节点数: " << tree.countNodes(tree.root) << std::endl;
    
    return 0;
}

