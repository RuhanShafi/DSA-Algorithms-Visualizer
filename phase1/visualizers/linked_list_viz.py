"""
Linked List Visualizer with PyGame
Interactive visualization of linked list operations with pointer animations
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, draw_instructions, draw_stats, get_font
from phase1.linked_list import LinkedList


class LinkedListVisualizer:
    """
    Interactive linked list visualization
    """
    
    def __init__(self, screen):
        """Initialize linked list visualizer"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Linked list instance
        self.linked_list = LinkedList()
        
        # Animation state
        self.animating = False
        self.animation_progress = 0
        self.animation_speed = 5
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI components"""
        # Input boxes
        self.value_input = InputBox(50, 150, 120, 40, "Value:", numeric_only=True)
        self.position_input = InputBox(50, 200, 120, 40, "Position:", numeric_only=True)
        
        # Buttons - Insert operations
        self.insert_head_btn = Button(190, 150, 130, 40, "Insert Head", SUCCESS_COLOR, "#059669")
        self.insert_tail_btn = Button(330, 150, 130, 40, "Insert Tail", SUCCESS_COLOR, "#059669")
        self.insert_pos_btn = Button(470, 150, 130, 40, "Insert at Pos", INFO_COLOR, BUTTON_HOVER_COLOR)
        
        # Buttons - Delete operations
        self.delete_val_btn = Button(190, 200, 130, 40, "Delete Value", DANGER_COLOR, DANGER_HOVER_COLOR)
        self.delete_pos_btn = Button(330, 200, 130, 40, "Delete at Pos", DANGER_COLOR, DANGER_HOVER_COLOR)
        
        # Buttons - Other operations
        self.reverse_btn = Button(470, 200, 130, 40, "Reverse", WARNING_COLOR, "#d97706")
        self.search_btn = Button(610, 150, 130, 40, "Search", INFO_COLOR, BUTTON_HOVER_COLOR)
        self.clear_btn = Button(610, 200, 130, 40, "Clear All", DANGER_COLOR, DANGER_HOVER_COLOR)
        
        self.back_btn = Button(50, 800, 150, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Status label
        self.status_label = Label(50, 260, "", NORMAL_FONT_SIZE, TEXT_SECONDARY)
        
        # Instructions
        self.instructions = [
            "Insert: Add nodes at head, tail, or position",
            "Delete: Remove by value or position",
            "Reverse: Reverse entire list",
            "Search: Find position of value",
            "Arrows show next pointers"
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
            
            # Handle input boxes
            self.value_input.handle_event(event, mouse_pos)
            self.position_input.handle_event(event, mouse_pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.animating:
                value = self.value_input.get_value()
                position = self.position_input.get_value()
                
                # Insert operations
                if self.insert_head_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        self.linked_list.insert_at_head(value)
                        self.status_label.set_text(f"Inserted {value} at head")
                    else:
                        self.status_label.set_text("Enter a value")
                
                elif self.insert_tail_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        self.linked_list.insert_at_tail(value)
                        self.status_label.set_text(f"Inserted {value} at tail")
                    else:
                        self.status_label.set_text("Enter a value")
                
                elif self.insert_pos_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        try:
                            self.linked_list.insert_at_position(value, position)
                            self.status_label.set_text(f"Inserted {value} at position {position}")
                        except IndexError as e:
                            self.status_label.set_text(str(e))
                    else:
                        self.status_label.set_text("Enter a value")
                
                # Delete operations
                elif self.delete_val_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        if self.linked_list.delete_by_value(value):
                            self.status_label.set_text(f"Deleted {value}")
                        else:
                            self.status_label.set_text(f"Value {value} not found")
                    else:
                        self.status_label.set_text("Enter a value")
                
                elif self.delete_pos_btn.is_clicked(mouse_pos):
                    try:
                        deleted = self.linked_list.delete_at_position(position)
                        self.status_label.set_text(f"Deleted {deleted} from position {position}")
                    except IndexError as e:
                        self.status_label.set_text(str(e))
                
                # Other operations
                elif self.reverse_btn.is_clicked(mouse_pos):
                    self.linked_list.reverse()
                    self.status_label.set_text("List reversed")
                
                elif self.search_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        pos = self.linked_list.search(value)
                        if pos != -1:
                            self.status_label.set_text(f"Found {value} at position {pos}")
                        else:
                            self.status_label.set_text(f"Value {value} not found")
                    else:
                        self.status_label.set_text("Enter a value to search")
                
                elif self.clear_btn.is_clicked(mouse_pos):
                    self.linked_list.clear()
                    self.status_label.set_text("List cleared")
                
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
        
        # Update input boxes
        self.value_input.update(self.clock.get_time())
        self.position_input.update(self.clock.get_time())
        
        return True
    
    def draw_linked_list(self):
        """Draw the linked list with nodes and pointers"""
        nodes = self.linked_list.get_nodes()
        
        if not nodes:
            # Draw empty message
            empty_font = get_font(NORMAL_FONT_SIZE)
            empty_text = empty_font.render("List is empty - insert nodes to begin", True, TEXT_MUTED)
            empty_rect = empty_text.get_rect(center=(WINDOW_WIDTH // 2, 450))
            self.screen.blit(empty_text, empty_rect)
            return
        
        # Calculate layout
        node_width = 80
        node_height = 60
        arrow_width = 50
        start_x = 100
        start_y = 400
        
        # Wrap to multiple rows if needed
        max_per_row = 10
        
        # Draw HEAD label
        head_font = get_font(SMALL_FONT_SIZE)
        head_text = head_font.render("HEAD →", True, SUCCESS_COLOR)
        self.screen.blit(head_text, (start_x - 80, start_y + 15))
        
        for i, node in enumerate(nodes):
            row = i // max_per_row
            col = i % max_per_row
            
            x = start_x + col * (node_width + arrow_width)
            y = start_y + row * 120
            
            # Draw node box
            node_rect = pygame.Rect(x, y, node_width, node_height)
            pygame.draw.rect(self.screen, LINKED_LIST_COLOR, node_rect, border_radius=5)
            pygame.draw.rect(self.screen, (10, 120, 200), node_rect, 3, border_radius=5)
            
            # Draw data
            data_font = get_font(NORMAL_FONT_SIZE)
            data_text = data_font.render(str(node.data), True, TEXT_COLOR)
            data_rect = data_text.get_rect(center=(x + node_width // 2, y + node_height // 2))
            self.screen.blit(data_text, data_rect)
            
            # Draw position number
            pos_font = get_font(SMALL_FONT_SIZE)
            pos_text = pos_font.render(f"[{i}]", True, TEXT_MUTED)
            pos_rect = pos_text.get_rect(center=(x + node_width // 2, y - 15))
            self.screen.blit(pos_text, pos_rect)
            
            # Draw arrow to next node (if not last and not wrapping)
            if i < len(nodes) - 1:
                next_row = (i + 1) // max_per_row
                
                if row == next_row:
                    # Horizontal arrow
                    arrow_start = (x + node_width, y + node_height // 2)
                    arrow_end = (x + node_width + arrow_width, y + node_height // 2)
                    
                    # Draw line
                    pygame.draw.line(self.screen, TEXT_COLOR, arrow_start, arrow_end, 3)
                    
                    # Draw arrowhead
                    arrow_points = [
                        arrow_end,
                        (arrow_end[0] - 10, arrow_end[1] - 6),
                        (arrow_end[0] - 10, arrow_end[1] + 6)
                    ]
                    pygame.draw.polygon(self.screen, TEXT_COLOR, arrow_points)
                else:
                    # Vertical arrow (wrapping to next row)
                    arrow_start = (x + node_width // 2, y + node_height)
                    arrow_end = (x + node_width // 2, y + node_height + 60)
                    
                    pygame.draw.line(self.screen, TEXT_COLOR, arrow_start, arrow_end, 3)
                    
                    arrow_points = [
                        arrow_end,
                        (arrow_end[0] - 6, arrow_end[1] - 10),
                        (arrow_end[0] + 6, arrow_end[1] - 10)
                    ]
                    pygame.draw.polygon(self.screen, TEXT_COLOR, arrow_points)
            else:
                # Last node - draw NULL
                null_x = x + node_width + 15
                null_font = get_font(SMALL_FONT_SIZE)
                null_text = null_font.render("NULL", True, DANGER_COLOR)
                null_rect = null_text.get_rect(midleft=(null_x, y + node_height // 2))
                self.screen.blit(null_text, null_rect)
    
    def draw(self):
        """Draw all elements"""
        self.screen.fill(BG_COLOR)
        
        # Draw title
        title_font = get_font(TITLE_FONT_SIZE)
        title = title_font.render("Linked List Visualizer", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw UI panel
        panel = Panel(30, 130, 730, 160, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)
        
        # Draw UI elements
        mouse_pos = pygame.mouse.get_pos()
        self.value_input.draw(self.screen)
        self.position_input.draw(self.screen)
        self.insert_head_btn.draw(self.screen, mouse_pos)
        self.insert_tail_btn.draw(self.screen, mouse_pos)
        self.insert_pos_btn.draw(self.screen, mouse_pos)
        self.delete_val_btn.draw(self.screen, mouse_pos)
        self.delete_pos_btn.draw(self.screen, mouse_pos)
        self.reverse_btn.draw(self.screen, mouse_pos)
        self.search_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)
        
        # Draw status
        self.status_label.draw(self.screen)
        
        # Draw instructions panel
        inst_panel = Panel(30, 310, 760, 180, BG_SECONDARY, TEXT_MUTED)
        inst_panel.draw(self.screen)
        
        inst_title = Label(50, 330, "Instructions:", NORMAL_FONT_SIZE, TEXT_COLOR)
        inst_title.draw(self.screen)
        draw_instructions(self.screen, self.instructions, 50, 360)
        
        # Draw stats panel
        stats_panel = Panel(30, 710, 760, 120, BG_SECONDARY, TEXT_MUTED)
        stats_panel.draw(self.screen)
        
        stats_title = Label(50, 730, "List Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
        stats_title.draw(self.screen)
        
        stats = {
            "Size": self.linked_list.size(),
            "Empty": "Yes" if self.linked_list.is_empty() else "No",
            "Data": str(self.linked_list.get_all_data()[:8]) + ("..." if self.linked_list.size() > 8 else "")
        }
        draw_stats(self.screen, stats, 50, 760)
        
        # Draw the linked list visualization
        self.draw_linked_list()
        
        pygame.display.flip()
    
    def run(self):
        """Main visualization loop"""
        while self.running:
            if not self.handle_events():
                break
            
            self.draw()
            self.clock.tick(FPS)
        
        return True


def main():
    """Standalone test function"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Linked List Visualizer")
    
    visualizer = LinkedListVisualizer(screen)
    visualizer.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()