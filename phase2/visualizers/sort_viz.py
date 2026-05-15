"""
Sorting Algorithm Visualizer
Interactive visualization of sorting algorithms with bar chart representation
"""

import pygame
import sys
import random
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, Slider, draw_instructions, draw_stats, get_font
from phase2.sorting import SortingAlgorithms


class SortingVisualizer:
    """
    Interactive sorting algorithm visualization
    """
    
    def __init__(self, screen):
        """Initialize sorting visualizer"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Array settings
        self.array_size = 30
        self.array = []
        self.generate_random_array()
        
        # Algorithm state
        self.algorithm = 'bubble'  # 'bubble', 'selection', 'merge', 'quick'
        self.sorting = False
        self.paused = False
        self.sort_generator = None
        self.current_state = None
        self.animation_delay = 50  # ms
        self.timer = 0
        
        # Statistics
        self.comparisons = 0
        self.swaps = 0
        self.operations = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components"""
        # Algorithm selection buttons
        self.bubble_btn = Button(30, 150, 140, 40, "Bubble Sort", BUTTON_COLOR, BUTTON_HOVER_COLOR)
        self.selection_btn = Button(180, 150, 140, 40, "Selection Sort", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        self.merge_btn = Button(330, 150, 140, 40, "Merge Sort", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Control buttons
        self.start_btn = Button(30, 220, 140, 50, "▶ Start", SUCCESS_COLOR, "#059669")
        self.pause_btn = Button(180, 220, 140, 50, "⏸ Pause", WARNING_COLOR, "#d97706")
        self.reset_btn = Button(330, 220, 140, 50, "Reset", DANGER_COLOR, DANGER_HOVER_COLOR)
        
        # Array generation buttons
        self.random_btn = Button(30, 290, 140, 40, "Random", INFO_COLOR, BUTTON_HOVER_COLOR)
        self.reverse_btn = Button(180, 290, 140, 40, "Reversed", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        self.nearly_btn = Button(330, 290, 140, 40, "Nearly Sorted", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Size slider
        self.size_slider = Slider(30, 360, 440, 10, 100, self.array_size, "Array Size")
        
        # Speed slider
        self.speed_slider = Slider(30, 440, 440, 1, 200, 100, "Speed")
        
        # Back button
        self.back_btn = Button(30, 800, 140, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Status label
        self.status_label = Label(30, 520, "", NORMAL_FONT_SIZE, TEXT_SECONDARY)
        
        # Instructions
        self.instructions = [
            "Choose sorting algorithm",
            "Generate array pattern",
            "Adjust size and speed",
            "Click Start to sort",
            "Pause/Resume anytime"
        ]
    
    def generate_random_array(self):
        """Generate random array"""
        self.array = [random.randint(10, 400) for _ in range(self.array_size)]
        self.reset_sorting()
    
    def generate_reversed_array(self):
        """Generate reversed sorted array"""
        self.array = list(range(400, 10, -int(390 / self.array_size)))[:self.array_size]
        self.reset_sorting()
    
    def generate_nearly_sorted_array(self):
        """Generate nearly sorted array with few swaps"""
        self.array = list(range(10, 400, int(390 / self.array_size)))[:self.array_size]
        # Swap a few random pairs
        for _ in range(max(2, self.array_size // 10)):
            i, j = random.randint(0, self.array_size - 1), random.randint(0, self.array_size - 1)
            self.array[i], self.array[j] = self.array[j], self.array[i]
        self.reset_sorting()
    
    def reset_sorting(self):
        """Reset sorting state"""
        self.sorting = False
        self.paused = False
        self.sort_generator = None
        self.current_state = None
        self.comparisons = 0
        self.swaps = 0
        self.operations = 0
        self.timer = 0
    
    def start_sorting(self):
        """Start the sorting algorithm"""
        if self.sorting and not self.paused:
            return
        
        if not self.sorting:
            # Start new sort
            if self.algorithm == 'bubble':
                self.sort_generator = SortingAlgorithms.bubble_sort(self.array)
            elif self.algorithm == 'selection':
                self.sort_generator = SortingAlgorithms.selection_sort(self.array)
            elif self.algorithm == 'merge':
                self.sort_generator = SortingAlgorithms.merge_sort(self.array)
            elif self.algorithm == 'quick':
                self.sort_generator = SortingAlgorithms.quick_sort(self.array)
            
            self.sorting = True
            self.paused = False
            self.status_label.set_text(f"Sorting with {self.algorithm.title()} Sort...")
        else:
            # Resume
            self.paused = False
            self.status_label.set_text("Resumed")
    
    def pause_sorting(self):
        """Pause the sorting"""
        if self.sorting and not self.paused:
            self.paused = True
            self.status_label.set_text("Paused")
    
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
                elif event.key == pygame.K_SPACE:
                    if self.sorting:
                        if self.paused:
                            self.start_sorting()
                        else:
                            self.pause_sorting()
                    else:
                        self.start_sorting()
            
            # Handle sliders
            if self.size_slider.handle_event(event, mouse_pos):
                new_size = int(self.size_slider.get_value())
                if new_size != self.array_size:
                    self.array_size = new_size
                    self.generate_random_array()
            
            if self.speed_slider.handle_event(event, mouse_pos):
                speed_val = self.speed_slider.get_value()
                self.animation_delay = int(201 - speed_val)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Algorithm buttons
                if self.bubble_btn.is_clicked(mouse_pos) and not self.sorting:
                    self.algorithm = 'bubble'
                    self.status_label.set_text("Algorithm: Bubble Sort")
                elif self.selection_btn.is_clicked(mouse_pos) and not self.sorting:
                    self.algorithm = 'selection'
                    self.status_label.set_text("Algorithm: Selection Sort")
                elif self.merge_btn.is_clicked(mouse_pos) and not self.sorting:
                    self.algorithm = 'merge'
                    self.status_label.set_text("Algorithm: Merge Sort")
                
                # Control buttons
                elif self.start_btn.is_clicked(mouse_pos):
                    self.start_sorting()
                elif self.pause_btn.is_clicked(mouse_pos):
                    self.pause_sorting()
                elif self.reset_btn.is_clicked(mouse_pos):
                    self.generate_random_array()
                    self.status_label.set_text("Reset")
                
                # Array generation buttons
                elif self.random_btn.is_clicked(mouse_pos) and not self.sorting:
                    self.generate_random_array()
                    self.status_label.set_text("Generated random array")
                elif self.reverse_btn.is_clicked(mouse_pos) and not self.sorting:
                    self.generate_reversed_array()
                    self.status_label.set_text("Generated reversed array")
                elif self.nearly_btn.is_clicked(mouse_pos) and not self.sorting:
                    self.generate_nearly_sorted_array()
                    self.status_label.set_text("Generated nearly sorted array")
                
                # Back button
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
        
        return True
    
    def update(self, dt):
        """Update sorting animation"""
        if self.sorting and not self.paused and self.sort_generator:
            self.timer += dt
            
            if self.timer >= self.animation_delay:
                self.timer = 0
                
                try:
                    # Get next step
                    self.array, state = next(self.sort_generator)
                    self.current_state = state
                    
                    # Update statistics
                    self.comparisons = state.get('comparisons', self.comparisons)
                    self.swaps = state.get('swaps', self.swaps)
                    self.operations = state.get('operations', self.operations)
                    
                    # Check if complete
                    if state.get('phase') == 'complete':
                        self.sorting = False
                        self.status_label.set_text("Sorting complete!")
                
                except StopIteration:
                    self.sorting = False
                    self.status_label.set_text("Sorting complete!")
    
    def draw_array(self):
        """Draw the array as bars"""
        if not self.array:
            return
        
        # Calculate bar dimensions
        array_area_width = 900
        array_area_height = 500
        array_x = 520
        array_y = 250
        
        bar_width = array_area_width // len(self.array)
        max_height = max(self.array) if self.array else 1
        
        for i, value in enumerate(self.array):
            bar_height = int((value / max_height) * array_area_height)
            x = array_x + i * bar_width
            y = array_y + array_area_height - bar_height
            
            # Determine color based on state
            color = DEFAULT_COLOR
            
            if self.current_state:
                phase = self.current_state.get('phase', '')
                
                # Bubble/Selection sort coloring
                if 'comparing_indices' in self.current_state:
                    if i in self.current_state['comparing_indices']:
                        color = COMPARING_COLOR if phase == 'comparing' else SWAPPING_COLOR
                
                # Sorted elements
                if 'sorted_indices' in self.current_state:
                    if i in self.current_state['sorted_indices']:
                        color = SORTED_COLOR
                
                # Merge sort coloring
                if 'active_range' in self.current_state:
                    active = self.current_state['active_range']
                    if len(active) >= 2 and active[0] <= i <= active[1]:
                        color = INFO_COLOR
            
            # Draw bar
            pygame.draw.rect(self.screen, color, (x, y, bar_width - 2, bar_height))
            pygame.draw.rect(self.screen, TEXT_MUTED, (x, y, bar_width - 2, bar_height), 1)
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BG_COLOR)
        
        # Title
        title_font = get_font(TITLE_FONT_SIZE)
        title = title_font.render("Sorting Algorithm Visualizer", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Left panel
        panel = Panel(20, 140, 480, 400, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)
        
        # Highlight selected algorithm
        mouse_pos = pygame.mouse.get_pos()
        
        if self.algorithm == 'bubble':
            self.bubble_btn.color = BUTTON_COLOR
            self.selection_btn.color = SECONDARY_BUTTON_COLOR
            self.merge_btn.color = SECONDARY_BUTTON_COLOR
        elif self.algorithm == 'selection':
            self.bubble_btn.color = SECONDARY_BUTTON_COLOR
            self.selection_btn.color = BUTTON_COLOR
            self.merge_btn.color = SECONDARY_BUTTON_COLOR
        elif self.algorithm == 'merge':
            self.bubble_btn.color = SECONDARY_BUTTON_COLOR
            self.selection_btn.color = SECONDARY_BUTTON_COLOR
            self.merge_btn.color = BUTTON_COLOR
        
        # Draw buttons
        self.bubble_btn.draw(self.screen, mouse_pos)
        self.selection_btn.draw(self.screen, mouse_pos)
        self.merge_btn.draw(self.screen, mouse_pos)
        self.start_btn.draw(self.screen, mouse_pos)
        self.pause_btn.draw(self.screen, mouse_pos)
        self.reset_btn.draw(self.screen, mouse_pos)
        self.random_btn.draw(self.screen, mouse_pos)
        self.reverse_btn.draw(self.screen, mouse_pos)
        self.nearly_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)
        
        # Draw sliders
        self.size_slider.draw(self.screen)
        self.speed_slider.draw(self.screen)
        
        # Status
        self.status_label.draw(self.screen)
        
        # Instructions
        inst_panel = Panel(20, 560, 480, 180, BG_SECONDARY, TEXT_MUTED)
        inst_panel.draw(self.screen)
        
        inst_label = Label(30, 580, "Instructions:", NORMAL_FONT_SIZE, TEXT_COLOR)
        inst_label.draw(self.screen)
        draw_instructions(self.screen, self.instructions, 30, 610)
        
        # Draw array visualization
        self.draw_array()
        
        # Statistics
        stats_panel = Panel(520, 140, 880, 80, BG_SECONDARY, TEXT_MUTED)
        stats_panel.draw(self.screen)
        
        stats_title = Label(540, 160, "Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
        stats_title.draw(self.screen)
        
        stats = {
            "Array Size": len(self.array),
            "Comparisons": self.comparisons,
            "Swaps/Operations": max(self.swaps, self.operations),
            "Status": "Sorting..." if self.sorting else "Ready"
        }
        draw_stats(self.screen, stats, 540, 185)
        
        # Algorithm info
        info = SortingAlgorithms.get_algorithm_info(self.algorithm)
        if info:
            info_panel = Panel(520, 770, 880, 80, BG_SECONDARY, TEXT_MUTED)
            info_panel.draw(self.screen)
            
            info_title = Label(540, 785, f"Algorithm: {info['name']}", NORMAL_FONT_SIZE, TEXT_COLOR)
            info_title.draw(self.screen)
            
            complexity_text = f"Best: {info['best']} | Average: {info['average']} | Worst: {info['worst']}"
            complexity_label = Label(540, 810, complexity_text, SMALL_FONT_SIZE, TEXT_SECONDARY)
            complexity_label.draw(self.screen)
        
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
    pygame.display.set_caption("Sorting Visualizer")
    
    visualizer = SortingVisualizer(screen)
    visualizer.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()