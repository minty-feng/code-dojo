/**
 * AVL树实现
 * 严格平衡的二叉搜索树
 */

#include <iostream>
#include <algorithm>

struct AVLNode {
    int val;
    AVLNode* left;
    AVLNode* right;
    int height;
    
    AVLNode(int v) : val(v), left(nullptr), right(nullptr), height(1) {}
};


class AVLTree {
private:
    AVLNode* root;
    
    int getHeight(AVLNode* node) {
        return node ? node->height : 0;
    }
    
    void updateHeight(AVLNode* node) {
        if (node) {
            node->height = 1 + std::max(getHeight(node->left), getHeight(node->right));
        }
    }
    
    int getBalance(AVLNode* node) {
        if (!node) return 0;
        return getHeight(node->left) - getHeight(node->right);
    }
    
    AVLNode* rightRotate(AVLNode* z) {
        AVLNode* y = z->left;
        AVLNode* T3 = y->right;
        
        y->right = z;
        z->left = T3;
        
        updateHeight(z);
        updateHeight(y);
        
        return y;
    }
    
    AVLNode* leftRotate(AVLNode* z) {
        AVLNode* y = z->right;
        AVLNode* T3 = y->left;
        
        y->left = z;
        z->right = T3;
        
        updateHeight(z);
        updateHeight(y);
        
        return y;
    }
    
    AVLNode* insertHelper(AVLNode* node, int val) {
        // 1. BST插入
        if (!node) {
            return new AVLNode(val);
        }
        
        if (val < node->val) {
            node->left = insertHelper(node->left, val);
        } else if (val > node->val) {
            node->right = insertHelper(node->right, val);
        } else {
            return node;  // 重复值
        }
        
        // 2. 更新高度
        updateHeight(node);
        
        // 3. 获取平衡因子
        int balance = getBalance(node);
        
        // 4. 四种情况调整
        
        // LL
        if (balance > 1 && val < node->left->val) {
            return rightRotate(node);
        }
        
        // RR
        if (balance < -1 && val > node->right->val) {
            return leftRotate(node);
        }
        
        // LR
        if (balance > 1 && val > node->left->val) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }
        
        // RL
        if (balance < -1 && val < node->right->val) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }
        
        return node;
    }
    
    AVLNode* findMin(AVLNode* node) {
        while (node->left) {
            node = node->left;
        }
        return node;
    }
    
    void printTreeHelper(AVLNode* node, int level, std::string prefix) const {
        if (node) {
            int bf = getBalance(node);
            std::cout << std::string(level * 4, ' ') << prefix 
                      << node->val << "(h:" << node->height << ",bf:" << bf << ")" 
                      << std::endl;
            if (node->left || node->right) {
                printTreeHelper(node->left, level + 1, "L--- ");
                printTreeHelper(node->right, level + 1, "R--- ");
            }
        }
    }
    
    void deleteTree(AVLNode* node) {
        if (node) {
            deleteTree(node->left);
            deleteTree(node->right);
            delete node;
        }
    }

public:
    AVLTree() : root(nullptr) {}
    
    ~AVLTree() {
        deleteTree(root);
    }
    
    void insert(int val) {
        root = insertHelper(root, val);
    }
    
    void printTree() const {
        printTreeHelper(root, 0, "Root: ");
    }
};


int main() {
    std::cout << "=== AVL树演示 ===" << std::endl << std::endl;
    
    AVLTree avl;
    
    std::vector<int> values = {10, 20, 30, 40, 50, 25};
    std::cout << "依次插入: ";
    for (int val : values) {
        std::cout << val << " ";
    }
    std::cout << std::endl << std::endl;
    
    for (int val : values) {
        avl.insert(val);
        std::cout << "插入 " << val << ":" << std::endl;
        avl.printTree();
        std::cout << std::endl;
    }
    
    return 0;
}

