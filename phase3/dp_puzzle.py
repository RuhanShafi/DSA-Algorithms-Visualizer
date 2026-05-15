"""
Dynamic Programming Puzzle: Grid Path Counting
Count unique paths in a grid with obstacles
"""

from typing import List, Tuple, Optional


class GridPathDP:
    """
    Dynamic Programming solution for grid path counting
    """
    
    def __init__(self, rows: int, cols: int):
        """
        Initialize grid path counter
        
        Args:
            rows: Number of rows
            cols: Number of columns
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.dp_table = None
        self.computation_order = []
    
    def set_obstacle(self, row: int, col: int):
        """
        Mark a cell as an obstacle
        
        Args:
            row: Row index
            col: Column index
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1
    
    def remove_obstacle(self, row: int, col: int):
        """
        Remove obstacle from a cell
        
        Args:
            row: Row index
            col: Column index
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 0
    
    def clear_obstacles(self):
        """Remove all obstacles"""
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
    def is_obstacle(self, row: int, col: int) -> bool:
        """Check if cell is an obstacle"""
        return self.grid[row][col] == 1
    
    def count_paths_tabulation(self, start: Tuple[int, int] = (0, 0), 
                              end: Tuple[int, int] = None) -> int:
        """
        Count paths using tabulation (bottom-up DP)
        Only right and down movements allowed
        
        Args:
            start: Starting position (row, col)
            end: Ending position (row, col), defaults to bottom-right
            
        Returns:
            Number of unique paths
        """
        if end is None:
            end = (self.rows - 1, self.cols - 1)
        
        # Check if start or end is obstacle
        if self.grid[start[0]][start[1]] == 1 or self.grid[end[0]][end[1]] == 1:
            return 0
        
        # Initialize DP table
        self.dp_table = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.computation_order = []
        
        # Base case: starting position
        self.dp_table[start[0]][start[1]] = 1
        self.computation_order.append((start[0], start[1], 1))
        
        # Fill first row
        for col in range(start[1] + 1, self.cols):
            if self.grid[start[0]][col] == 1:
                break  # Can't go further right if obstacle
            self.dp_table[start[0]][col] = 1
            self.computation_order.append((start[0], col, 1))
        
        # Fill first column
        for row in range(start[0] + 1, self.rows):
            if self.grid[row][start[1]] == 1:
                break  # Can't go further down if obstacle
            self.dp_table[row][start[1]] = 1
            self.computation_order.append((row, start[1], 1))
        
        # Fill rest of table
        for row in range(start[0] + 1, self.rows):
            for col in range(start[1] + 1, self.cols):
                if self.grid[row][col] == 1:
                    self.dp_table[row][col] = 0
                else:
                    # Paths from top + paths from left
                    from_top = self.dp_table[row - 1][col]
                    from_left = self.dp_table[row][col - 1]
                    self.dp_table[row][col] = from_top + from_left
                
                self.computation_order.append((row, col, self.dp_table[row][col]))
        
        return self.dp_table[end[0]][end[1]]
    
    def count_paths_memoization(self, start: Tuple[int, int] = (0, 0), 
                               end: Tuple[int, int] = None,
                               memo: dict = None) -> int:
        """
        Count paths using memoization (top-down DP)
        
        Args:
            start: Starting position
            end: Ending position
            memo: Memoization dictionary
            
        Returns:
            Number of unique paths
        """
        if end is None:
            end = (self.rows - 1, self.cols - 1)
        
        if memo is None:
            memo = {}
            self.computation_order = []
        
        # Base cases
        if start == end:
            return 1
        
        if (start[0] >= self.rows or start[1] >= self.cols or 
            self.grid[start[0]][start[1]] == 1):
            return 0
        
        # Check memo
        if start in memo:
            return memo[start]
        
        # Recursive case: go right + go down
        right = self.count_paths_memoization((start[0], start[1] + 1), end, memo)
        down = self.count_paths_memoization((start[0] + 1, start[1]), end, memo)
        
        result = right + down
        memo[start] = result
        self.computation_order.append((start[0], start[1], result))
        
        return result
    
    def reconstruct_one_path(self) -> Optional[List[Tuple[int, int]]]:
        """
        Reconstruct one valid path using the DP table
        
        Returns:
            List of (row, col) positions forming a path, or None if no path exists
        """
        if self.dp_table is None:
            return None
        
        # Start from end
        path = []
        row, col = self.rows - 1, self.cols - 1
        
        # Check if path exists
        if self.dp_table[row][col] == 0:
            return None
        
        path.append((row, col))
        
        # Backtrack to start
        while row > 0 or col > 0:
            # Try to go left
            if col > 0 and self.dp_table[row][col - 1] > 0:
                col -= 1
            # Otherwise go up
            elif row > 0 and self.dp_table[row - 1][col] > 0:
                row -= 1
            else:
                break
            
            path.append((row, col))
        
        path.reverse()
        return path
    
    def get_all_paths(self, current: Tuple[int, int] = (0, 0), 
                     end: Tuple[int, int] = None,
                     path: List[Tuple[int, int]] = None) -> List[List[Tuple[int, int]]]:
        """
        Get all possible paths (warning: exponential for large grids)
        
        Args:
            current: Current position
            end: End position
            path: Current path
            
        Returns:
            List of all valid paths
        """
        if end is None:
            end = (self.rows - 1, self.cols - 1)
        
        if path is None:
            path = []
        
        path = path + [current]
        
        # Reached destination
        if current == end:
            return [path]
        
        # Out of bounds or obstacle
        if (current[0] >= self.rows or current[1] >= self.cols or 
            self.grid[current[0]][current[1]] == 1):
            return []
        
        all_paths = []
        
        # Go right
        all_paths.extend(self.get_all_paths((current[0], current[1] + 1), end, path))
        
        # Go down
        all_paths.extend(self.get_all_paths((current[0] + 1, current[1]), end, path))
        
        return all_paths
    
    def get_dp_table(self) -> List[List[int]]:
        """
        Get the DP table
        
        Returns:
            2D list with path counts for each cell
        """
        return self.dp_table if self.dp_table else [[0] * self.cols for _ in range(self.rows)]
    
    def get_computation_order(self) -> List[Tuple[int, int, int]]:
        """
        Get the order in which cells were computed
        
        Returns:
            List of (row, col, value) tuples
        """
        return self.computation_order
    
    def reset(self):
        """Reset DP table and computation order"""
        self.dp_table = None
        self.computation_order = []
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the problem
        
        Returns:
            Dictionary with statistics
        """
        obstacle_count = sum(row.count(1) for row in self.grid)
        
        stats = {
            'rows': self.rows,
            'cols': self.cols,
            'total_cells': self.rows * self.cols,
            'obstacle_count': obstacle_count,
            'walkable_cells': self.rows * self.cols - obstacle_count,
            'has_solution': self.dp_table is not None
        }
        
        if self.dp_table:
            stats['total_paths'] = self.dp_table[self.rows - 1][self.cols - 1]
            stats['cells_computed'] = len(self.computation_order)
        
        return stats
    
    def __str__(self):
        """String representation"""
        result = f"GridPathDP({self.rows}x{self.cols})\n"
        for row in self.grid:
            result += " ".join("█" if cell == 1 else "·" for cell in row) + "\n"
        return result


class GridPathWithWeights:
    """
    Extended version with weighted cells (for minimum cost path)
    """
    
    def __init__(self, rows: int, cols: int):
        """Initialize with weights"""
        self.rows = rows
        self.cols = cols
        self.weights = [[1 for _ in range(cols)] for _ in range(rows)]
        self.dp_table = None
    
    def set_weight(self, row: int, col: int, weight: int):
        """Set weight for a cell"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.weights[row][col] = weight
    
    def min_cost_path(self) -> int:
        """
        Find minimum cost path from top-left to bottom-right
        
        Returns:
            Minimum cost
        """
        self.dp_table = [[float('inf')] * self.cols for _ in range(self.rows)]
        
        # Base case
        self.dp_table[0][0] = self.weights[0][0]
        
        # Fill first row
        for col in range(1, self.cols):
            self.dp_table[0][col] = self.dp_table[0][col - 1] + self.weights[0][col]
        
        # Fill first column
        for row in range(1, self.rows):
            self.dp_table[row][0] = self.dp_table[row - 1][0] + self.weights[row][0]
        
        # Fill rest
        for row in range(1, self.rows):
            for col in range(1, self.cols):
                from_top = self.dp_table[row - 1][col]
                from_left = self.dp_table[row][col - 1]
                self.dp_table[row][col] = min(from_top, from_left) + self.weights[row][col]
        
        return self.dp_table[self.rows - 1][self.cols - 1]