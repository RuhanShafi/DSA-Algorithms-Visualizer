"""
Unit Tests for Phase 2: Algorithm Visualizer
Tests for Sorting, Graph Traversal, and Heap Operations
"""

import unittest
import sys
import time
import random

sys.path.append("..")

from phase2.sorting import SortingAlgorithms
from phase2.graph import Graph, GraphTraversal
from phase2.heap import MinHeap, MaxHeap


class TestSorting(unittest.TestCase):
    """Test cases for sorting algorithms"""

    def setUp(self):
        """Set up test fixtures"""
        self.small_array = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_array = [1, 2, 3, 4, 5]
        self.reverse_array = [5, 4, 3, 2, 1]
        self.duplicate_array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

    def test_bubble_sort_correctness(self):
        """Test bubble sort produces correct result"""
        result = None
        for arr, state in SortingAlgorithms.bubble_sort(self.small_array):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, sorted(self.small_array))
        self.assertTrue(SortingAlgorithms.is_sorted(result))

    def test_selection_sort_correctness(self):
        """Test selection sort produces correct result"""
        result = None
        for arr, state in SortingAlgorithms.selection_sort(self.small_array):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, sorted(self.small_array))
        self.assertTrue(SortingAlgorithms.is_sorted(result))

    def test_merge_sort_correctness(self):
        """Test merge sort produces correct result"""
        result = None
        for arr, state in SortingAlgorithms.merge_sort(self.small_array):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, sorted(self.small_array))
        self.assertTrue(SortingAlgorithms.is_sorted(result))

    def test_sorting_already_sorted(self):
        """Test sorting already sorted array"""
        result = None
        for arr, state in SortingAlgorithms.bubble_sort(self.sorted_array):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, self.sorted_array)

    def test_sorting_reversed(self):
        """Test sorting reversed array"""
        result = None
        for arr, state in SortingAlgorithms.selection_sort(self.reverse_array):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, sorted(self.reverse_array))

    def test_sorting_duplicates(self):
        """Test sorting array with duplicates"""
        result = None
        for arr, state in SortingAlgorithms.merge_sort(self.duplicate_array):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, sorted(self.duplicate_array))

    def test_sorting_single_element(self):
        """Test sorting single element"""
        single = [42]
        result = None
        for arr, state in SortingAlgorithms.bubble_sort(single):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, [42])

    def test_sorting_empty(self):
        """Test sorting empty array"""
        empty = []
        result = None
        for arr, state in SortingAlgorithms.bubble_sort(empty):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(result, [])

    def test_bubble_sort_statistics(self):
        """Test bubble sort tracks comparisons and swaps"""
        final_state = None
        for arr, state in SortingAlgorithms.bubble_sort(self.small_array):
            if state["phase"] == "complete":
                final_state = state

        self.assertIn("comparisons", final_state)
        self.assertIn("swaps", final_state)
        self.assertGreater(final_state["comparisons"], 0)


class TestGraph(unittest.TestCase):
    """Test cases for graph data structure"""

    def setUp(self):
        """Set up test fixtures"""
        self.graph = Graph(directed=False)

    def test_add_node(self):
        """Test adding nodes"""
        self.assertTrue(self.graph.add_node(1))
        self.assertTrue(self.graph.add_node(2))
        self.assertFalse(self.graph.add_node(1))  # Duplicate

        self.assertEqual(self.graph.node_count, 2)

    def test_add_edge(self):
        """Test adding edges"""
        self.graph.add_edge(1, 2)

        self.assertEqual(self.graph.edge_count, 1)
        self.assertTrue(self.graph.has_edge(1, 2))
        # Undirected graph should have reverse edge
        self.assertTrue(self.graph.has_edge(2, 1))

    def test_directed_graph(self):
        """Test directed graph behavior"""
        directed = Graph(directed=True)
        directed.add_edge(1, 2)

        self.assertTrue(directed.has_edge(1, 2))
        self.assertFalse(directed.has_edge(2, 1))

    def test_remove_edge(self):
        """Test removing edges"""
        self.graph.add_edge(1, 2)
        self.assertTrue(self.graph.remove_edge(1, 2))

        self.assertFalse(self.graph.has_edge(1, 2))

    def test_get_neighbors(self):
        """Test getting neighbors"""
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)

        neighbors = self.graph.get_neighbors(1)
        self.assertEqual(set(neighbors), {2, 3})

    def test_get_degree(self):
        """Test degree calculation"""
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(1, 4)

        self.assertEqual(self.graph.get_degree(1), 3)


class TestGraphTraversal(unittest.TestCase):
    """Test cases for graph traversal algorithms"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a simple graph
        #     1
        #    / \
        #   2   3
        #  / \
        # 4   5
        self.graph = Graph(directed=False)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(2, 4)
        self.graph.add_edge(2, 5)

    def test_bfs_visits_all_nodes(self):
        """Test BFS visits all reachable nodes"""
        visited = set()

        for node, state in GraphTraversal.bfs(self.graph, 1):
            if state["phase"] == "visiting":
                visited.add(node)

        self.assertEqual(visited, {1, 2, 3, 4, 5})

    def test_bfs_correct_levels(self):
        """Test BFS computes correct levels"""
        final_state = None

        for node, state in GraphTraversal.bfs(self.graph, 1):
            if state["phase"] == "complete":
                final_state = state

        levels = final_state["levels"]
        self.assertEqual(levels[1], 0)
        self.assertEqual(levels[2], 1)
        self.assertEqual(levels[3], 1)
        self.assertEqual(levels[4], 2)
        self.assertEqual(levels[5], 2)

    def test_dfs_visits_all_nodes(self):
        """Test DFS visits all reachable nodes"""
        visited = set()

        for node, state in GraphTraversal.dfs(self.graph, 1):
            if state["phase"] == "visiting":
                visited.add(node)

        self.assertEqual(visited, {1, 2, 3, 4, 5})

    def test_path_reconstruction(self):
        """Test path reconstruction from BFS"""
        final_state = None

        for node, state in GraphTraversal.bfs(self.graph, 1):
            if state["phase"] == "complete":
                final_state = state

        path = GraphTraversal.reconstruct_path(final_state["parents"], 1, 5)

        self.assertIsNotNone(path)
        self.assertEqual(path[0], 1)
        self.assertEqual(path[-1], 5)
        self.assertIn(2, path)  # Must go through node 2

    def test_disconnected_graph(self):
        """Test traversal on disconnected graph"""
        self.graph.add_node(6)
        self.graph.add_node(7)
        self.graph.add_edge(6, 7)

        visited = set()
        for node, state in GraphTraversal.bfs(self.graph, 1):
            if state["phase"] == "visiting":
                visited.add(node)

        # Should not visit disconnected component
        self.assertNotIn(6, visited)
        self.assertNotIn(7, visited)

    def test_connected_components(self):
        """Test finding connected components"""
        # Add disconnected component
        self.graph.add_node(6)
        self.graph.add_node(7)
        self.graph.add_edge(6, 7)

        components = GraphTraversal.find_connected_components(self.graph)

        self.assertEqual(len(components), 2)

    def test_cycle_detection(self):
        """Test cycle detection"""
        # Current graph has no cycle
        self.assertFalse(GraphTraversal.has_cycle(self.graph))

        # Add edge to create cycle
        self.graph.add_edge(3, 4)
        self.assertTrue(GraphTraversal.has_cycle(self.graph))


class TestMinHeap(unittest.TestCase):
    """Test cases for MinHeap"""

    def setUp(self):
        """Set up test fixtures"""
        self.heap = MinHeap(max_size=10)

    def test_insert_single(self):
        """Test single insertion"""
        result = None
        for arr, state in self.heap.insert(50):
            if state["phase"] == "complete":
                result = arr

        self.assertEqual(self.heap.peek(), 50)
        self.assertEqual(self.heap.get_size(), 1)

    def test_insert_multiple(self):
        """Test multiple insertions maintain heap property"""
        values = [50, 30, 70, 20, 40, 60, 80]

        for val in values:
            for arr, state in self.heap.insert(val):
                pass

        # Root should be minimum
        self.assertEqual(self.heap.peek(), 20)

    def test_extract_min(self):
        """Test extraction maintains heap property"""
        values = [50, 30, 70, 20, 40]
        for val in values:
            for arr, state in self.heap.insert(val):
                pass

        # Extract minimum
        extracted = None
        for arr, state, val in self.heap.extract_min():
            if state["phase"] == "complete":
                extracted = val

        self.assertEqual(extracted, 20)
        self.assertEqual(self.heap.get_size(), 4)

    def test_extract_order(self):
        """Test extractions come out in sorted order"""
        values = [50, 30, 70, 20, 40, 60, 80]
        for val in values:
            for arr, state in self.heap.insert(val):
                pass

        extracted = []
        while not self.heap.is_empty():
            val = None
            for arr, state, v in self.heap.extract_min():
                if state["phase"] == "complete":
                    val = v
            if val is not None:
                extracted.append(val)

        self.assertEqual(extracted, sorted(values))

    def test_overflow(self):
        """Test heap overflow"""
        small_heap = MinHeap(max_size=3)

        for arr, state in small_heap.insert(1):
            pass
        for arr, state in small_heap.insert(2):
            pass
        for arr, state in small_heap.insert(3):
            pass

        with self.assertRaises(OverflowError):
            for arr, state in small_heap.insert(4):
                pass

    def test_underflow(self):
        """Test extract from empty heap"""
        with self.assertRaises(IndexError):
            for arr, state, val in self.heap.extract_min():
                pass


class TestMaxHeap(unittest.TestCase):
    """Test cases for MaxHeap"""

    def setUp(self):
        """Set up test fixtures"""
        self.heap = MaxHeap(max_size=10)

    def test_insert_maintains_max_property(self):
        """Test insertions maintain max-heap property"""
        values = [50, 30, 70, 20, 40, 60, 80]

        for val in values:
            for arr, state in self.heap.insert(val):
                pass

        # Root should be maximum
        self.assertEqual(self.heap.peek(), 80)

    def test_extract_max_order(self):
        """Test extractions come out in reverse sorted order"""
        values = [50, 30, 70, 20, 40, 60, 80]
        for val in values:
            for arr, state in self.heap.insert(val):
                pass

        extracted = []
        while not self.heap.is_empty():
            val = None
            for arr, state, v in self.heap.extract_max():
                if state["phase"] == "complete":
                    val = v
            if val is not None:
                extracted.append(val)

        self.assertEqual(extracted, sorted(values, reverse=True))


class TestPerformance(unittest.TestCase):
    """Performance benchmarking tests"""

    def test_sorting_performance(self):
        """Benchmark sorting algorithms"""
        size = 100
        test_array = [random.randint(1, 1000) for _ in range(size)]

        # Bubble sort
        start = time.time()
        for arr, state in SortingAlgorithms.bubble_sort(test_array):
            if state["phase"] == "complete":
                break
        bubble_time = time.time() - start

        # Merge sort
        start = time.time()
        for arr, state in SortingAlgorithms.merge_sort(test_array):
            if state["phase"] == "complete":
                break
        merge_time = time.time() - start

        print(f"\nSorting Performance (n=100):")
        print(f"  Bubble Sort: {bubble_time:.4f}s")
        print(f"  Merge Sort: {merge_time:.4f}s")

        # Merge sort should be significantly faster
        self.assertLess(merge_time, bubble_time)

    def test_graph_traversal_performance(self):
        """Benchmark graph traversal"""
        # Create larger graph
        graph = Graph(directed=False)
        for i in range(100):
            graph.add_edge(i, i + 1)

        # BFS
        start = time.time()
        for node, state in GraphTraversal.bfs(graph, 0):
            if state["phase"] == "complete":
                break
        bfs_time = time.time() - start

        # DFS
        start = time.time()
        for node, state in GraphTraversal.dfs(graph, 0):
            if state["phase"] == "complete":
                break
        dfs_time = time.time() - start

        print(f"\nGraph Traversal Performance (100 nodes):")
        print(f"  BFS: {bfs_time:.4f}s")
        print(f"  DFS: {dfs_time:.4f}s")

    def test_heap_operations_performance(self):
        """Benchmark heap operations"""
        heap = MinHeap(max_size=1000)

        # Insert 1000 elements
        start = time.time()
        for i in range(1000):
            for arr, state in heap.insert(random.randint(1, 10000)):
                pass
        insert_time = time.time() - start

        # Extract all elements
        start = time.time()
        while not heap.is_empty():
            for arr, state, val in heap.extract_min():
                if state["phase"] == "complete":
                    break
        extract_time = time.time() - start

        print(f"\nHeap Performance (1000 operations):")
        print(f"  1000 inserts: {insert_time:.4f}s")
        print(f"  1000 extracts: {extract_time:.4f}s")


def run_tests():
    """Run all Phase 2 tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSorting))
    suite.addTests(loader.loadTestsFromTestCase(TestGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestGraphTraversal))
    suite.addTests(loader.loadTestsFromTestCase(TestMinHeap))
    suite.addTests(loader.loadTestsFromTestCase(TestMaxHeap))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("PHASE 2 TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
