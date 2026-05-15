"""
Graph Data Structure and Traversal Algorithms
BFS and DFS with step-by-step tracking for visualization
"""

from typing import List, Dict, Set, Tuple, Optional, Generator
from collections import deque


class Graph:
    """
    Graph data structure with adjacency list representation
    Supports both directed and undirected graphs
    """

    def __init__(self, directed: bool = False):
        """
        Initialize graph

        Args:
            directed: If True, graph is directed
        """
        self.adj_list: Dict[int, List[int]] = {}
        self.directed = directed
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, node: int) -> bool:
        """
        Add a node to the graph

        Args:
            node: Node identifier

        Returns:
            True if node was added, False if already exists
        """
        if node not in self.adj_list:
            self.adj_list[node] = []
            self.node_count += 1
            return True
        return False

    def add_edge(self, from_node: int, to_node: int, weight: float = 1.0) -> bool:
        """
        Add an edge to the graph

        Args:
            from_node: Starting node
            to_node: Ending node
            weight: Edge weight (for weighted graphs)

        Returns:
            True if edge was added
        """
        # Ensure nodes exist
        self.add_node(from_node)
        self.add_node(to_node)

        # Add edge
        if to_node not in self.adj_list[from_node]:
            self.adj_list[from_node].append(to_node)
            self.edge_count += 1

            # Add reverse edge if undirected
            if not self.directed and from_node not in self.adj_list[to_node]:
                self.adj_list[to_node].append(from_node)

            return True
        return False

    def remove_edge(self, from_node: int, to_node: int) -> bool:
        """
        Remove an edge from the graph

        Args:
            from_node: Starting node
            to_node: Ending node

        Returns:
            True if edge was removed
        """
        if from_node in self.adj_list and to_node in self.adj_list[from_node]:
            self.adj_list[from_node].remove(to_node)
            self.edge_count -= 1

            # Remove reverse edge if undirected
            if not self.directed and from_node in self.adj_list[to_node]:
                self.adj_list[to_node].remove(from_node)

            return True
        return False

    def get_neighbors(self, node: int) -> List[int]:
        """
        Get neighbors of a node

        Args:
            node: Node identifier

        Returns:
            List of neighboring nodes
        """
        return self.adj_list.get(node, []).copy()

    def get_nodes(self) -> List[int]:
        """Get list of all nodes"""
        return list(self.adj_list.keys())

    def has_edge(self, from_node: int, to_node: int) -> bool:
        """Check if edge exists"""
        return to_node in self.adj_list.get(from_node, [])

    def get_degree(self, node: int) -> int:
        """Get degree of a node (number of edges)"""
        return len(self.adj_list.get(node, []))

    def clear(self):
        """Remove all nodes and edges"""
        self.adj_list.clear()
        self.node_count = 0
        self.edge_count = 0

    def __str__(self):
        return f"Graph(nodes={self.node_count}, edges={self.edge_count}, directed={self.directed})"

    def __repr__(self):
        return self.__str__()


class GraphTraversal:
    """
    Graph traversal algorithms with step-by-step tracking
    """

    @staticmethod
    def bfs(graph: Graph, start_node: int) -> Generator[Tuple[int, dict], None, None]:
        """
        Breadth-First Search with step-by-step tracking

        Args:
            graph: Graph to traverse
            start_node: Starting node

        Yields:
            Tuple of (current_node, state_info)
            state_info contains: visited, queue, parents, level
        """
        if start_node not in graph.adj_list:
            return

        visited: Set[int] = set()
        queue: deque = deque([start_node])
        parents: Dict[int, Optional[int]] = {start_node: None}
        levels: Dict[int, int] = {start_node: 0}

        # Yield initial state
        yield (
            start_node,
            {
                "visited": set(),
                "queue": list(queue),
                "current": start_node,
                "neighbors": [],
                "parents": parents.copy(),
                "levels": levels.copy(),
                "phase": "start",
            },
        )

        while queue:
            current = queue.popleft()

            if current in visited:
                continue

            visited.add(current)
            neighbors = graph.get_neighbors(current)

            # Yield visiting state
            yield (
                current,
                {
                    "visited": visited.copy(),
                    "queue": list(queue),
                    "current": current,
                    "neighbors": neighbors,
                    "parents": parents.copy(),
                    "levels": levels.copy(),
                    "phase": "visiting",
                },
            )

            # Add neighbors to queue
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
                    if neighbor not in parents:
                        parents[neighbor] = current
                        levels[neighbor] = levels[current] + 1

                    # Yield discovered state
                    yield (
                        neighbor,
                        {
                            "visited": visited.copy(),
                            "queue": list(queue),
                            "current": current,
                            "neighbors": neighbors,
                            "discovered": neighbor,
                            "parents": parents.copy(),
                            "levels": levels.copy(),
                            "phase": "discovered",
                        },
                    )

        # Final state
        yield (
            -1,
            {
                "visited": visited.copy(),
                "queue": [],
                "current": -1,
                "neighbors": [],
                "parents": parents.copy(),
                "levels": levels.copy(),
                "phase": "complete",
            },
        )

    @staticmethod
    def dfs(graph: Graph, start_node: int) -> Generator[Tuple[int, dict], None, None]:
        """
        Depth-First Search with step-by-step tracking

        Args:
            graph: Graph to traverse
            start_node: Starting node

        Yields:
            Tuple of (current_node, state_info)
        """
        if start_node not in graph.adj_list:
            return

        visited: Set[int] = set()
        stack: List[int] = [start_node]
        parents: Dict[int, Optional[int]] = {start_node: None}
        discovery_time: Dict[int, int] = {}
        time = [0]

        # Yield initial state
        yield (
            start_node,
            {
                "visited": set(),
                "stack": stack.copy(),
                "current": start_node,
                "neighbors": [],
                "parents": parents.copy(),
                "discovery_time": discovery_time.copy(),
                "phase": "start",
            },
        )

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)
            time[0] += 1
            discovery_time[current] = time[0]
            neighbors = graph.get_neighbors(current)

            # Yield visiting state
            yield (
                current,
                {
                    "visited": visited.copy(),
                    "stack": stack.copy(),
                    "current": current,
                    "neighbors": neighbors,
                    "parents": parents.copy(),
                    "discovery_time": discovery_time.copy(),
                    "phase": "visiting",
                },
            )

            # Add neighbors to stack (in reverse for consistent order)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    if neighbor not in stack:
                        stack.append(neighbor)
                    if neighbor not in parents:
                        parents[neighbor] = current

                    # Yield discovered state
                    yield (
                        neighbor,
                        {
                            "visited": visited.copy(),
                            "stack": stack.copy(),
                            "current": current,
                            "neighbors": neighbors,
                            "discovered": neighbor,
                            "parents": parents.copy(),
                            "discovery_time": discovery_time.copy(),
                            "phase": "discovered",
                        },
                    )

        # Final state
        yield (
            -1,
            {
                "visited": visited.copy(),
                "stack": [],
                "current": -1,
                "neighbors": [],
                "parents": parents.copy(),
                "discovery_time": discovery_time.copy(),
                "phase": "complete",
            },
        )

    @staticmethod
    def reconstruct_path(
        parents: Dict[int, Optional[int]], start: int, end: int
    ) -> Optional[List[int]]:
        """
        Reconstruct path from start to end using parent pointers

        Args:
            parents: Dictionary of parent pointers
            start: Start node
            end: End node

        Returns:
            List of nodes in path, or None if no path exists
        """
        if end not in parents:
            return None

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = parents.get(current)

        path.reverse()

        # Verify path starts at start node
        if path[0] != start:
            return None

        return path

    @staticmethod
    def find_connected_components(graph: Graph) -> List[Set[int]]:
        """
        Find all connected components in graph

        Args:
            graph: Graph to analyze

        Returns:
            List of sets, each containing nodes in a component
        """
        visited = set()
        components = []

        for node in graph.get_nodes():
            if node not in visited:
                # BFS to find component
                component = set()
                queue = deque([node])

                while queue:
                    current = queue.popleft()
                    if current in visited:
                        continue

                    visited.add(current)
                    component.add(current)

                    for neighbor in graph.get_neighbors(current):
                        if neighbor not in visited:
                            queue.append(neighbor)

                components.append(component)

        return components

    @staticmethod
    def has_cycle(graph: Graph) -> bool:
        """
        Detect if graph has a cycle

        Args:
            graph: Graph to check

        Returns:
            True if cycle exists
        """
        visited = set()
        rec_stack = set()

        def dfs_cycle(node: int, parent: Optional[int]) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get_neighbors(node):
                if neighbor not in visited:
                    if dfs_cycle(neighbor, node):
                        return True
                elif neighbor in rec_stack:
                    # For undirected graphs, skip parent
                    if not graph.directed or neighbor != parent:
                        return True

            rec_stack.remove(node)
            return False

        for node in graph.get_nodes():
            if node not in visited:
                if dfs_cycle(node, None):
                    return True

        return False
