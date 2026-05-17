"""
Heap Visualizer with PyGame  — fixed layout
Place in phase2/visualizers/heap_viz.py
"""

import pygame
import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, draw_instructions, draw_stats, get_font
from phase2.heap import MinHeap, MaxHeap


class HeapVisualizer:

    # Tree area: sits in the right 2/3 of the screen
    TREE_X = 330
    TREE_Y = 160
    TREE_W = WINDOW_WIDTH - 340
    TREE_H = 520   # fixed height for tree

    # Array area: directly below the tree
    ARRAY_Y_OFFSET = 20   # gap between tree bottom and array bar

    NODE_R = 24    # node circle radius

    def __init__(self, screen):
        self.screen = screen
        self.clock  = pygame.time.Clock()
        self.running = True

        self.heap_type = 'min'
        self.heap = MinHeap(max_size=15)

        self.animating = False
        self.animation_generator = None
        self.current_state = None
        self.animation_delay = 500
        self.timer = 0

        self.setup_ui()

    def setup_ui(self):
        bx, bw, bh = 20, 290, 40

        self.value_input = InputBox(bx, 165, 140, bh, "Value:", numeric_only=True)

        self.insert_btn  = Button(bx,       215, bw, bh, "Insert",       SUCCESS_COLOR,          "#059669",              font_size=14)
        self.extract_btn = Button(bx,       263, bw, bh, "Extract Root", DANGER_COLOR,           DANGER_HOVER_COLOR,     font_size=14)
        self.peek_btn    = Button(bx,       311, bw, bh, "Peek Root",    INFO_COLOR,             BUTTON_HOVER_COLOR,     font_size=14)
        self.clear_btn   = Button(bx,       359, bw, bh, "Clear",        WARNING_COLOR,          "#d97706",              font_size=14)

        self.min_heap_btn = Button(bx,      415, (bw-10)//2, bh, "Min-Heap", BUTTON_COLOR,           BUTTON_HOVER_COLOR,     font_size=14)
        self.max_heap_btn = Button(bx+(bw-10)//2+10, 415, (bw-10)//2, bh, "Max-Heap", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=14)

        self.back_btn = Button(bx, WINDOW_HEIGHT - 70, bw, 44, "<- Back",
                               SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=14)

        self.status_label = Label(bx, 475, "", SMALL_FONT_SIZE, TEXT_SECONDARY)

        self.instructions = [
            "Insert: add value, bubbles up",
            "Extract Root: removes min/max",
            "Peek: view root without removing",
            "Min-Heap: parent <= children",
            "Max-Heap: parent >= children",
            "Highlighted = nodes being compared",
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

            self.value_input.handle_event(event, mouse_pos)

            if event.type == pygame.MOUSEBUTTONDOWN and not self.animating:
                value = self.value_input.get_value()

                if self.insert_btn.is_clicked(mouse_pos):
                    if self.value_input.get_text().strip():
                        try:
                            self.animation_generator = self.heap.insert(value)
                            self.animating = True
                            self.status_label.set_text(f"Inserting {value}...")
                            self.value_input.set_text("")
                        except OverflowError as e:
                            self.status_label.set_text(str(e))
                    else:
                        self.status_label.set_text("Enter a value first.")

                elif self.extract_btn.is_clicked(mouse_pos):
                    try:
                        if self.heap_type == 'min':
                            self.animation_generator = self.heap.extract_min()
                        else:
                            self.animation_generator = self.heap.extract_max()
                        self.animating = True
                        self.status_label.set_text("Extracting root...")
                    except IndexError as e:
                        self.status_label.set_text(str(e))

                elif self.peek_btn.is_clicked(mouse_pos):
                    v = self.heap.peek()
                    self.status_label.set_text(
                        f"Root: {v}" if v is not None else "Heap is empty.")

                elif self.clear_btn.is_clicked(mouse_pos):
                    self.heap.clear()
                    self.current_state = None
                    self.status_label.set_text("Cleared.")

                elif self.min_heap_btn.is_clicked(mouse_pos):
                    if self.heap.is_empty():
                        self.heap_type = 'min'
                        self.heap = MinHeap(max_size=15)
                        self.status_label.set_text("Switched to Min-Heap.")
                    else:
                        self.status_label.set_text("Clear the heap first to switch type.")

                elif self.max_heap_btn.is_clicked(mouse_pos):
                    if self.heap.is_empty():
                        self.heap_type = 'max'
                        self.heap = MaxHeap(max_size=15)
                        self.status_label.set_text("Switched to Max-Heap.")
                    else:
                        self.status_label.set_text("Clear the heap first to switch type.")

                elif self.back_btn.is_clicked(mouse_pos):
                    return False

        self.value_input.update(self.clock.get_time())
        return True

    def update(self, dt):
        if not self.animating or not self.animation_generator:
            return
        self.timer += dt
        if self.timer < self.animation_delay:
            return
        self.timer = 0
        try:
            result = next(self.animation_generator)
            if len(result) == 2:
                _, state = result
                extracted = None
            else:
                _, state, extracted = result
            self.current_state = state
            if state['phase'] == 'complete':
                self.animating = False
                if extracted is not None:
                    self.status_label.set_text(f"Extracted: {extracted}")
                else:
                    self.status_label.set_text("Done.")
        except StopIteration:
            self.animating = False

    # ─── Tree drawing ─────────────────────────────────────────────────────────

    def _tree_positions(self):
        """Return dict {index: (x, y)} for each node in the heap."""
        size = self.heap.get_size()
        if size == 0:
            return {}

        positions = {}
        for i in range(size):
            level      = int(math.log2(i + 1))
            pos_in_lvl = i - (2 ** level - 1)
            nodes_in_lvl = 2 ** level

            # Horizontal span shrinks with depth
            usable_w = self.TREE_W - 2 * self.NODE_R
            x_spacing = usable_w / nodes_in_lvl
            x = self.TREE_X + self.NODE_R + x_spacing * (pos_in_lvl + 0.5)
            y = self.TREE_Y + level * 90 + self.NODE_R
            positions[i] = (int(x), int(y))

        return positions

    def draw_tree(self):
        arr  = self.heap.get_array()
        size = self.heap.get_size()
        if size == 0:
            empty = get_font(NORMAL_FONT_SIZE).render(
                "Heap is empty -- insert values to begin", True, TEXT_MUTED)
            self.screen.blit(empty, empty.get_rect(
                center=(self.TREE_X + self.TREE_W // 2,
                        self.TREE_Y + self.TREE_H // 2)))
            return

        pos = self._tree_positions()

        # Edges
        for i in range(size):
            for child in (2*i+1, 2*i+2):
                if child < size:
                    pygame.draw.line(self.screen, TEXT_MUTED, pos[i], pos[child], 2)

        # Nodes
        comparing = set()
        if self.current_state and 'comparing_indices' in self.current_state:
            comparing = set(self.current_state['comparing_indices'])

        for i in range(size):
            x, y = pos[i]
            color = COMPARING_COLOR if i in comparing else HEAP_COLOR
            pygame.draw.circle(self.screen, color, (x, y), self.NODE_R)
            pygame.draw.circle(self.screen, TEXT_COLOR, (x, y), self.NODE_R, 2)

            v   = str(arr[i])
            fs  = 16 if len(v) <= 2 else 13 if len(v) <= 4 else 10
            vt  = get_font(fs).render(v, True, TEXT_COLOR)
            # clip text width to node diameter
            if vt.get_width() > self.NODE_R * 2 - 4:
                vt = get_font(10).render(v, True, TEXT_COLOR)
            self.screen.blit(vt, vt.get_rect(center=(x, y)))

    # ─── Array bar ────────────────────────────────────────────────────────────

    def draw_array(self):
        arr  = self.heap.get_array()
        size = self.heap.get_size()

        # Position: directly below the tree area, within right panel
        array_y = self.TREE_Y + self.TREE_H + self.ARRAY_Y_OFFSET
        avail_w = self.TREE_W

        if size == 0:
            return

        # Box size: fit all boxes in available width, max box = 60, min = 28
        raw_box = min(60, avail_w // max(size, 1))
        box_w   = max(28, raw_box)
        box_h   = 40
        gap     = 4
        total_w = size * (box_w + gap) - gap
        start_x = self.TREE_X + (avail_w - total_w) // 2

        # Section label
        lbl = get_font(SMALL_FONT_SIZE).render("Array representation:", True, TEXT_COLOR)
        self.screen.blit(lbl, (self.TREE_X, array_y - 22))

        comparing = set()
        if self.current_state and 'comparing_indices' in self.current_state:
            comparing = set(self.current_state['comparing_indices'])

        for i in range(size):
            x    = start_x + i * (box_w + gap)
            rect = pygame.Rect(x, array_y, box_w, box_h)

            color = COMPARING_COLOR if i in comparing else BG_TERTIARY
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            pygame.draw.rect(self.screen, TEXT_MUTED, rect, 1, border_radius=4)

            # Value — pick font so it fits inside box_w - 6 px
            v  = str(arr[i])
            fs = 14 if len(v) <= 2 else 12 if len(v) <= 4 else 10
            vt = get_font(fs).render(v, True, TEXT_COLOR)
            while vt.get_width() > box_w - 4 and fs > 8:
                fs -= 1
                vt = get_font(fs).render(v, True, TEXT_COLOR)
            self.screen.blit(vt, vt.get_rect(center=rect.center))

            # Index below box
            idx = get_font(11).render(str(i), True, TEXT_MUTED)
            self.screen.blit(idx, idx.get_rect(center=(x + box_w // 2, array_y + box_h + 10)))

    # ─── Main draw ────────────────────────────────────────────────────────────

    def draw(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Title
        heap_name = "Min-Heap" if self.heap_type == 'min' else "Max-Heap"
        tf = get_font(TITLE_FONT_SIZE)
        t  = tf.render(f"{heap_name} Visualizer", True, TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, 60)))

        # Left panel
        Panel(10, 140, 315, WINDOW_HEIGHT - 155, BG_SECONDARY, TEXT_MUTED).draw(self.screen)

        self.value_input.draw(self.screen)
        self.insert_btn.draw(self.screen, mouse_pos)
        self.extract_btn.draw(self.screen, mouse_pos)
        self.peek_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)

        # Heap type highlight
        if self.heap_type == 'min':
            self.min_heap_btn.color = BUTTON_COLOR
            self.max_heap_btn.color = SECONDARY_BUTTON_COLOR
        else:
            self.min_heap_btn.color = SECONDARY_BUTTON_COLOR
            self.max_heap_btn.color = BUTTON_COLOR
        self.min_heap_btn.draw(self.screen, mouse_pos)
        self.max_heap_btn.draw(self.screen, mouse_pos)

        self.status_label.draw(self.screen)

        # Instructions
        inst_y = 530
        Panel(15, inst_y, 305, 160, BG_TERTIARY, TEXT_MUTED).draw(self.screen)
        ih = get_font(SMALL_FONT_SIZE).render("Instructions:", True, TEXT_COLOR)
        self.screen.blit(ih, (25, inst_y + 8))
        draw_instructions(self.screen, self.instructions, 22, inst_y + 30)

        self.back_btn.draw(self.screen, mouse_pos)

        # Stats
        stats_y = 700
        Panel(15, stats_y, 305, 120, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        st = get_font(SMALL_FONT_SIZE).render("Stats:", True, TEXT_COLOR)
        self.screen.blit(st, (25, stats_y + 8))
        draw_stats(self.screen, {
            "Type":  heap_name,
            "Size":  f"{self.heap.get_size()} / {self.heap.max_size}",
            "Empty": "Yes" if self.heap.is_empty() else "No",
            "Root":  str(self.heap.peek()) if not self.heap.is_empty() else "N/A",
        }, 25, stats_y + 28)

        # Right panel background
        Panel(self.TREE_X - 5, 140, self.TREE_W + 10, WINDOW_HEIGHT - 155,
              BG_SECONDARY, TEXT_MUTED).draw(self.screen)

        self.draw_tree()
        self.draw_array()

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
    pygame.display.set_caption("Heap Visualizer")
    HeapVisualizer(screen).run()
    pygame.quit()


if __name__ == "__main__":
    main()