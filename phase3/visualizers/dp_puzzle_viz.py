"""
Dynamic Programming Puzzle Visualizer with PyGame
Place in project root alongside test.py.
"""

import pygame
import sys
import os
from collections import deque

# Always resolve relative to this file so it works from any working directory
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from config import *
from utils.ui_components import Button, Label, Panel, draw_instructions, get_font
from phase3.dp_puzzle import GridPathDP


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

        # Compute cell size to fit: width = 1400 - 310 left panel - 20 right margin
        # height = 900 - 140 top - 160 bottom stats+legend
        avail_w = WINDOW_WIDTH - 310 - 20
        avail_h = WINDOW_HEIGHT - 140 - 170
        self.cell_size = min(avail_w // self.GRID_COLS, avail_h // self.GRID_ROWS)
        self.cell_size = max(self.cell_size, 30)   # at least 30px

        self.grid_x = 305
        self.grid_y = 140

        self.mouse_pressed = False
        self.last_cell = None

        # Animation
        self.animating = False
        self.anim_queue = deque()
        self.anim_revealed = {}   # (r,c) -> value
        self.anim_timer = 0
        self.anim_speed = 60      # ms per step
        self.highlight_cell = None

        # Results
        self.dp_table = None
        self.path = []
        self.total_paths = 0
        self.solved = False

        self.start = (0, 0)
        self.goal = (self.GRID_ROWS - 1, self.GRID_COLS - 1)

        self.status_text = "Click cells to add walls, then press Solve."
        self.setup_ui()

    # ─────────────────────────────────────────────────────────────────────────

    def setup_ui(self):
        bx, bw, bh = 20, 265, 40
        self.solve_btn       = Button(bx, 155, bw, bh, "Solve (DP)",   SUCCESS_COLOR,          "#059669",              font_size=14)
        self.show_path_btn   = Button(bx, 203, bw, bh, "Show Path",    INFO_COLOR,             BUTTON_HOVER_COLOR,     font_size=14)
        self.clear_walls_btn = Button(bx, 251, bw, bh, "Clear Walls",  WARNING_COLOR,          "#d97706",              font_size=14)
        self.reset_btn       = Button(bx, 299, bw, bh, "Reset All",    DANGER_COLOR,           DANGER_HOVER_COLOR,     font_size=14)

        hw = (bw - 10) // 2
        self.slow_btn = Button(bx,        355, hw, 34, "Slow",  SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=13)
        self.fast_btn = Button(bx+hw+10,  355, hw, 34, "Fast",  SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=13)

        self.back_btn = Button(bx, WINDOW_HEIGHT - 70, bw, 44, "<- Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=14)

        self.instructions = [
            "Click/drag grid cells to place walls",
            "Green = Start  |  Red = Goal",
            "Solve fills DP table cell-by-cell",
            "Each value = # unique paths to cell",
            "Show Path traces one valid route",
            "Slow/Fast adjusts animation speed",
        ]

    # ─────────────────────────────────────────────────────────────────────────

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.animating:
                    # any button click skips animation
                    pass
                if self.solve_btn.is_clicked(mouse_pos):
                    self._start_solve()
                elif self.show_path_btn.is_clicked(mouse_pos):
                    self._show_path()
                elif self.clear_walls_btn.is_clicked(mouse_pos):
                    self._clear_walls()
                elif self.reset_btn.is_clicked(mouse_pos):
                    self._reset()
                elif self.slow_btn.is_clicked(mouse_pos):
                    self.anim_speed = 160
                    self.status_text = "Speed: Slow"
                elif self.fast_btn.is_clicked(mouse_pos):
                    self.anim_speed = 8
                    self.status_text = "Speed: Fast"
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
                else:
                    if not self.animating:
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
        mx, my = mouse_pos
        gx, gy = self.grid_x, self.grid_y
        cs = self.cell_size
        if not (gx <= mx < gx + self.GRID_COLS * cs and gy <= my < gy + self.GRID_ROWS * cs):
            return
        col = (mx - gx) // cs
        row = (my - gy) // cs
        if not (0 <= row < self.GRID_ROWS and 0 <= col < self.GRID_COLS):
            return
        if (row, col) == self.last_cell:
            return
        self.last_cell = (row, col)
        if (row, col) in (self.start, self.goal):
            return
        self.dp.grid[row][col] ^= 1
        self._clear_solve_state()

    # ─────────────────────────────────────────────────────────────────────────

    def _start_solve(self):
        self._clear_solve_state()
        self.dp.reset()
        self.total_paths = self.dp.count_paths_tabulation(self.start, self.goal)
        self.dp_table = self.dp.get_dp_table()
        self.solved = True

        self.anim_revealed.clear()
        self.anim_queue = deque(self.dp.get_computation_order())
        self.animating = bool(self.anim_queue)
        self.status_text = "Filling DP table..."

    def _show_path(self):
        if not self.solved:
            self.status_text = "Solve first!"
            return
        if self.animating:
            # fast-forward: reveal everything now
            while self.anim_queue:
                r, c, v = self.anim_queue.popleft()
                self.anim_revealed[(r, c)] = v
            self.animating = False
        self.path = self.dp.reconstruct_one_path() or []
        if self.path:
            self.status_text = f"Path length: {len(self.path)}  |  Total paths: {self.total_paths:,}"
        else:
            self.status_text = "No path exists!"

    def _clear_walls(self):
        self.dp.clear_obstacles()
        self._clear_solve_state()
        self.status_text = "Walls cleared."

    def _reset(self):
        self.dp = GridPathDP(self.GRID_ROWS, self.GRID_COLS)
        self._clear_solve_state()
        self.status_text = "Reset. Click cells to add walls."

    def _clear_solve_state(self):
        self.animating = False
        self.anim_queue.clear()
        self.anim_revealed.clear()
        self.dp_table = None
        self.path = []
        self.solved = False
        self.total_paths = 0
        self.highlight_cell = None

    # ─────────────────────────────────────────────────────────────────────────

    def update(self, dt):
        if not self.animating:
            return
        self.anim_timer += dt
        # consume as many steps as time allows
        while self.anim_timer >= self.anim_speed:
            self.anim_timer -= self.anim_speed
            if not self.anim_queue:
                self.animating = False
                self.status_text = (
                    f"Done!  Total paths: {self.total_paths:,}  |  "
                    "Press 'Show Path' to trace one."
                )
                self.highlight_cell = None
                return
            r, c, v = self.anim_queue.popleft()
            self.anim_revealed[(r, c)] = v
            self.highlight_cell = (r, c)

    # ─────────────────────────────────────────────────────────────────────────

    def _cell_rect(self, row, col):
        return pygame.Rect(
            self.grid_x + col * self.cell_size,
            self.grid_y + row * self.cell_size,
            self.cell_size, self.cell_size
        )

    def _value_color(self, val, max_val):
        if max_val == 0:
            return BG_TERTIARY
        t = min(1.0, val / max(max_val, 1))
        return _lerp_color((25, 55, 105), (59, 130, 246), t)

    def draw(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # ── Title ─────────────────────────────────────────────────────────────
        get_font(HEADING_FONT_SIZE).render   # warm up
        tf = get_font(HEADING_FONT_SIZE)
        t = tf.render("Dynamic Programming  --  Grid Path Counter", True, TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, 50)))
        sub = get_font(SMALL_FONT_SIZE).render(
            "Count unique paths: Start -> Goal  (right or down moves only)", True, TEXT_MUTED)
        self.screen.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, 80)))

        # ── Left panel ────────────────────────────────────────────────────────
        Panel(10, 130, 285, WINDOW_HEIGHT - 145, BG_SECONDARY, TEXT_MUTED).draw(self.screen)

        self.solve_btn.draw(self.screen, mouse_pos)
        self.show_path_btn.draw(self.screen, mouse_pos)
        self.clear_walls_btn.draw(self.screen, mouse_pos)
        self.reset_btn.draw(self.screen, mouse_pos)
        self.slow_btn.draw(self.screen, mouse_pos)
        self.fast_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)

        # Status
        sf = get_font(SMALL_FONT_SIZE)
        # word-wrap status across left panel width
        words = self.status_text.split()
        line, lines_out = "", []
        for w in words:
            test = (line + " " + w).strip()
            if sf.size(test)[0] < 265:
                line = test
            else:
                lines_out.append(line)
                line = w
        if line:
            lines_out.append(line)
        for i, l in enumerate(lines_out[:3]):
            st = sf.render(l, True, TEXT_SECONDARY)
            self.screen.blit(st, (20, 408 + i * 20))

        # Instructions
        inst_y = 480
        Panel(15, inst_y, 275, 155, BG_TERTIARY, TEXT_MUTED).draw(self.screen)
        ih = get_font(SMALL_FONT_SIZE).render("How it works:", True, TEXT_COLOR)
        self.screen.blit(ih, (25, inst_y + 8))
        draw_instructions(self.screen, self.instructions, 22, inst_y + 30)

        # ── Grid ──────────────────────────────────────────────────────────────
        max_val = max(self.anim_revealed.values(), default=1) or 1

        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                rect = self._cell_rect(row, col)
                cell = (row, col)

                if cell == self.start:
                    bg = START_COLOR
                elif cell == self.goal:
                    bg = END_COLOR
                elif self.dp.grid[row][col] == 1:
                    bg = WALL_COLOR
                elif cell in self.path:
                    bg = PATH_FOUND_COLOR
                elif cell in self.anim_revealed:
                    bg = self._value_color(self.anim_revealed[cell], max_val)
                else:
                    bg = GRID_BG_COLOR

                pygame.draw.rect(self.screen, bg, rect)

                border_col = (255, 255, 80) if cell == self.highlight_cell else GRID_LINE_COLOR
                border_w   = 2              if cell == self.highlight_cell else 1
                pygame.draw.rect(self.screen, border_col, rect, border_w)

                # DP value text — only for non-wall, non-start/goal cells
                if cell not in (self.start, self.goal) and self.dp.grid[row][col] == 0:
                    if cell in self.anim_revealed:
                        v = self.anim_revealed[cell]
                        # pick font size so it fits in the cell
                        if v < 10:
                            fs = 16
                        elif v < 100:
                            fs = 14
                        elif v < 10000:
                            fs = 11
                        else:
                            fs = 9
                        vt = get_font(fs).render(str(v), True, TEXT_COLOR)
                        # clip text to cell
                        if vt.get_width() <= rect.width - 4:
                            self.screen.blit(vt, vt.get_rect(center=rect.center))

                # S / G label on start/goal
                if cell == self.start:
                    lt = get_font(16).render("S", True, TEXT_COLOR)
                    self.screen.blit(lt, lt.get_rect(center=rect.center))
                elif cell == self.goal:
                    lt = get_font(16).render("G", True, TEXT_COLOR)
                    self.screen.blit(lt, lt.get_rect(center=rect.center))

        # ── Stats bar ─────────────────────────────────────────────────────────
        grid_w    = self.GRID_COLS * self.cell_size
        grid_bot  = self.grid_y + self.GRID_ROWS * self.cell_size
        stats_y   = grid_bot + 8
        Panel(self.grid_x, stats_y, grid_w, 52, BG_SECONDARY, TEXT_MUTED).draw(self.screen)

        wall_count = sum(self.dp.grid[r][c]
                         for r in range(self.GRID_ROWS) for c in range(self.GRID_COLS))
        walkable   = self.GRID_ROWS * self.GRID_COLS - wall_count
        stat_parts = [
            f"Grid: {self.GRID_ROWS}x{self.GRID_COLS}",
            f"Walls: {wall_count}",
            f"Filled: {len(self.anim_revealed)}/{walkable}",
            f"Paths: {self.total_paths:,}" if self.solved else "Not solved",
        ]
        col_w = grid_w // len(stat_parts)
        for i, p in enumerate(stat_parts):
            tx = get_font(SMALL_FONT_SIZE).render(p, True, TEXT_SECONDARY)
            self.screen.blit(tx, (self.grid_x + 8 + i * col_w, stats_y + 17))

        # ── Legend ────────────────────────────────────────────────────────────
        leg_y  = stats_y + 60
        legend = [
            (START_COLOR,       "Start"),
            (END_COLOR,         "Goal"),
            (WALL_COLOR,        "Wall"),
            (PATH_FOUND_COLOR,  "Path"),
            ((59, 130, 246),    "DP value"),
        ]
        lx = self.grid_x
        for color, label in legend:
            pygame.draw.rect(self.screen, color, (lx, leg_y, 14, 14), border_radius=2)
            lt = get_font(12).render(label, True, TEXT_SECONDARY)
            self.screen.blit(lt, (lx + 18, leg_y + 1))
            lx += lt.get_width() + 36

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