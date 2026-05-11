"""
Binary Search Tree Implementation
BST with insert, delete, search, and traversal operations
"""


class TreeNode:
    """
    Node class for Binary Search Tree
    """

    def __init__(self, value):
        """
        Initialize a tree node

        Args:
            value: Value to store in the node
        """
        self.value = value
        self.left = None
        self.right = None
        self.x = 0  # For visualization positioning
        self.y = 0

    def __str__(self):
        return f"TreeNode({self.value})"

    def __repr__(self):
        return f"TreeNode(value={self.value}, left={self.left.value if self.left else None}, right={self.right.value if self.right else None})"


class BinarySearchTree:
    """
    Binary Search Tree implementation
    Maintains BST property: left < parent < right
    """

    def __init__(self):
        """Initialize an empty BST"""
        self.root = None
        self.size_count = 0

    def insert(self, value):
        """
        Insert a value into the BST

        Args:
            value: Value to insert

        Returns:
            bool: True if inserted, False if value already exists
        """
        if self.root is None:
            self.root = TreeNode(value)
            self.size_count += 1
            return True

        return self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """Helper method for recursive insertion"""
        if value == node.value:
            return False  # Duplicate values not allowed

        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                self.size_count += 1
                return True
            else:
                return self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
                self.size_count += 1
                return True
            else:
                return self._insert_recursive(node.right, value)

    def delete(self, value):
        """
        Delete a value from the BST

        Args:
            value: Value to delete

        Returns:
            bool: True if deleted, False if value not found
        """
        self.root, deleted = self._delete_recursive(self.root, value)
        if deleted:
            self.size_count -= 1
        return deleted

    def _delete_recursive(self, node, value):
        """Helper method for recursive deletion"""
        if node is None:
            return None, False

        deleted = False

        if value < node.value:
            node.left, deleted = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete_recursive(node.right, value)
        else:
            # Node to delete found
            deleted = True

            # Case 1: Leaf node
            if node.left is None and node.right is None:
                return None, True

            # Case 2: One child
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            # Case 3: Two children
            # Find inorder successor (minimum in right subtree)
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right, _ = self._delete_recursive(node.right, successor.value)

        return node, deleted

    def _find_min(self, node):
        """Find node with minimum value in subtree"""
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, value):
        """
        Search for a value in the BST

        Args:
            value: Value to search for

        Returns:
            TreeNode: Node containing the value, or None if not found
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """Helper method for recursive search"""
        if node is None or node.value == value:
            return node

        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def inorder_traversal(self):
        """
        Perform inorder traversal (Left, Root, Right)
        Returns sorted order for BST

        Returns:
            list: Values in inorder sequence
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Helper method for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        """
        Perform preorder traversal (Root, Left, Right)

        Returns:
            list: Values in preorder sequence
        """
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        """Helper method for preorder traversal"""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        """
        Perform postorder traversal (Left, Right, Root)

        Returns:
            list: Values in postorder sequence
        """
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        """Helper method for postorder traversal"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def height(self):
        """
        Calculate the height of the tree

        Returns:
            int: Height (number of edges on longest path from root to leaf)
        """
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        """Helper method for height calculation"""
        if node is None:
            return -1

        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)

        return 1 + max(left_height, right_height)

    def is_empty(self):
        """
        Check if tree is empty

        Returns:
            bool: True if tree has no nodes
        """
        return self.root is None

    def size(self):
        """
        Get the number of nodes in the tree

        Returns:
            int: Number of nodes
        """
        return self.size_count

    def clear(self):
        """
        Remove all nodes from the tree
        """
        self.root = None
        self.size_count = 0

    def get_all_nodes(self):
        """
        Get list of all nodes (inorder)

        Returns:
            list: All node objects
        """
        result = []
        self._get_nodes_recursive(self.root, result)
        return result

    def _get_nodes_recursive(self, node, result):
        """Helper method to get all nodes"""
        if node:
            self._get_nodes_recursive(node.left, result)
            result.append(node)
            self._get_nodes_recursive(node.right, result)

    def __str__(self):
        """String representation of BST"""
        return f"BST({self.inorder_traversal()})"

    def __repr__(self):
        """Detailed string representation"""
        return f"BinarySearchTree(size={self.size_count}, inorder={self.inorder_traversal()})"

    def __len__(self):
        """Support len() function"""
        return self.size()
