"""
NC62 判断是不是平衡二叉树
https://www.nowcoder.com/practice/8b3b95850edb4115918ecebdf1b4d222

输入一棵节点数为 n 二叉树，判断该二叉树是否是平衡二叉树。
平衡二叉树：任何节点的两个子树的高度差不超过1。

时间复杂度：O(n)
空间复杂度：O(h)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_balanced(root):
    """
    判断是否为平衡二叉树
    """
    def height(node):
        if not node:
            return 0
        
        left_height = height(node.left)
        if left_height == -1:
            return -1
        
        right_height = height(node.right)
        if right_height == -1:
            return -1
        
        # 检查平衡性
        if abs(left_height - right_height) > 1:
            return -1
        
        return max(left_height, right_height) + 1
    
    return height(root) != -1

# 测试
if __name__ == "__main__":
    # 平衡二叉树
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.left = TreeNode(4)
    root1.left.right = TreeNode(5)
    
    print(f"树1是否平衡: {is_balanced(root1)}")
    
    # 不平衡二叉树
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.left.left = TreeNode(3)
    root2.left.left.left = TreeNode(4)
    
    print(f"树2是否平衡: {is_balanced(root2)}")

