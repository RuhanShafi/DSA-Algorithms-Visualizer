"""
Event Queue Simulator Visualizer with PyGame
Interactive visualization of priority-queue based event scheduling
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import *
from utils.ui_components import Button, InputBox, Label, Panel, draw_instructions, draw_stats, get_font
from phase3.event_queue import EventQueue, EventSimulator


class EventQueueVisualizer:
    """Interactive event queue / priority queue visualization"""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.simulator = EventSimulator()
        self.queue = self.simulator.get_queue()

        # Track visual state
        self.last_processed = None
        self.highlight_timer = 0
        self.highlight_duration = 1500  # ms

        self.setup_ui()
        self._load_demo_events()

    def _load_demo_events(self):
        """Pre-load some demo events so the screen isn't empty"""
        self.simulator.schedule_task(2.0, 3.0, "Compile Code", priority=3)
        self.simulator.schedule_meeting(5.0, 1.0, "Daily Standup", priority=2)
        self.simulator.schedule_deadline(8.0, "Sprint Review", priority=1)
        self.simulator.schedule_recurring(0.0, 10.0, 3, "Health Check", priority=5)

    def setup_ui(self):
        # Input fields
        self.time_input = InputBox(30, 165, 100, 36, "Time:", numeric_only=True)
        self.priority_input = InputBox(145, 165, 80, 36, "Priority:", numeric_only=True)
        self.desc_input = InputBox(240, 165, 200, 36, "Description:", numeric_only=False)

        # Buttons
        self.add_btn = Button(455, 165, 110, 36, "Add Event", SUCCESS_COLOR, "#059669", font_size=14)
        self.process_btn = Button(30, 215, 160, 40, "▶ Process Next", BUTTON_COLOR, BUTTON_HOVER_COLOR, font_size=14)
        self.process_all_btn = Button(200, 215, 160, 40, "⏩ Process All", INFO_COLOR, BUTTON_HOVER_COLOR, font_size=14)
        self.reset_btn = Button(370, 215, 100, 40, "Reset", DANGER_COLOR, DANGER_HOVER_COLOR, font_size=14)
        self.demo_btn = Button(480, 215, 100, 40, "Demo", WARNING_COLOR, "#d97706", font_size=14)
        self.back_btn = Button(30, 820, 130, 44, "← Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=14)

        self.status_label = Label(30, 268, "", SMALL_FONT_SIZE, TEXT_SECONDARY)

        self.instructions = [
            "Add events with time, priority & description",
            "Lower priority number = processed first",
            "Events at same time sorted by priority",
            "Process Next: advance simulation one step",
            "Process All: run entire simulation",
        ]

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            self.time_input.handle_event(event, mouse_pos)
            self.priority_input.handle_event(event, mouse_pos)
            self.desc_input.handle_event(event, mouse_pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.add_btn.is_clicked(mouse_pos):
                    self._add_event()
                elif self.process_btn.is_clicked(mouse_pos):
                    self._process_next()
                elif self.process_all_btn.is_clicked(mouse_pos):
                    self._process_all()
                elif self.reset_btn.is_clicked(mouse_pos):
                    self._reset()
                elif self.demo_btn.is_clicked(mouse_pos):
                    self._reset()
                    self._load_demo_events()
                    self.status_label.set_text("Demo events loaded!")
                elif self.back_btn.is_clicked(mouse_pos):
                    return False

        dt = self.clock.get_time()
        self.time_input.update(dt)
        self.priority_input.update(dt)
        self.desc_input.update(dt)

        if self.highlight_timer > 0:
            self.highlight_timer -= self.clock.get_time()
            if self.highlight_timer <= 0:
                self.last_processed = None

        return True

    def _add_event(self):
        t = self.time_input.get_value() or 0
        p = self.priority_input.get_value() or 5
        d = self.desc_input.get_text().strip() or "New Event"
        t = max(float(t), self.queue.current_time)
        try:
            self.queue.add_event(float(t), int(p), d)
            self.status_label.set_text(f"Added: '{d}' at t={t:.1f} (priority {p})")
            self.desc_input.set_text("")
        except Exception as e:
            self.status_label.set_text(str(e))

    def _process_next(self):
        ev = self.queue.process_next_event()
        if ev:
            self.last_processed = ev
            self.highlight_timer = self.highlight_duration
            self.status_label.set_text(
                f"Processed: '{ev.description}' at t={ev.time:.1f} (priority {ev.priority})"
            )
        else:
            self.status_label.set_text("Queue is empty — nothing to process.")

    def _process_all(self):
        count = 0
        last = None
        while not self.queue.is_empty():
            last = self.queue.process_next_event()
            count += 1
        if count:
            self.last_processed = last
            self.highlight_timer = self.highlight_duration
            self.status_label.set_text(f"Processed all {count} events. Final time: {self.queue.current_time:.1f}")
        else:
            self.status_label.set_text("Queue was already empty.")

    def _reset(self):
        self.queue.reset()
        self.last_processed = None
        self.highlight_timer = 0
        self.status_label.set_text("Simulator reset.")

    # ── Drawing ──────────────────────────────────────────────────────────

    def _color_for_priority(self, priority):
        """Map priority 1-10 to a color (1=red/urgent, 10=gray/low)"""
        colors = [
            (239, 68, 68),   # 1 - red
            (245, 101, 66),  # 2
            (245, 158, 11),  # 3 - amber
            (234, 179, 8),   # 4
            (132, 204, 22),  # 5 - lime
            (34, 197, 94),   # 6 - green
            (20, 184, 166),  # 7 - teal
            (59, 130, 246),  # 8 - blue
            (139, 92, 246),  # 9 - purple
            (100, 116, 139), # 10 - slate
        ]
        idx = max(0, min(9, priority - 1))
        return colors[idx]

    def _draw_event_card(self, surface, ev, x, y, w, h, highlight=False, processed=False):
        alpha_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pri_color = self._color_for_priority(ev.priority)
        bg_color = (pri_color[0], pri_color[1], pri_color[2], 40 if not highlight else 90)
        border_color = pri_color

        pygame.draw.rect(alpha_surf, bg_color, (0, 0, w, h), border_radius=8)
        surface.blit(alpha_surf, (x, y))
        pygame.draw.rect(surface, border_color, (x, y, w, h), 2, border_radius=8)

        if processed:
            pygame.draw.line(surface, TEXT_MUTED, (x + 8, y + h // 2), (x + w - 8, y + h // 2), 1)

        font_sm = get_font(12)
        font_md = get_font(14)

        # Priority badge
        badge_r = pygame.Rect(x + 6, y + 6, 28, 20)
        pygame.draw.rect(surface, border_color, badge_r, border_radius=4)
        pri_txt = font_sm.render(f"P{ev.priority}", True, TEXT_COLOR)
        surface.blit(pri_txt, pri_txt.get_rect(center=badge_r.center))

        # Time
        time_txt = font_sm.render(f"t={ev.time:.1f}", True, TEXT_SECONDARY)
        surface.blit(time_txt, (x + 40, y + 8))

        # Description
        desc = ev.description
        if len(desc) > 30:
            desc = desc[:28] + "…"
        desc_txt = font_md.render(desc, True, TEXT_COLOR if not processed else TEXT_MUTED)
        surface.blit(desc_txt, (x + 6, y + 30))

        # ID tag
        id_txt = font_sm.render(f"#{ev.event_id}", True, TEXT_MUTED)
        surface.blit(id_txt, id_txt.get_rect(right=x + w - 6, top=y + 8))

    def draw(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Title
        tfont = get_font(HEADING_FONT_SIZE)
        t = tfont.render("Event Queue Simulator", True, TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, 55)))
        sub = get_font(SMALL_FONT_SIZE).render(
            "Priority Queue — lower number = higher priority", True, TEXT_MUTED)
        self.screen.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, 85)))

        # Control panel
        Panel(20, 140, WINDOW_WIDTH - 40, 175, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        self.time_input.draw(self.screen)
        self.priority_input.draw(self.screen)
        self.desc_input.draw(self.screen)
        self.add_btn.draw(self.screen, mouse_pos)
        self.process_btn.draw(self.screen, mouse_pos)
        self.process_all_btn.draw(self.screen, mouse_pos)
        self.reset_btn.draw(self.screen, mouse_pos)
        self.demo_btn.draw(self.screen, mouse_pos)
        self.status_label.draw(self.screen)

        # ── Pending events column ──
        col_x = 20
        col_y = 295
        col_w = (WINDOW_WIDTH - 60) // 2
        col_h = WINDOW_HEIGHT - col_y - 80

        Panel(col_x, col_y, col_w, col_h, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        hdr = get_font(NORMAL_FONT_SIZE)
        pending = self.queue.get_pending_events()
        hdr_t = hdr.render(f"Pending Events  ({len(pending)})", True, TEXT_COLOR)
        self.screen.blit(hdr_t, (col_x + 12, col_y + 10))

        card_h = 60
        gap = 6
        visible = (col_h - 40) // (card_h + gap)
        clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(col_x, col_y + 36, col_w, col_h - 40))
        for i, ev in enumerate(pending[:visible]):
            cx = col_x + 8
            cy = col_y + 38 + i * (card_h + gap)
            self._draw_event_card(self.screen, ev, cx, cy, col_w - 16, card_h)
        if len(pending) > visible:
            more = get_font(12).render(f"+ {len(pending) - visible} more…", True, TEXT_MUTED)
            self.screen.blit(more, (col_x + 12, col_y + col_h - 20))
        self.screen.set_clip(clip)

        # Empty queue message
        if not pending:
            empty = get_font(SMALL_FONT_SIZE).render("Queue is empty", True, TEXT_MUTED)
            self.screen.blit(empty, empty.get_rect(center=(col_x + col_w // 2, col_y + col_h // 2)))

        # ── Processed events column ──
        col2_x = col_x + col_w + 20
        col2_w = col_w
        Panel(col2_x, col_y, col2_w, col_h, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        processed_events = self.queue.get_processed_events()
        hdr2 = hdr.render(f"Processed  ({len(processed_events)})", True, TEXT_COLOR)
        self.screen.blit(hdr2, (col2_x + 12, col_y + 10))

        self.screen.set_clip(pygame.Rect(col2_x, col_y + 36, col2_w, col_h - 40))
        show = list(reversed(processed_events))  # most recent first
        for i, ev in enumerate(show[:visible]):
            is_last = (self.last_processed and ev.event_id == self.last_processed.event_id
                       and self.highlight_timer > 0)
            cx = col2_x + 8
            cy = col_y + 38 + i * (card_h + gap)
            self._draw_event_card(self.screen, ev, cx, cy, col2_w - 16, card_h,
                                  highlight=is_last, processed=True)
        self.screen.set_clip(clip)

        if not processed_events:
            empty2 = get_font(SMALL_FONT_SIZE).render("No events processed yet", True, TEXT_MUTED)
            self.screen.blit(empty2, empty2.get_rect(center=(col2_x + col2_w // 2, col_y + col_h // 2)))

        # ── Stats strip ──
        stats_y = col_y + col_h + 8
        Panel(20, stats_y, WINDOW_WIDTH - 40, 44, BG_SECONDARY, TEXT_MUTED).draw(self.screen)
        sf = get_font(SMALL_FONT_SIZE)
        parts = [
            f"Simulation Time: {self.queue.current_time:.1f}",
            f"Pending: {self.queue.size()}",
            f"Processed: {len(self.queue.get_processed_events())}",
            f"Total Events: {self.queue.next_event_id - 1}",
        ]
        for i, p in enumerate(parts):
            tx = sf.render(p, True, TEXT_SECONDARY)
            self.screen.blit(tx, (30 + i * 340, stats_y + 14))

        # Instructions side panel
        inst_y = col_y
        inst_x = WINDOW_WIDTH - 20  # we'll use full width above, instructions embedded
        # (instructions shown in status bar area instead for this wide layout)

        self.back_btn.draw(self.screen, mouse_pos)

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
