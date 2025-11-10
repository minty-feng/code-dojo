"""
红黑树实现
"""

# 颜色常量
RED = 0
BLACK = 1


class RBNode:
    """红黑树节点"""
    
    def __init__(self, val, color=RED):
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    """红黑树实现"""
    
    def __init__(self):
        # 哨兵节点
        self.NIL = RBNode(0, BLACK)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        
        self.root = self.NIL
    
    def insert(self, val):
        """插入节点"""
        # BST插入
        new_node = RBNode(val, RED)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        parent = None
        curr = self.root
        
        while curr != self.NIL:
            parent = curr
            if val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        
        new_node.parent = parent
        
        if parent is None:
            self.root = new_node
        elif val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # 修复红黑树性质
        self._insert_fixup(new_node)
    
    def _insert_fixup(self, node):
        """插入后修复"""
        while node.parent and node.parent.color == RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.color == RED:
                    # 情况1：叔叔是红色
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # 情况2：当前节点是右孩子
                        node = node.parent
                        self._left_rotate(node)
                    
                    # 情况3：当前节点是左孩子
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._right_rotate(node.parent.parent)
            else:
                # 对称情况
                uncle = node.parent.parent.left
                
                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._left_rotate(node.parent.parent)
        
        self.root.color = BLACK
    
    def _left_rotate(self, x):
        """左旋"""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _right_rotate(self, y):
        """右旋"""
        x = y.left
        y.left = x.right
        
        if x.right != self.NIL:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        
        x.right = y
        y.parent = x
    
    def search(self, val):
        """查找节点"""
        curr = self.root
        while curr != self.NIL and curr.val != val:
            if val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return curr if curr != self.NIL else None
    
    def inorder(self):
        """中序遍历"""
        result = []
        self._inorder_helper(self.root, result)
        return result
    
    def _inorder_helper(self, node, result):
        """中序遍历辅助函数"""
        if node != self.NIL:
            self._inorder_helper(node.left, result)
            result.append(node.val)
            self._inorder_helper(node.right, result)
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        """打印树结构"""
        if node is None:
            node = self.root
        
        if node != self.NIL:
            color = "🔴" if node.color == RED else "⚫"
            print(" " * (level * 4) + prefix + f"{color}{node.val}")
            if node.left != self.NIL or node.right != self.NIL:
                self.print_tree(node.left, level + 1, "L--- ")
                self.print_tree(node.right, level + 1, "R--- ")


def demo():
    """演示红黑树的使用"""
    print("=== 红黑树演示 ===\n")
    
    tree = RBTree()
    
    # 插入节点
    values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
    print(f"插入节点: {values}\n")
    
    for val in values:
        tree.insert(val)
        print(f"插入 {val}:")
        tree.print_tree()
        print()
    
    # 中序遍历
    print("中序遍历（应该是有序的）:")
    print(tree.inorder())
    print()
    
    # 查找
    search_val = 10
    result = tree.search(search_val)
    if result:
        color = "红色" if result.color == RED else "黑色"
        print(f"找到节点 {search_val}，颜色: {color}")
    else:
        print(f"未找到节点 {search_val}")


if __name__ == '__main__':
    demo()

