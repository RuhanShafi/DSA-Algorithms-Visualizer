"""
Unit Tests for Phase 3: Puzzle Challenges
Tests for Pathfinding, Event Queue, and Dynamic Programming
"""

import unittest
import sys
import time
sys.path.append('..')

from phase3.pathfinding import PathfindingAlgorithms
from phase3.event_queue import EventQueue, EventSimulator, Event
from phase3.dp_puzzle import GridPathDP, GridPathWithWeights


class TestPathfinding(unittest.TestCase):
    """Test cases for pathfinding algorithms"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Simple 5x5 grid
        self.simple_grid = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        
        # Grid with no path
        self.blocked_grid = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
    
    def test_manhattan_distance(self):
        """Test Manhattan distance heuristic"""
        dist = PathfindingAlgorithms.manhattan_distance((0, 0), (3, 4))
        self.assertEqual(dist, 7)
        
        dist = PathfindingAlgorithms.manhattan_distance((2, 3), (2, 3))
        self.assertEqual(dist, 0)
    
    def test_euclidean_distance(self):
        """Test Euclidean distance heuristic"""
        dist = PathfindingAlgorithms.euclidean_distance((0, 0), (3, 4))
        self.assertEqual(dist, 5.0)
        
        dist = PathfindingAlgorithms.euclidean_distance((0, 0), (0, 0))
        self.assertEqual(dist, 0.0)
    
    def test_get_neighbors(self):
        """Test neighbor generation"""
        neighbors = PathfindingAlgorithms.get_neighbors((2, 2), self.simple_grid)
        self.assertEqual(len(neighbors), 4)  # All 4 directions should be clear
        
        # Top-left corner
        neighbors = PathfindingAlgorithms.get_neighbors((0, 0), self.simple_grid)
        self.assertEqual(len(neighbors), 2)  # Only right and down
    
    def test_astar_simple_path(self):
        """Test A* on simple grid"""
        path, visited, stats = PathfindingAlgorithms.a_star(
            self.simple_grid, (0, 0), (4, 4)
        )
        
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
        self.assertEqual(stats['algorithm'], 'A*')
    
    def test_astar_no_path(self):
        """Test A* when no path exists"""
        path, visited, stats = PathfindingAlgorithms.a_star(
            self.blocked_grid, (0, 0), (4, 0)
        )
        
        self.assertEqual(len(path), 0)
        self.assertGreater(len(visited), 0)
    
    def test_dijkstra_simple_path(self):
        """Test Dijkstra on simple grid"""
        path, visited, stats = PathfindingAlgorithms.dijkstra(
            self.simple_grid, (0, 0), (4, 4)
        )
        
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
        self.assertEqual(stats['algorithm'], 'Dijkstra')
    
    def test_astar_vs_dijkstra(self):
        """Compare A* and Dijkstra performance"""
        # A* should explore fewer nodes due to heuristic
        path_astar, visited_astar, stats_astar = PathfindingAlgorithms.a_star(
            self.simple_grid, (0, 0), (4, 4)
        )
        
        path_dijkstra, visited_dijkstra, stats_dijkstra = PathfindingAlgorithms.dijkstra(
            self.simple_grid, (0, 0), (4, 4)
        )
        
        # Both should find a path
        self.assertGreater(len(path_astar), 0)
        self.assertGreater(len(path_dijkstra), 0)
        
        # A* typically explores fewer nodes
        self.assertLessEqual(
            stats_astar['nodes_expanded'],
            stats_dijkstra['nodes_expanded']
        )
    
    def test_path_reconstruction(self):
        """Test path reconstruction"""
        parents = {
            (0, 0): None,
            (0, 1): (0, 0),
            (0, 2): (0, 1),
            (1, 2): (0, 2),
            (2, 2): (1, 2)
        }
        
        path = PathfindingAlgorithms.reconstruct_path(parents, (0, 0), (2, 2))
        
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))
        self.assertEqual(len(path), 5)


class TestEventQueue(unittest.TestCase):
    """Test cases for Event Queue"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.queue = EventQueue()
    
    def test_add_event(self):
        """Test adding events"""
        event = self.queue.add_event(10.0, 1, "Test Event")
        
        self.assertEqual(event.time, 10.0)
        self.assertEqual(event.priority, 1)
        self.assertEqual(self.queue.size(), 1)
    
    def test_event_ordering(self):
        """Test events are ordered by time and priority"""
        self.queue.add_event(10.0, 2, "Event 1")
        self.queue.add_event(5.0, 1, "Event 2")
        self.queue.add_event(10.0, 1, "Event 3")
        
        # Should process in order: 5.0, 10.0 (priority 1), 10.0 (priority 2)
        event1 = self.queue.process_next_event()
        self.assertEqual(event1.time, 5.0)
        
        event2 = self.queue.process_next_event()
        self.assertEqual(event2.time, 10.0)
        self.assertEqual(event2.priority, 1)
        
        event3 = self.queue.process_next_event()
        self.assertEqual(event3.time, 10.0)
        self.assertEqual(event3.priority, 2)
    
    def test_process_next_event(self):
        """Test processing events"""
        self.queue.add_event(10.0, 1, "Event 1")
        self.queue.add_event(5.0, 1, "Event 2")
        
        event = self.queue.process_next_event()
        
        self.assertEqual(event.time, 5.0)
        self.assertEqual(self.queue.current_time, 5.0)
        self.assertEqual(self.queue.size(), 1)
    
    def test_peek_next_event(self):
        """Test peeking at next event"""
        self.queue.add_event(10.0, 1, "Event 1")
        
        event = self.queue.peek_next_event()
        
        self.assertIsNotNone(event)
        self.assertEqual(self.queue.size(), 1)  # Size shouldn't change
    
    def test_process_until_time(self):
        """Test processing events until a specific time"""
        self.queue.add_event(5.0, 1, "Event 1")
        self.queue.add_event(10.0, 1, "Event 2")
        self.queue.add_event(15.0, 1, "Event 3")
        
        processed = self.queue.process_until_time(12.0)
        
        self.assertEqual(len(processed), 2)
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.current_time, 12.0)
    
    def test_process_n_events(self):
        """Test processing n events"""
        for i in range(5):
            self.queue.add_event(float(i), 1, f"Event {i}")
        
        processed = self.queue.process_n_events(3)
        
        self.assertEqual(len(processed), 3)
        self.assertEqual(self.queue.size(), 2)
    
    def test_is_empty(self):
        """Test empty queue detection"""
        self.assertTrue(self.queue.is_empty())
        
        self.queue.add_event(10.0, 1, "Event")
        self.assertFalse(self.queue.is_empty())
        
        self.queue.process_next_event()
        self.assertTrue(self.queue.is_empty())
    
    def test_clear(self):
        """Test clearing queue"""
        self.queue.add_event(10.0, 1, "Event 1")
        self.queue.add_event(20.0, 1, "Event 2")
        
        self.queue.clear()
        
        self.assertTrue(self.queue.is_empty())
    
    def test_statistics(self):
        """Test statistics generation"""
        self.queue.add_event(10.0, 1, "Event 1")
        self.queue.process_next_event()
        self.queue.add_event(20.0, 1, "Event 2")
        
        stats = self.queue.get_statistics()
        
        self.assertEqual(stats['current_time'], 10.0)
        self.assertEqual(stats['pending_events'], 1)
        self.assertEqual(stats['processed_events'], 1)


class TestEventSimulator(unittest.TestCase):
    """Test cases for Event Simulator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.simulator = EventSimulator()
    
    def test_schedule_task(self):
        """Test task scheduling"""
        self.simulator.schedule_task(10.0, 5.0, "Task 1")
        
        queue = self.simulator.get_queue()
        self.assertEqual(queue.size(), 2)  # Start and end events
    
    def test_schedule_meeting(self):
        """Test meeting scheduling"""
        self.simulator.schedule_meeting(15.0, 2.0, "Team Meeting")
        
        queue = self.simulator.get_queue()
        self.assertEqual(queue.size(), 1)
    
    def test_schedule_recurring(self):
        """Test recurring event scheduling"""
        self.simulator.schedule_recurring(0.0, 5.0, 3, "Backup")
        
        queue = self.simulator.get_queue()
        self.assertEqual(queue.size(), 3)


class TestGridPathDP(unittest.TestCase):
    """Test cases for Dynamic Programming Grid Path"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.dp = GridPathDP(5, 5)
    
    def test_count_paths_no_obstacles(self):
        """Test path counting with no obstacles"""
        count = self.dp.count_paths_tabulation()
        
        # For 5x5 grid: C(8,4) = 70 paths
        self.assertEqual(count, 70)
    
    def test_count_paths_with_obstacles(self):
        """Test path counting with obstacles"""
        self.dp.set_obstacle(2, 2)
        count = self.dp.count_paths_tabulation()
        
        # Should have fewer paths
        self.assertLess(count, 70)
        self.assertGreater(count, 0)
    
    def test_count_paths_blocked(self):
        """Test when path is completely blocked"""
        # Block entire middle column
        for row in range(5):
            self.dp.set_obstacle(row, 2)
        
        count = self.dp.count_paths_tabulation()
        self.assertEqual(count, 0)
    
    def test_reconstruct_path(self):
        """Test path reconstruction"""
        self.dp.count_paths_tabulation()
        path = self.dp.reconstruct_one_path()
        
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
    
    def test_memoization(self):
        """Test memoization approach"""
        count = self.dp.count_paths_memoization()
        
        self.assertEqual(count, 70)
    
    def test_get_all_paths_small_grid(self):
        """Test getting all paths on small grid"""
        small_dp = GridPathDP(3, 3)
        all_paths = small_dp.get_all_paths()
        
        # For 3x3 grid: C(4,2) = 6 paths
        self.assertEqual(len(all_paths), 6)
    
    def test_obstacle_methods(self):
        """Test obstacle manipulation"""
        self.dp.set_obstacle(2, 2)
        self.assertTrue(self.dp.is_obstacle(2, 2))
        
        self.dp.remove_obstacle(2, 2)
        self.assertFalse(self.dp.is_obstacle(2, 2))
        
        self.dp.set_obstacle(1, 1)
        self.dp.clear_obstacles()
        self.assertFalse(self.dp.is_obstacle(1, 1))
    
    def test_statistics(self):
        """Test statistics generation"""
        self.dp.set_obstacle(2, 2)
        self.dp.count_paths_tabulation()
        
        stats = self.dp.get_statistics()
        
        self.assertEqual(stats['rows'], 5)
        self.assertEqual(stats['cols'], 5)
        self.assertEqual(stats['obstacle_count'], 1)
        self.assertTrue(stats['has_solution'])


class TestGridPathWithWeights(unittest.TestCase):
    """Test cases for weighted grid paths"""
    
    def test_min_cost_path(self):
        """Test minimum cost path calculation"""
        weighted = GridPathWithWeights(3, 3)
        
        # Set some weights
        weighted.set_weight(0, 1, 5)
        weighted.set_weight(1, 0, 3)
        
        cost = weighted.min_cost_path()
        
        # Should find a valid path
        self.assertGreater(cost, 0)
        self.assertLess(cost, float('inf'))


class TestPerformance(unittest.TestCase):
    """Performance benchmarking tests"""
    
    def test_pathfinding_performance(self):
        """Benchmark pathfinding algorithms"""
        # Large grid
        size = 50
        grid = [[0 for _ in range(size)] for _ in range(size)]
        
        # A* performance
        start_time = time.time()
        path_astar, _, stats_astar = PathfindingAlgorithms.a_star(
            grid, (0, 0), (size-1, size-1)
        )
        astar_time = time.time() - start_time
        
        # Dijkstra performance
        start_time = time.time()
        path_dijkstra, _, stats_dijkstra = PathfindingAlgorithms.dijkstra(
            grid, (0, 0), (size-1, size-1)
        )
        dijkstra_time = time.time() - start_time
        
        print(f"\nPathfinding Performance (50x50 grid):")
        print(f"  A*: {astar_time:.4f}s, nodes: {stats_astar['nodes_expanded']}")
        print(f"  Dijkstra: {dijkstra_time:.4f}s, nodes: {stats_dijkstra['nodes_expanded']}")
        
        # A* should be faster
        self.assertLess(astar_time, dijkstra_time * 2)
    
    def test_event_queue_performance(self):
        """Benchmark event queue operations"""
        queue = EventQueue()
        
        # Add many events
        start_time = time.time()
        for i in range(1000):
            queue.add_event(float(i), i % 10, f"Event {i}")
        add_time = time.time() - start_time
        
        # Process all events
        start_time = time.time()
        while not queue.is_empty():
            queue.process_next_event()
        process_time = time.time() - start_time
        
        print(f"\nEvent Queue Performance:")
        print(f"  1000 additions: {add_time:.4f}s")
        print(f"  1000 processes: {process_time:.4f}s")
    
    def test_dp_performance(self):
        """Benchmark DP algorithm"""
        dp = GridPathDP(20, 20)
        
        # Tabulation
        start_time = time.time()
        count_tab = dp.count_paths_tabulation()
        tab_time = time.time() - start_time
        
        # Memoization
        dp.reset()
        start_time = time.time()
        count_memo = dp.count_paths_memoization()
        memo_time = time.time() - start_time
        
        print(f"\nDP Performance (20x20 grid):")
        print(f"  Tabulation: {tab_time:.4f}s, paths: {count_tab}")
        print(f"  Memoization: {memo_time:.4f}s, paths: {count_memo}")
        
        self.assertEqual(count_tab, count_memo)


def run_tests():
    """Run all Phase 3 tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPathfinding))
    suite.addTests(loader.loadTestsFromTestCase(TestEventQueue))
    suite.addTests(loader.loadTestsFromTestCase(TestEventSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestGridPathDP))
    suite.addTests(loader.loadTestsFromTestCase(TestGridPathWithWeights))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("PHASE 3 TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)