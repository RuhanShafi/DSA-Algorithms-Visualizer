"""
Heap Visualizer with PyGame
Interactive visualization of min/max heap operations
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, draw_instructions, draw_stats, get_font
from phase2.heap import MinHeap, MaxHeap


class HeapVisualizer:
    """
    Interactive heap visualization
    """
    
    def __init__(self, screen):
        """Initialize heap visualizer"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Heap instances
        self.heap_type = 'min'  # 'min' or 'max'
        self.heap = MinHeap(max_size=15)
        
        # Animation state
        self.animating = False
        self.animation_generator = None
        self.current_state = None
        self.animation_delay = 500  # ms
        self.timer = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI components"""
        # Input box
        self.value_input = InputBox(50, 150, 150, 40, "Value:", numeric_only=True)
        
        # Buttons
        self.insert_btn = Button(220, 150, 120, 40, "Insert", SUCCESS_COLOR, "#059669")
        self.extract_btn = Button(350, 150, 120, 40, "Extract", DANGER_COLOR, DANGER_HOVER_COLOR)
        self.peek_btn = Button(480, 150, 120, 40, "Peek", INFO_COLOR, BUTTON_HOVER_COLOR)
        self.clear_btn = Button(610, 150, 120, 40, "Clear", WARNING_COLOR, "#d97706")
        
        # Heap type buttons
        self.min_heap_btn = Button(50, 210, 120, 40, "Min-Heap", BUTTON_COLOR, BUTTON_HOVER_COLOR)
        self.max_heap_btn = Button(180, 210, 120, 40, "Max-Heap", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        self.back_btn = Button(50, 800, 150, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Status label
        self.status_label = Label(50, 270, "", NORMAL_FONT_SIZE, TEXT_SECONDARY)
        
        # Instructions
        self.instructions = [
            "Insert: Add element (bubbles up)",
            "Extract: Remove root (bubbles down)",
            "Peek: View root element",
            "Min-Heap: Parent ≤ Children",
            "Max-Heap: Parent ≥ Children"
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
            
            # Handle input box
            self.value_input.handle_event(event, mouse_pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.animating:
                value = self.value_input.get_value()
                
                # Operations
                if self.insert_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        try:
                            self.animation_generator = self.heap.insert(value)
                            self.animating = True
                            self.value_input.set_text("")
                        except OverflowError as e:
                            self.status_label.set_text(str(e))
                    else:
                        self.status_label.set_text("Enter a value")
                
                elif self.extract_btn.is_clicked(mouse_pos):
                    try:
                        if self.heap_type == 'min':
                            self.animation_generator = self.heap.extract_min()
                        else:
                            self.animation_generator = self.heap.extract_max()
                        self.animating = True
                    except IndexError as e:
                        self.status_label.set_text(str(e))
                
                elif self.peek_btn.is_clicked(mouse_pos):
                    value = self.heap.peek()
                    if value is not None:
                        self.status_label.set_text(f"Root: {value}")
                    else:
                        self.status_label.set_text("Heap is empty")
                
                elif self.clear_btn.is_clicked(mouse_pos):
                    self.heap.clear()
                    self.status_label.set_text("Heap cleared")
                
                # Heap type selection
                elif self.min_heap_btn.is_clicked(mouse_pos):
                    if not self.heap.is_empty():
                        self.status_label.set_text("Clear heap first to switch type")
                    else:
                        self.heap_type = 'min'
                        self.heap = MinHeap(max_size=15)
                        self.status_label.set_text("Switched to Min-Heap")
                
                elif self.max_heap_btn.is_clicked(mouse_pos):
                    if not self.heap.is_empty():
                        self.status_label.set_text("Clear heap first to switch type")
                    else:
                        self.heap_type = 'max'
                        self.heap = MaxHeap(max_size=15)
                        self.status_label.set_text("Switched to Max-Heap")
                
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
        
        # Update input box
        self.value_input.update(self.clock.get_time())
        
        return True
    
    def update(self, dt):
        """Update animation"""
        if self.animating and self.animation_generator:
            self.timer += dt
            
            if self.timer >= self.animation_delay:
                self.timer = 0
                
                try:
                    result = next(self.animation_generator)
                    
                    # Handle both insert and extract return formats
                    if len(result) == 2:
                        arr, state = result
                        extracted = None
                    else:
                        arr, state, extracted = result
                    
                    self.current_state = state
                    
                    if state['phase'] == 'complete':
                        self.animating = False
                        if extracted is not None:
                            self.status_label.set_text(f"Extracted: {extracted}")
                        else:
                            self.status_label.set_text("Operation complete")
                
                except StopIteration:
                    self.animating = False
    
    def calculate_tree_position(self, index, level, pos_in_level):
        """Calculate position for heap element in tree layout"""
        start_x = 700
        start_y = 350
        level_spacing = 80
        
        # Calculate horizontal spacing based on level
        max_at_level = 2 ** level
        total_width = 600
        spacing = total_width / (max_at_level + 1)
        
        x = start_x - total_width // 2 + spacing * (pos_in_level + 1)
        y = start_y + level * level_spacing
        
        return int(x), int(y)
    
    def draw_heap_tree(self):
        """Draw heap as a tree structure"""
        if self.heap.is_empty():
            empty_font = get_font(NORMAL_FONT_SIZE)
            empty_text = empty_font.render("Heap is empty", True, TEXT_MUTED)
            empty_rect = empty_text.get_rect(center=(WINDOW_WIDTH // 2, 450))
            self.screen.blit(empty_text, empty_rect)
            return
        
        heap_array = self.heap.get_array()
        size = self.heap.get_size()
        
        # Calculate positions for all nodes
        positions = {}
        for i in range(size):
            level = int(__import__('math').log2(i + 1))
            pos_in_level = i - (2 ** level - 1)
            positions[i] = self.calculate_tree_position(i, level, pos_in_level)
        
        # Draw edges first
        for i in range(size):
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            if left_child < size:
                pygame.draw.line(self.screen, TEXT_MUTED, 
                               positions[i], positions[left_child], 2)
            if right_child < size:
                pygame.draw.line(self.screen, TEXT_MUTED,
                               positions[i], positions[right_child], 2)
        
        # Draw nodes
        for i in range(size):
            x, y = positions[i]
            
            # Determine color based on state
            color = HEAP_COLOR
            if self.current_state and 'comparing_indices' in self.current_state:
                if i in self.current_state['comparing_indices']:
                    color = COMPARING_COLOR
            
            # Draw circle
            radius = 25
            pygame.draw.circle(self.screen, color, (x, y), radius)
            pygame.draw.circle(self.screen, TEXT_COLOR, (x, y), radius, 2)
            
            # Draw value
            value_font = get_font(NORMAL_FONT_SIZE)
            value_text = value_font.render(str(heap_array[i]), True, TEXT_COLOR)
            value_rect = value_text.get_rect(center=(x, y))
            self.screen.blit(value_text, value_rect)
    
    def draw_heap_array(self):
        """Draw heap as array representation"""
        if self.heap.is_empty():
            return
        
        heap_array = self.heap.get_array()
        size = self.heap.get_size()
        
        # Draw array
        box_width = 50
        box_height = 50
        start_x = 250
        start_y = 750
        
        # Title
        array_font = get_font(SMALL_FONT_SIZE)
        array_text = array_font.render("Array Representation:", True, TEXT_COLOR)
        self.screen.blit(array_text, (start_x, start_y - 30))
        
        for i in range(min(size, 15)):  # Show up to 15 elements
            x = start_x + i * (box_width + 5)
            
            # Draw box
            rect = pygame.Rect(x, start_y, box_width, box_height)
            pygame.draw.rect(self.screen, BG_TERTIARY, rect, border_radius=3)
            pygame.draw.rect(self.screen, TEXT_MUTED, rect, 2, border_radius=3)
            
            # Draw value
            val_font = get_font(SMALL_FONT_SIZE)
            val_text = val_font.render(str(heap_array[i]), True, TEXT_COLOR)
            val_rect = val_text.get_rect(center=rect.center)
            self.screen.blit(val_text, val_rect)
            
            # Draw index
            idx_text = val_font.render(f"[{i}]", True, TEXT_MUTED)
            idx_rect = idx_text.get_rect(center=(x + box_width // 2, start_y - 15))
            self.screen.blit(idx_text, idx_rect)
    
    def draw(self):
        """Draw all elements"""
        self.screen.fill(BG_COLOR)
        
        # Draw title
        title_font = get_font(TITLE_FONT_SIZE)
        heap_name = "Min-Heap" if self.heap_type == 'min' else "Max-Heap"
        title = title_font.render(f"{heap_name} Visualizer", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw UI panel
        panel = Panel(30, 130, 720, 160, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)
        
        # Draw UI elements
        mouse_pos = pygame.mouse.get_pos()
        self.value_input.draw(self.screen)
        self.insert_btn.draw(self.screen, mouse_pos)
        self.extract_btn.draw(self.screen, mouse_pos)
        self.peek_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)
        
        # Highlight selected heap type
        if self.heap_type == 'min':
            self.min_heap_btn.color = BUTTON_COLOR
            self.max_heap_btn.color = SECONDARY_BUTTON_COLOR
        else:
            self.min_heap_btn.color = SECONDARY_BUTTON_COLOR
            self.max_heap_btn.color = BUTTON_COLOR
        
        self.min_heap_btn.draw(self.screen, mouse_pos)
        self.max_heap_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)
        
        # Draw status
        self.status_label.draw(self.screen)
        
        # Draw instructions panel
        inst_panel = Panel(790, 130, 580, 180, BG_SECONDARY, TEXT_MUTED)
        inst_panel.draw(self.screen)
        
        inst_title = Label(810, 150, "Instructions:", NORMAL_FONT_SIZE, TEXT_COLOR)
        inst_title.draw(self.screen)
        draw_instructions(self.screen, self.instructions, 810, 180)
        
        # Draw stats panel
        stats_panel = Panel(790, 330, 580, 120, BG_SECONDARY, TEXT_MUTED)
        stats_panel.draw(self.screen)
        
        stats_title = Label(810, 350, "Heap Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
        stats_title.draw(self.screen)
        
        stats = {
            "Type": heap_name,
            "Size": f"{self.heap.get_size()} / {self.heap.max_size}",
            "Empty": "Yes" if self.heap.is_empty() else "No",
            "Root": str(self.heap.peek()) if not self.heap.is_empty() else "N/A"
        }
        draw_stats(self.screen, stats, 810, 380)
        
        # Draw visualizations
        self.draw_heap_tree()
        self.draw_heap_array()
        
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
    pygame.display.set_caption("Heap Visualizer")
    
    visualizer = HeapVisualizer(screen)
    visualizer.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()