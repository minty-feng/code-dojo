"""
NC66 两个链表的第一个公共节点
https://www.nowcoder.com/practice/6ab1d9a29e88450685099d45c9e31e46

输入两个无环的单向链表，找出它们的第一个公共节点，如果没有公共节点则返回空。

解法：双指针
让两个指针分别走完两个链表，这样就能在第二轮相遇在公共节点。

时间复杂度：O(m+n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def find_first_common_node(head1, head2):
    """
    找到第一个公共节点 - 双指针法
    """
    if not head1 or not head2:
        return None
    
    p1, p2 = head1, head2
    
    # 两个指针分别走完两个链表
    # p1走完链表1再走链表2，p2走完链表2再走链表1
    # 这样走的总长度相同，会在公共节点相遇
    while p1 != p2:
        p1 = p1.next if p1 else head2
        p2 = p2.next if p2 else head1
    
    return p1

# 测试
if __name__ == "__main__":
    # 创建两个相交的链表
    # 链表1: 1 -> 2 -> 3
    #                     \
    #                      6 -> 7
    #                     /
    # 链表2:      4 -> 5
    
    common = ListNode(6, ListNode(7))
    
    head1 = ListNode(1, ListNode(2, ListNode(3, common)))
    head2 = ListNode(4, ListNode(5, common))
    
    result = find_first_common_node(head1, head2)
    if result:
        print(f"第一个公共节点值: {result.val}")
    else:
        print("无公共节点")

