"""
Heap Data Structure Implementation
Min-Heap and Max-Heap with step-by-step operations for visualization
"""

from typing import List, Tuple, Optional, Generator


class MinHeap:
    """
    Min-Heap implementation with array representation
    Parent at index i, children at 2i+1 and 2i+2
    """

    def __init__(self, max_size: int = 31):
        """
        Initialize min-heap

        Args:
            max_size: Maximum number of elements
        """
        self.heap: List[Optional[int]] = []
        self.max_size = max_size
        self.size = 0

    def parent(self, index: int) -> int:
        """Get parent index"""
        return (index - 1) // 2

    def left_child(self, index: int) -> int:
        """Get left child index"""
        return 2 * index + 1

    def right_child(self, index: int) -> int:
        """Get right child index"""
        return 2 * index + 2

    def has_left_child(self, index: int) -> bool:
        """Check if node has left child"""
        return self.left_child(index) < self.size

    def has_right_child(self, index: int) -> bool:
        """Check if node has right child"""
        return self.right_child(index) < self.size

    def has_parent(self, index: int) -> bool:
        """Check if node has parent"""
        return self.parent(index) >= 0

    def swap(self, i: int, j: int):
        """Swap two elements"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, value: int) -> Generator[Tuple[List[int], dict], None, None]:
        """
        Insert value into heap with step-by-step tracking

        Args:
            value: Value to insert

        Yields:
            Tuple of (current_heap, state_info)
        """
        if self.size >= self.max_size:
            raise OverflowError("Heap is full")

        # Add to end
        self.heap.append(value)
        self.size += 1
        index = self.size - 1

        # Yield insertion state
        yield (
            self.heap.copy(),
            {
                "operation": "insert",
                "value": value,
                "index": index,
                "comparing_indices": [],
                "phase": "inserted",
            },
        )

        # Bubble up
        while (
            self.has_parent(index) and self.heap[index] < self.heap[self.parent(index)]
        ):
            parent_idx = self.parent(index)

            # Yield comparison state
            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_up",
                    "value": value,
                    "index": index,
                    "parent_index": parent_idx,
                    "comparing_indices": [index, parent_idx],
                    "phase": "comparing",
                },
            )

            # Swap with parent
            self.swap(index, parent_idx)

            # Yield swap state
            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_up",
                    "value": value,
                    "index": parent_idx,
                    "parent_index": self.parent(parent_idx)
                    if self.has_parent(parent_idx)
                    else -1,
                    "comparing_indices": [index, parent_idx],
                    "phase": "swapped",
                },
            )

            index = parent_idx

        # Final state
        yield (
            self.heap.copy(),
            {
                "operation": "insert",
                "value": value,
                "index": index,
                "comparing_indices": [],
                "phase": "complete",
            },
        )

    def extract_min(
        self,
    ) -> Generator[Tuple[List[int], dict, Optional[int]], None, None]:
        """
        Extract minimum element with step-by-step tracking

        Yields:
            Tuple of (current_heap, state_info, extracted_value)
        """
        if self.size == 0:
            raise IndexError("Heap is empty")

        min_value = self.heap[0]

        # Yield extraction state
        yield (
            self.heap.copy(),
            {
                "operation": "extract_min",
                "extracted_value": min_value,
                "index": 0,
                "comparing_indices": [0],
                "phase": "extracting",
            },
            None,
        )

        # Move last element to root
        self.heap[0] = self.heap[self.size - 1]
        self.heap.pop()
        self.size -= 1

        if self.size > 0:
            # Yield moved state
            yield (
                self.heap.copy(),
                {
                    "operation": "extract_min",
                    "extracted_value": min_value,
                    "index": 0,
                    "comparing_indices": [0],
                    "phase": "moved",
                },
                None,
            )

            # Bubble down
            yield from self._bubble_down_generator(0)

        # Final state with extracted value
        yield (
            self.heap.copy(),
            {
                "operation": "extract_min",
                "extracted_value": min_value,
                "index": -1,
                "comparing_indices": [],
                "phase": "complete",
            },
            min_value,
        )

    def _bubble_down_generator(
        self, index: int
    ) -> Generator[Tuple[List[int], dict], None, None]:
        """Helper generator for bubble down operation"""
        while self.has_left_child(index):
            smaller_child_idx = self.left_child(index)

            # Find smaller child
            if self.has_right_child(index):
                right_idx = self.right_child(index)
                if self.heap[right_idx] < self.heap[smaller_child_idx]:
                    smaller_child_idx = right_idx

            # Check if we need to swap
            if self.heap[index] <= self.heap[smaller_child_idx]:
                break

            # Yield comparison state
            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_down",
                    "index": index,
                    "child_index": smaller_child_idx,
                    "comparing_indices": [index, smaller_child_idx],
                    "phase": "comparing",
                },
            )

            # Swap
            self.swap(index, smaller_child_idx)

            # Yield swap state
            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_down",
                    "index": smaller_child_idx,
                    "child_index": smaller_child_idx,
                    "comparing_indices": [index, smaller_child_idx],
                    "phase": "swapped",
                },
            )

            index = smaller_child_idx

    def peek(self) -> Optional[int]:
        """Get minimum element without removing"""
        return self.heap[0] if self.size > 0 else None

    def is_empty(self) -> bool:
        """Check if heap is empty"""
        return self.size == 0

    def is_full(self) -> bool:
        """Check if heap is full"""
        return self.size >= self.max_size

    def get_size(self) -> int:
        """Get current size"""
        return self.size

    def get_array(self) -> List[int]:
        """Get heap as array"""
        return self.heap.copy()

    def clear(self):
        """Clear all elements"""
        self.heap.clear()
        self.size = 0

    def __str__(self):
        return f"MinHeap({self.heap[: self.size]})"

    def __repr__(self):
        return self.__str__()


class MaxHeap:
    """
    Max-Heap implementation (mirror of MinHeap with reversed comparisons)
    """

    def __init__(self, max_size: int = 31):
        """Initialize max-heap"""
        self.heap: List[Optional[int]] = []
        self.max_size = max_size
        self.size = 0

    def parent(self, index: int) -> int:
        return (index - 1) // 2

    def left_child(self, index: int) -> int:
        return 2 * index + 1

    def right_child(self, index: int) -> int:
        return 2 * index + 2

    def has_left_child(self, index: int) -> bool:
        return self.left_child(index) < self.size

    def has_right_child(self, index: int) -> bool:
        return self.right_child(index) < self.size

    def has_parent(self, index: int) -> bool:
        return self.parent(index) >= 0

    def swap(self, i: int, j: int):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, value: int) -> Generator[Tuple[List[int], dict], None, None]:
        """Insert value into max-heap"""
        if self.size >= self.max_size:
            raise OverflowError("Heap is full")

        self.heap.append(value)
        self.size += 1
        index = self.size - 1

        yield (
            self.heap.copy(),
            {
                "operation": "insert",
                "value": value,
                "index": index,
                "phase": "inserted",
            },
        )

        # Bubble up (reversed comparison for max-heap)
        while (
            self.has_parent(index) and self.heap[index] > self.heap[self.parent(index)]
        ):
            parent_idx = self.parent(index)

            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_up",
                    "value": value,
                    "index": index,
                    "parent_index": parent_idx,
                    "comparing_indices": [index, parent_idx],
                    "phase": "comparing",
                },
            )

            self.swap(index, parent_idx)

            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_up",
                    "value": value,
                    "index": parent_idx,
                    "comparing_indices": [index, parent_idx],
                    "phase": "swapped",
                },
            )

            index = parent_idx

        yield (
            self.heap.copy(),
            {
                "operation": "insert",
                "value": value,
                "index": index,
                "phase": "complete",
            },
        )

    def extract_max(
        self,
    ) -> Generator[Tuple[List[int], dict, Optional[int]], None, None]:
        """Extract maximum element"""
        if self.size == 0:
            raise IndexError("Heap is empty")

        max_value = self.heap[0]

        yield (
            self.heap.copy(),
            {
                "operation": "extract_max",
                "extracted_value": max_value,
                "index": 0,
                "phase": "extracting",
            },
            None,
        )

        self.heap[0] = self.heap[self.size - 1]
        self.heap.pop()
        self.size -= 1

        if self.size > 0:
            yield (
                self.heap.copy(),
                {
                    "operation": "extract_max",
                    "extracted_value": max_value,
                    "index": 0,
                    "phase": "moved",
                },
                None,
            )

            yield from self._bubble_down_generator(0)

        yield (
            self.heap.copy(),
            {
                "operation": "extract_max",
                "extracted_value": max_value,
                "phase": "complete",
            },
            max_value,
        )

    def _bubble_down_generator(
        self, index: int
    ) -> Generator[Tuple[List[int], dict], None, None]:
        """Helper for bubble down (reversed for max-heap)"""
        while self.has_left_child(index):
            larger_child_idx = self.left_child(index)

            if self.has_right_child(index):
                right_idx = self.right_child(index)
                if self.heap[right_idx] > self.heap[larger_child_idx]:
                    larger_child_idx = right_idx

            if self.heap[index] >= self.heap[larger_child_idx]:
                break

            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_down",
                    "index": index,
                    "child_index": larger_child_idx,
                    "comparing_indices": [index, larger_child_idx],
                    "phase": "comparing",
                },
            )

            self.swap(index, larger_child_idx)

            yield (
                self.heap.copy(),
                {
                    "operation": "bubble_down",
                    "index": larger_child_idx,
                    "comparing_indices": [index, larger_child_idx],
                    "phase": "swapped",
                },
            )

            index = larger_child_idx

    def peek(self) -> Optional[int]:
        return self.heap[0] if self.size > 0 else None

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size >= self.max_size

    def get_size(self) -> int:
        return self.size

    def get_array(self) -> List[int]:
        return self.heap.copy()

    def clear(self):
        self.heap.clear()
        self.size = 0

    def __str__(self):
        return f"MaxHeap({self.heap[: self.size]})"
