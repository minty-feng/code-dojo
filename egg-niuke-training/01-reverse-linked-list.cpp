/**
 * NC78 反转链表
 * https://www.nowcoder.com/practice/75e878df47f24fdc9dc3e400ec6058ca
 * 
 * 给定一个单链表的头节点head，请反转链表，并返回反转后链表的头节点。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    /**
     * 反转链表 - 迭代法
     */
    ListNode* ReverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;
        
        while (curr) {
            ListNode* next = curr->next;  // 保存下一个节点
            curr->next = prev;             // 反转指针
            prev = curr;                   // prev前进
            curr = next;                   // curr前进
        }
        
        return prev;
    }
    
    /**
     * 反转链表 - 递归法
     */
    ListNode* ReverseListRecursive(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }
        
        // 递归反转后面的链表
        ListNode* newHead = ReverseListRecursive(head->next);
        
        // 当前节点的下一个节点指向当前节点
        head->next->next = head;
        head->next = nullptr;
        
        return newHead;
    }
};

// 辅助函数
ListNode* createList(int arr[], int n) {
    if (n == 0) return nullptr;
    ListNode* head = new ListNode(arr[0]);
    ListNode* curr = head;
    for (int i = 1; i < n; i++) {
        curr->next = new ListNode(arr[i]);
        curr = curr->next;
    }
    return head;
}

void printList(ListNode* head) {
    while (head) {
        cout << head->val;
        if (head->next) cout << " -> ";
        head = head->next;
    }
    cout << endl;
}

int main() {
    Solution solution;
    
    int arr[] = {1, 2, 3, 4, 5};
    ListNode* head = createList(arr, 5);
    
    cout << "原链表: ";
    printList(head);
    
    head = solution.ReverseList(head);
    
    cout << "反转后: ";
    printList(head);
    
    return 0;
}

