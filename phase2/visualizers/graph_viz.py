"""
Graph Traversal Visualizer with PyGame
Interactive visualization of BFS and DFS algorithms
"""

import pygame
import sys
import os
import math
from collections import deque

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, draw_instructions, draw_stats, get_font
from phase2.graph import Graph, GraphTraversal


class GraphVisualizer:
    """
    Interactive graph traversal visualization
    """
    
    def __init__(self, screen):
        """Initialize graph visualizer"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Graph instance
        self.graph = Graph(directed=False)
        
        # Node positions (manually placed or auto-layout)
        self.node_positions = {}
        
        # Visualization state
        self.algorithm = 'bfs'  # 'bfs' or 'dfs'
        self.start_node = None
        self.traversing = False
        self.traversal_generator = None
        self.current_state = None
        self.animation_speed = 500  # ms
        self.timer = 0
        
        # Mode
        self.mode = 'add_node'  # 'add_node', 'add_edge', 'select_start', 'delete'
        self.selected_node = None
        
        # Create sample graph
        self.create_sample_graph()
        
        self.setup_ui()
        
    def create_sample_graph(self):
        """Create a sample graph for demonstration"""
        # Create nodes
        for i in range(1, 8):
            self.graph.add_node(i)
        
        # Add edges
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (5, 7)]
        for u, v in edges:
            self.graph.add_edge(u, v)
        
        # Set positions (circular layout)
        center_x = 700
        center_y = 450
        radius = 200
        nodes = self.graph.get_nodes()
        
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[node] = (int(x), int(y))
    
    def setup_ui(self):
        """Setup UI components"""
        # Mode buttons
        self.add_node_btn = Button(30, 150, 140, 40, "Add Node", BUTTON_COLOR, BUTTON_HOVER_COLOR)
        self.add_edge_btn = Button(180, 150, 140, 40, "Add Edge", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        self.select_start_btn = Button(330, 150, 140, 40, "Select Start", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Algorithm buttons
        self.bfs_btn = Button(30, 210, 140, 40, "BFS", BUTTON_COLOR, BUTTON_HOVER_COLOR)
        self.dfs_btn = Button(180, 210, 140, 40, "DFS", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Control buttons
        self.start_btn = Button(30, 270, 140, 50, "▶ Start", SUCCESS_COLOR, "#059669")
        self.reset_btn = Button(180, 270, 140, 50, "Reset", WARNING_COLOR, "#d97706")
        self.clear_btn = Button(330, 270, 140, 50, "Clear Graph", DANGER_COLOR, DANGER_HOVER_COLOR)
        
        self.back_btn = Button(30, 800, 150, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Status label
        self.status_label = Label(30, 340, "", SMALL_FONT_SIZE, TEXT_SECONDARY)
        
        # Instructions
        self.instructions = [
            "1. Add nodes by clicking on canvas",
            "2. Switch to Add Edge mode",
            "3. Click two nodes to connect",
            "4. Select Start to choose start node",
            "5. Choose BFS or DFS and click Start"
        ]
    
    def handle_events(self):
        """Handle user input events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.traversing:
                # Mode buttons
                if self.add_node_btn.is_clicked(mouse_pos):
                    self.mode = 'add_node'
                    self.selected_node = None
                    self.status_label.set_text("Mode: Add Node - Click on canvas")
                
                elif self.add_edge_btn.is_clicked(mouse_pos):
                    self.mode = 'add_edge'
                    self.selected_node = None
                    self.status_label.set_text("Mode: Add Edge - Click two nodes")
                
                elif self.select_start_btn.is_clicked(mouse_pos):
                    self.mode = 'select_start'
                    self.selected_node = None
                    self.status_label.set_text("Mode: Select Start - Click a node")
                
                # Algorithm buttons
                elif self.bfs_btn.is_clicked(mouse_pos):
                    self.algorithm = 'bfs'
                    self.status_label.set_text("Algorithm: BFS selected")
                
                elif self.dfs_btn.is_clicked(mouse_pos):
                    self.algorithm = 'dfs'
                    self.status_label.set_text("Algorithm: DFS selected")
                
                # Control buttons
                elif self.start_btn.is_clicked(mouse_pos):
                    self.start_traversal()
                
                elif self.reset_btn.is_clicked(mouse_pos):
                    self.reset_traversal()
                
                elif self.clear_btn.is_clicked(mouse_pos):
                    self.graph.clear()
                    self.node_positions.clear()
                    self.start_node = None
                    self.reset_traversal()
                    self.status_label.set_text("Graph cleared")
                
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
                
                # Canvas clicks
                else:
                    self.handle_canvas_click(mouse_pos)
        
        return True
    
    def handle_canvas_click(self, mouse_pos):
        """Handle clicks on the canvas area"""
        # Check if click is in canvas area
        if mouse_pos[0] < 500:
            return
        
        clicked_node = self.get_node_at_position(mouse_pos)
        
        if self.mode == 'add_node':
            if clicked_node is None:
                # Add new node
                new_node = len(self.graph.get_nodes()) + 1
                self.graph.add_node(new_node)
                self.node_positions[new_node] = mouse_pos
                self.status_label.set_text(f"Added node {new_node}")
        
        elif self.mode == 'add_edge':
            if clicked_node is not None:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                    self.status_label.set_text(f"Selected node {clicked_node}, click another")
                else:
                    if clicked_node != self.selected_node:
                        self.graph.add_edge(self.selected_node, clicked_node)
                        self.status_label.set_text(f"Added edge {self.selected_node} - {clicked_node}")
                    self.selected_node = None
        
        elif self.mode == 'select_start':
            if clicked_node is not None:
                self.start_node = clicked_node
                self.status_label.set_text(f"Start node: {clicked_node}")
    
    def get_node_at_position(self, pos):
        """Get node at mouse position"""
        for node, (x, y) in self.node_positions.items():
            distance = math.sqrt((pos[0] - x)**2 + (pos[1] - y)**2)
            if distance < NODE_RADIUS:
                return node
        return None
    
    def start_traversal(self):
        """Start graph traversal"""
        if self.start_node is None:
            self.status_label.set_text("Please select a start node first")
            return
        
        if self.graph.node_count == 0:
            self.status_label.set_text("Graph is empty")
            return
        
        self.traversing = True
        self.timer = 0
        
        if self.algorithm == 'bfs':
            self.traversal_generator = GraphTraversal.bfs(self.graph, self.start_node)
        else:
            self.traversal_generator = GraphTraversal.dfs(self.graph, self.start_node)
        
        self.status_label.set_text(f"Running {self.algorithm.upper()}...")
    
    def reset_traversal(self):
        """Reset traversal state"""
        self.traversing = False
        self.traversal_generator = None
        self.current_state = None
        self.status_label.set_text("Traversal reset")
    
    def update(self, dt):
        """Update traversal animation"""
        if self.traversing and self.traversal_generator:
            self.timer += dt
            
            if self.timer >= self.animation_speed:
                self.timer = 0
                
                try:
                    node, state = next(self.traversal_generator)
                    self.current_state = state
                    
                    if state['phase'] == 'complete':
                        self.traversing = False
                        self.status_label.set_text(f"{self.algorithm.upper()} complete!")
                
                except StopIteration:
                    self.traversing = False
                    self.status_label.set_text(f"{self.algorithm.upper()} complete!")
    
    def draw_graph(self):
        """Draw the graph"""
        # Draw edges
        for node in self.graph.get_nodes():
            if node in self.node_positions:
                x1, y1 = self.node_positions[node]
                
                for neighbor in self.graph.get_neighbors(node):
                    if neighbor in self.node_positions:
                        x2, y2 = self.node_positions[neighbor]
                        
                        # Don't draw edge twice for undirected graphs
                        if not self.graph.directed or node < neighbor:
                            pygame.draw.line(self.screen, TEXT_MUTED, (x1, y1), (x2, y2), 3)
        
        # Draw nodes
        for node in self.graph.get_nodes():
            if node in self.node_positions:
                x, y = self.node_positions[node]
                
                # Determine color based on state
                if self.current_state:
                    if node == self.current_state.get('current'):
                        color = VISITING_COLOR
                    elif node in self.current_state.get('visited', set()):
                        color = VISITED_COLOR
                    elif node in self.current_state.get('queue', []) or node in self.current_state.get('stack', []):
                        color = COMPARING_COLOR
                    elif node == self.start_node:
                        color = START_COLOR
                    else:
                        color = GRAPH_NODE_COLOR
                else:
                    if node == self.start_node:
                        color = START_COLOR
                    elif node == self.selected_node:
                        color = WARNING_COLOR
                    else:
                        color = GRAPH_NODE_COLOR
                
                # Draw circle
                pygame.draw.circle(self.screen, color, (x, y), NODE_RADIUS)
                pygame.draw.circle(self.screen, TEXT_COLOR, (x, y), NODE_RADIUS, 3)
                
                # Draw node label
                label_font = get_font(NORMAL_FONT_SIZE)
                label_text = label_font.render(str(node), True, TEXT_COLOR)
                label_rect = label_text.get_rect(center=(x, y))
                self.screen.blit(label_text, label_rect)
    
    def draw(self):
        """Draw all elements"""
        self.screen.fill(BG_COLOR)
        
        # Draw title
        title_font = get_font(TITLE_FONT_SIZE)
        title = title_font.render("Graph Traversal Visualizer", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw left panel
        panel = Panel(20, 140, 470, 200, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)
        
        # Highlight selected mode
        mouse_pos = pygame.mouse.get_pos()
        
        if self.mode == 'add_node':
            self.add_node_btn.color = BUTTON_COLOR
            self.add_edge_btn.color = SECONDARY_BUTTON_COLOR
            self.select_start_btn.color = SECONDARY_BUTTON_COLOR
        elif self.mode == 'add_edge':
            self.add_node_btn.color = SECONDARY_BUTTON_COLOR
            self.add_edge_btn.color = BUTTON_COLOR
            self.select_start_btn.color = SECONDARY_BUTTON_COLOR
        elif self.mode == 'select_start':
            self.add_node_btn.color = SECONDARY_BUTTON_COLOR
            self.add_edge_btn.color = SECONDARY_BUTTON_COLOR
            self.select_start_btn.color = BUTTON_COLOR
        
        # Highlight selected algorithm
        if self.algorithm == 'bfs':
            self.bfs_btn.color = BUTTON_COLOR
            self.dfs_btn.color = SECONDARY_BUTTON_COLOR
        else:
            self.bfs_btn.color = SECONDARY_BUTTON_COLOR
            self.dfs_btn.color = BUTTON_COLOR
        
        # Draw buttons
        self.add_node_btn.draw(self.screen, mouse_pos)
        self.add_edge_btn.draw(self.screen, mouse_pos)
        self.select_start_btn.draw(self.screen, mouse_pos)
        self.bfs_btn.draw(self.screen, mouse_pos)
        self.dfs_btn.draw(self.screen, mouse_pos)
        self.start_btn.draw(self.screen, mouse_pos)
        self.reset_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)
        
        # Draw status
        self.status_label.draw(self.screen)
        
        # Draw instructions
        inst_panel = Panel(20, 370, 470, 200, BG_SECONDARY, TEXT_MUTED)
        inst_panel.draw(self.screen)
        
        inst_title = Label(40, 390, "Instructions:", NORMAL_FONT_SIZE, TEXT_COLOR)
        inst_title.draw(self.screen)
        draw_instructions(self.screen, self.instructions, 40, 420)
        
        # Draw stats
        stats_panel = Panel(20, 590, 470, 180, BG_SECONDARY, TEXT_MUTED)
        stats_panel.draw(self.screen)
        
        stats_title = Label(40, 610, "Graph Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
        stats_title.draw(self.screen)
        
        stats = {
            "Nodes": self.graph.node_count,
            "Edges": self.graph.edge_count,
            "Start Node": self.start_node if self.start_node else "None",
            "Algorithm": self.algorithm.upper()
        }
        draw_stats(self.screen, stats, 40, 640)
        
        # Draw canvas
        canvas = Panel(510, 140, 870, 740, BG_SECONDARY, TEXT_MUTED)
        canvas.draw(self.screen)
        
        # Draw graph
        self.draw_graph()
        
        # Draw queue/stack if traversing
        if self.current_state:
            queue_stack = self.current_state.get('queue', self.current_state.get('stack', []))
            if queue_stack:
                label = "Queue:" if 'queue' in self.current_state else "Stack:"
                queue_font = get_font(SMALL_FONT_SIZE)
                queue_text = queue_font.render(f"{label} {queue_stack}", True, TEXT_COLOR)
                self.screen.blit(queue_text, (530, 850))
        
        pygame.display.flip()
    
    def run(self):
        """Main loop"""
        while self.running:
            dt = self.clock.tick(FPS)
            
            if not self.handle_events():
                break
            
            self.update(dt)
            self.draw()
        
        return True


def main():
    """Standalone test"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Graph Traversal Visualizer")
    
    visualizer = GraphVisualizer(screen)
    visualizer.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()