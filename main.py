"""
DSA Explorer - Main Entry Point
Interactive Data Structures and Algorithms Visualizer
COMPLETE VERSION - All Visualizers + In-App Test Runner
"""

import pygame
import sys
from config import *
from utils.ui_components import Button, get_font

# ── Phase 1 ──────────────────────────────────────────────────────────────────
try:
    from phase1.visualizers.stack_viz import StackVisualizer
    from phase1.visualizers.queue_viz import QueueVisualizer
    from phase1.visualizers.linked_list_viz import LinkedListVisualizer
    from phase1.visualizers.bst_viz import BSTVisualizer
    PHASE1_AVAILABLE = True
except ImportError as e:
    PHASE1_AVAILABLE = False
    print(f"Warning: Phase 1 visualizers not found: {e}")

# ── Phase 2 ──────────────────────────────────────────────────────────────────
try:
    from phase2.visualizers.sort_viz import SortingVisualizer
    from phase2.visualizers.graph_viz import GraphVisualizer
    from phase2.visualizers.heap_viz import HeapVisualizer
    PHASE2_AVAILABLE = True
except ImportError as e:
    PHASE2_AVAILABLE = False
    print(f"Warning: Phase 2 visualizers not found: {e}")

# ── Phase 3 ──────────────────────────────────────────────────────────────────
try:
    from phase3.visualizers.pathfinding_viz import PathfindingVisualizer
    from phase3.visualizers.event_queue_viz import EventQueueVisualizer
    from phase3.visualizers.dp_puzzle_viz import DPPuzzleVisualizer
    PHASE3_AVAILABLE = True
except ImportError as e:
    PHASE3_AVAILABLE = False
    print(f"Warning: Phase 3 visualizers not found: {e}")

# ── Test runner ───────────────────────────────────────────────────────────────
try:
    import importlib.util as _ilu, os as _os
    # test_runner_viz.py lives in the same directory as test.py (project root)
    _root = _os.path.dirname(_os.path.abspath(__file__))
    _spec = _ilu.spec_from_file_location(
        "test_runner_viz",
        _os.path.join(_root, "test_runner_viz.py")
    )
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    TestRunnerVisualizer = _mod.TestRunnerVisualizer
    TESTS_AVAILABLE = True
except Exception as e:
    TESTS_AVAILABLE = False
    TestRunnerVisualizer = None
    print(f"Warning: Test runner not found: {e}")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _btn(screen_w, y, text, color, hover, enabled=True):
    b = Button(screen_w // 2 - BUTTON_WIDTH // 2, y, BUTTON_WIDTH, BUTTON_HEIGHT,
               text, color, hover)
    b.set_enabled(enabled)
    return b


class DSAExplorer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DSA Explorer & Visualizer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "MENU"

    # ── Shared drawing ────────────────────────────────────────────────────────

    def _title(self, text, y):
        s = get_font(TITLE_FONT_SIZE).render(text, True, TEXT_COLOR)
        self.screen.blit(s, s.get_rect(center=(WINDOW_WIDTH // 2, y)))

    def _subtitle(self, text, y):
        s = get_font(SUBTITLE_FONT_SIZE).render(text, True, TEXT_SECONDARY)
        self.screen.blit(s, s.get_rect(center=(WINDOW_WIDTH // 2, y)))

    def _footer(self):
        s = get_font(SMALL_FONT_SIZE).render(
            "Use mouse to navigate • ESC to go back", True, TEXT_MUTED)
        self.screen.blit(s, s.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)))

    def _event_loop(self, buttons_map):
        """Generic event loop.  buttons_map: {button: action_callable | state_string}
        Returns False when QUIT or ESC, True otherwise.  Call per frame."""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False, mouse_pos
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False, mouse_pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn, action in buttons_map.items():
                    if btn.is_clicked(mouse_pos):
                        if callable(action):
                            action()
                        else:
                            self.current_state = action
                        return True, mouse_pos
        return True, mouse_pos

    # ── Main menu ─────────────────────────────────────────────────────────────

    def main_menu(self):
        while self.running and self.current_state == "MENU":
            self.screen.fill(BG_COLOR)
            self._title("DSA EXPLORER", 100)
            self._subtitle("Interactive Data Structures & Algorithms Visualizer", 150)

            p1_btn = _btn(WINDOW_WIDTH, 220, "Phase 1: Data Structures",
                          BUTTON_COLOR if PHASE1_AVAILABLE else SECONDARY_BUTTON_COLOR,
                          BUTTON_HOVER_COLOR if PHASE1_AVAILABLE else SECONDARY_BUTTON_HOVER,
                          PHASE1_AVAILABLE)
            p2_btn = _btn(WINDOW_WIDTH, 300, "Phase 2: Algorithms",
                          BUTTON_COLOR if PHASE2_AVAILABLE else SECONDARY_BUTTON_COLOR,
                          BUTTON_HOVER_COLOR if PHASE2_AVAILABLE else SECONDARY_BUTTON_HOVER,
                          PHASE2_AVAILABLE)
            p3_btn = _btn(WINDOW_WIDTH, 380, "Phase 3: Puzzles",
                          BUTTON_COLOR if PHASE3_AVAILABLE else SECONDARY_BUTTON_COLOR,
                          BUTTON_HOVER_COLOR if PHASE3_AVAILABLE else SECONDARY_BUTTON_HOVER,
                          PHASE3_AVAILABLE)
            help_btn = _btn(WINDOW_WIDTH, 460, "Help & Instructions",
                            SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
            exit_btn = _btn(WINDOW_WIDTH, 540, "Exit", DANGER_COLOR, DANGER_HOVER_COLOR)

            bmap = {
                p1_btn: "PHASE1",
                p2_btn: "PHASE2",
                p3_btn: "PHASE3",
                help_btn: self.show_help,
                exit_btn: lambda: setattr(self, 'running', False),
            }
            cont, mouse_pos = self._event_loop(bmap)
            if not cont:
                if self.current_state == "MENU":
                    self.running = False
                break

            for b in [p1_btn, p2_btn, p3_btn, help_btn, exit_btn]:
                b.draw(self.screen, mouse_pos)
            self._footer()
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── Phase 1 menu ──────────────────────────────────────────────────────────

    def phase1_menu(self):
        while self.running and self.current_state == "PHASE1":
            self.screen.fill(BG_COLOR)
            self._title("PHASE 1: Data Structures", 80)
            self._subtitle("Explore foundational data structures", 130)

            W2 = WINDOW_WIDTH // 2
            stack_btn  = Button(W2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Stack Visualizer",      BUTTON_COLOR,            BUTTON_HOVER_COLOR)
            queue_btn  = Button(W2 - BUTTON_WIDTH // 2, 270, BUTTON_WIDTH, BUTTON_HEIGHT, "Queue Visualizer",      BUTTON_COLOR,            BUTTON_HOVER_COLOR)
            ll_btn     = Button(W2 - BUTTON_WIDTH // 2, 340, BUTTON_WIDTH, BUTTON_HEIGHT, "Linked List Editor",    BUTTON_COLOR,            BUTTON_HOVER_COLOR)
            bst_btn    = Button(W2 - BUTTON_WIDTH // 2, 410, BUTTON_WIDTH, BUTTON_HEIGHT, "Binary Search Tree",    BUTTON_COLOR,            BUTTON_HOVER_COLOR)
            test_btn   = Button(W2 - BUTTON_WIDTH // 2, 490, BUTTON_WIDTH, BUTTON_HEIGHT, "Run Phase 1 Tests",  INFO_COLOR,              BUTTON_HOVER_COLOR)
            test_btn.set_enabled(TESTS_AVAILABLE)
            back_btn   = Button(W2 - BUTTON_WIDTH // 2, 575, BUTTON_WIDTH, BUTTON_HEIGHT, "Back to Menu",        SECONDARY_BUTTON_COLOR,  SECONDARY_BUTTON_HOVER)

            bmap = {
                stack_btn: lambda: StackVisualizer(self.screen).run(),
                queue_btn: lambda: QueueVisualizer(self.screen).run(),
                ll_btn:    lambda: LinkedListVisualizer(self.screen).run(),
                bst_btn:   lambda: BSTVisualizer(self.screen).run(),
                test_btn:  lambda: TestRunnerVisualizer(self.screen, 1).run(),
                back_btn:  "MENU",
            }
            cont, mouse_pos = self._event_loop(bmap)
            if not cont:
                self.current_state = "MENU"
                break

            for b in [stack_btn, queue_btn, ll_btn, bst_btn, test_btn, back_btn]:
                b.draw(self.screen, mouse_pos)
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── Phase 2 menu ──────────────────────────────────────────────────────────

    def phase2_menu(self):
        while self.running and self.current_state == "PHASE2":
            self.screen.fill(BG_COLOR)
            self._title("PHASE 2: Algorithm Visualizer", 80)
            self._subtitle("Watch algorithms in action", 130)

            W2 = WINDOW_WIDTH // 2
            sort_btn  = Button(W2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Sorting Algorithms",        BUTTON_COLOR,           BUTTON_HOVER_COLOR)
            graph_btn = Button(W2 - BUTTON_WIDTH // 2, 270, BUTTON_WIDTH, BUTTON_HEIGHT, "Graph Traversal (BFS/DFS)", BUTTON_COLOR,           BUTTON_HOVER_COLOR)
            heap_btn  = Button(W2 - BUTTON_WIDTH // 2, 340, BUTTON_WIDTH, BUTTON_HEIGHT, "Heap Operations",           BUTTON_COLOR,           BUTTON_HOVER_COLOR)
            test_btn  = Button(W2 - BUTTON_WIDTH // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT, "Run Phase 2 Tests",      INFO_COLOR,             BUTTON_HOVER_COLOR)
            back_btn  = Button(W2 - BUTTON_WIDTH // 2, 505, BUTTON_WIDTH, BUTTON_HEIGHT, "Back to Menu",            SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
            test_btn.set_enabled(TESTS_AVAILABLE)

            bmap = {
                sort_btn:  lambda: SortingVisualizer(self.screen).run(),
                graph_btn: lambda: GraphVisualizer(self.screen).run(),
                heap_btn:  lambda: HeapVisualizer(self.screen).run(),
                test_btn:  lambda: TestRunnerVisualizer(self.screen, 2).run(),
                back_btn:  "MENU",
            }
            cont, mouse_pos = self._event_loop(bmap)
            if not cont:
                self.current_state = "MENU"
                break

            for b in [sort_btn, graph_btn, heap_btn, test_btn, back_btn]:
                b.draw(self.screen, mouse_pos)
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── Phase 3 menu ──────────────────────────────────────────────────────────

    def phase3_menu(self):
        while self.running and self.current_state == "PHASE3":
            self.screen.fill(BG_COLOR)
            self._title("PHASE 3: Puzzle Challenges", 80)
            self._subtitle("Apply algorithms to solve puzzles", 130)

            W2 = WINDOW_WIDTH // 2
            path_btn  = Button(W2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "Pathfinding Puzzle (A*)",   BUTTON_COLOR,           BUTTON_HOVER_COLOR)
            eq_btn    = Button(W2 - BUTTON_WIDTH // 2, 270, BUTTON_WIDTH, BUTTON_HEIGHT, "Event Queue Simulator",     BUTTON_COLOR,           BUTTON_HOVER_COLOR)
            dp_btn    = Button(W2 - BUTTON_WIDTH // 2, 340, BUTTON_WIDTH, BUTTON_HEIGHT, "DP Grid Path Puzzle",        BUTTON_COLOR,           BUTTON_HOVER_COLOR)
            test_btn  = Button(W2 - BUTTON_WIDTH // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT, "Run Phase 3 Tests",      INFO_COLOR,             BUTTON_HOVER_COLOR)
            back_btn  = Button(W2 - BUTTON_WIDTH // 2, 505, BUTTON_WIDTH, BUTTON_HEIGHT, "Back to Menu",            SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
            test_btn.set_enabled(TESTS_AVAILABLE)

            bmap = {
                path_btn: lambda: PathfindingVisualizer(self.screen).run(),
                eq_btn:   lambda: EventQueueVisualizer(self.screen).run(),
                dp_btn:   lambda: DPPuzzleVisualizer(self.screen).run(),
                test_btn: lambda: TestRunnerVisualizer(self.screen, 3).run(),
                back_btn: "MENU",
            }
            cont, mouse_pos = self._event_loop(bmap)
            if not cont:
                self.current_state = "MENU"
                break

            for b in [path_btn, eq_btn, dp_btn, test_btn, back_btn]:
                b.draw(self.screen, mouse_pos)
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── Help screen ───────────────────────────────────────────────────────────

    def show_help(self):
        showing = True
        while showing and self.running:
            self.screen.fill(BG_COLOR)
            self._title("Help & Instructions", 60)

            lines = [
                "Welcome to DSA Explorer",
                "",
                "  Phase 1 — All 4 Data Structures:",
                "     Stack  •  Queue  •  Linked List  •  Binary Search Tree",
                "",
                "  Phase 2 — All 3 Algorithm Visualizers:",
                "     Sorting (Bubble / Selection / Merge)",
                "     Graph Traversal (BFS & DFS)",
                "     Heap Operations (Min-Heap & Max-Heap)",
                "",
                "  Phase 3 — All 3 Puzzle Visualizers:",
                "     Pathfinding (A* & Dijkstra)",
                "     Event Queue Simulator (Priority Queue)",
                "     DP Grid Path Counter (Tabulation + animation)",
                "",
                "  In-App Test Runner — available in each Phase submenu",
                "     Runs the full unittest suite and streams results live.",
                "     Use ↑↓ / scroll to navigate results.",
                "",
                "Controls:",
                "  Mouse — click buttons & interact with visualizations",
                "  ESC   — return to previous menu",
                "  Space — play/pause in supported visualizers",
            ]

            font = get_font(NORMAL_FONT_SIZE)
            y = 130
            for line in lines:
                s = font.render(line, True, TEXT_COLOR)
                self.screen.blit(s, s.get_rect(center=(WINDOW_WIDTH // 2, y)))
                y += 26

            back_btn = Button(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, y + 20,
                              BUTTON_WIDTH, BUTTON_HEIGHT,
                              "← Back to Menu", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    showing = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    showing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.is_clicked(mouse_pos):
                        showing = False

            back_btn.draw(self.screen, mouse_pos)
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        while self.running:
            if self.current_state == "MENU":
                self.main_menu()
            elif self.current_state == "PHASE1":
                self.phase1_menu()
            elif self.current_state == "PHASE2":
                self.phase2_menu()
            elif self.current_state == "PHASE3":
                self.phase3_menu()
            else:
                self.current_state = "MENU"

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    DSAExplorer().run()