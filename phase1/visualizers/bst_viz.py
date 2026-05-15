"""
Binary Search Tree Visualizer with PyGame
Interactive visualization of BST operations with tree layout
"""

import pygame
import sys
import os
import math

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, draw_instructions, draw_stats, get_font
from phase1.bst import BinarySearchTree


class BSTVisualizer:
    """
    Interactive binary search tree visualization
    """
    
    def __init__(self, screen):
        """Initialize BST visualizer"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # BST instance
        self.bst = BinarySearchTree()
        
        # Traversal state
        self.traversal_mode = None  # 'inorder', 'preorder', 'postorder'
        self.traversal_result = []
        self.highlighted_nodes = set()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI components"""
        # Input box
        self.value_input = InputBox(50, 150, 150, 40, "Value:", numeric_only=True)
        
        # Buttons - Operations
        self.insert_btn = Button(220, 150, 120, 40, "Insert", SUCCESS_COLOR, "#059669")
        self.delete_btn = Button(350, 150, 120, 40, "Delete", DANGER_COLOR, DANGER_HOVER_COLOR)
        self.search_btn = Button(480, 150, 120, 40, "Search", INFO_COLOR, BUTTON_HOVER_COLOR)
        self.clear_btn = Button(610, 150, 120, 40, "Clear", WARNING_COLOR, "#d97706")
        
        # Buttons - Traversals
        self.inorder_btn = Button(50, 210, 120, 40, "In-Order", BUTTON_COLOR, BUTTON_HOVER_COLOR)
        self.preorder_btn = Button(180, 210, 120, 40, "Pre-Order", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        self.postorder_btn = Button(310, 210, 120, 40, "Post-Order", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        self.clear_trav_btn = Button(440, 210, 140, 40, "Clear Traversal", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        self.back_btn = Button(50, 800, 150, 50, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
        
        # Status label
        self.status_label = Label(50, 270, "", NORMAL_FONT_SIZE, TEXT_SECONDARY)
        
        # Instructions
        self.instructions = [
            "Insert: Add node maintaining BST property",
            "Delete: Remove node (handles 3 cases)",
            "Search: Find if value exists",
            "Traversals: Show different orders",
            "Left < Parent < Right property"
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
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                value = self.value_input.get_value()
                
                # Operations
                if self.insert_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        if self.bst.insert(value):
                            self.status_label.set_text(f"Inserted {value}")
                            self.value_input.set_text("")
                        else:
                            self.status_label.set_text(f"Value {value} already exists")
                    else:
                        self.status_label.set_text("Enter a value")
                
                elif self.delete_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        if self.bst.delete(value):
                            self.status_label.set_text(f"Deleted {value}")
                            self.value_input.set_text("")
                        else:
                            self.status_label.set_text(f"Value {value} not found")
                    else:
                        self.status_label.set_text("Enter a value")
                
                elif self.search_btn.is_clicked(mouse_pos):
                    if value != 0 or self.value_input.get_text() == "0":
                        if self.bst.search(value):
                            self.status_label.set_text(f"Found {value} in tree")
                            self.highlighted_nodes = {value}
                        else:
                            self.status_label.set_text(f"Value {value} not found")
                            self.highlighted_nodes.clear()
                    else:
                        self.status_label.set_text("Enter a value")
                
                elif self.clear_btn.is_clicked(mouse_pos):
                    self.bst.clear()
                    self.traversal_result = []
                    self.highlighted_nodes.clear()
                    self.status_label.set_text("Tree cleared")
                
                # Traversals
                elif self.inorder_btn.is_clicked(mouse_pos):
                    self.traversal_mode = 'inorder'
                    self.traversal_result = self.bst.inorder_traversal()
                    self.status_label.set_text(f"In-order: {self.traversal_result}")
                
                elif self.preorder_btn.is_clicked(mouse_pos):
                    self.traversal_mode = 'preorder'
                    self.traversal_result = self.bst.preorder_traversal()
                    self.status_label.set_text(f"Pre-order: {self.traversal_result}")
                
                elif self.postorder_btn.is_clicked(mouse_pos):
                    self.traversal_mode = 'postorder'
                    self.traversal_result = self.bst.postorder_traversal()
                    self.status_label.set_text(f"Post-order: {self.traversal_result}")
                
                elif self.clear_trav_btn.is_clicked(mouse_pos):
                    self.traversal_mode = None
                    self.traversal_result = []
                    self.highlighted_nodes.clear()
                    self.status_label.set_text("Traversal cleared")
                
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
        
        # Update input box
        self.value_input.update(self.clock.get_time())
        
        return True
    
    def calculate_positions(self, node, x, y, h_spacing, depth=0):
        """Recursively calculate positions for tree nodes"""
        if node is None:
            return
        
        node.x = x
        node.y = y
        
        # Calculate positions for children
        spacing = h_spacing / (2 ** depth)
        
        if node.left:
            self.calculate_positions(node.left, x - spacing, y + 80, h_spacing, depth + 1)
        if node.right:
            self.calculate_positions(node.right, x + spacing, y + 80, h_spacing, depth + 1)
    
    def draw_tree(self):
        """Draw the BST"""
        if self.bst.is_empty():
            # Draw empty message
            empty_font = get_font(NORMAL_FONT_SIZE)
            empty_text = empty_font.render("Tree is empty - insert nodes to begin", True, TEXT_MUTED)
            empty_rect = empty_text.get_rect(center=(WINDOW_WIDTH // 2, 500))
            self.screen.blit(empty_text, empty_rect)
            return
        
        # Calculate positions
        root_x = WINDOW_WIDTH // 2
        root_y = 350
        h_spacing = 400
        
        self.calculate_positions(self.bst.root, root_x, root_y, h_spacing)
        
        # Draw edges first (so they appear behind nodes)
        self.draw_edges(self.bst.root)
        
        # Draw nodes
        self.draw_nodes(self.bst.root)
    
    def draw_edges(self, node):
        """Draw edges between nodes"""
        if node is None:
            return
        
        # Draw edge to left child
        if node.left:
            pygame.draw.line(
                self.screen,
                TEXT_MUTED,
                (node.x, node.y),
                (node.left.x, node.left.y),
                3
            )
            self.draw_edges(node.left)
        
        # Draw edge to right child
        if node.right:
            pygame.draw.line(
                self.screen,
                TEXT_MUTED,
                (node.x, node.y),
                (node.right.x, node.right.y),
                3
            )
            self.draw_edges(node.right)
    
    def draw_nodes(self, node):
        """Draw nodes as circles"""
        if node is None:
            return
        
        # Determine color
        if node.value in self.highlighted_nodes:
            color = WARNING_COLOR
            border_color = "#f59e0b"
        else:
            color = TREE_NODE_COLOR
            border_color = (20, 150, 60)
        
        # Draw circle
        radius = 25
        pygame.draw.circle(self.screen, color, (node.x, node.y), radius)
        pygame.draw.circle(self.screen, border_color, (node.x, node.y), radius, 3)
        
        # Draw value
        value_font = get_font(NORMAL_FONT_SIZE)
        value_text = value_font.render(str(node.value), True, TEXT_COLOR)
        value_rect = value_text.get_rect(center=(node.x, node.y))
        self.screen.blit(value_text, value_rect)
        
        # Recursively draw children
        self.draw_nodes(node.left)
        self.draw_nodes(node.right)
    
    def draw(self):
        """Draw all elements"""
        self.screen.fill(BG_COLOR)
        
        # Draw title
        title_font = get_font(TITLE_FONT_SIZE)
        title = title_font.render("Binary Search Tree Visualizer", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Draw UI panel
        panel = Panel(30, 130, 720, 140, BG_SECONDARY, TEXT_MUTED)
        panel.draw(self.screen)
        
        # Draw UI elements
        mouse_pos = pygame.mouse.get_pos()
        self.value_input.draw(self.screen)
        self.insert_btn.draw(self.screen, mouse_pos)
        self.delete_btn.draw(self.screen, mouse_pos)
        self.search_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)
        
        # Highlight selected traversal
        if self.traversal_mode == 'inorder':
            self.inorder_btn.color = BUTTON_COLOR
            self.preorder_btn.color = SECONDARY_BUTTON_COLOR
            self.postorder_btn.color = SECONDARY_BUTTON_COLOR
        elif self.traversal_mode == 'preorder':
            self.inorder_btn.color = SECONDARY_BUTTON_COLOR
            self.preorder_btn.color = BUTTON_COLOR
            self.postorder_btn.color = SECONDARY_BUTTON_COLOR
        elif self.traversal_mode == 'postorder':
            self.inorder_btn.color = SECONDARY_BUTTON_COLOR
            self.preorder_btn.color = SECONDARY_BUTTON_COLOR
            self.postorder_btn.color = BUTTON_COLOR
        else:
            self.inorder_btn.color = SECONDARY_BUTTON_COLOR
            self.preorder_btn.color = SECONDARY_BUTTON_COLOR
            self.postorder_btn.color = SECONDARY_BUTTON_COLOR
        
        self.inorder_btn.draw(self.screen, mouse_pos)
        self.preorder_btn.draw(self.screen, mouse_pos)
        self.postorder_btn.draw(self.screen, mouse_pos)
        self.clear_trav_btn.draw(self.screen, mouse_pos)
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
        stats_panel = Panel(790, 330, 580, 140, BG_SECONDARY, TEXT_MUTED)
        stats_panel.draw(self.screen)
        
        stats_title = Label(810, 350, "Tree Statistics:", NORMAL_FONT_SIZE, TEXT_COLOR)
        stats_title.draw(self.screen)
        
        stats = {
            "Size": self.bst.size(),
            "Height": self.bst.height(),
            "Empty": "Yes" if self.bst.is_empty() else "No",
            "In-order": str(self.bst.inorder_traversal()[:10]) + ("..." if self.bst.size() > 10 else "")
        }
        draw_stats(self.screen, stats, 810, 380)
        
        # Draw the tree visualization
        self.draw_tree()
        
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
    pygame.display.set_caption("Binary Search Tree Visualizer")
    
    visualizer = BSTVisualizer(screen)
    visualizer.run()
    
    pygame.quit()


if __name__ == "__main__":
    main()