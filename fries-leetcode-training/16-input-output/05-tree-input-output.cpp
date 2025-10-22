/*
05-树结构输入输出处理

题目描述：
演示二叉树的输入输出处理，包括层序遍历构建和输出。

输入格式：
第一行：整数n（节点数量）
第二行：n个整数，按层序遍历顺序，null用-1表示

输出格式：
输出二叉树的层序遍历结果

示例：
输入：
7
1 2 3 4 5 6 7

输出：
1 2 3 4 5 6 7
*/

#include <iostream>
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* left, TreeNode* right) : val(x), left(left), right(right) {}
};

TreeNode* buildTreeFromLevelOrder(const vector<int>& values) {
    if (values.empty() || values[0] == -1) return nullptr;
    
    TreeNode* root = new TreeNode(values[0]);
    queue<TreeNode*> q;
    q.push(root);
    
    int i = 1;
    while (!q.empty() && i < values.size()) {
        TreeNode* node = q.front();
        q.pop();
        
        // 左子节点
        if (i < values.size() && values[i] != -1) {
            node->left = new TreeNode(values[i]);
            q.push(node->left);
        }
        i++;
        
        // 右子节点
        if (i < values.size() && values[i] != -1) {
            node->right = new TreeNode(values[i]);
            q.push(node->right);
        }
        i++;
    }
    
    return root;
}

vector<int> levelOrderTraversal(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    
    queue<TreeNode*> q;
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

void printTreeLevelOrder(TreeNode* root) {
    vector<int> values = levelOrderTraversal(root);
    for (int i = 0; i < values.size(); i++) {
        cout << values[i];
        if (i < values.size() - 1) cout << " ";
    }
    cout << endl;
}

void deleteTree(TreeNode* root) {
    if (!root) return;
    
    queue<TreeNode*> q;
    q.push(root);
    
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        
        if (node->left) q.push(node->left);
        if (node->right) q.push(node->right);
        
        delete node;
    }
}

void testCases() {
    cout << "=== 树结构输入输出测试 ===" << endl;
    
    // 模拟输入
    vector<int> values = {1, 2, 3, 4, 5, 6, 7};
    cout << "输入数组: ";
    for (int i = 0; i < values.size(); i++) {
        cout << values[i];
        if (i < values.size() - 1) cout << " ";
    }
    cout << endl;
    
    // 构建二叉树
    TreeNode* root = buildTreeFromLevelOrder(values);
    
    // 输出层序遍历
    cout << "层序遍历输出:" << endl;
    printTreeLevelOrder(root);
    
    // 测试包含null的情况
    cout << "\n包含null的测试:" << endl;
    vector<int> nullValues = {1, 2, 3, -1, -1, 4, 5};
    cout << "输入数组: ";
    for (int i = 0; i < nullValues.size(); i++) {
        cout << nullValues[i];
        if (i < nullValues.size() - 1) cout << " ";
    }
    cout << endl;
    
    TreeNode* nullRoot = buildTreeFromLevelOrder(nullValues);
    printTreeLevelOrder(nullRoot);
    
    // 清理内存
    deleteTree(root);
    deleteTree(nullRoot);
}

int main() {
    // 运行测试
    testCases();
    
    // 交互式输入（取消注释以启用）
    // int n;
    // cin >> n;
    // vector<int> values(n);
    // for (int i = 0; i < n; i++) {
    //     cin >> values[i];
    // }
    // TreeNode* root = buildTreeFromLevelOrder(values);
    // printTreeLevelOrder(root);
    // deleteTree(root);
    
    return 0;
}
