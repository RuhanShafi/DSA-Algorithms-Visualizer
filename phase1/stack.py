"""
Stack Data Structure Implementation
LIFO (Last In First Out) data structure with array-based implementation
"""

from config import MAX_STACK_SIZE


class Stack:
    """
    Array-based stack implementation with size limit
    """

    def __init__(self, max_size=MAX_STACK_SIZE):
        """
        Initialize an empty stack

        Args:
            max_size (int): Maximum number of elements the stack can hold
        """
        self.items = []
        self.max_size = max_size

    def push(self, item):
        """
        Add an item to the top of the stack

        Args:
            item: Element to push onto stack

        Returns:
            bool: True if successful, False if stack is full

        Raises:
            OverflowError: If stack is full
        """
        if self.is_full():
            raise OverflowError("Stack overflow: Cannot push to full stack")

        self.items.append(item)
        return True

    def pop(self):
        """
        Remove and return the top item from the stack

        Returns:
            The top item from the stack

        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Stack underflow: Cannot pop from empty stack")

        return self.items.pop()

    def peek(self):
        """
        Return the top item without removing it

        Returns:
            The top item from the stack

        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek: Stack is empty")

        return self.items[-1]

    def is_empty(self):
        """
        Check if stack is empty

        Returns:
            bool: True if stack has no elements
        """
        return len(self.items) == 0

    def is_full(self):
        """
        Check if stack is full

        Returns:
            bool: True if stack has reached maximum capacity
        """
        return len(self.items) >= self.max_size

    def size(self):
        """
        Get the current number of elements in the stack

        Returns:
            int: Number of elements
        """
        return len(self.items)

    def clear(self):
        """
        Remove all elements from the stack
        """
        self.items = []

    def get_items(self):
        """
        Get a copy of all items in the stack (bottom to top)

        Returns:
            list: Copy of stack items
        """
        return self.items.copy()

    def __str__(self):
        """String representation of stack"""
        return f"Stack({self.items})"

    def __repr__(self):
        """Detailed string representation"""
        return (
            f"Stack(items={self.items}, size={self.size()}, max_size={self.max_size})"
        )

    def __len__(self):
        """Support len() function"""
        return self.size()
