"""
AVL树实现
严格平衡的二叉搜索树
"""

class AVLNode:
    """AVL树节点"""
    
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """AVL树实现"""
    
    def __init__(self):
        self.root = None
    
    def _get_height(self, node):
        """获取节点高度"""
        return node.height if node else 0
    
    def _update_height(self, node):
        """更新节点高度"""
        if node:
            node.height = 1 + max(
                self._get_height(node.left),
                self._get_height(node.right)
            )
    
    def _get_balance(self, node):
        """获取平衡因子"""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _right_rotate(self, z):
        """右旋
        
            z                y
           / \              / \
          y   T4    =>     x   z
         / \                  / \
        x   T3               T3  T4
        """
        y = z.left
        T3 = y.right
        
        # 旋转
        y.right = z
        z.left = T3
        
        # 更新高度
        self._update_height(z)
        self._update_height(y)
        
        return y
    
    def _left_rotate(self, z):
        """左旋
        
          z                  y
         / \                / \
        T4  y      =>      z   x
           / \            / \
          T3  x          T4  T3
        """
        y = z.right
        T3 = y.left
        
        # 旋转
        y.left = z
        z.right = T3
        
        # 更新高度
        self._update_height(z)
        self._update_height(y)
        
        return y
    
    def insert(self, val):
        """插入节点"""
        self.root = self._insert(self.root, val)
    
    def _insert(self, root, val):
        """插入辅助函数"""
        # 1. BST插入
        if not root:
            return AVLNode(val)
        
        if val < root.val:
            root.left = self._insert(root.left, val)
        elif val > root.val:
            root.right = self._insert(root.right, val)
        else:
            return root  # 重复值不插入
        
        # 2. 更新高度
        self._update_height(root)
        
        # 3. 获取平衡因子
        balance = self._get_balance(root)
        
        # 4. 四种情况调整
        
        # LL型：右旋
        if balance > 1 and val < root.left.val:
            return self._right_rotate(root)
        
        # RR型：左旋
        if balance < -1 and val > root.right.val:
            return self._left_rotate(root)
        
        # LR型：先左旋左子树，再右旋根
        if balance > 1 and val > root.left.val:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        
        # RL型：先右旋右子树，再左旋根
        if balance < -1 and val < root.right.val:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
        
        return root
    
    def delete(self, val):
        """删除节点"""
        self.root = self._delete(self.root, val)
    
    def _delete(self, root, val):
        """删除辅助函数"""
        # 1. BST删除
        if not root:
            return None
        
        if val < root.val:
            root.left = self._delete(root.left, val)
        elif val > root.val:
            root.right = self._delete(root.right, val)
        else:
            # 找到要删除的节点
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            
            # 两个子节点：用后继替换
            successor = self._find_min(root.right)
            root.val = successor.val
            root.right = self._delete(root.right, successor.val)
        
        if not root:
            return None
        
        # 2. 更新高度
        self._update_height(root)
        
        # 3. 重新平衡
        balance = self._get_balance(root)
        
        # LL
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)
        
        # RR
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)
        
        # LR
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        
        # RL
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
        
        return root
    
    def _find_min(self, root):
        """找最小节点"""
        while root.left:
            root = root.left
        return root
    
    def inorder(self):
        """中序遍历"""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, root, result):
        if root:
            self._inorder(root.left, result)
            result.append(root.val)
            self._inorder(root.right, result)
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        """打印树结构"""
        if node is None:
            node = self.root
        
        if node:
            bf = self._get_balance(node)
            print(" " * (level * 4) + prefix + f"{node.val}(h:{node.height},bf:{bf})")
            if node.left or node.right:
                self.print_tree(node.left, level + 1, "L--- ")
                self.print_tree(node.right, level + 1, "R--- ")


def demo():
    """演示AVL树操作"""
    print("=== AVL树演示 ===\n")
    
    avl = AVLTree()
    
    # 插入节点
    values = [10, 20, 30, 40, 50, 25]
    print(f"依次插入: {values}\n")
    
    for val in values:
        avl.insert(val)
        print(f"插入 {val}:")
        avl.print_tree()
        print()
    
    # 中序遍历
    print(f"中序遍历（有序）: {avl.inorder()}\n")
    
    # 删除节点
    print("删除节点 20:")
    avl.delete(20)
    avl.print_tree()
    print()
    
    print(f"中序遍历: {avl.inorder()}")


if __name__ == '__main__':
    demo()

