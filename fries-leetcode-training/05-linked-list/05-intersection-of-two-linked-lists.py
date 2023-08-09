"""
LeetCode 160. 相交链表
https://leetcode.cn/problems/intersection-of-two-linked-lists/

给你两个单链表的头节点headA和headB，请你找出并返回两个单链表相交的起始节点。

双指针

时间复杂度：O(m+n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def get_intersection_node(headA, headB):
    """
    相交链表 - 双指针法
    
    Args:
        headA: 第一个链表头节点
        headB: 第二个链表头节点
        
    Returns:
        相交的起始节点，无相交则返回None
    """
    if not headA or not headB:
        return None
    
    ptrA = headA
    ptrB = headB
    
    # 当两个指针都走完两个链表时，会在相交点相遇
    while ptrA != ptrB:
        ptrA = ptrA.next if ptrA else headB
        ptrB = ptrB.next if ptrB else headA
    
    return ptrA


def test_get_intersection_node():
    """测试函数"""
    # 创建相交的链表
    # 链表A: 4->1->8->4->5
    # 链表B: 5->6->1->8->4->5
    # 相交点: 8
    
    common = ListNode(8)
    common.next = ListNode(4)
    common.next.next = ListNode(5)
    
    headA = ListNode(4)
    headA.next = ListNode(1)
    headA.next.next = common
    
    headB = ListNode(5)
    headB.next = ListNode(6)
    headB.next.next = ListNode(1)
    headB.next.next.next = common
    
    intersection = get_intersection_node(headA, headB)
    if intersection:
        print(f"相交节点值: {intersection.val}")  # 期望: 8
    else:
        print("无相交")


if __name__ == "__main__":
    test_get_intersection_node()
