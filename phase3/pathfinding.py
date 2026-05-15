"""
Pathfinding Algorithms: A* and Dijkstra
Optimized implementations for grid-based pathfinding
"""

import heapq
from typing import List, Tuple, Optional, Dict, Set


class PathfindingNode:
    """Node for pathfinding with priority queue support"""
    __slots__ = ('pos', 'g', 'h', 'f', 'parent')
    
    def __init__(self, pos: Tuple[int, int], g: float = 0, h: float = 0, parent: Optional[Tuple[int, int]] = None):
        self.pos = pos
        self.g = g  # Cost from start
        self.h = h  # Heuristic cost to goal
        self.f = g + h  # Total cost
        self.parent = parent
    
    def __lt__(self, other):
        """Comparison for priority queue (with tie-breaking)"""
        if self.f == other.f:
            return self.h < other.h  # Prefer nodes closer to goal
        return self.f < other.f


class PathfindingAlgorithms:
    """
    Collection of pathfinding algorithms
    """
    
    # Movement directions (4-directional)
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Movement directions (8-directional with diagonals)
    DIRECTIONS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), 
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    @staticmethod
    def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """
        Calculate Manhattan distance heuristic
        
        Args:
            pos1: Starting position (row, col)
            pos2: Target position (row, col)
            
        Returns:
            Manhattan distance
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    @staticmethod
    def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calculate Euclidean distance heuristic
        
        Args:
            pos1: Starting position (row, col)
            pos2: Target position (row, col)
            
        Returns:
            Euclidean distance
        """
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    @staticmethod
    def get_neighbors(pos: Tuple[int, int], grid: List[List[int]], 
                     diagonal: bool = False) -> List[Tuple[int, int]]:
        """
        Get valid neighboring positions
        
        Args:
            pos: Current position (row, col)
            grid: 2D grid (0 = walkable, 1 = wall)
            diagonal: Allow diagonal movement
            
        Returns:
            List of valid neighbor positions
        """
        rows, cols = len(grid), len(grid[0])
        directions = PathfindingAlgorithms.DIRECTIONS_8 if diagonal else PathfindingAlgorithms.DIRECTIONS
        
        neighbors = []
        for dr, dc in directions:
            new_row, new_col = pos[0] + dr, pos[1] + dc
            
            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                # Check if walkable
                if grid[new_row][new_col] == 0:
                    neighbors.append((new_row, new_col))
        
        return neighbors
    
    @staticmethod
    def reconstruct_path(parents: Dict[Tuple[int, int], Optional[Tuple[int, int]]], 
                        start: Tuple[int, int], 
                        goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct path from parent pointers
        
        Args:
            parents: Dictionary mapping position to parent position
            start: Start position
            goal: Goal position
            
        Returns:
            List of positions from start to goal
        """
        path = []
        current = goal
        
        while current is not None:
            path.append(current)
            current = parents.get(current)
        
        path.reverse()
        return path
    
    @staticmethod
    def a_star(grid: List[List[int]], 
              start: Tuple[int, int], 
              goal: Tuple[int, int],
              heuristic: str = 'manhattan',
              diagonal: bool = False) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]], Dict]:
        """
        A* pathfinding algorithm
        
        Args:
            grid: 2D grid (0 = walkable, 1 = wall)
            start: Start position (row, col)
            goal: Goal position (row, col)
            heuristic: 'manhattan' or 'euclidean'
            diagonal: Allow diagonal movement
            
        Returns:
            Tuple of (path, visited_nodes, stats)
            - path: List of positions from start to goal (empty if no path)
            - visited_nodes: List of explored positions in order
            - stats: Dictionary with algorithm statistics
        """
        # Choose heuristic function
        h_func = (PathfindingAlgorithms.euclidean_distance if heuristic == 'euclidean' 
                 else PathfindingAlgorithms.manhattan_distance)
        
        # Initialize
        open_heap = []
        start_h = h_func(start, goal)
        heapq.heappush(open_heap, (start_h, 0, start))  # (f, g, pos)
        
        closed_set: Set[Tuple[int, int]] = set()
        g_scores: Dict[Tuple[int, int], float] = {start: 0}
        parents: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        
        visited_order = []
        nodes_expanded = 0
        
        while open_heap:
            f, g, current = heapq.heappop(open_heap)
            
            # Skip if already processed
            if current in closed_set:
                continue
            
            # Mark as visited
            closed_set.add(current)
            visited_order.append(current)
            nodes_expanded += 1
            
            # Check if goal reached
            if current == goal:
                path = PathfindingAlgorithms.reconstruct_path(parents, start, goal)
                stats = {
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'path_cost': g_scores[goal],
                    'algorithm': 'A*',
                    'heuristic': heuristic
                }
                return path, visited_order, stats
            
            # Explore neighbors
            for neighbor in PathfindingAlgorithms.get_neighbors(current, grid, diagonal):
                if neighbor in closed_set:
                    continue
                
                # Calculate cost (1 for cardinal, ~1.414 for diagonal)
                move_cost = 1.414 if diagonal and abs(neighbor[0] - current[0]) + abs(neighbor[1] - current[1]) == 2 else 1
                tentative_g = g_scores[current] + move_cost
                
                # Update if better path found
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    h = h_func(neighbor, goal)
                    f = tentative_g + h
                    heapq.heappush(open_heap, (f, tentative_g, neighbor))
                    parents[neighbor] = current
        
        # No path found
        stats = {
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'path_cost': float('inf'),
            'algorithm': 'A*',
            'heuristic': heuristic
        }
        return [], visited_order, stats
    
    @staticmethod
    def dijkstra(grid: List[List[int]], 
                start: Tuple[int, int], 
                goal: Tuple[int, int],
                diagonal: bool = False) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]], Dict]:
        """
        Dijkstra's pathfinding algorithm (A* with h=0)
        
        Args:
            grid: 2D grid (0 = walkable, 1 = wall)
            start: Start position (row, col)
            goal: Goal position (row, col)
            diagonal: Allow diagonal movement
            
        Returns:
            Tuple of (path, visited_nodes, stats)
        """
        # Initialize
        open_heap = []
        heapq.heappush(open_heap, (0, start))  # (cost, pos)
        
        closed_set: Set[Tuple[int, int]] = set()
        costs: Dict[Tuple[int, int], float] = {start: 0}
        parents: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        
        visited_order = []
        nodes_expanded = 0
        
        while open_heap:
            current_cost, current = heapq.heappop(open_heap)
            
            # Skip if already processed
            if current in closed_set:
                continue
            
            # Mark as visited
            closed_set.add(current)
            visited_order.append(current)
            nodes_expanded += 1
            
            # Check if goal reached
            if current == goal:
                path = PathfindingAlgorithms.reconstruct_path(parents, start, goal)
                stats = {
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'path_cost': costs[goal],
                    'algorithm': 'Dijkstra'
                }
                return path, visited_order, stats
            
            # Explore neighbors
            for neighbor in PathfindingAlgorithms.get_neighbors(current, grid, diagonal):
                if neighbor in closed_set:
                    continue
                
                # Calculate cost
                move_cost = 1.414 if diagonal and abs(neighbor[0] - current[0]) + abs(neighbor[1] - current[1]) == 2 else 1
                tentative_cost = costs[current] + move_cost
                
                # Update if better path found
                if neighbor not in costs or tentative_cost < costs[neighbor]:
                    costs[neighbor] = tentative_cost
                    heapq.heappush(open_heap, (tentative_cost, neighbor))
                    parents[neighbor] = current
        
        # No path found
        stats = {
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'path_cost': float('inf'),
            'algorithm': 'Dijkstra'
        }
        return [], visited_order, stats