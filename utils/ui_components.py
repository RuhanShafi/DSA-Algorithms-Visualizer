"""
Reusable UI Components for DSA Explorer
Includes buttons, sliders, input boxes, and other common UI elements
"""

import pygame
from config import *


def get_font(size):
    """
    Get a pygame font object of specified size

    Args:
        size (int): Font size in points

    Returns:
        pygame.font.Font: Font object
    """
    if FONT_PATH:
        return pygame.font.Font(FONT_PATH, size)
    return pygame.font.Font(None, size)


class Button:
    """
    Clickable button with hover effects
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        color,
        hover_color,
        text_color=TEXT_COLOR,
        font_size=BUTTON_FONT_SIZE,
        border_radius=8,
    ):
        """
        Initialize a button

        Args:
            x, y: Position of top-left corner
            width, height: Button dimensions
            text: Button text
            color: Normal button color
            hover_color: Color when mouse hovers
            text_color: Text color
            font_size: Size of button text
            border_radius: Rounded corner radius
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = get_font(font_size)
        self.border_radius = border_radius
        self.enabled = True

    def draw(self, surface, mouse_pos):
        """
        Draw the button on the surface

        Args:
            surface: Pygame surface to draw on
            mouse_pos: Current mouse position tuple (x, y)
        """
        # Determine color based on hover state
        current_color = (
            self.hover_color
            if self.is_hovered(mouse_pos) and self.enabled
            else self.color
        )

        if not self.enabled:
            current_color = tuple(
                max(0, c - 50) for c in self.color
            )  # Darken if disabled

        # Draw button rectangle with rounded corners
        pygame.draw.rect(
            surface, current_color, self.rect, border_radius=self.border_radius
        )

        # Draw text centered on button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        """Check if mouse is hovering over button"""
        return self.rect.collidepoint(mouse_pos) if self.enabled else False

    def is_clicked(self, mouse_pos):
        """Check if button was clicked"""
        return self.is_hovered(mouse_pos) if self.enabled else False

    def set_enabled(self, enabled):
        """Enable or disable the button"""
        self.enabled = enabled


class Slider:
    """
    Horizontal slider for adjusting values
    """

    def __init__(self, x, y, width, min_val, max_val, initial_val, label=""):
        """
        Initialize a slider

        Args:
            x, y: Position
            width: Slider width
            min_val: Minimum value
            max_val: Maximum value
            initial_val: Starting value
            label: Optional label text
        """
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.font = get_font(SMALL_FONT_SIZE)
        self.dragging = False

        # Calculate handle position
        self.handle_radius = 12
        self.update_handle_pos()

    def update_handle_pos(self):
        """Update handle position based on current value"""
        percentage = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + int(percentage * self.rect.width)

    def draw(self, surface):
        """Draw the slider"""
        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, TEXT_COLOR)
            surface.blit(label_surface, (self.rect.x, self.rect.y - 25))

        # Draw track
        pygame.draw.rect(surface, BG_TERTIARY, self.rect, border_radius=5)

        # Draw filled portion
        filled_rect = pygame.Rect(
            self.rect.x, self.rect.y, self.handle_x - self.rect.x, self.rect.height
        )
        pygame.draw.rect(surface, BUTTON_COLOR, filled_rect, border_radius=5)

        # Draw handle
        pygame.draw.circle(
            surface,
            BUTTON_HOVER_COLOR,
            (self.handle_x, self.rect.centery),
            self.handle_radius,
        )
        pygame.draw.circle(
            surface,
            TEXT_COLOR,
            (self.handle_x, self.rect.centery),
            self.handle_radius,
            2,
        )

        # Draw value
        value_text = self.font.render(str(int(self.value)), True, TEXT_COLOR)
        value_rect = value_text.get_rect(center=(self.handle_x, self.rect.centery + 25))
        surface.blit(value_text, value_rect)

    def handle_event(self, event, mouse_pos):
        """
        Handle mouse events for slider interaction

        Args:
            event: Pygame event
            mouse_pos: Current mouse position

        Returns:
            bool: True if value changed
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_rect = pygame.Rect(
                self.handle_x - self.handle_radius,
                self.rect.centery - self.handle_radius,
                self.handle_radius * 2,
                self.handle_radius * 2,
            )
            if handle_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
                self.dragging = True
                self.update_value(mouse_pos[0])
                return True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(mouse_pos[0])
            return True

        return False

    def update_value(self, mouse_x):
        """Update slider value based on mouse x position"""
        # Clamp to slider bounds
        mouse_x = max(self.rect.x, min(mouse_x, self.rect.right))

        # Calculate value
        percentage = (mouse_x - self.rect.x) / self.rect.width
        self.value = self.min_val + percentage * (self.max_val - self.min_val)

        # Update handle position
        self.update_handle_pos()

    def get_value(self):
        """Get current slider value"""
        return self.value


class InputBox:
    """
    Text input box for user input
    """

    def __init__(
        self, x, y, width, height, label="", initial_text="", numeric_only=False
    ):
        """
        Initialize an input box

        Args:
            x, y: Position
            width, height: Dimensions
            label: Label text above input
            initial_text: Starting text
            numeric_only: If True, only accept numeric input
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = initial_text
        self.numeric_only = numeric_only
        self.font = get_font(NORMAL_FONT_SIZE)
        self.label_font = get_font(SMALL_FONT_SIZE)
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def draw(self, surface):
        """Draw the input box"""
        # Draw label
        if self.label:
            label_surface = self.label_font.render(self.label, True, TEXT_SECONDARY)
            surface.blit(label_surface, (self.rect.x, self.rect.y - 25))

        # Draw box
        border_color = BUTTON_COLOR if self.active else BG_TERTIARY
        pygame.draw.rect(surface, BG_SECONDARY, self.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=5)

        # Draw text
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surface, text_rect)

        # Draw cursor if active
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            pygame.draw.line(
                surface,
                TEXT_COLOR,
                (cursor_x, self.rect.y + 10),
                (cursor_x, self.rect.bottom - 10),
                2,
            )

    def handle_event(self, event, mouse_pos):
        """
        Handle events for input box

        Args:
            event: Pygame event
            mouse_pos: Mouse position

        Returns:
            bool: True if text changed
        """
        changed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                changed = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                changed = True
            else:
                char = event.unicode
                if self.numeric_only:
                    if char.isdigit() or (char == "-" and len(self.text) == 0):
                        self.text += char
                        changed = True
                else:
                    if char.isprintable():
                        self.text += char
                        changed = True

        return changed

    def update(self, dt):
        """Update cursor blink animation"""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # Blink every 500ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def get_text(self):
        """Get current input text"""
        return self.text

    def get_value(self):
        """Get numeric value if numeric_only is True"""
        if self.numeric_only and self.text:
            try:
                return int(self.text)
            except ValueError:
                return 0
        return self.text

    def set_text(self, text):
        """Set input text"""
        self.text = str(text)


class Label:
    """
    Static text label
    """

    def __init__(
        self, x, y, text, font_size=NORMAL_FONT_SIZE, color=TEXT_COLOR, centered=False
    ):
        """
        Initialize a label

        Args:
            x, y: Position
            text: Label text
            font_size: Text size
            color: Text color
            centered: If True, center text at x position
        """
        self.x = x
        self.y = y
        self.text = text
        self.font = get_font(font_size)
        self.color = color
        self.centered = centered

    def draw(self, surface):
        """Draw the label"""
        text_surface = self.font.render(self.text, True, self.color)
        if self.centered:
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            surface.blit(text_surface, text_rect)
        else:
            surface.blit(text_surface, (self.x, self.y))

    def set_text(self, text):
        """Update label text"""
        self.text = text


class Panel:
    """
    Container panel with background
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        color=BG_SECONDARY,
        border_color=None,
        border_radius=10,
    ):
        """
        Initialize a panel

        Args:
            x, y: Position
            width, height: Dimensions
            color: Background color
            border_color: Optional border color
            border_radius: Rounded corner radius
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_radius = border_radius

    def draw(self, surface):
        """Draw the panel"""
        pygame.draw.rect(
            surface, self.color, self.rect, border_radius=self.border_radius
        )
        if self.border_color:
            pygame.draw.rect(
                surface,
                self.border_color,
                self.rect,
                2,
                border_radius=self.border_radius,
            )


def draw_instructions(surface, instructions, x, y):
    """
    Draw a list of instruction strings

    Args:
        surface: Pygame surface
        instructions: List of instruction strings
        x, y: Starting position
    """
    font = get_font(SMALL_FONT_SIZE)
    for i, instruction in enumerate(instructions):
        text_surface = font.render(instruction, True, TEXT_SECONDARY)
        surface.blit(text_surface, (x, y + i * 20))


def draw_stats(surface, stats_dict, x, y):
    """
    Draw statistics as key-value pairs

    Args:
        surface: Pygame surface
        stats_dict: Dictionary of stat name to value
        x, y: Starting position
    """
    font = get_font(NORMAL_FONT_SIZE)
    offset = 0
    for key, value in stats_dict.items():
        text = f"{key}: {value}"
        text_surface = font.render(text, True, TEXT_COLOR)
        surface.blit(text_surface, (x, y + offset))
        offset += 25
