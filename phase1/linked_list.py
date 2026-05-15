"""
Linked List Data Structure Implementation
Singly linked list with insert, delete, reverse operations
"""


class Node:
    """
    Node class for linked list
    """

    def __init__(self, data):
        """
        Initialize a node

        Args:
            data: Data to store in the node
        """
        self.data = data
        self.next = None

    def __str__(self):
        return f"Node({self.data})"

    def __repr__(self):
        return f"Node(data={self.data}, next={'None' if not self.next else self.next.data})"


class LinkedList:
    """
    Singly linked list implementation
    """

    def __init__(self):
        """Initialize an empty linked list"""
        self.head = None
        self.size_count = 0

    def insert_at_head(self, data):
        """
        Insert a new node at the beginning of the list

        Args:
            data: Data to insert

        Returns:
            bool: True if successful
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size_count += 1
        return True

    def insert_at_tail(self, data):
        """
        Insert a new node at the end of the list

        Args:
            data: Data to insert

        Returns:
            bool: True if successful
        """
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        self.size_count += 1
        return True

    def insert_at_position(self, data, position):
        """
        Insert a new node at a specific position (0-indexed)

        Args:
            data: Data to insert
            position: Index where to insert (0 = head)

        Returns:
            bool: True if successful

        Raises:
            IndexError: If position is invalid
        """
        if position < 0 or position > self.size_count:
            raise IndexError(
                f"Invalid position: {position}. Must be between 0 and {self.size_count}"
            )

        if position == 0:
            return self.insert_at_head(data)

        new_node = Node(data)
        current = self.head

        for _ in range(position - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size_count += 1
        return True

    def delete_by_value(self, value):
        """
        Delete the first node with the specified value

        Args:
            value: Value to search for and delete

        Returns:
            bool: True if node was found and deleted, False otherwise
        """
        if self.head is None:
            return False

        # If head needs to be deleted
        if self.head.data == value:
            self.head = self.head.next
            self.size_count -= 1
            return True

        # Search for the node to delete
        current = self.head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                self.size_count -= 1
                return True
            current = current.next

        return False

    def delete_at_position(self, position):
        """
        Delete node at a specific position (0-indexed)

        Args:
            position: Index of node to delete

        Returns:
            The data from the deleted node

        Raises:
            IndexError: If position is invalid or list is empty
        """
        if self.head is None:
            raise IndexError("Cannot delete from empty list")

        if position < 0 or position >= self.size_count:
            raise IndexError(
                f"Invalid position: {position}. Must be between 0 and {self.size_count - 1}"
            )

        # Delete head
        if position == 0:
            data = self.head.data
            self.head = self.head.next
            self.size_count -= 1
            return data

        # Traverse to node before target
        current = self.head
        for _ in range(position - 1):
            current = current.next

        data = current.next.data
        current.next = current.next.next
        self.size_count -= 1
        return data

    def reverse(self):
        """
        Reverse the linked list in place

        Returns:
            bool: True if successful
        """
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev
        return True

    def search(self, value):
        """
        Search for a value in the list

        Args:
            value: Value to search for

        Returns:
            int: Position of value (0-indexed), or -1 if not found
        """
        current = self.head
        position = 0

        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1

        return -1

    def get_at_position(self, position):
        """
        Get data at a specific position

        Args:
            position: Index to retrieve

        Returns:
            Data at the position

        Raises:
            IndexError: If position is invalid
        """
        if position < 0 or position >= self.size_count:
            raise IndexError(f"Invalid position: {position}")

        current = self.head
        for _ in range(position):
            current = current.next

        return current.data

    def is_empty(self):
        """
        Check if list is empty

        Returns:
            bool: True if list has no nodes
        """
        return self.head is None

    def size(self):
        """
        Get the number of nodes in the list

        Returns:
            int: Number of nodes
        """
        return self.size_count

    def clear(self):
        """
        Remove all nodes from the list
        """
        self.head = None
        self.size_count = 0

    def get_all_data(self):
        """
        Get list of all data values

        Returns:
            list: All data values in order
        """
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def get_nodes(self):
        """
        Get list of all node objects

        Returns:
            list: All node objects in order
        """
        result = []
        current = self.head
        while current:
            result.append(current)
            current = current.next
        return result

    def __str__(self):
        """String representation of linked list"""
        return f"LinkedList({' -> '.join(str(data) for data in self.get_all_data())})"

    def __repr__(self):
        """Detailed string representation"""
        return f"LinkedList(size={self.size_count}, data={self.get_all_data()})"

    def __len__(self):
        """Support len() function"""
        return self.size()
