"""
DSA Explorer - Main Entry Point
Interactive Data Structures and Algorithms Visualizer
"""

import pygame
import sys
from config import *
from utils.ui_components import Button, get_font


class DSAExplorer:
    """Main application class managing the DSA Explorer"""

    def __init__(self):
        """Initialize the DSA Explorer application"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DSA Explorer & Visualizer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "MENU"

    def draw_title(self, text, y_pos):
        """Draw a centered title on screen"""
        title_font = get_font(TITLE_FONT_SIZE)
        title_surface = title_font.render(text, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
        self.screen.blit(title_surface, title_rect)

    def draw_subtitle(self, text, y_pos):
        """Draw a centered subtitle on screen"""
        subtitle_font = get_font(SUBTITLE_FONT_SIZE)
        subtitle_surface = subtitle_font.render(text, True, TEXT_SECONDARY)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
        self.screen.blit(subtitle_surface, subtitle_rect)

    def main_menu(self):
        """Display and handle the main menu"""
        while self.running and self.current_state == "MENU":
            self.screen.fill(BG_COLOR)

            # Draw title and subtitle
            self.draw_title("Assessment 2: DSA Explorer and Visualiser App", 100)
            self.draw_subtitle("By Ruhan Shafi", 150)

            # Create menu buttons
            phase1_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                220,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Phase 1: Data Structures",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )

            phase2_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                300,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Phase 2: Algorithms",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )

            phase3_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                380,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Phase 3: Puzzles",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )

            help_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                460,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Help & Instructions",
                SECONDARY_BUTTON_COLOR,
                SECONDARY_BUTTON_HOVER,
            )

            exit_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                540,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Exit",
                DANGER_COLOR,
                DANGER_HOVER_COLOR,
            )

            # Handle events
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if phase1_btn.is_clicked(mouse_pos):
                        self.current_state = "PHASE1"
                        self.phase1_menu()
                    elif phase2_btn.is_clicked(mouse_pos):
                        self.current_state = "PHASE2"
                        self.phase2_menu()
                    elif phase3_btn.is_clicked(mouse_pos):
                        self.current_state = "PHASE3"
                        self.phase3_menu()
                    elif help_btn.is_clicked(mouse_pos):
                        self.show_help()
                    elif exit_btn.is_clicked(mouse_pos):
                        self.running = False

            # Draw all buttons
            phase1_btn.draw(self.screen, mouse_pos)
            phase2_btn.draw(self.screen, mouse_pos)
            phase3_btn.draw(self.screen, mouse_pos)
            help_btn.draw(self.screen, mouse_pos)
            exit_btn.draw(self.screen, mouse_pos)

            # Draw footer
            footer_font = get_font(SMALL_FONT_SIZE)
            footer_text = footer_font.render(
                "Use mouse to navigate • ESC to go back", True, TEXT_MUTED
            )
            footer_rect = footer_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
            )
            self.screen.blit(footer_text, footer_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    def phase1_menu(self):
        """Phase 1: Data Structures submenu"""
        while self.running and self.current_state == "PHASE1":
            self.screen.fill(BG_COLOR)

            self.draw_title("PHASE 1: Data Structures", 80)
            self.draw_subtitle("Explore foundational data structures", 130)

            # Create submenu buttons
            stack_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                200,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Stack Visualizer",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            queue_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                270,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Queue Visualizer",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            linked_list_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                340,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Linked List Editor",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            bst_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                410,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Binary Search Tree",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            back_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                500,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "← Back to Menu",
                SECONDARY_BUTTON_COLOR,
                SECONDARY_BUTTON_HOVER,
            )

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_state = "MENU"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if stack_btn.is_clicked(mouse_pos):
                        print("Stack visualizer - To be implemented")
                        # from phase1.visualizers.stack_viz import StackVisualizer
                        # StackVisualizer(self.screen).run()
                    elif queue_btn.is_clicked(mouse_pos):
                        print("Queue visualizer - To be implemented")
                    elif linked_list_btn.is_clicked(mouse_pos):
                        print("Linked List editor - To be implemented")
                    elif bst_btn.is_clicked(mouse_pos):
                        print("BST visualizer - To be implemented")
                    elif back_btn.is_clicked(mouse_pos):
                        self.current_state = "MENU"

            stack_btn.draw(self.screen, mouse_pos)
            queue_btn.draw(self.screen, mouse_pos)
            linked_list_btn.draw(self.screen, mouse_pos)
            bst_btn.draw(self.screen, mouse_pos)
            back_btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            self.clock.tick(FPS)

    def phase2_menu(self):
        """Phase 2: Algorithms submenu"""
        while self.running and self.current_state == "PHASE2":
            self.screen.fill(BG_COLOR)

            self.draw_title("PHASE 2: Algorithm Visualizer", 80)
            self.draw_subtitle("Watch algorithms in action", 130)

            sorting_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                200,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Sorting Algorithms",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            graph_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                270,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Graph Traversal (BFS/DFS)",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            heap_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                340,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Heap Operations",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            back_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                430,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "← Back to Menu",
                SECONDARY_BUTTON_COLOR,
                SECONDARY_BUTTON_HOVER,
            )

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_state = "MENU"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sorting_btn.is_clicked(mouse_pos):
                        print("Sorting algorithms - To be implemented")
                    elif graph_btn.is_clicked(mouse_pos):
                        print("Graph traversal - To be implemented")
                    elif heap_btn.is_clicked(mouse_pos):
                        print("Heap operations - To be implemented")
                    elif back_btn.is_clicked(mouse_pos):
                        self.current_state = "MENU"

            sorting_btn.draw(self.screen, mouse_pos)
            graph_btn.draw(self.screen, mouse_pos)
            heap_btn.draw(self.screen, mouse_pos)
            back_btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            self.clock.tick(FPS)

    def phase3_menu(self):
        """Phase 3: Puzzles submenu"""
        while self.running and self.current_state == "PHASE3":
            self.screen.fill(BG_COLOR)

            self.draw_title("PHASE 3: Puzzle Challenges", 80)
            self.draw_subtitle("Apply algorithms to solve puzzles", 130)

            pathfinding_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                200,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Pathfinding Puzzle (A*)",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            event_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                270,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Event Queue Simulator",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            dp_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                340,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Dynamic Programming Puzzle",
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
            )
            back_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                430,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Back to Menu",
                SECONDARY_BUTTON_COLOR,
                SECONDARY_BUTTON_HOVER,
            )

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_state = "MENU"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pathfinding_btn.is_clicked(mouse_pos):
                        print("Pathfinding puzzle - To be implemented")
                    elif event_btn.is_clicked(mouse_pos):
                        print("Event queue - To be implemented")
                    elif dp_btn.is_clicked(mouse_pos):
                        print("DP puzzle - To be implemented")
                    elif back_btn.is_clicked(mouse_pos):
                        self.current_state = "MENU"

            pathfinding_btn.draw(self.screen, mouse_pos)
            event_btn.draw(self.screen, mouse_pos)
            dp_btn.draw(self.screen, mouse_pos)
            back_btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            self.clock.tick(FPS)

    def show_help(self):
        """Display help and instructions screen"""
        showing_help = True
        while showing_help and self.running:
            self.screen.fill(BG_COLOR)

            self.draw_title("Help & Instructions", 60)

            # Help text
            help_font = get_font(NORMAL_FONT_SIZE)
            help_lines = [
                "Welcome to DSA Explorer!",
                "",
                "Phase 1: Explore fundamental data structures like stacks, queues,",
                "         linked lists, and binary search trees.",
                "",
                "Phase 2: Visualize sorting algorithms, graph traversal (BFS/DFS),",
                "         and heap operations.",
                "",
                "Phase 3: Solve puzzles using pathfinding (A*), event queues,",
                "         and dynamic programming.",
                "",
                "Controls:",
                "• Mouse: Click buttons to navigate and interact",
                "• ESC: Return to previous menu",
                "• Each module has specific controls shown on screen",
            ]

            y_offset = 150
            for line in help_lines:
                text_surface = help_font.render(line, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 30

            back_btn = Button(
                WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
                580,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "← Back to Menu",
                SECONDARY_BUTTON_COLOR,
                SECONDARY_BUTTON_HOVER,
            )

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    showing_help = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        showing_help = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.is_clicked(mouse_pos):
                        showing_help = False

            back_btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        """Main application loop"""
        self.main_menu()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = DSAExplorer()
    app.run()
