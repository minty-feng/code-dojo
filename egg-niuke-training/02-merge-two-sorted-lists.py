"""
NC33 合并两个排序的链表
https://www.nowcoder.com/practice/d8b6b4358f774294a89de2a6ac4d9337

输入两个递增的链表，合并这两个链表并使新链表中的节点仍然是递增排序的。

时间复杂度：O(n+m)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_lists(l1, l2):
    """
    合并两个排序链表
    """
    dummy = ListNode(0)
    curr = dummy
    
    while l1 and l2:
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    
    # 连接剩余节点
    curr.next = l1 if l1 else l2
    
    return dummy.next

def merge_two_lists_recursive(l1, l2):
    """
    递归法
    """
    if not l1:
        return l2
    if not l2:
        return l1
    
    if l1.val < l2.val:
        l1.next = merge_two_lists_recursive(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_lists_recursive(l1, l2.next)
        return l2

# 测试
if __name__ == "__main__":
    def create_list(arr):
        if not arr:
            return None
        head = ListNode(arr[0])
        curr = head
        for val in arr[1:]:
            curr.next = ListNode(val)
            curr = curr.next
        return head
    
    def print_list(head):
        values = []
        while head:
            values.append(str(head.val))
            head = head.next
        print(' -> '.join(values))
    
    l1 = create_list([1, 3, 5])
    l2 = create_list([2, 4, 6])
    
    print("链表1:")
    print_list(l1)
    print("链表2:")
    print_list(l2)
    
    merged = merge_two_lists(l1, l2)
    print("合并后:")
    print_list(merged)

