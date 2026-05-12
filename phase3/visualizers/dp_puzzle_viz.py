"""
Dynamic Programming Puzzle Visualizer with PyGame
Interactive grid path counting with animated DP table fill
"""

import pygame
import sys
import os
from collections import deque

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, Label, Panel, draw_instructions, get_font
from phase3.dp_puzzle import GridPathDP


# ── Color helpers ─────────────────────────────────────────────────────────────

def _lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class DPPuzzleVisualizer:
    """Interactive DP grid-path visualizer"""

    GRID_ROWS = 8
    GRID_COLS = 12

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.dp = GridPathDP(self.GRID_ROWS, self.GRID_COLS)

        # Grid display origin
        self.cell_size = 52
        self.grid_x = 310
        self.grid_y = 140

        # Draw-mode: 'obstacle' | 'start' | 'goal'  (start/goal fixed for now)
        self.draw_mode = 'obstacle'
        self.mouse_pressed = False
        self.last_cell = None

        # Animation state
        self.animating = False
        self.anim_queue = deque()   # (row, col, value) steps
        self.anim_revealed = {}     # (r,c) -> display_value
        self.anim_timer = 0
        self.anim_speed = 60        # ms per cell
        self.highlight_cell = None
        self.highlight_timer = 0

        # Results
        self.dp_table = None
        self.path = []
        self.total_paths = 0
        self.solved = False

        # Start / goal (fixed corners by default)
        self.start = (0, 0)
        self.goal = (self.GRID_ROWS - 1, self.GRID_COLS - 1)

        self.setup_ui()

    # ── UI Setup ─────────────────────────────────────────────────────────────

    def setup_ui(self):
        bx = 20
        self.solve_btn = Button(bx, 160, 150, 42, "▶ Solve (DP)", SUCCESS_COLOR, "#059669", font_size=14)
        self.show_path_btn = Button(bx, 212, 150, 42, "Show Path", INFO_COLOR, BUTTON_HOVER_COLOR, font_size=14)
        self.clear_walls_btn = Button(bx, 264, 150, 42, "Clear Walls", WARNING_COLOR, "#d97706", font_size=14)
        self.reset_btn = Button(bx, 316, 150, 42, "Reset All", DANGER_COLOR, DANGER_HOVER_COLOR, font_size=14)

        self.slow_btn = Button(bx, 390, 70, 34, "Slow", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=13)
        self.fast_btn = Button(bx + 80, 390, 70, 34, "Fast", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=13)

        self.back_btn = Button(bx, 820, 130, 44, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=14)

        self.status_label = Label(bx, 440, "", SMALL_FONT_SIZE, TEXT_SECONDARY)

        self.instructions = [
            "Click grid cells to toggle walls",
            "Green cell = Start (top-left)",
            "Red cell = Goal (bottom-right)",
            "DP fills table bottom-up",
            "Each cell = paths from Start",
            "Path shown in gold",
        ]

    # ── Event Handling ────────────────────────────────────────────────────────

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and not self.animating:
                if self.solve_btn.is_clicked(mouse_pos):
                    self._start_solve()
                elif self.show_path_btn.is_clicked(mouse_pos):
                    self._show_path()
                elif self.clear_walls_btn.is_clicked(mouse_pos):
                    self._clear_walls()
                elif self.reset_btn.is_clicked(mouse_pos):
                    self._reset()
                elif self.slow_btn.is_clicked(mouse_pos):
                    self.anim_speed = 150
                    self.status_label.set_text("Speed: Slow")
                elif self.fast_btn.is_clicked(mouse_pos):
                    self.anim_speed = 15
                    self.status_label.set_text("Speed: Fast")
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
                else:
                    self.mouse_pressed = True
                    self._handle_grid_click(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                self.last_cell = None

            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed and not self.animating:
                    self._handle_grid_click(mouse_pos)

        return True

    def _handle_grid_click(self, mouse_pos):
        gx, gy = self.grid_x, self.grid_y
        mx, my = mouse_pos
        if not (gx <= mx < gx + self.GRID_COLS * self.cell_size and
                gy <= my < gy + self.GRID_ROWS * self.cell_size):
            return
        col = (mx - gx) // self.cell_size
        row = (my - gy) // self.cell_size
        if (row, col) == self.last_cell:
            return
        self.last_cell = (row, col)
        if (row, col) in (self.start, self.goal):
            return
        self.dp.grid[row][col] ^= 1
        # reset solved state when grid changes
        self._clear_solve_state()

    # ── Solve Logic ───────────────────────────────────────────────────────────

    def _start_solve(self):
        self._clear_solve_state()
        self.dp.reset()
        self.total_paths = self.dp.count_paths_tabulation(self.start, self.goal)
        self.dp_table = self.dp.get_dp_table()
        self.solved = True

        # Build animation queue from computation order
        self.anim_revealed.clear()
        self.anim_queue = deque(self.dp.get_computation_order())
        self.animating = True
        self.status_label.set_text("Filling DP table…")

    def _show_path(self):
        if not self.solved:
            self.status_label.set_text("Solve first!")
            return
        self.path = self.dp.reconstruct_one_path() or []
        if self.path:
            self.status_label.set_text(f"One path shown  |  Total unique paths: {self.total_paths:,}")
        else:
            self.status_label.set_text("No path exists!")

    def _clear_walls(self):
        self.dp.clear_obstacles()
        self._clear_solve_state()
        self.status_label.set_text("Walls cleared.")

    def _reset(self):
        self.dp = GridPathDP(self.GRID_ROWS, self.GRID_COLS)
        self._clear_solve_state()
        self.status_label.set_text("Reset.")

    def _clear_solve_state(self):
        self.animating = False
        self.anim_queue.clear()
        self.anim_revealed.clear()
        self.dp_table = None
        self.path = []
        self.solved = False
        self.total_paths = 0

    # ── Animation Update ──────────────────────────────────────────────────────

    def update(self, dt):
        if not self.animating:
            return
        self.anim_timer += dt
        steps = max(1, self.anim_timer // self.anim_speed)
        self.anim_timer %= self.anim_speed
        for _ in range(int(steps)):
            if not self.anim_queue:
                self.animating = False
                self.status_label.set_text(
                    f"Done!  Total paths: {self.total_paths:,}  |  Press 'Show Path' to trace one."
                )
                return
            r, c, v = self.anim_queue.popleft()
            self.anim_revealed[(r, c)] = v
            self.highlight_cell = (r, c)

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _cell_rect(self, row, col):
        x = self.grid_x + col * self.cell_size
        y = self.grid_y + row * self.cell_size
        return pygame.Rect(x, y, self.cell_size, self.cell_size)

    def _value_color(self, val, max_val):
        if max_val == 0:
            return BG_TERTIARY
        t = min(1.0, val / max(max_val, 1))
        low = (30, 58, 100)   # dark blue
        high = (59, 130, 246)  # bright blue
        return _lerp_color(low, high, t)

    def draw(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Title
        tf = get_font(HEADING_FONT_SIZE)
        t = tf.render("Dynamic Programming  —  Grid Path Counter", True, TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, 55)))
        sub = get_font(SMALL_FONT_SIZE).render(
            "Count unique paths from Start → Goal (move right or down only)", True, TEXT_MUTED)
        self.screen.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, 85)))

        # Left panel
        Panel(15, 140, 275, WINDOW_HEIGHT - 160, BG_SECONDARY, TEXT_MUTED).draw(self.screen)

        self.solve_btn.draw(self.screen, mouse_pos)
        self.show_path_btn.draw(self.screen, mouse_pos)
        self.clear_walls_btn.draw(self.screen, mouse_pos)
        self.reset_btn.draw(self.screen, mouse_pos)
        self.slow_btn.draw(self.screen, mouse_pos)
        self.fast_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)
        self.status_label.draw(self.screen)

        # Instructions
        inst_y = 510
        get_font(NORMAL_FONT_SIZE)
        Panel(20, inst_y, 265, 185, BG_TERTIARY, TEXT_MUTED).draw(self.screen)
        ih = get_font(SMALL_FONT_SIZE).render("How it works:", True, TEXT_COLOR)
        self.screen.blit(ih, (30, inst_y + 10))
        draw_instructions(self.screen, self.instructions, 28, inst_y + 32)

        # ── Grid ──────────────────────────────────────────────────────────────
        max_val = max(self.anim_revealed.values(), default=1) or 1

        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                rect = self._cell_rect(row, col)
                cell = (row, col)

                # Background
                if cell == self.start:
                    bg = START_COLOR
                elif cell == self.goal:
                    bg = END_COLOR
                elif self.dp.grid[row][col] == 1:
                    bg = WALL_COLOR
                elif cell in self.path:
                    bg = PATH_FOUND_COLOR
                elif cell in self.anim_revealed:
                    v = self.anim_revealed[cell]
                    bg = self._value_color(v, max_val)
                else:
                    bg = GRID_BG_COLOR

                pygame.draw.rect(self.screen, bg, rect)
                border_col = (255, 255, 100) if cell == self.highlight_cell else GRID_LINE_COLOR
                border_w = 2 if cell == self.highlight_cell else 1
                pygame.draw.rect(self.screen, border_col, rect, border_w)

                # Value label
                if cell in self.anim_revealed and self.dp.grid[row][col] == 0:
                    v = self.anim_revealed[cell]
                    s = str(v) if v < 1000 else "…"
                    fs = 14 if v < 100 else 11
                    vf = get_font(fs)
                    vt = vf.render(s, True, TEXT_COLOR if bg != GRID_BG_COLOR else (100, 100, 120))
                    self.screen.blit(vt, vt.get_rect(center=rect.center))

                # Start / Goal labels
                if cell == self.start:
                    lt = get_font(11).render("S", True, TEXT_COLOR)
                    self.screen.blit(lt, lt.get_rect(center=rect.center))
                elif cell == self.goal:
                    lt = get_font(11).render("G", True, TEXT_COLOR)
                    self.screen.blit(lt, lt.get_rect(center=rect.center))

        # ── Stats bar below grid ───────────────────────────────────────────────
        grid_bottom = self.grid_y + self.GRID_ROWS * self.cell_size + 10
        Panel(self.grid_x, grid_bottom, self.GRID_COLS * self.cell_size, 60, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        sf = get_font(SMALL_FONT_SIZE)
        revealed = len(self.anim_revealed)
        total_cells = self.GRID_ROWS * self.GRID_COLS - sum(self.dp.grid[r][c] for r in range(self.GRID_ROWS) for c in range(self.GRID_COLS))
        parts = [
            f"Grid: {self.GRID_ROWS}×{self.GRID_COLS}",
            f"Walls: {sum(self.dp.grid[r][c] for r in range(self.GRID_ROWS) for c in range(self.GRID_COLS))}",
            f"Cells filled: {revealed}/{total_cells}",
            f"Total paths: {self.total_paths:,}" if self.solved else "Not solved yet",
        ]
        for i, p in enumerate(parts):
            tx = sf.render(p, True, TEXT_SECONDARY)
            self.screen.blit(tx, (self.grid_x + 10 + i * (self.GRID_COLS * self.cell_size // 4), grid_bottom + 20))

        # Legend
        leg_y = grid_bottom + 75
        legend = [
            (START_COLOR, "Start"),
            (END_COLOR, "Goal"),
            (WALL_COLOR, "Wall (click to toggle)"),
            (PATH_FOUND_COLOR, "Path"),
            ((59, 130, 246), "DP value (# paths)"),
        ]
        lx = self.grid_x
        for color, label in legend:
            pygame.draw.rect(self.screen, color, (lx, leg_y, 16, 16), border_radius=3)
            lt = get_font(12).render(label, True, TEXT_SECONDARY)
            self.screen.blit(lt, (lx + 20, leg_y + 1))
            lx += lt.get_width() + 50

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            if not self.handle_events():
                break
            self.update(dt)
            self.draw()
        return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("DP Puzzle Visualizer")
    DPPuzzleVisualizer(screen).run()
    pygame.quit()


if __name__ == "__main__":
    main()
