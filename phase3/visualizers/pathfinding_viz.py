"""
Pathfinding Puzzle Visualizer
Interactive grid-based pathfinding with A* and Dijkstra
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, Label, Panel, draw_instructions, draw_stats, get_font
from phase3.pathfinding import PathfindingAlgorithms
from collections import deque


class PathfindingVisualizer:
    """
    Interactive pathfinding puzzle visualization
    """
    
    def __init__(self, screen):
        """Initialize pathfinding visualizer"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Grid settings
        self.grid_rows = 25
        self.grid_cols = 35
        self.cell_size = 25
        self.grid = [[0 for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]
        
        # Grid position
        self.grid_x = 400
        self.grid_y = 150
        
        # State
        self.start = None
        self.goal = None
        self.path = []
        self.visited = []
        self.stats = {}
        
        # Drawing state
        self.draw_mode = 'wall'  # 'wall', 'start', 'goal'
        self.mouse_pressed = False
        self.last_cell = None
        
        # Animation
        self.animating = False
        self.animation_queue = deque()
        self.animation_speed = 10  # ms per step
        self.animation_timer = 0
        
        # Algorithm
        self.algorithm = 'astar'  # 'astar' or 'dijkstra'
        self.heuristic = 'manhattan'  # 'manhattan' or 'euclidean'
        self.diagonal = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components"""
        # Mode buttons
        self.wall_btn = Button(30, 150, 140, 40, "Wall", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        self.start_btn = Button(30, 200, 140, 40, "Start", SUCCESS_COLOR, "#059669")
        self.goal_btn = Button(30, 250, 140, 40, "Goal", DANGER_COLOR, DANGER_HOVER_COLOR)
        
        # Algorithm buttons
        self.astar_btn = Button(30, 320, 140, 40, "A* Algorithm", BUTTON_COLOR, BUTTON_HOVER_COLOR)
        self.dijkstra_btn = Button(30, 370, 140, 40, "Dijkstra", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Action buttons
        self.find_btn = Button(30, 440, 140, 50, "Find Path", SUCCESS_COLOR, "#059669")
        self.clear_path_btn = Button(190, 440, 140, 50, "Clear Path", WARNING_COLOR, "#d97706")
        self.clear_all_btn = Button(30, 500, 140, 50, "Clear All", DANGER_COLOR, DANGER_HOVER_COLOR)
        self.random_maze_btn = Button(190, 500, 140, 50, "Random Maze", INFO_COLOR, BUTTON_HOVER_COLOR)
        
        # Back button
        self.back_btn = Button(30, 800, 140, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Status label
        self.status_label = Label(30, 580, "", NORMAL_FONT_SIZE, TEXT_SECONDARY)
        
        # Instructions
        self.instructions = [
            "Click/drag to draw walls",
            "Use buttons to place Start/Goal",
            "Choose algorithm and find path",
            "Green = explored, Yellow = path"
        ]
    
    def handle_events(self):
        """Handle user input"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.animating:
                # Mode buttons
                if self.wall_btn.is_clicked(mouse_pos):
                    self.draw_mode = 'wall'
                elif self.start_btn.is_clicked(mouse_pos):
                    self.draw_mode = 'start'
                elif self.goal_btn.is_clicked(mouse_pos):
                    self.draw_mode = 'goal'
                
                # Algorithm buttons
                elif self.astar_btn.is_clicked(mouse_pos):
                    self.algorithm = 'astar'
                    self.status_label.set_text("Algorithm: A*")
                elif self.dijkstra_btn.is_clicked(mouse_pos):
                    self.algorithm = 'dijkstra'
                    self.status_label.set_text("Algorithm: Dijkstra")
                
                # Action buttons
                elif self.find_btn.is_clicked(mouse_pos):
                    self.find_path()
                elif self.clear_path_btn.is_clicked(mouse_pos):
                    self.clear_path()
                elif self.clear_all_btn.is_clicked(mouse_pos):
                    self.clear_all()
                elif self.random_maze_btn.is_clicked(mouse_pos):
                    self.generate_random_maze()
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
                
                # Grid interaction
                else:
                    self.mouse_pressed = True
                    self.handle_grid_click(mouse_pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                self.last_cell = None
            
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed and not self.animating:
                    self.handle_grid_click(mouse_pos)
        
        return True
    
    def handle_grid_click(self, mouse_pos):
        """Handle clicking on the grid"""
        # Check if click is within grid
        grid_rect = pygame.Rect(self.grid_x, self.grid_y, 
                               self.grid_cols * self.cell_size,
                               self.grid_rows * self.cell_size)
        
        if not grid_rect.collidepoint(mouse_pos):
            return
        
        # Calculate grid position
        col = (mouse_pos[0] - self.grid_x) // self.cell_size
        row = (mouse_pos[1] - self.grid_y) // self.cell_size
        
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            # Prevent repeated actions on same cell
            if (row, col) == self.last_cell and self.draw_mode == 'wall':
                return
            
            self.last_cell = (row, col)
            
            if self.draw_mode == 'wall':
                # Toggle wall
                if (row, col) != self.start and (row, col) != self.goal:
                    self.grid[row][col] = 1 - self.grid[row][col]
            elif self.draw_mode == 'start':
                self.start = (row, col)
                self.grid[row][col] = 0  # Clear wall if any
                self.status_label.set_text(f"Start set: ({row}, {col})")
            elif self.draw_mode == 'goal':
                self.goal = (row, col)
                self.grid[row][col] = 0  # Clear wall if any
                self.status_label.set_text(f"Goal set: ({row}, {col})")
    
    def find_path(self):
        """Run pathfinding algorithm"""
        if not self.start or not self.goal:
            self.status_label.set_text("Set both start and goal!")
            return
        
        # Clear previous path
        self.path = []
        self.visited = []
        
        # Run algorithm
        if self.algorithm == 'astar':
            self.path, self.visited, self.stats = PathfindingAlgorithms.a_star(
                self.grid, self.start, self.goal, self.heuristic, self.diagonal
            )
        else:
            self.path, self.visited, self.stats = PathfindingAlgorithms.dijkstra(
                self.grid, self.start, self.goal, self.diagonal
            )
        
        # Start animation
        if self.visited or self.path:
            self.start_animation()
        else:
            self.status_label.set_text("No path found!")
    
    def start_animation(self):
        """Start pathfinding animation"""
        self.animating = True
        self.animation_queue = deque()
        
        # Add visited cells to queue
        for cell in self.visited:
            if cell != self.start and cell != self.goal:
                self.animation_queue.append(('visited', cell))
        
        # Add path cells to queue
        for cell in self.path:
            if cell != self.start and cell != self.goal:
                self.animation_queue.append(('path', cell))
        
        self.animation_timer = 0
    
    def update_animation(self, dt):
        """Update animation state"""
        if not self.animating or not self.animation_queue:
            if self.animating:
                self.animating = False
                msg = f"Path found! Length: {self.stats.get('path_length', 0)}, Nodes: {self.stats.get('nodes_expanded', 0)}"
                self.status_label.set_text(msg)
            return
        
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            
            # Process next animation step
            if self.animation_queue:
                self.animation_queue.popleft()
    
    def clear_path(self):
        """Clear path and visited cells"""
        self.path = []
        self.visited = []
        self.stats = {}
        self.animating = False
        self.animation_queue.clear()
        self.status_label.set_text("Path cleared")
    
    def clear_all(self):
        """Clear everything"""
        self.grid = [[0 for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]
        self.start = None
        self.goal = None
        self.clear_path()
        self.status_label.set_text("Grid cleared")
    
    def generate_random_maze(self):
        """Generate a random maze"""
        import random
        
        self.clear_all()
        
        # Random walls (20% density)
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if random.random() < 0.2:
                    self.grid[row][col] = 1
        
        # Set random start and goal
        self.start = (random.randint(0, self.grid_rows - 1), 
                     random.randint(0, self.grid_cols // 4))
        self.goal = (random.randint(0, self.grid_rows - 1), 
                    random.randint(3 * self.grid_cols // 4, self.grid_cols - 1))
        
        # Ensure start and goal are clear
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.goal[0]][self.goal[1]] = 0
        
        self.status_label.set_text("Random maze generated!")
    
    def draw_grid(self):
        """Draw the grid"""
        # Draw cells
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x = self.grid_x + col * self.cell_size
                y = self.grid_y + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                # Determine color
                if (row, col) == self.start:
                    color = START_COLOR
                elif (row, col) == self.goal:
                    color = END_COLOR
                elif self.grid[row][col] == 1:
                    color = WALL_COLOR
                elif (row, col) in self.path:
                    color = PATH_FOUND_COLOR
                elif (row, col) in self.visited:
                    # Check if should be shown yet in animation
                    if self.animating:
                        index = self.visited.index((row, col))
                        shown_count = len(self.visited) - len([x for x in self.animation_queue if x[0] == 'visited'])
                        if index < shown_count:
                            color = EXPLORED_COLOR
                        else:
                            color = GRID_BG_COLOR
                    else:
                        color = EXPLORED_COLOR
                else:
                    color = GRID_BG_COLOR
                
                # Draw cell
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_LINE_COLOR, rect, 1)
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BG_COLOR)
        
        # Title
        title_font = get_font(TITLE_FONT_SIZE)
        title = title_font.render("Pathfinding Puzzle", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Left panel
        panel = Panel(20, 140, 340, 480, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)
        
        # Mode label
        mode_label = Label(30, 120, "Drawing Mode:", NORMAL_FONT_SIZE, TEXT_COLOR)
        mode_label.draw(self.screen)
        
        # Algorithm label
        algo_label = Label(30, 300, "Algorithm:", NORMAL_FONT_SIZE, TEXT_COLOR)
        algo_label.draw(self.screen)
        
        # Highlight selected mode
        mouse_pos = pygame.mouse.get_pos()
        
        if self.draw_mode == 'wall':
            self.wall_btn.color = BUTTON_COLOR
        else:
            self.wall_btn.color = SECONDARY_BUTTON_COLOR
        
        if self.draw_mode == 'start':
            self.start_btn.color = BUTTON_COLOR
        else:
            self.start_btn.color = SUCCESS_COLOR
        
        if self.draw_mode == 'goal':
            self.goal_btn.color = BUTTON_COLOR
        else:
            self.goal_btn.color = DANGER_COLOR
        
        # Highlight selected algorithm
        if self.algorithm == 'astar':
            self.astar_btn.color = BUTTON_COLOR
            self.dijkstra_btn.color = SECONDARY_BUTTON_COLOR
        else:
            self.astar_btn.color = SECONDARY_BUTTON_COLOR
            self.dijkstra_btn.color = BUTTON_COLOR
        
        # Draw buttons
        self.wall_btn.draw(self.screen, mouse_pos)
        self.start_btn.draw(self.screen, mouse_pos)
        self.goal_btn.draw(self.screen, mouse_pos)
        self.astar_btn.draw(self.screen, mouse_pos)
        self.dijkstra_btn.draw(self.screen, mouse_pos)
        self.find_btn.draw(self.screen, mouse_pos)
        self.clear_path_btn.draw(self.screen, mouse_pos)
        self.clear_all_btn.draw(self.screen, mouse_pos)
        self.random_maze_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)
        
        # Status
        self.status_label.draw(self.screen)
        
        # Instructions
        inst_panel = Panel(20, 630, 340, 140, BG_SECONDARY, TEXT_MUTED)
        inst_panel.draw(self.screen)
        
        inst_label = Label(30, 650, "Instructions:", NORMAL_FONT_SIZE, TEXT_COLOR)
        inst_label.draw(self.screen)
        draw_instructions(self.screen, self.instructions, 30, 680)
        
        # Draw grid
        self.draw_grid()
        
        # Draw stats if available
        if self.stats:
            stats_panel = Panel(self.grid_x, self.grid_y + self.grid_rows * self.cell_size + 20,
                              self.grid_cols * self.cell_size, 100, BG_SECONDARY, TEXT_MUTED)
            stats_panel.draw(self.screen)
            
            stats_label = Label(self.grid_x + 10, self.grid_y + self.grid_rows * self.cell_size + 30,
                              "Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
            stats_label.draw(self.screen)
            
            stats_display = {
                "Algorithm": self.stats.get('algorithm', 'N/A'),
                "Path Length": self.stats.get('path_length', 0),
                "Nodes Expanded": self.stats.get('nodes_expanded', 0),
                "Path Cost": f"{self.stats.get('path_cost', 0):.2f}"
            }
            draw_stats(self.screen, stats_display, self.grid_x + 10, 
                      self.grid_y + self.grid_rows * self.cell_size + 60)
        
        pygame.display.flip()
    
    def run(self):
        """Main loop"""
        while self.running:
            dt = self.clock.tick(FPS)
            
            if not self.handle_events():
                break
            
            self.update_animation(dt)
            self.draw()
        
        return True


def main():
    """Standalone test"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Puzzle")
    
    visualizer = PathfindingVisualizer(screen)
    visualizer.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()