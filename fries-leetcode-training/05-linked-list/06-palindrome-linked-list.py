"""
LeetCode 234. 回文链表
https://leetcode.cn/problems/palindrome-linked-list/

给你一个单链表的头节点head，请你判断该链表是否为回文链表。

快慢指针 + 反转

时间复杂度：O(n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def is_palindrome(head):
    """
    回文链表 - 快慢指针 + 反转法
    
    Args:
        head: 链表头节点
        
    Returns:
        是否为回文链表
    """
    if not head or not head.next:
        return True
    
    # 找到链表中点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # 反转后半部分
    second_half = reverse_list(slow)
    
    # 比较前半部分和反转后的后半部分
    first_half = head
    while second_half:
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next
    
    return True


def reverse_list(head):
    """
    反转链表
    
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


def test_is_palindrome():
    """测试函数"""
    # 测试用例1: 1->2->2->1 (回文)
    head1 = ListNode(1)
    head1.next = ListNode(2)
    head1.next.next = ListNode(2)
    head1.next.next.next = ListNode(1)
    
    result1 = is_palindrome(head1)
    print(f"测试1 (1->2->2->1): {result1}")  # 期望: True
    
    # 测试用例2: 1->2 (非回文)
    head2 = ListNode(1)
    head2.next = ListNode(2)
    
    result2 = is_palindrome(head2)
    print(f"测试2 (1->2): {result2}")  # 期望: False


if __name__ == "__main__":
    test_is_palindrome()
