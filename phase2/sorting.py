"""
Sorting Algorithms Implementation
Bubble Sort, Selection Sort, Merge Sort with step tracking for visualization
"""

from typing import List, Tuple, Generator


class SortingAlgorithms:
    """
    Collection of sorting algorithms with step-by-step tracking
    """

    @staticmethod
    def bubble_sort(arr: List[int]) -> Generator[Tuple[List[int], dict], None, None]:
        """
        Bubble Sort with step-by-step tracking
        Yields state after each comparison/swap

        Args:
            arr: List of integers to sort

        Yields:
            Tuple of (current_array, state_info)
            state_info contains: comparing_indices, swapped, comparisons, swaps
        """
        arr = arr.copy()
        n = len(arr)
        comparisons = 0
        swaps = 0

        for i in range(n):
            swapped = False

            for j in range(0, n - i - 1):
                comparisons += 1

                # Yield comparison state
                yield (
                    arr.copy(),
                    {
                        "comparing_indices": [j, j + 1],
                        "swapped": False,
                        "comparisons": comparisons,
                        "swaps": swaps,
                        "sorted_indices": list(range(n - i, n)),
                        "phase": "comparing",
                    },
                )

                # Compare and swap if needed
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
                    swapped = True

                    # Yield swap state
                    yield (
                        arr.copy(),
                        {
                            "comparing_indices": [j, j + 1],
                            "swapped": True,
                            "comparisons": comparisons,
                            "swaps": swaps,
                            "sorted_indices": list(range(n - i, n)),
                            "phase": "swapping",
                        },
                    )

            # If no swaps, array is sorted
            if not swapped:
                break

        # Final sorted state
        yield (
            arr.copy(),
            {
                "comparing_indices": [],
                "swapped": False,
                "comparisons": comparisons,
                "swaps": swaps,
                "sorted_indices": list(range(n)),
                "phase": "complete",
            },
        )

    @staticmethod
    def selection_sort(arr: List[int]) -> Generator[Tuple[List[int], dict], None, None]:
        """
        Selection Sort with step-by-step tracking

        Args:
            arr: List of integers to sort

        Yields:
            Tuple of (current_array, state_info)
        """
        arr = arr.copy()
        n = len(arr)
        comparisons = 0
        swaps = 0

        for i in range(n):
            min_idx = i

            # Find minimum in unsorted portion
            for j in range(i + 1, n):
                comparisons += 1

                # Yield comparison state
                yield (
                    arr.copy(),
                    {
                        "comparing_indices": [min_idx, j],
                        "min_index": min_idx,
                        "current_index": i,
                        "comparisons": comparisons,
                        "swaps": swaps,
                        "sorted_indices": list(range(i)),
                        "phase": "finding_min",
                    },
                )

                if arr[j] < arr[min_idx]:
                    min_idx = j

            # Swap minimum to correct position
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swaps += 1

                # Yield swap state
                yield (
                    arr.copy(),
                    {
                        "comparing_indices": [i, min_idx],
                        "min_index": min_idx,
                        "current_index": i,
                        "comparisons": comparisons,
                        "swaps": swaps,
                        "sorted_indices": list(range(i + 1)),
                        "phase": "swapping",
                    },
                )

        # Final sorted state
        yield (
            arr.copy(),
            {
                "comparing_indices": [],
                "min_index": -1,
                "current_index": -1,
                "comparisons": comparisons,
                "swaps": swaps,
                "sorted_indices": list(range(n)),
                "phase": "complete",
            },
        )

    @staticmethod
    def merge_sort(arr: List[int]) -> Generator[Tuple[List[int], dict], None, None]:
        """
        Merge Sort with step-by-step tracking

        Args:
            arr: List of integers to sort

        Yields:
            Tuple of (current_array, state_info)
        """
        result = arr.copy()
        comparisons = [0]
        operations = [0]

        def merge_sort_helper(left: int, right: int):
            if left >= right:
                return

            mid = (left + right) // 2

            # Yield divide state
            yield (
                result.copy(),
                {
                    "left": left,
                    "mid": mid,
                    "right": right,
                    "comparisons": comparisons[0],
                    "operations": operations[0],
                    "phase": "dividing",
                    "active_range": [left, right],
                },
            )

            # Recursively sort left and right halves
            yield from merge_sort_helper(left, mid)
            yield from merge_sort_helper(mid + 1, right)

            # Merge the sorted halves
            yield from merge(left, mid, right)

        def merge(left: int, mid: int, right: int):
            # Create temporary arrays
            left_arr = result[left : mid + 1]
            right_arr = result[mid + 1 : right + 1]

            i = j = 0
            k = left

            # Merge arrays
            while i < len(left_arr) and j < len(right_arr):
                comparisons[0] += 1
                operations[0] += 1

                yield (
                    result.copy(),
                    {
                        "left": left,
                        "mid": mid,
                        "right": right,
                        "comparisons": comparisons[0],
                        "operations": operations[0],
                        "phase": "merging",
                        "comparing_indices": [left + i, mid + 1 + j],
                        "active_range": [left, right],
                    },
                )

                if left_arr[i] <= right_arr[j]:
                    result[k] = left_arr[i]
                    i += 1
                else:
                    result[k] = right_arr[j]
                    j += 1
                k += 1

            # Copy remaining elements
            while i < len(left_arr):
                result[k] = left_arr[i]
                operations[0] += 1
                i += 1
                k += 1

            while j < len(right_arr):
                result[k] = right_arr[j]
                operations[0] += 1
                j += 1
                k += 1

            # Yield merged state
            yield (
                result.copy(),
                {
                    "left": left,
                    "mid": mid,
                    "right": right,
                    "comparisons": comparisons[0],
                    "operations": operations[0],
                    "phase": "merged",
                    "active_range": [left, right],
                },
            )

        # Start merge sort
        if len(arr) > 0:
            yield from merge_sort_helper(0, len(arr) - 1)

        # Final sorted state
        yield (
            result.copy(),
            {
                "left": 0,
                "mid": 0,
                "right": len(arr) - 1,
                "comparisons": comparisons[0],
                "operations": operations[0],
                "phase": "complete",
                "active_range": [],
            },
        )

    @staticmethod
    def quick_sort(arr: List[int]) -> Generator[Tuple[List[int], dict], None, None]:
        """
        Quick Sort with step-by-step tracking (bonus algorithm)

        Args:
            arr: List of integers to sort

        Yields:
            Tuple of (current_array, state_info)
        """
        result = arr.copy()
        comparisons = [0]
        swaps = [0]

        def partition(low: int, high: int):
            pivot = result[high]
            i = low - 1

            # Yield pivot selection
            yield (
                result.copy(),
                {
                    "pivot_index": high,
                    "pivot_value": pivot,
                    "low": low,
                    "high": high,
                    "comparisons": comparisons[0],
                    "swaps": swaps[0],
                    "phase": "pivot_selected",
                },
            )

            for j in range(low, high):
                comparisons[0] += 1

                yield (
                    result.copy(),
                    {
                        "pivot_index": high,
                        "comparing_indices": [j, high],
                        "low": low,
                        "high": high,
                        "comparisons": comparisons[0],
                        "swaps": swaps[0],
                        "phase": "comparing",
                    },
                )

                if result[j] < pivot:
                    i += 1
                    result[i], result[j] = result[j], result[i]
                    swaps[0] += 1

                    yield (
                        result.copy(),
                        {
                            "pivot_index": high,
                            "swapping_indices": [i, j],
                            "low": low,
                            "high": high,
                            "comparisons": comparisons[0],
                            "swaps": swaps[0],
                            "phase": "swapping",
                        },
                    )

            # Place pivot in correct position
            result[i + 1], result[high] = result[high], result[i + 1]
            swaps[0] += 1

            yield (
                result.copy(),
                {
                    "pivot_index": i + 1,
                    "low": low,
                    "high": high,
                    "comparisons": comparisons[0],
                    "swaps": swaps[0],
                    "phase": "pivot_placed",
                },
            )

            return i + 1

        def quick_sort_helper(low: int, high: int):
            if low < high:
                # Partition and get pivot index
                pi_gen = partition(low, high)
                pi = None
                for state in pi_gen:
                    yield state
                    if state[1]["phase"] == "pivot_placed":
                        pi = state[1]["pivot_index"]

                # Recursively sort left and right
                yield from quick_sort_helper(low, pi - 1)
                yield from quick_sort_helper(pi + 1, high)

        if len(arr) > 0:
            yield from quick_sort_helper(0, len(arr) - 1)

        # Final state
        yield (
            result.copy(),
            {"comparisons": comparisons[0], "swaps": swaps[0], "phase": "complete"},
        )

    @staticmethod
    def is_sorted(arr: List[int]) -> bool:
        """Check if array is sorted"""
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    @staticmethod
    def get_algorithm_info(algorithm: str) -> dict:
        """
        Get information about sorting algorithm

        Args:
            algorithm: Name of algorithm

        Returns:
            Dictionary with time/space complexity info
        """
        info = {
            "bubble": {
                "name": "Bubble Sort",
                "best": "O(n)",
                "average": "O(n²)",
                "worst": "O(n²)",
                "space": "O(1)",
                "stable": True,
            },
            "selection": {
                "name": "Selection Sort",
                "best": "O(n²)",
                "average": "O(n²)",
                "worst": "O(n²)",
                "space": "O(1)",
                "stable": False,
            },
            "merge": {
                "name": "Merge Sort",
                "best": "O(n log n)",
                "average": "O(n log n)",
                "worst": "O(n log n)",
                "space": "O(n)",
                "stable": True,
            },
            "quick": {
                "name": "Quick Sort",
                "best": "O(n log n)",
                "average": "O(n log n)",
                "worst": "O(n²)",
                "space": "O(log n)",
                "stable": False,
            },
        }

        return info.get(algorithm, {})
