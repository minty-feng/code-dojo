/**
 * 二叉搜索树（BST）实现
 */

#include <iostream>
#include <vector>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};


class BST {
private:
    TreeNode* root;
    
    TreeNode* insertHelper(TreeNode* node, int val) {
        if (!node) {
            return new TreeNode(val);
        }
        
        if (val < node->val) {
            node->left = insertHelper(node->left, val);
        } else if (val > node->val) {
            node->right = insertHelper(node->right, val);
        }
        
        return node;
    }
    
    TreeNode* deleteHelper(TreeNode* node, int val) {
        if (!node) {
            return nullptr;
        }
        
        if (val < node->val) {
            node->left = deleteHelper(node->left, val);
        } else if (val > node->val) {
            node->right = deleteHelper(node->right, val);
        } else {
            // 找到要删除的节点
            
            // 情况1：没有子节点或只有一个子节点
            if (!node->left) {
                TreeNode* temp = node->right;
                delete node;
                return temp;
            }
            if (!node->right) {
                TreeNode* temp = node->left;
                delete node;
                return temp;
            }
            
            // 情况2：有两个子节点
            TreeNode* successor = findMin(node->right);
            node->val = successor->val;
            node->right = deleteHelper(node->right, successor->val);
        }
        
        return node;
    }
    
    TreeNode* findMin(TreeNode* node) const {
        while (node->left) {
            node = node->left;
        }
        return node;
    }
    
    TreeNode* findMax(TreeNode* node) const {
        while (node->right) {
            node = node->right;
        }
        return node;
    }
    
    void inorderHelper(TreeNode* node, std::vector<int>& result) const {
        if (node) {
            inorderHelper(node->left, result);
            result.push_back(node->val);
            inorderHelper(node->right, result);
        }
    }
    
    void printTreeHelper(TreeNode* node, int level, std::string prefix) const {
        if (node) {
            std::cout << std::string(level * 4, ' ') << prefix << node->val << std::endl;
            if (node->left || node->right) {
                printTreeHelper(node->left, level + 1, "L--- ");
                printTreeHelper(node->right, level + 1, "R--- ");
            }
        }
    }
    
    void deleteTree(TreeNode* node) {
        if (node) {
            deleteTree(node->left);
            deleteTree(node->right);
            delete node;
        }
    }

public:
    BST() : root(nullptr) {}
    
    ~BST() {
        deleteTree(root);
    }
    
    void insert(int val) {
        root = insertHelper(root, val);
    }
    
    void remove(int val) {
        root = deleteHelper(root, val);
    }
    
    TreeNode* search(int val) const {
        TreeNode* curr = root;
        while (curr && curr->val != val) {
            if (val < curr->val) {
                curr = curr->left;
            } else {
                curr = curr->right;
            }
        }
        return curr;
    }
    
    int getMin() const {
        if (!root) throw std::runtime_error("Empty tree");
        return findMin(root)->val;
    }
    
    int getMax() const {
        if (!root) throw std::runtime_error("Empty tree");
        return findMax(root)->val;
    }
    
    std::vector<int> inorder() const {
        std::vector<int> result;
        inorderHelper(root, result);
        return result;
    }
    
    void printTree() const {
        printTreeHelper(root, 0, "Root: ");
    }
};


int main() {
    std::cout << "=== 二叉搜索树演示 ===" << std::endl << std::endl;
    
    BST bst;
    
    // 插入
    std::vector<int> values = {5, 3, 7, 2, 4, 6, 8};
    std::cout << "插入节点: ";
    for (int val : values) {
        std::cout << val << " ";
        bst.insert(val);
    }
    std::cout << std::endl << std::endl;
    
    std::cout << "树结构:" << std::endl;
    bst.printTree();
    
    // 遍历
    std::cout << "\n中序遍历（有序）: [";
    std::vector<int> inorder_result = bst.inorder();
    for (size_t i = 0; i < inorder_result.size(); i++) {
        std::cout << inorder_result[i];
        if (i < inorder_result.size() - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;
    
    // 查找
    int search_val = 4;
    TreeNode* found = bst.search(search_val);
    std::cout << "\n查找 " << search_val << ": " 
              << (found ? "找到" : "未找到") << std::endl;
    
    // 最小最大值
    std::cout << "最小值: " << bst.getMin() << std::endl;
    std::cout << "最大值: " << bst.getMax() << std::endl;
    
    // 删除
    std::cout << "\n删除节点 3" << std::endl;
    bst.remove(3);
    std::cout << "树结构:" << std::endl;
    bst.printTree();
    
    return 0;
}

