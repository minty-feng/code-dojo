"""
LeetCode 21. 合并两个有序链表
https://leetcode.cn/problems/merge-two-sorted-lists/

将两个升序链表合并为一个新的升序链表并返回。

归并排序思想

时间复杂度：O(n+m)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(l1, l2):
    """
    合并两个有序链表 - 归并排序思想
    
    Args:
        l1: 第一个有序链表
        l2: 第二个有序链表
        
    Returns:
        合并后的有序链表
    """
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    current.next = l1 or l2
    return dummy.next


def test_merge_two_lists():
    """测试函数"""
    # 创建测试链表1: 1->2->4
    l1 = ListNode(1)
    l1.next = ListNode(2)
    l1.next.next = ListNode(4)
    
    # 创建测试链表2: 1->3->4
    l2 = ListNode(1)
    l2.next = ListNode(3)
    l2.next.next = ListNode(4)
    
    merged = merge_two_lists(l1, l2)
    
    print("合并结果:")
    current = merged
    while current:
        print(current.val, end="->")
        current = current.next
    print("None")


if __name__ == "__main__":
    test_merge_two_lists()
