/**
 * 红黑树实现（简化版，仅实现插入）
 * 完整实现较复杂，建议学习STL源码
 */

#include <iostream>

enum Color { RED, BLACK };

struct RBNode {
    int val;
    Color color;
    RBNode* left;
    RBNode* right;
    RBNode* parent;
    
    RBNode(int v) : val(v), color(RED), left(nullptr), right(nullptr), parent(nullptr) {}
};


class RBTree {
private:
    RBNode* root;
    RBNode* NIL;  // 哨兵节点
    
    void leftRotate(RBNode* x) {
        RBNode* y = x->right;
        x->right = y->left;
        
        if (y->left != NIL) {
            y->left->parent = x;
        }
        
        y->parent = x->parent;
        
        if (!x->parent) {
            root = y;
        } else if (x == x->parent->left) {
            x->parent->left = y;
        } else {
            x->parent->right = y;
        }
        
        y->left = x;
        x->parent = y;
    }
    
    void rightRotate(RBNode* y) {
        RBNode* x = y->left;
        y->left = x->right;
        
        if (x->right != NIL) {
            x->right->parent = y;
        }
        
        x->parent = y->parent;
        
        if (!y->parent) {
            root = x;
        } else if (y == y->parent->left) {
            y->parent->left = x;
        } else {
            y->parent->right = x;
        }
        
        x->right = y;
        y->parent = x;
    }
    
    void insertFixup(RBNode* node) {
        while (node->parent && node->parent->color == RED) {
            if (node->parent == node->parent->parent->left) {
                RBNode* uncle = node->parent->parent->right;
                
                if (uncle->color == RED) {
                    // 情况1
                    node->parent->color = BLACK;
                    uncle->color = BLACK;
                    node->parent->parent->color = RED;
                    node = node->parent->parent;
                } else {
                    if (node == node->parent->right) {
                        // 情况2
                        node = node->parent;
                        leftRotate(node);
                    }
                    // 情况3
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    rightRotate(node->parent->parent);
                }
            } else {
                RBNode* uncle = node->parent->parent->left;
                
                if (uncle->color == RED) {
                    node->parent->color = BLACK;
                    uncle->color = BLACK;
                    node->parent->parent->color = RED;
                    node = node->parent->parent;
                } else {
                    if (node == node->parent->left) {
                        node = node->parent;
                        rightRotate(node);
                    }
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    leftRotate(node->parent->parent);
                }
            }
        }
        root->color = BLACK;
    }
    
    void printTreeHelper(RBNode* node, int level, std::string prefix) {
        if (node && node != NIL) {
            std::string colorStr = (node->color == RED) ? "🔴" : "⚫";
            std::cout << std::string(level * 4, ' ') << prefix 
                      << colorStr << node->val << std::endl;
            if (node->left != NIL || node->right != NIL) {
                printTreeHelper(node->left, level + 1, "L--- ");
                printTreeHelper(node->right, level + 1, "R--- ");
            }
        }
    }

public:
    RBTree() {
        NIL = new RBNode(0);
        NIL->color = BLACK;
        NIL->left = NIL->right = NIL->parent = nullptr;
        root = NIL;
    }
    
    void insert(int val) {
        RBNode* newNode = new RBNode(val);
        newNode->left = NIL;
        newNode->right = NIL;
        
        RBNode* parent = nullptr;
        RBNode* curr = root;
        
        while (curr != NIL) {
            parent = curr;
            if (val < curr->val) {
                curr = curr->left;
            } else {
                curr = curr->right;
            }
        }
        
        newNode->parent = parent;
        
        if (!parent) {
            root = newNode;
        } else if (val < parent->val) {
            parent->left = newNode;
        } else {
            parent->right = newNode;
        }
        
        insertFixup(newNode);
    }
    
    void printTree() {
        printTreeHelper(root, 0, "Root: ");
    }
};


int main() {
    std::cout << "=== 红黑树演示 ===" << std::endl << std::endl;
    
    RBTree tree;
    
    std::vector<int> values = {7, 3, 18, 10, 22, 8, 11, 26};
    std::cout << "插入节点: ";
    for (int val : values) {
        std::cout << val << " ";
    }
    std::cout << std::endl << std::endl;
    
    for (int val : values) {
        tree.insert(val);
        std::cout << "插入 " << val << ":" << std::endl;
        tree.printTree();
        std::cout << std::endl;
    }
    
    return 0;
}

