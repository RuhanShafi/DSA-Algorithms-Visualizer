"""
Queue Visualizer with PyGame
Interactive visualization of queue operations (FIFO)
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, draw_instructions, draw_stats, get_font
from phase1.queue import Queue


class QueueVisualizer:
    """
    Interactive queue visualization
    """
    
    def __init__(self, screen):
        """Initialize queue visualizer"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Queue instance
        self.queue = Queue(MAX_QUEUE_SIZE)
        
        # Animation state
        self.animating = False
        self.animation_type = None  # 'enqueue' or 'dequeue'
        self.animation_progress = 0
        self.animation_speed = 10
        self.animating_value = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI components"""
        # Input box
        self.input_box = InputBox(50, 150, 150, 40, "Enter value:", numeric_only=True)
        
        # Buttons
        self.enqueue_btn = Button(220, 150, 140, 40, "Enqueue", SUCCESS_COLOR, "#059669")
        self.dequeue_btn = Button(370, 150, 140, 40, "Dequeue", DANGER_COLOR, DANGER_HOVER_COLOR)
        self.peek_btn = Button(520, 150, 140, 40, "Peek", INFO_COLOR, BUTTON_HOVER_COLOR)
        self.clear_btn = Button(670, 150, 140, 40, "Clear", WARNING_COLOR, "#d97706")
        self.back_btn = Button(50, 800, 150, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Status label
        self.status_label = Label(50, 220, "", NORMAL_FONT_SIZE, TEXT_SECONDARY)
        
        # Instructions
        self.instructions = [
            "Enqueue: Add element to rear",
            "Dequeue: Remove element from front",
            "Peek: View front element",
            "Clear: Empty the entire queue",
            "FIFO: First In, First Out"
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
            if self.input_box.handle_event(event, mouse_pos):
                pass
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.animating:
                # Enqueue button
                if self.enqueue_btn.is_clicked(mouse_pos):
                    value = self.input_box.get_value()
                    if value != 0 or self.input_box.get_text() == "0":
                        try:
                            self.queue.enqueue(value)
                            self.start_animation('enqueue', value)
                            self.status_label.set_text(f"Enqueued: {value}")
                            self.input_box.set_text("")
                        except OverflowError as e:
                            self.status_label.set_text(str(e))
                    else:
                        self.status_label.set_text("Please enter a value")
                
                # Dequeue button
                elif self.dequeue_btn.is_clicked(mouse_pos):
                    try:
                        value = self.queue.dequeue()
                        self.start_animation('dequeue', value)
                        self.status_label.set_text(f"Dequeued: {value}")
                    except IndexError as e:
                        self.status_label.set_text(str(e))
                
                # Peek button
                elif self.peek_btn.is_clicked(mouse_pos):
                    try:
                        value = self.queue.peek()
                        self.status_label.set_text(f"Front element: {value}")
                    except IndexError as e:
                        self.status_label.set_text(str(e))
                
                # Clear button
                elif self.clear_btn.is_clicked(mouse_pos):
                    self.queue.clear()
                    self.status_label.set_text("Queue cleared")
                
                # Back button
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
        
        # Update input box cursor
        self.input_box.update(self.clock.get_time())
        
        return True
    
    def start_animation(self, anim_type, value):
        """Start an animation"""
        self.animating = True
        self.animation_type = anim_type
        self.animation_progress = 0
        self.animating_value = value
    
    def update_animation(self):
        """Update animation state"""
        if self.animating:
            self.animation_progress += self.animation_speed
            if self.animation_progress >= 100:
                self.animating = False
                self.animation_progress = 0
    
    def draw_queue(self):
        """Draw the queue visualization"""
        # Queue container position
        queue_x = 200
        queue_y = 450
        box_width = 100
        box_height = 80
        
        # Draw queue title
        title_font = get_font(HEADING_FONT_SIZE)
        title = title_font.render("QUEUE (FIFO)", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 280))
        self.screen.blit(title, title_rect)
        
        # Draw "FRONT" and "REAR" indicators
        front_font = get_font(SMALL_FONT_SIZE)
        front_text = front_font.render("← FRONT", True, SUCCESS_COLOR)
        self.screen.blit(front_text, (queue_x - 100, queue_y + 20))
        
        rear_text = front_font.render("REAR →", True, DANGER_COLOR)
        items = self.queue.get_items()
        rear_x = queue_x + len(items) * (box_width + 10) + 20
        self.screen.blit(rear_text, (rear_x, queue_y + 20))
        
        # Draw queue elements
        items = self.queue.get_items()
        
        for i, item in enumerate(items):
            x_pos = queue_x + i * (box_width + 10)
            
            # Determine color
            if i == 0:  # Front element
                color = QUEUE_COLOR
                border_color = (200, 50, 120)
            else:
                color = BG_TERTIARY
                border_color = TEXT_MUTED
            
            # Draw box
            rect = pygame.Rect(x_pos, queue_y, box_width, box_height)
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)
            
            # Draw value
            value_font = get_font(NORMAL_FONT_SIZE)
            value_text = value_font.render(str(item), True, TEXT_COLOR)
            value_rect = value_text.get_rect(center=rect.center)
            self.screen.blit(value_text, value_rect)
            
            # Draw index
            index_font = get_font(SMALL_FONT_SIZE)
            index_text = index_font.render(f"[{i}]", True, TEXT_MUTED)
            index_rect = index_text.get_rect(center=(x_pos + box_width // 2, queue_y - 20))
            self.screen.blit(index_text, index_rect)
        
        # Draw animation
        if self.animating and self.animating_value is not None:
            if self.animation_type == 'enqueue':
                # Animate element entering from right
                progress_ratio = self.animation_progress / 100
                start_x = queue_x + len(items) * (box_width + 10) + 200
                end_x = queue_x + (len(items) - 1) * (box_width + 10)
                current_x = start_x + (end_x - start_x) * progress_ratio
                
                rect = pygame.Rect(current_x, queue_y, box_width, box_height)
                pygame.draw.rect(self.screen, SUCCESS_COLOR, rect, border_radius=5)
                pygame.draw.rect(self.screen, "#059669", rect, 3, border_radius=5)
                
                value_font = get_font(NORMAL_FONT_SIZE)
                value_text = value_font.render(str(self.animating_value), True, TEXT_COLOR)
                value_rect = value_text.get_rect(center=rect.center)
                self.screen.blit(value_text, value_rect)
            
            elif self.animation_type == 'dequeue':
                # Animate element exiting from left
                progress_ratio = self.animation_progress / 100
                start_x = queue_x
                end_x = queue_x - 300
                current_x = start_x + (end_x - start_x) * progress_ratio
                
                rect = pygame.Rect(current_x, queue_y, box_width, box_height)
                pygame.draw.rect(self.screen, DANGER_COLOR, rect, border_radius=5)
                pygame.draw.rect(self.screen, DANGER_HOVER_COLOR, rect, 3, border_radius=5)
                
                value_font = get_font(NORMAL_FONT_SIZE)
                value_text = value_font.render(str(self.animating_value), True, TEXT_COLOR)
                value_rect = value_text.get_rect(center=rect.center)
                self.screen.blit(value_text, value_rect)
        
        # Draw empty slots
        for i in range(len(items), MAX_QUEUE_SIZE):
            x_pos = queue_x + i * (box_width + 10)
            rect = pygame.Rect(x_pos, queue_y, box_width, box_height)
            pygame.draw.rect(self.screen, BG_SECONDARY, rect, border_radius=5)
            pygame.draw.rect(self.screen, TEXT_MUTED, rect, 1, border_radius=5)
    
    def draw(self):
        """Draw all elements"""
        self.screen.fill(BG_COLOR)
        
        # Draw title
        title_font = get_font(TITLE_FONT_SIZE)
        title = title_font.render("Queue Visualizer", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw UI panel
        panel = Panel(30, 130, 800, 120, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)
        
        # Draw UI elements
        mouse_pos = pygame.mouse.get_pos()
        self.input_box.draw(self.screen)
        self.enqueue_btn.draw(self.screen, mouse_pos)
        self.dequeue_btn.draw(self.screen, mouse_pos)
        self.peek_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)
        
        # Draw status
        self.status_label.draw(self.screen)
        
        # Draw instructions panel
        inst_panel = Panel(30, 570, 760, 180, BG_SECONDARY, TEXT_MUTED)
        inst_panel.draw(self.screen)
        
        inst_title = Label(50, 590, "Instructions:", NORMAL_FONT_SIZE, TEXT_COLOR)
        inst_title.draw(self.screen)
        draw_instructions(self.screen, self.instructions, 50, 620)
        
        # Draw stats panel
        stats_panel = Panel(30, 770, 760, 120, BG_SECONDARY, TEXT_MUTED)
        stats_panel.draw(self.screen)
        
        stats_title = Label(50, 790, "Queue Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
        stats_title.draw(self.screen)
        
        stats = {
            "Size": f"{self.queue.size()} / {MAX_QUEUE_SIZE}",
            "Empty": "Yes" if self.queue.is_empty() else "No",
            "Full": "Yes" if self.queue.is_full() else "No"
        }
        draw_stats(self.screen, stats, 50, 820)
        
        # Draw the queue visualization
        self.draw_queue()
        
        pygame.display.flip()
    
    def run(self):
        """Main visualization loop"""
        while self.running:
            if not self.handle_events():
                break
            
            self.update_animation()
            self.draw()
            self.clock.tick(FPS)
        
        return True


def main():
    """Standalone test function"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Queue Visualizer")
    
    visualizer = QueueVisualizer(screen)
    visualizer.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()