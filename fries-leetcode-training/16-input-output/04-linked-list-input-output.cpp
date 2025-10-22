/*
04-链表输入输出处理

题目描述：
演示链表的输入输出处理，包括链表构建和遍历。

输入格式：
第一行：整数n（链表长度）
第二行：n个整数，表示链表节点的值

输出格式：
输出链表的所有节点值，空格分隔

示例：
输入：
5
1 2 3 4 5

输出：
1 2 3 4 5
*/

#include <iostream>
#include <vector>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};

ListNode* buildLinkedList(const vector<int>& values) {
    if (values.empty()) return nullptr;
    
    ListNode* head = new ListNode(values[0]);
    ListNode* current = head;
    
    for (int i = 1; i < values.size(); i++) {
        current->next = new ListNode(values[i]);
        current = current->next;
    }
    
    return head;
}

void printLinkedList(ListNode* head) {
    vector<int> values;
    ListNode* current = head;
    
    while (current) {
        values.push_back(current->val);
        current = current->next;
    }
    
    for (int i = 0; i < values.size(); i++) {
        cout << values[i];
        if (i < values.size() - 1) cout << " ";
    }
    cout << endl;
}

vector<int> linkedListToArray(ListNode* head) {
    vector<int> result;
    ListNode* current = head;
    
    while (current) {
        result.push_back(current->val);
        current = current->next;
    }
    
    return result;
}

void deleteLinkedList(ListNode* head) {
    while (head) {
        ListNode* temp = head;
        head = head->next;
        delete temp;
    }
}

void testCases() {
    cout << "=== 链表输入输出测试 ===" << endl;
    
    // 模拟输入
    vector<int> values = {1, 2, 3, 4, 5};
    cout << "输入数组: ";
    for (int i = 0; i < values.size(); i++) {
        cout << values[i];
        if (i < values.size() - 1) cout << " ";
    }
    cout << endl;
    
    // 构建链表
    ListNode* head = buildLinkedList(values);
    
    // 输出链表
    cout << "输出链表:" << endl;
    printLinkedList(head);
    
    // 验证转换
    vector<int> converted = linkedListToArray(head);
    cout << "转换回数组: ";
    for (int i = 0; i < converted.size(); i++) {
        cout << converted[i];
        if (i < converted.size() - 1) cout << " ";
    }
    cout << endl;
    
    // 测试空链表
    cout << "\n空链表测试:" << endl;
    ListNode* emptyHead = buildLinkedList({});
    printLinkedList(emptyHead);
    
    // 清理内存
    deleteLinkedList(head);
    deleteLinkedList(emptyHead);
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
    // ListNode* head = buildLinkedList(values);
    // printLinkedList(head);
    // deleteLinkedList(head);
    
    return 0;
}
