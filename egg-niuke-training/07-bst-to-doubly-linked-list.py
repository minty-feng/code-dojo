"""
NC79 二叉搜索树与双向链表
https://www.nowcoder.com/practice/947f6eb80d944a84850b0538bf0ec3a5

输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的双向链表。

中序遍历 + 记录前驱节点

时间复杂度：O(n)
空间复杂度：O(h)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def convert(root):
    """
    将BST转换为双向链表
    """
    if not root:
        return None
    
    # 记录前驱节点和头节点
    prev = [None]
    head = [None]
    
    def inorder(node):
        if not node:
            return
        
        # 左子树
        inorder(node.left)
        
        # 处理当前节点
        if prev[0]:
            prev[0].right = node
            node.left = prev[0]
        else:
            head[0] = node  # 记录头节点
        
        prev[0] = node
        
        # 右子树
        inorder(node.right)
    
    inorder(root)
    return head[0]

# 测试
if __name__ == "__main__":
    # 创建BST:  4
    #          /   \
    #         2     6
    #        / \   / \
    #       1   3 5   7
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(6)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)
    
    head = convert(root)
    
    # 打印双向链表
    print("正向遍历:")
    curr = head
    while curr:
        print(curr.val, end=" ")
        if not curr.right:
            tail = curr
        curr = curr.right
    
    print("\n反向遍历:")
    curr = tail
    while curr:
        print(curr.val, end=" ")
        curr = curr.left

