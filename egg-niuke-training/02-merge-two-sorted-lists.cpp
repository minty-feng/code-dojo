/**
 * NC33 合并两个排序的链表
 * https://www.nowcoder.com/practice/d8b6b4358f774294a89de2a6ac4d9337
 * 
 * 输入两个递增的链表，合并这两个链表并使新链表中的节点仍然是递增排序的。
 * 
 * 时间复杂度：O(n+m)
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
     * 合并两个排序链表 - 迭代法
     */
    ListNode* Merge(ListNode* l1, ListNode* l2) {
        ListNode dummy(0);
        ListNode* curr = &dummy;
        
        while (l1 && l2) {
            if (l1->val < l2->val) {
                curr->next = l1;
                l1 = l1->next;
            } else {
                curr->next = l2;
                l2 = l2->next;
            }
            curr = curr->next;
        }
        
        // 连接剩余节点
        curr->next = l1 ? l1 : l2;
        
        return dummy.next;
    }
    
    /**
     * 递归法
     */
    ListNode* MergeRecursive(ListNode* l1, ListNode* l2) {
        if (!l1) return l2;
        if (!l2) return l1;
        
        if (l1->val < l2->val) {
            l1->next = MergeRecursive(l1->next, l2);
            return l1;
        } else {
            l2->next = MergeRecursive(l1, l2->next);
            return l2;
        }
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
    
    int arr1[] = {1, 3, 5};
    int arr2[] = {2, 4, 6};
    
    ListNode* l1 = createList(arr1, 3);
    ListNode* l2 = createList(arr2, 3);
    
    cout << "链表1: ";
    printList(l1);
    cout << "链表2: ";
    printList(l2);
    
    ListNode* merged = solution.Merge(l1, l2);
    
    cout << "合并后: ";
    printList(merged);
    
    return 0;
}

