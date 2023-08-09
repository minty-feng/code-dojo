"""
LeetCode 206. 反转链表
https://leetcode.cn/problems/reverse-linked-list/

给你单链表的头节点head，请你反转链表，并返回反转后的链表。

迭代/递归

时间复杂度：O(n)
空间复杂度：O(1) 迭代 / O(n) 递归
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list_iterative(head):
    """
    反转链表 - 迭代法
    
    Args:
        head: 链表头节点
        
    Returns:
        反转后的链表头节点
    """
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev


def reverse_list_recursive(head):
    """
    反转链表 - 递归法
    
    Args:
        head: 链表头节点
        
    Returns:
        反转后的链表头节点
    """
    if not head or not head.next:
        return head
    
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return new_head


def test_reverse_list():
    """测试函数"""
    # 创建测试链表: 1->2->3->4->5
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    
    # 测试迭代法
    reversed_head1 = reverse_list_iterative(head)
    print("迭代法反转结果:")
    current = reversed_head1
    while current:
        print(current.val, end="->")
        current = current.next
    print("None")


if __name__ == "__main__":
    test_reverse_list()
