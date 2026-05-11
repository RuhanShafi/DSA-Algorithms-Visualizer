"""
Configuration file for DSA Explorer
Contains all colors, dimensions, fonts, and global settings
"""

# Window Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS = 60

# Color Palette - Modern Dark Theme
BG_COLOR = (30, 30, 46)  # Dark blue background
BG_SECONDARY = (30, 41, 59)  # Slightly lighter background
BG_TERTIARY = (51, 65, 85)  # Card/panel background

# Button Colors
BUTTON_COLOR = (59, 130, 246)  # Primary blue
BUTTON_HOVER_COLOR = (37, 99, 235)  # Darker blue on hover
SECONDARY_BUTTON_COLOR = (71, 85, 105)  # Gray button
SECONDARY_BUTTON_HOVER = (100, 116, 139)  # Gray hover

# Status Colors
SUCCESS_COLOR = (16, 185, 129)  # Green
DANGER_COLOR = (239, 68, 68)  # Red
DANGER_HOVER_COLOR = (220, 38, 38)  # Darker red
WARNING_COLOR = (245, 158, 11)  # Orange/Yellow
INFO_COLOR = (59, 130, 246)  # Blue

# Text Colors
TEXT_COLOR = (241, 245, 249)  # Light gray/white
TEXT_SECONDARY = (203, 213, 225)  # Medium gray
TEXT_MUTED = (100, 116, 139)  # Muted gray

# Data Structure Visualization Colors
STACK_COLOR = (139, 92, 246)  # Purple
QUEUE_COLOR = (236, 72, 153)  # Pink
LINKED_LIST_COLOR = (14, 165, 233)  # Sky blue
TREE_NODE_COLOR = (34, 197, 94)  # Green
GRAPH_NODE_COLOR = (251, 146, 60)  # Orange
HEAP_COLOR = (245, 158, 11)  # Amber

# Algorithm State Colors
DEFAULT_COLOR = (148, 163, 184)  # Slate gray
COMPARING_COLOR = (250, 204, 21)  # Yellow
SWAPPING_COLOR = (239, 68, 68)  # Red
SORTED_COLOR = (34, 197, 94)  # Green
VISITING_COLOR = (59, 130, 246)  # Blue
VISITED_COLOR = (147, 197, 253)  # Light blue
PATH_COLOR = (251, 191, 36)  # Gold

# Grid/Cell Colors (for pathfinding)
GRID_BG_COLOR = (255, 255, 255)  # White
GRID_LINE_COLOR = (226, 232, 240)  # Light gray
WALL_COLOR = (51, 65, 85)  # Dark gray
START_COLOR = (16, 185, 129)  # Green
END_COLOR = (239, 68, 68)  # Red
EXPLORED_COLOR = (191, 219, 254)  # Light blue
PATH_FOUND_COLOR = (251, 191, 36)  # Gold

# Font Sizes
TITLE_FONT_SIZE = 48
SUBTITLE_FONT_SIZE = 20
HEADING_FONT_SIZE = 32
NORMAL_FONT_SIZE = 16
SMALL_FONT_SIZE = 14
BUTTON_FONT_SIZE = 18

# Button Dimensions
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 60
SMALL_BUTTON_WIDTH = 150
SMALL_BUTTON_HEIGHT = 40

# Animation Settings
ANIMATION_SPEED_SLOW = 1000  # milliseconds
ANIMATION_SPEED_MEDIUM = 500
ANIMATION_SPEED_FAST = 100
DEFAULT_ANIMATION_SPEED = ANIMATION_SPEED_MEDIUM

# Data Structure Limits
MAX_STACK_SIZE = 10
MAX_QUEUE_SIZE = 10
MAX_LINKED_LIST_SIZE = 15
MAX_TREE_DEPTH = 5
MAX_HEAP_SIZE = 31  # Complete binary tree with 5 levels

# Grid Settings
DEFAULT_GRID_ROWS = 20
DEFAULT_GRID_COLS = 30
MIN_GRID_SIZE = 10
MAX_GRID_SIZE = 50
CELL_SIZE = 25

# Graph Settings
NODE_RADIUS = 30
EDGE_WIDTH = 3
ARROW_SIZE = 10

# Spacing and Padding
PADDING = 20
MARGIN = 10
ELEMENT_SPACING = 60

# File Paths
FONT_PATH = None  # Will use pygame default font
# FONT_PATH = "assets/fonts/Roboto-Regular.ttf"  # Uncomment to use custom font

# Test Configuration
ENABLE_BENCHMARKING = True
BENCHMARK_ITERATIONS = 100
TEST_DATA_SIZES = [10, 50, 100, 500, 1000]

# Debug Settings
DEBUG_MODE = False
SHOW_FPS = False
SHOW_COORDINATES = False
