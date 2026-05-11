"""
Queue Data Structure Implementation
FIFO (First In First Out) data structure with circular array implementation
"""

from config import MAX_QUEUE_SIZE


class Queue:
    """
    Circular array-based queue implementation with size limit
    """

    def __init__(self, max_size=MAX_QUEUE_SIZE):
        """
        Initialize an empty queue

        Args:
            max_size (int): Maximum number of elements the queue can hold
        """
        self.items = [None] * max_size
        self.max_size = max_size
        self.front = 0
        self.rear = -1
        self.count = 0

    def enqueue(self, item):
        """
        Add an item to the rear of the queue

        Args:
            item: Element to add to queue

        Returns:
            bool: True if successful

        Raises:
            OverflowError: If queue is full
        """
        if self.is_full():
            raise OverflowError("Queue overflow: Cannot enqueue to full queue")

        self.rear = (self.rear + 1) % self.max_size
        self.items[self.rear] = item
        self.count += 1
        return True

    def dequeue(self):
        """
        Remove and return the front item from the queue

        Returns:
            The front item from the queue

        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Queue underflow: Cannot dequeue from empty queue")

        item = self.items[self.front]
        self.items[self.front] = None  # Clear the slot
        self.front = (self.front + 1) % self.max_size
        self.count -= 1
        return item

    def peek(self):
        """
        Return the front item without removing it

        Returns:
            The front item from the queue

        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek: Queue is empty")

        return self.items[self.front]

    def is_empty(self):
        """
        Check if queue is empty

        Returns:
            bool: True if queue has no elements
        """
        return self.count == 0

    def is_full(self):
        """
        Check if queue is full

        Returns:
            bool: True if queue has reached maximum capacity
        """
        return self.count >= self.max_size

    def size(self):
        """
        Get the current number of elements in the queue

        Returns:
            int: Number of elements
        """
        return self.count

    def clear(self):
        """
        Remove all elements from the queue
        """
        self.items = [None] * self.max_size
        self.front = 0
        self.rear = -1
        self.count = 0

    def get_items(self):
        """
        Get a list of all items in the queue (front to rear)

        Returns:
            list: Items in order from front to rear
        """
        if self.is_empty():
            return []

        result = []
        index = self.front
        for _ in range(self.count):
            result.append(self.items[index])
            index = (index + 1) % self.max_size
        return result

    def __str__(self):
        """String representation of queue"""
        return f"Queue({self.get_items()})"

    def __repr__(self):
        """Detailed string representation"""
        return f"Queue(items={self.get_items()}, size={self.size()}, max_size={self.max_size})"

    def __len__(self):
        """Support len() function"""
        return self.size()
