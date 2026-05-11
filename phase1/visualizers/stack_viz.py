"""
Stack Visualizer with PyGame
Interactive visualization of stack operations
"""

import pygame
import sys

sys.path.append("../..")

from config import *
from utils.ui_components import (
    Button,
    InputBox,
    Label,
    Panel,
    draw_instructions,
    draw_stats,
    get_font,
)
from phase1.stack import Stack


class StackVisualizer:
    """
    Interactive stack visualization
    """

    def __init__(self, screen):
        """
        Initialize stack visualizer

        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Stack instance
        self.stack = Stack(MAX_STACK_SIZE)

        # Animation state
        self.animating = False
        self.animation_type = None  # 'push' or 'pop'
        self.animation_progress = 0
        self.animation_speed = 10
        self.animating_value = None

        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components"""
        # Input box for value
        self.input_box = InputBox(50, 150, 150, 40, "Enter value:", numeric_only=True)

        # Buttons
        self.push_btn = Button(220, 150, 120, 40, "Push", SUCCESS_COLOR, "#059669")
        self.pop_btn = Button(
            360, 150, 120, 40, "Pop", DANGER_COLOR, DANGER_HOVER_COLOR
        )
        self.peek_btn = Button(
            500, 150, 120, 40, "Peek", INFO_COLOR, BUTTON_HOVER_COLOR
        )
        self.clear_btn = Button(640, 150, 120, 40, "Clear", WARNING_COLOR, "#d97706")
        self.back_btn = Button(
            50, 800, 150, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER
        )

        # Labels
        self.status_label = Label(50, 220, "", NORMAL_FONT_SIZE, TEXT_SECONDARY)

        # Instructions
        self.instructions = [
            "Push: Add element to top of stack",
            "Pop: Remove and return top element",
            "Peek: View top element without removing",
            "Clear: Empty the entire stack",
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
                # Push button
                if self.push_btn.is_clicked(mouse_pos):
                    value = self.input_box.get_value()
                    if value != 0 or self.input_box.get_text() == "0":
                        try:
                            self.stack.push(value)
                            self.start_animation("push", value)
                            self.status_label.set_text(f"Pushed: {value}")
                            self.input_box.set_text("")
                        except OverflowError as e:
                            self.status_label.set_text(str(e))
                    else:
                        self.status_label.set_text("Please enter a value")

                # Pop button
                elif self.pop_btn.is_clicked(mouse_pos):
                    try:
                        value = self.stack.pop()
                        self.start_animation("pop", value)
                        self.status_label.set_text(f"Popped: {value}")
                    except IndexError as e:
                        self.status_label.set_text(str(e))

                # Peek button
                elif self.peek_btn.is_clicked(mouse_pos):
                    try:
                        value = self.stack.peek()
                        self.status_label.set_text(f"Top element: {value}")
                    except IndexError as e:
                        self.status_label.set_text(str(e))

                # Clear button
                elif self.clear_btn.is_clicked(mouse_pos):
                    self.stack.clear()
                    self.status_label.set_text("Stack cleared")

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

    def draw_stack(self):
        """Draw the stack visualization"""
        # Stack container position
        stack_x = 900
        stack_y = 650
        box_width = 200
        box_height = 50

        # Draw stack title
        title_font = get_font(HEADING_FONT_SIZE)
        title = title_font.render("STACK", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(stack_x + box_width // 2, 280))
        self.screen.blit(title, title_rect)

        # Draw "TOP" indicator
        top_font = get_font(SMALL_FONT_SIZE)
        top_text = top_font.render("← TOP", True, WARNING_COLOR)
        self.screen.blit(
            top_text, (stack_x + box_width + 20, stack_y - box_height // 2 - 10)
        )

        # Draw stack elements from bottom to top
        items = self.stack.get_items()

        for i, item in enumerate(items):
            y_pos = stack_y - (i * box_height)

            # Determine color based on position
            if i == len(items) - 1:  # Top element
                color = STACK_COLOR
                border_color = (100, 60, 200)
            else:
                color = BG_TERTIARY
                border_color = TEXT_MUTED

            # Draw box
            rect = pygame.Rect(stack_x, y_pos - box_height, box_width, box_height)
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)

            # Draw value
            value_font = get_font(NORMAL_FONT_SIZE)
            value_text = value_font.render(str(item), True, TEXT_COLOR)
            value_rect = value_text.get_rect(center=rect.center)
            self.screen.blit(value_text, value_rect)

        # Draw animation
        if self.animating and self.animating_value is not None:
            if self.animation_type == "push":
                # Animate element dropping in from top
                progress_ratio = self.animation_progress / 100
                start_y = 200
                end_y = stack_y - ((len(items) - 1) * box_height) - box_height
                current_y = start_y + (end_y - start_y) * progress_ratio

                rect = pygame.Rect(stack_x, current_y, box_width, box_height)
                pygame.draw.rect(self.screen, SUCCESS_COLOR, rect, border_radius=5)
                pygame.draw.rect(self.screen, "#059669", rect, 3, border_radius=5)

                value_font = get_font(NORMAL_FONT_SIZE)
                value_text = value_font.render(
                    str(self.animating_value), True, TEXT_COLOR
                )
                value_rect = value_text.get_rect(center=rect.center)
                self.screen.blit(value_text, value_rect)

            elif self.animation_type == "pop":
                # Animate element rising out
                progress_ratio = self.animation_progress / 100
                start_y = stack_y - (len(items) * box_height) - box_height
                end_y = 100
                current_y = start_y + (end_y - start_y) * progress_ratio

                alpha = int(255 * (1 - progress_ratio))
                color_with_alpha = (*DANGER_COLOR, alpha)

                rect = pygame.Rect(stack_x, current_y, box_width, box_height)
                pygame.draw.rect(self.screen, DANGER_COLOR, rect, border_radius=5)
                pygame.draw.rect(
                    self.screen, DANGER_HOVER_COLOR, rect, 3, border_radius=5
                )

                value_font = get_font(NORMAL_FONT_SIZE)
                value_text = value_font.render(
                    str(self.animating_value), True, TEXT_COLOR
                )
                value_rect = value_text.get_rect(center=rect.center)
                self.screen.blit(value_text, value_rect)

        # Draw empty slots
        for i in range(len(items), MAX_STACK_SIZE):
            y_pos = stack_y - (i * box_height)
            rect = pygame.Rect(stack_x, y_pos - box_height, box_width, box_height)
            pygame.draw.rect(self.screen, BG_SECONDARY, rect, border_radius=5)
            pygame.draw.rect(self.screen, TEXT_MUTED, rect, 1, border_radius=5)

        # Draw base line
        pygame.draw.line(
            self.screen,
            TEXT_COLOR,
            (stack_x - 20, stack_y + 10),
            (stack_x + box_width + 20, stack_y + 10),
            3,
        )

    def draw(self):
        """Draw all elements"""
        self.screen.fill(BG_COLOR)

        # Draw title
        title_font = get_font(TITLE_FONT_SIZE)
        title = title_font.render("Stack Visualizer", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)

        # Draw UI panel
        panel = Panel(30, 130, 760, 120, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)

        # Draw UI elements
        mouse_pos = pygame.mouse.get_pos()
        self.input_box.draw(self.screen)
        self.push_btn.draw(self.screen, mouse_pos)
        self.pop_btn.draw(self.screen, mouse_pos)
        self.peek_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)

        # Draw status
        self.status_label.draw(self.screen)

        # Draw instructions panel
        inst_panel = Panel(30, 280, 760, 180, BG_SECONDARY, TEXT_MUTED)
        inst_panel.draw(self.screen)

        inst_title = Label(50, 300, "Instructions:", NORMAL_FONT_SIZE, TEXT_COLOR)
        inst_title.draw(self.screen)
        draw_instructions(self.screen, self.instructions, 50, 330)

        # Draw stats panel
        stats_panel = Panel(30, 480, 760, 120, BG_SECONDARY, TEXT_MUTED)
        stats_panel.draw(self.screen)

        stats_title = Label(50, 500, "Stack Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
        stats_title.draw(self.screen)

        stats = {
            "Size": f"{self.stack.size()} / {MAX_STACK_SIZE}",
            "Empty": "Yes" if self.stack.is_empty() else "No",
            "Full": "Yes" if self.stack.is_full() else "No",
        }
        draw_stats(self.screen, stats, 50, 530)

        # Draw the stack visualization
        self.draw_stack()

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
    pygame.display.set_caption("Stack Visualizer")

    visualizer = StackVisualizer(screen)
    visualizer.run()

    pygame.quit()


if __name__ == "__main__":
    main()
