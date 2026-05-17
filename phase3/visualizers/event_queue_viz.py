"""
Event Queue Simulator Visualizer with PyGame
Place in project root alongside test.py.

Features:
  - Add events with custom time, priority, description
  - Sort view by Time or Priority
  - Click any pending event to select it, then process just that one
  - Process Next (top of sorted order) or Process All
  - Demo pre-loads a realistic scenario
"""

import pygame
import sys
import os
import heapq

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, get_font
from phase3.event_queue import EventQueue


class EventQueueVisualizer:

    def __init__(self, screen):
        self.screen = screen
        self.clock  = pygame.time.Clock()
        self.running = True

        self.queue = EventQueue()

        # Sort mode: 'time' | 'priority'
        self.sort_mode = 'time'

        # Selected pending event (by event_id) for targeted processing
        self.selected_id = None

        # Last processed event highlight
        self.last_processed  = None
        self.highlight_timer = 0
        self.HIGHLIGHT_MS    = 1800

        self.setup_ui()
        self._load_demo()

    # ─── UI ──────────────────────────────────────────────────────────────────

    def setup_ui(self):
        # Input row
        self.time_input  = InputBox( 20, 160, 90,  36, "Time:",     numeric_only=True)
        self.prio_input  = InputBox(120, 160, 70,  36, "Priority:", numeric_only=True)
        self.desc_input  = InputBox(200, 160, 230, 36, "Desc:",     numeric_only=False)
        self.add_btn     = Button(440, 160, 100, 36, "Add",  SUCCESS_COLOR, "#059669",              font_size=14)

        # Sort toggles
        self.sort_time_btn = Button( 20, 208, 120, 34, "Sort: Time",     BUTTON_COLOR,           BUTTON_HOVER_COLOR,     font_size=13)
        self.sort_prio_btn = Button(148, 208, 140, 34, "Sort: Priority", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=13)

        # Controls
        self.process_sel_btn  = Button(300, 208, 160, 34, "Process Selected", WARNING_COLOR,  "#d97706",          font_size=13)
        self.process_next_btn = Button(468, 208, 130, 34, "Process Next",     BUTTON_COLOR,   BUTTON_HOVER_COLOR, font_size=13)
        self.process_all_btn  = Button(606, 208, 120, 34, "Process All",      INFO_COLOR,     BUTTON_HOVER_COLOR, font_size=13)

        self.demo_btn  = Button(734, 208, 80, 34, "Demo",  WARNING_COLOR,          "#d97706",              font_size=13)
        self.reset_btn = Button(822, 208, 80, 34, "Reset", DANGER_COLOR,           DANGER_HOVER_COLOR,     font_size=13)

        self.back_btn = Button(20, WINDOW_HEIGHT - 64, 130, 44,
                               "<- Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=14)

        self.status_label = Label(20, 252, "", SMALL_FONT_SIZE, TEXT_SECONDARY)

    # ─── Demo ────────────────────────────────────────────────────────────────

    def _load_demo(self):
        self.queue.reset()
        self.selected_id    = None
        self.last_processed = None
        events = [
            (0.0,  5, "Health Check #1"),
            (2.0,  3, "Compile Code"),
            (3.0,  1, "DEADLINE: Feature Freeze"),
            (5.0,  2, "Daily Standup"),
            (5.0,  4, "Compile Code End"),
            (8.0,  1, "DEADLINE: Sprint Review"),
            (10.0, 5, "Health Check #2"),
            (12.0, 4, "Deploy to Staging"),
            (15.0, 2, "Team Retrospective"),
            (20.0, 5, "Health Check #3"),
        ]
        for t, p, d in events:
            self.queue.add_event(t, p, d)
        self.status_label.set_text("Demo loaded. Click a pending event to select it.")

    # ─── Sorted view of pending ───────────────────────────────────────────────

    def _sorted_pending(self):
        pending = self.queue.get_pending_events()   # already sorted by (time, priority)
        if self.sort_mode == 'priority':
            pending = sorted(pending, key=lambda e: (e.priority, e.time))
        # sort_mode == 'time' keeps heap order (time, priority)
        return pending

    # ─── Processing ──────────────────────────────────────────────────────────

    def _process_next(self):
        """Process whichever event is first in the current sort order."""
        pending = self._sorted_pending()
        if not pending:
            self.status_label.set_text("Queue is empty.")
            return
        target = pending[0]
        self._remove_and_record(target)

    def _process_selected(self):
        if self.selected_id is None:
            self.status_label.set_text("No event selected. Click one in the left panel.")
            return
        pending = self._sorted_pending()
        target  = next((e for e in pending if e.event_id == self.selected_id), None)
        if target is None:
            self.status_label.set_text("Selected event no longer pending.")
            self.selected_id = None
            return
        self._remove_and_record(target)

    def _remove_and_record(self, event):
        """Pull a specific event out of the heap (by rebuilding it), record it."""
        # Remove from heap by rebuilding without the target
        new_heap = [e for e in self.queue.heap if e.event_id != event.event_id]
        heapq.heapify(new_heap)
        self.queue.heap = new_heap
        self.queue.current_time = max(self.queue.current_time, event.time)
        self.queue.processed_events.append(event)
        self.queue.event_history.append(('processed', event, self.queue.current_time))

        self.last_processed  = event
        self.highlight_timer = self.HIGHLIGHT_MS
        self.selected_id     = None
        self.status_label.set_text(
            f"Processed: '{event.description}'  t={event.time:.1f}  priority={event.priority}")

    def _process_all(self):
        count = 0
        last  = None
        for ev in self._sorted_pending():
            self.queue.processed_events.append(ev)
            self.queue.current_time = max(self.queue.current_time, ev.time)
            last  = ev
            count += 1
        self.queue.heap = []
        if count:
            self.last_processed  = last
            self.highlight_timer = self.HIGHLIGHT_MS
            self.selected_id     = None
            self.status_label.set_text(
                f"Processed all {count} events.  Sim time: {self.queue.current_time:.1f}")
        else:
            self.status_label.set_text("Queue was already empty.")

    def _add_event(self):
        t = self.time_input.get_value()  or 0
        p = self.prio_input.get_value()  or 5
        d = self.desc_input.get_text().strip() or "New Event"
        t = max(float(t), 0.0)
        try:
            self.queue.add_event(float(t), int(p), d)
            self.status_label.set_text(f"Added: '{d}'  t={t:.1f}  priority={p}")
            self.desc_input.set_text("")
        except Exception as e:
            self.status_label.set_text(str(e))

    # ─── Events ──────────────────────────────────────────────────────────────

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            self.time_input.handle_event(event, mouse_pos)
            self.prio_input.handle_event(event, mouse_pos)
            self.desc_input.handle_event(event, mouse_pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.add_btn.is_clicked(mouse_pos):
                    self._add_event()
                elif self.sort_time_btn.is_clicked(mouse_pos):
                    self.sort_mode = 'time'
                    self.status_label.set_text("Sorted by Time")
                elif self.sort_prio_btn.is_clicked(mouse_pos):
                    self.sort_mode = 'priority'
                    self.status_label.set_text("Sorted by Priority")
                elif self.process_sel_btn.is_clicked(mouse_pos):
                    self._process_selected()
                elif self.process_next_btn.is_clicked(mouse_pos):
                    self._process_next()
                elif self.process_all_btn.is_clicked(mouse_pos):
                    self._process_all()
                elif self.demo_btn.is_clicked(mouse_pos):
                    self._load_demo()
                elif self.reset_btn.is_clicked(mouse_pos):
                    self.queue.reset()
                    self.selected_id    = None
                    self.last_processed = None
                    self.status_label.set_text("Reset.")
                elif self.back_btn.is_clicked(mouse_pos):
                    return False
                else:
                    # Check if user clicked a pending-event card
                    self._check_card_click(mouse_pos)

        dt = self.clock.get_time()
        self.time_input.update(dt)
        self.prio_input.update(dt)
        self.desc_input.update(dt)

        if self.highlight_timer > 0:
            self.highlight_timer -= self.clock.get_time()

        return True

    def _check_card_click(self, mouse_pos):
        """See if the click landed on a pending-event card and select it."""
        for ev, rect in self._pending_card_rects:
            if rect.collidepoint(mouse_pos):
                if self.selected_id == ev.event_id:
                    self.selected_id = None   # toggle off
                    self.status_label.set_text("Selection cleared.")
                else:
                    self.selected_id = ev.event_id
                    self.status_label.set_text(
                        f"Selected: '{ev.description}'  t={ev.time:.1f}  P{ev.priority}")
                return

    # ─── Drawing ─────────────────────────────────────────────────────────────

    def _priority_color(self, p):
        palette = [
            (239,  68,  68),  # 1 red
            (245, 101,  66),
            (245, 158,  11),  # 3 amber
            (234, 179,   8),
            (132, 204,  22),  # 5 lime
            ( 34, 197,  94),  # 6 green
            ( 20, 184, 166),
            ( 59, 130, 246),  # 8 blue
            (139,  92, 246),  # 9 purple
            (100, 116, 139),  # 10 slate
        ]
        return palette[max(0, min(9, int(p) - 1))]

    def _draw_card(self, surface, ev, x, y, w, h, selected=False, processed=False):
        # Background tint
        pri_col = self._priority_color(ev.priority)
        bg = (*pri_col, 60 if not selected else 120)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, bg, (0, 0, w, h), border_radius=7)
        surface.blit(s, (x, y))

        border_w = 3 if selected else 1
        pygame.draw.rect(surface, pri_col if not processed else TEXT_MUTED,
                         (x, y, w, h), border_w, border_radius=7)

        # Priority badge
        badge = pygame.Rect(x + 5, y + 5, 30, 18)
        pygame.draw.rect(surface, pri_col, badge, border_radius=3)
        bt = get_font(11).render(f"P{ev.priority}", True, TEXT_COLOR)
        surface.blit(bt, bt.get_rect(center=badge.center))

        # Time
        tt = get_font(11).render(f"t={ev.time:.1f}", True, TEXT_SECONDARY)
        surface.blit(tt, (x + 40, y + 7))

        # ID
        idt = get_font(11).render(f"#{ev.event_id}", True, TEXT_MUTED)
        surface.blit(idt, idt.get_rect(right=x + w - 5, top=y + 7))

        # Description
        desc = ev.description if len(ev.description) <= 28 else ev.description[:26] + ".."
        txt_col = TEXT_MUTED if processed else TEXT_COLOR
        dt = get_font(13).render(desc, True, txt_col)
        surface.blit(dt, (x + 5, y + 26))

        # Selected indicator
        if selected:
            sel_t = get_font(11).render("SELECTED", True, WARNING_COLOR)
            surface.blit(sel_t, sel_t.get_rect(right=x + w - 5, bottom=y + h - 4))

    def draw(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # ── Title ─────────────────────────────────────────────────────────────
        tf = get_font(HEADING_FONT_SIZE)
        t  = tf.render("Event Queue Simulator", True, TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, 48)))
        sub = get_font(SMALL_FONT_SIZE).render(
            "Priority Queue  |  lower number = higher priority  |  click a card to select it",
            True, TEXT_MUTED)
        self.screen.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, 78)))

        # ── Control bar ───────────────────────────────────────────────────────
        Panel(10, 138, WINDOW_WIDTH - 20, 120, BG_SECONDARY, TEXT_MUTED).draw(self.screen)

        self.time_input.draw(self.screen)
        self.prio_input.draw(self.screen)
        self.desc_input.draw(self.screen)
        self.add_btn.draw(self.screen, mouse_pos)

        # Highlight active sort
        self.sort_time_btn.color = BUTTON_COLOR           if self.sort_mode == 'time'     else SECONDARY_BUTTON_COLOR
        self.sort_prio_btn.color = BUTTON_COLOR           if self.sort_mode == 'priority' else SECONDARY_BUTTON_COLOR
        self.sort_time_btn.draw(self.screen, mouse_pos)
        self.sort_prio_btn.draw(self.screen, mouse_pos)

        # Dim "Process Selected" when nothing selected
        self.process_sel_btn.set_enabled(self.selected_id is not None)
        self.process_sel_btn.draw(self.screen, mouse_pos)
        self.process_next_btn.draw(self.screen, mouse_pos)
        self.process_all_btn.draw(self.screen, mouse_pos)
        self.demo_btn.draw(self.screen, mouse_pos)
        self.reset_btn.draw(self.screen, mouse_pos)

        self.status_label.draw(self.screen)
        self.back_btn.draw(self.screen, mouse_pos)

        # ── Two columns ───────────────────────────────────────────────────────
        col_top  = 268
        col_h    = WINDOW_HEIGHT - col_top - 80
        col_w    = (WINDOW_WIDTH - 30) // 2

        # Left: Pending
        Panel(10, col_top, col_w, col_h, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        pending = self._sorted_pending()
        mode_str = "Time" if self.sort_mode == 'time' else "Priority"
        hdr = get_font(NORMAL_FONT_SIZE).render(
            f"Pending  ({len(pending)})  --  sorted by {mode_str}", True, TEXT_COLOR)
        self.screen.blit(hdr, (18, col_top + 8))

        card_h = 52
        gap    = 5
        max_cards = (col_h - 36) // (card_h + gap)

        self._pending_card_rects = []   # [(event, Rect)] for click detection
        clip_r = pygame.Rect(10, col_top + 32, col_w, col_h - 36)
        old_clip = self.screen.get_clip()
        self.screen.set_clip(clip_r)

        for i, ev in enumerate(pending[:max_cards]):
            cx = 14
            cy = col_top + 34 + i * (card_h + gap)
            cw = col_w - 8
            selected = (ev.event_id == self.selected_id)
            self._draw_card(self.screen, ev, cx, cy, cw, card_h, selected=selected)
            self._pending_card_rects.append((ev, pygame.Rect(cx, cy, cw, card_h)))

        self.screen.set_clip(old_clip)

        if len(pending) > max_cards:
            more = get_font(12).render(f"+ {len(pending)-max_cards} more", True, TEXT_MUTED)
            self.screen.blit(more, (18, col_top + col_h - 18))

        if not pending:
            emp = get_font(SMALL_FONT_SIZE).render("Queue is empty", True, TEXT_MUTED)
            self.screen.blit(emp, emp.get_rect(center=(10 + col_w//2, col_top + col_h//2)))

        # Right: Processed
        rx = 20 + col_w
        Panel(rx, col_top, col_w, col_h, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        processed = list(reversed(self.queue.get_processed_events()))
        hdr2 = get_font(NORMAL_FONT_SIZE).render(
            f"Processed  ({len(processed)})  --  most recent first", True, TEXT_COLOR)
        self.screen.blit(hdr2, (rx + 8, col_top + 8))

        self.screen.set_clip(pygame.Rect(rx, col_top + 32, col_w, col_h - 36))
        for i, ev in enumerate(processed[:max_cards]):
            cx = rx + 4
            cy = col_top + 34 + i * (card_h + gap)
            cw = col_w - 8
            highlight = (self.last_processed and
                         ev.event_id == self.last_processed.event_id and
                         self.highlight_timer > 0)
            self._draw_card(self.screen, ev, cx, cy, cw, card_h,
                            selected=highlight, processed=not highlight)
        self.screen.set_clip(old_clip)

        if not processed:
            emp2 = get_font(SMALL_FONT_SIZE).render("Nothing processed yet", True, TEXT_MUTED)
            self.screen.blit(emp2, emp2.get_rect(center=(rx + col_w//2, col_top + col_h//2)))

        # ── Stats strip ───────────────────────────────────────────────────────
        stats_y = col_top + col_h + 6
        Panel(10, stats_y, WINDOW_WIDTH - 20, 36, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        sf = get_font(SMALL_FONT_SIZE)
        parts = [
            f"Sim Time: {self.queue.current_time:.1f}",
            f"Pending: {len(pending)}",
            f"Processed: {len(self.queue.get_processed_events())}",
            f"Total added: {self.queue.next_event_id - 1}",
            f"Selected: #{self.selected_id}" if self.selected_id else "Selected: none",
        ]
        col_step = (WINDOW_WIDTH - 40) // len(parts)
        for i, p in enumerate(parts):
            tx = sf.render(p, True, TEXT_SECONDARY)
            self.screen.blit(tx, (18 + i * col_step, stats_y + 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            if not self.handle_events():
                break
            self.draw()
        return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Event Queue Simulator")
    EventQueueVisualizer(screen).run()
    pygame.quit()


if __name__ == "__main__":
    main()