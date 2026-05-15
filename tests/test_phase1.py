"""
Unit Tests for Phase 1: Data Structures
Tests for Stack, Queue, Linked List, and Binary Search Tree
"""

import unittest
import sys
import time

sys.path.append("..")

from phase1.stack import Stack
from phase1.queue import Queue
from phase1.linked_list import LinkedList
from phase1.bst import BinarySearchTree


class TestStack(unittest.TestCase):
    """Test cases for Stack data structure"""

    def setUp(self):
        """Set up test fixtures"""
        self.stack = Stack(max_size=5)

    def test_push_pop_basic(self):
        """Test basic push and pop operations"""
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)

        self.assertEqual(self.stack.pop(), 30)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.pop(), 10)

    def test_is_empty(self):
        """Test empty stack detection"""
        self.assertTrue(self.stack.is_empty())
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())

    def test_is_full(self):
        """Test full stack detection"""
        for i in range(5):
            self.stack.push(i)
        self.assertTrue(self.stack.is_full())

    def test_overflow(self):
        """Test stack overflow handling"""
        for i in range(5):
            self.stack.push(i)

        with self.assertRaises(OverflowError):
            self.stack.push(99)

    def test_underflow(self):
        """Test stack underflow handling"""
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek(self):
        """Test peek operation"""
        self.stack.push(100)
        self.stack.push(200)

        self.assertEqual(self.stack.peek(), 200)
        self.assertEqual(self.stack.size(), 2)  # Size shouldn't change

    def test_clear(self):
        """Test clear operation"""
        self.stack.push(1)
        self.stack.push(2)
        self.stack.clear()

        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

    def test_size(self):
        """Test size tracking"""
        self.assertEqual(self.stack.size(), 0)
        self.stack.push(1)
        self.assertEqual(self.stack.size(), 1)
        self.stack.push(2)
        self.assertEqual(self.stack.size(), 2)
        self.stack.pop()
        self.assertEqual(self.stack.size(), 1)


class TestQueue(unittest.TestCase):
    """Test cases for Queue data structure"""

    def setUp(self):
        """Set up test fixtures"""
        self.queue = Queue(max_size=5)

    def test_enqueue_dequeue_basic(self):
        """Test basic enqueue and dequeue operations"""
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)

        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 20)
        self.assertEqual(self.queue.dequeue(), 30)

    def test_is_empty(self):
        """Test empty queue detection"""
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(1)
        self.assertFalse(self.queue.is_empty())

    def test_is_full(self):
        """Test full queue detection"""
        for i in range(5):
            self.queue.enqueue(i)
        self.assertTrue(self.queue.is_full())

    def test_overflow(self):
        """Test queue overflow handling"""
        for i in range(5):
            self.queue.enqueue(i)

        with self.assertRaises(OverflowError):
            self.queue.enqueue(99)

    def test_underflow(self):
        """Test queue underflow handling"""
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    def test_circular_behavior(self):
        """Test circular queue behavior"""
        # Fill queue
        for i in range(5):
            self.queue.enqueue(i)

        # Remove 2 elements
        self.queue.dequeue()
        self.queue.dequeue()

        # Add 2 more (should wrap around)
        self.queue.enqueue(100)
        self.queue.enqueue(200)

        self.assertEqual(self.queue.size(), 5)

    def test_peek(self):
        """Test peek operation"""
        self.queue.enqueue(100)
        self.queue.enqueue(200)

        self.assertEqual(self.queue.peek(), 100)
        self.assertEqual(self.queue.size(), 2)

    def test_clear(self):
        """Test clear operation"""
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.clear()

        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)


class TestLinkedList(unittest.TestCase):
    """Test cases for Linked List"""

    def setUp(self):
        """Set up test fixtures"""
        self.ll = LinkedList()

    def test_insert_at_head(self):
        """Test insertion at head"""
        self.ll.insert_at_head(10)
        self.ll.insert_at_head(20)
        self.ll.insert_at_head(30)

        self.assertEqual(self.ll.get_all_data(), [30, 20, 10])

    def test_insert_at_tail(self):
        """Test insertion at tail"""
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)

        self.assertEqual(self.ll.get_all_data(), [10, 20, 30])

    def test_insert_at_position(self):
        """Test insertion at specific position"""
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(30)
        self.ll.insert_at_position(20, 1)

        self.assertEqual(self.ll.get_all_data(), [10, 20, 30])

    def test_delete_by_value(self):
        """Test deletion by value"""
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)

        self.assertTrue(self.ll.delete_by_value(20))
        self.assertEqual(self.ll.get_all_data(), [10, 30])

        self.assertFalse(self.ll.delete_by_value(99))

    def test_delete_at_position(self):
        """Test deletion at position"""
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)

        deleted = self.ll.delete_at_position(1)
        self.assertEqual(deleted, 20)
        self.assertEqual(self.ll.get_all_data(), [10, 30])

    def test_reverse(self):
        """Test list reversal"""
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)

        self.ll.reverse()
        self.assertEqual(self.ll.get_all_data(), [30, 20, 10])

    def test_search(self):
        """Test search operation"""
        self.ll.insert_at_tail(10)
        self.ll.insert_at_tail(20)
        self.ll.insert_at_tail(30)

        self.assertEqual(self.ll.search(20), 1)
        self.assertEqual(self.ll.search(99), -1)

    def test_is_empty(self):
        """Test empty list detection"""
        self.assertTrue(self.ll.is_empty())
        self.ll.insert_at_head(1)
        self.assertFalse(self.ll.is_empty())

    def test_size(self):
        """Test size tracking"""
        self.assertEqual(self.ll.size(), 0)
        self.ll.insert_at_tail(1)
        self.assertEqual(self.ll.size(), 1)
        self.ll.insert_at_tail(2)
        self.assertEqual(self.ll.size(), 2)
        self.ll.delete_by_value(1)
        self.assertEqual(self.ll.size(), 1)


class TestBinarySearchTree(unittest.TestCase):
    """Test cases for Binary Search Tree"""

    def setUp(self):
        """Set up test fixtures"""
        self.bst = BinarySearchTree()

    def test_insert_basic(self):
        """Test basic insertion"""
        self.assertTrue(self.bst.insert(50))
        self.assertTrue(self.bst.insert(30))
        self.assertTrue(self.bst.insert(70))

        self.assertEqual(self.bst.size(), 3)

    def test_insert_duplicate(self):
        """Test duplicate insertion prevention"""
        self.bst.insert(50)
        self.assertFalse(self.bst.insert(50))
        self.assertEqual(self.bst.size(), 1)

    def test_search(self):
        """Test search operation"""
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)

        self.assertIsNotNone(self.bst.search(30))
        self.assertIsNone(self.bst.search(99))

    def test_inorder_traversal(self):
        """Test inorder traversal (should be sorted)"""
        values = [50, 30, 70, 20, 40, 60, 80]
        for val in values:
            self.bst.insert(val)

        result = self.bst.inorder_traversal()
        self.assertEqual(result, [20, 30, 40, 50, 60, 70, 80])

    def test_preorder_traversal(self):
        """Test preorder traversal"""
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)

        result = self.bst.preorder_traversal()
        self.assertEqual(result, [50, 30, 70])

    def test_postorder_traversal(self):
        """Test postorder traversal"""
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)

        result = self.bst.postorder_traversal()
        self.assertEqual(result, [30, 70, 50])

    def test_delete_leaf(self):
        """Test deletion of leaf node"""
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)

        self.assertTrue(self.bst.delete(30))
        self.assertIsNone(self.bst.search(30))
        self.assertEqual(self.bst.size(), 2)

    def test_delete_one_child(self):
        """Test deletion of node with one child"""
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(20)

        self.assertTrue(self.bst.delete(30))
        self.assertIsNotNone(self.bst.search(20))
        self.assertEqual(self.bst.size(), 2)

    def test_delete_two_children(self):
        """Test deletion of node with two children"""
        values = [50, 30, 70, 20, 40]
        for val in values:
            self.bst.insert(val)

        self.assertTrue(self.bst.delete(30))
        self.assertIsNone(self.bst.search(30))
        # Verify tree structure is maintained
        self.assertEqual(sorted(self.bst.inorder_traversal()), [20, 40, 50, 70])

    def test_height(self):
        """Test height calculation"""
        self.assertEqual(self.bst.height(), -1)  # Empty tree

        self.bst.insert(50)
        self.assertEqual(self.bst.height(), 0)

        self.bst.insert(30)
        self.bst.insert(70)
        self.assertEqual(self.bst.height(), 1)

    def test_is_empty(self):
        """Test empty tree detection"""
        self.assertTrue(self.bst.is_empty())
        self.bst.insert(50)
        self.assertFalse(self.bst.is_empty())

    def test_clear(self):
        """Test clear operation"""
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)

        self.bst.clear()
        self.assertTrue(self.bst.is_empty())
        self.assertEqual(self.bst.size(), 0)


class TestPerformance(unittest.TestCase):
    """Performance and benchmarking tests"""

    def test_stack_performance(self):
        """Benchmark stack operations"""
        stack = Stack(max_size=1000)

        # Test push performance
        start = time.time()
        for i in range(1000):
            stack.push(i)
        push_time = time.time() - start

        # Test pop performance
        start = time.time()
        for i in range(1000):
            stack.pop()
        pop_time = time.time() - start

        print(f"\nStack Performance:")
        print(f"  1000 pushes: {push_time:.4f}s")
        print(f"  1000 pops: {pop_time:.4f}s")

        # Both should be very fast (O(1) operations)
        self.assertLess(push_time, 0.1)
        self.assertLess(pop_time, 0.1)

    def test_linked_list_performance(self):
        """Benchmark linked list operations"""
        ll = LinkedList()

        # Test insert at head performance
        start = time.time()
        for i in range(100):
            ll.insert_at_head(i)
        insert_time = time.time() - start

        # Test search performance
        start = time.time()
        for i in range(100):
            ll.search(i)
        search_time = time.time() - start

        print(f"\nLinked List Performance:")
        print(f"  1000 inserts: {insert_time:.4f}s")
        print(f"  1000 searches: {search_time:.4f}s")

    def test_bst_performance(self):
        """Benchmark BST operations"""
        bst = BinarySearchTree()

        # Test insert performance
        start = time.time()
        for i in range(1000):
            bst.insert(i)
        insert_time = time.time() - start

        # Test search performance
        start = time.time()
        for i in range(1000):
            bst.search(i)
        search_time = time.time() - start

        print(f"\nBST Performance:")
        print(f"  1000 inserts: {insert_time:.4f}s")
        print(f"  1000 searches: {search_time:.4f}s")


def run_tests():
    """Run all tests with verbose output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestStack))
    suite.addTests(loader.loadTestsFromTestCase(TestQueue))
    suite.addTests(loader.loadTestsFromTestCase(TestLinkedList))
    suite.addTests(loader.loadTestsFromTestCase(TestBinarySearchTree))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
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
