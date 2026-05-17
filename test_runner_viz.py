"""
In-App Test Runner
Place in project root alongside test.py.

Shows:
  - Live streaming test results (pass/fail per test)
  - Full terminal-style unittest output appended at the end
"""

import pygame
import sys
import os
import unittest
import importlib.util
import threading
import time
import io

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from config import *
from utils.ui_components import Button, Panel, get_font


# ── Module loader (no __init__.py required) ───────────────────────────────────

def _load_module(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Coloured line ─────────────────────────────────────────────────────────────

class TestLine:
    def __init__(self, text, color=None):
        self.text  = text
        self.color = color or TEXT_COLOR


# ── Custom result collector ───────────────────────────────────────────────────

class UITestResult(unittest.TestResult):
    def __init__(self, lines):
        super().__init__()
        self.lines = lines

    def startTest(self, test):
        super().startTest(test)
        self.lines.append(TestLine(
            f"  o  {type(test).__name__}.{test._testMethodName}",
            TEXT_SECONDARY))

    def addSuccess(self, test):
        super().addSuccess(test)
        if self.lines:
            self.lines[-1] = TestLine(
                self.lines[-1].text.replace("  o  ", "  v  "), SUCCESS_COLOR)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.lines:
            self.lines[-1] = TestLine(
                self.lines[-1].text.replace("  o  ", "  x  "), DANGER_COLOR)
        self.lines.append(TestLine(
            f"      -> {str(err[1]).splitlines()[0][:100]}", DANGER_COLOR))

    def addError(self, test, err):
        super().addError(test, err)
        if self.lines:
            self.lines[-1] = TestLine(
                self.lines[-1].text.replace("  o  ", "  !  "), WARNING_COLOR)
        self.lines.append(TestLine(
            f"      -> {str(err[1]).splitlines()[0][:100]}", WARNING_COLOR))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.lines:
            self.lines[-1] = TestLine(
                self.lines[-1].text.replace("  o  ", "  -  "), TEXT_MUTED)


# ── Test class registry ───────────────────────────────────────────────────────

_PHASE_CLASSES = {
    1: [
        ("TestStack",            "tests/test_phase1.py"),
        ("TestQueue",            "tests/test_phase1.py"),
        ("TestLinkedList",       "tests/test_phase1.py"),
        ("TestBinarySearchTree", "tests/test_phase1.py"),
        ("TestPerformance",      "tests/test_phase1.py"),
    ],
    2: [
        ("TestSorting",          "tests/test_phase2.py"),
        ("TestGraph",            "tests/test_phase2.py"),
        ("TestGraphTraversal",   "tests/test_phase2.py"),
        ("TestMinHeap",          "tests/test_phase2.py"),
        ("TestMaxHeap",          "tests/test_phase2.py"),
        ("TestPerformance",      "tests/test_phase2.py"),
    ],
    3: [
        ("TestPathfinding",         "tests/test_phase3.py"),
        ("TestEventQueue",          "tests/test_phase3.py"),
        ("TestEventSimulator",      "tests/test_phase3.py"),
        ("TestGridPathDP",          "tests/test_phase3.py"),
        ("TestGridPathWithWeights", "tests/test_phase3.py"),
        ("TestPerformance",         "tests/test_phase3.py"),
    ],
}


# ── Background worker ─────────────────────────────────────────────────────────

def _run_suite(phase, lines, done_flag):
    lines.clear()
    lines.append(TestLine(f"  Loading Phase {phase} tests...", TEXT_SECONDARY))

    entries = _PHASE_CLASSES.get(phase, [])
    if not entries:
        lines.append(TestLine("  Unknown phase.", DANGER_COLOR))
        done_flag[0] = True
        return

    # Load test files
    loaded = {}
    for cls_name, rel in entries:
        if rel in loaded:
            continue
        abs_path = os.path.join(_ROOT, rel)
        if not os.path.isfile(abs_path):
            lines.append(TestLine(f"  ERROR: file not found: {abs_path}", DANGER_COLOR))
            done_flag[0] = True
            return
        try:
            mod_name = rel.replace("/", "_").replace("\\", "_").replace(".py", "")
            loaded[rel] = _load_module(mod_name, abs_path)
        except Exception as e:
            lines.append(TestLine(f"  ERROR loading {rel}: {e}", DANGER_COLOR))
            done_flag[0] = True
            return

    # Build suite
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()
    last_rel = None
    for cls_name, rel in entries:
        if rel != last_rel:
            lines.append(TestLine(""))
            lines.append(TestLine(f"  -- {rel} --", INFO_COLOR))
            last_rel = rel
        mod = loaded[rel]
        cls = getattr(mod, cls_name, None)
        if cls is None:
            lines.append(TestLine(f"  ! {cls_name} not found", WARNING_COLOR))
            continue
        lines.append(TestLine(f"  [ {cls_name} ]", TEXT_SECONDARY))
        suite.addTests(loader.loadTestsFromTestCase(cls))

    lines.append(TestLine(""))

    # ── Run with UI collector ─────────────────────────────────────────────────
    ui_result = UITestResult(lines)
    t0 = time.time()
    suite.run(ui_result)
    elapsed = time.time() - t0

    passed = ui_result.testsRun - len(ui_result.failures) - len(ui_result.errors)
    ok     = not ui_result.failures and not ui_result.errors
    scol   = SUCCESS_COLOR if ok else DANGER_COLOR
    word   = "ALL PASSED" if ok else "SOME FAILED"

    lines.append(TestLine(""))
    lines.append(TestLine("  " + "=" * 62, TEXT_MUTED))
    lines.append(TestLine(
        f"  {word}   Tests:{ui_result.testsRun}  Passed:{passed}  "
        f"Failed:{len(ui_result.failures)}  Errors:{len(ui_result.errors)}  "
        f"Time:{elapsed:.2f}s",
        scol))
    lines.append(TestLine("  " + "=" * 62, TEXT_MUTED))

    # ── Re-run with standard TextTestRunner → capture terminal output ─────────
    lines.append(TestLine(""))
    lines.append(TestLine("  -- Raw unittest output (verbosity=2) --", INFO_COLOR))

    buf    = io.StringIO()
    suite2 = unittest.TestSuite()    # rebuild (generators are exhausted)
    for cls_name, rel in entries:
        mod = loaded.get(rel)
        if mod is None:
            continue
        cls = getattr(mod, cls_name, None)
        if cls:
            suite2.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(stream=buf, verbosity=2)
    runner.run(suite2)

    raw = buf.getvalue()
    for raw_line in raw.splitlines():
        # colour dot/E/F markers
        stripped = raw_line.rstrip()
        if stripped.endswith(" ... ok"):
            col = SUCCESS_COLOR
        elif " ... FAIL" in stripped or " ... ERROR" in stripped:
            col = DANGER_COLOR
        elif stripped.startswith("FAIL:") or stripped.startswith("ERROR:"):
            col = DANGER_COLOR
        elif stripped.startswith("OK") or stripped.startswith("Ran "):
            col = SUCCESS_COLOR
        else:
            col = TEXT_SECONDARY
        lines.append(TestLine("  " + stripped, col))

    done_flag[0] = True


# ── Visualizer ────────────────────────────────────────────────────────────────

class TestRunnerVisualizer:

    def __init__(self, screen, phase):
        self.screen = screen
        self.phase  = phase
        self.clock  = pygame.time.Clock()
        self.running = True

        self.lines         = []
        self.scroll_offset = 0
        self.running_tests = False
        self.done_flag     = [False]
        self._thread       = None

        self.font_mono = get_font(SMALL_FONT_SIZE)
        self.line_h    = 20

        self.panel_x = 20
        self.panel_y = 108
        self.panel_w = WINDOW_WIDTH - 40
        self.panel_h = WINDOW_HEIGHT - 188

        self._setup_ui()

    def _setup_ui(self):
        self.run_btn = Button(
            20, 50, 230, 42,
            f"Run Phase {self.phase} Tests",
            SUCCESS_COLOR, "#059669", font_size=15)
        self.clear_btn = Button(
            260, 50, 110, 42,
            "Clear", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=15)
        self.back_btn = Button(
            WINDOW_WIDTH - 155, 50, 135, 42,
            "<- Back", SECONDARY_BUTTON_COLOR, SECONDARY_BUTTON_HOVER, font_size=15)

    def _start_tests(self):
        if self.running_tests:
            return
        self.lines.clear()
        self.scroll_offset = 0
        self.done_flag[0]  = False
        self.running_tests = True
        self._thread = threading.Thread(
            target=_run_suite,
            args=(self.phase, self.lines, self.done_flag),
            daemon=True)
        self._thread.start()

    def _max_scroll(self):
        return max(0, len(self.lines) * self.line_h - self.panel_h + 20)

    def _scroll(self, delta):
        self.scroll_offset = max(0, min(self._max_scroll(),
                                        self.scroll_offset + delta))

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_UP:
                    self._scroll(-self.line_h * 3)
                elif event.key == pygame.K_DOWN:
                    self._scroll(self.line_h * 3)
                elif event.key == pygame.K_HOME:
                    self.scroll_offset = 0
                elif event.key == pygame.K_END:
                    self._scroll(99999)
            if event.type == pygame.MOUSEWHEEL:
                self._scroll(-event.y * self.line_h * 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.run_btn.is_clicked(mouse_pos):
                    self._start_tests()
                elif self.clear_btn.is_clicked(mouse_pos):
                    self.lines.clear()
                    self.scroll_offset = 0
                    self.running_tests = False
                elif self.back_btn.is_clicked(mouse_pos):
                    return False

        if self.done_flag[0] and self.running_tests:
            self.running_tests = False
            self._scroll(99999)   # jump to bottom (raw output)

        return True

    def draw(self):
        self.screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        hf = get_font(HEADING_FONT_SIZE)
        ht = hf.render(f"Phase {self.phase}  --  Unit Test Runner", True, TEXT_COLOR)
        self.screen.blit(ht, ht.get_rect(midleft=(20, 25)))

        self.run_btn.draw(self.screen, mouse_pos)
        self.clear_btn.draw(self.screen, mouse_pos)
        self.back_btn.draw(self.screen, mouse_pos)

        if self.running_tests:
            tick = int(pygame.time.get_ticks() / 250) % 4
            rt = get_font(SMALL_FONT_SIZE).render(
                "  Running" + "." * (tick + 1), True, WARNING_COLOR)
            self.screen.blit(rt, (390, 65))

        Panel(self.panel_x, self.panel_y, self.panel_w, self.panel_h,
              BG_SECONDARY, TEXT_MUTED).draw(self.screen)

        clip = pygame.Rect(self.panel_x + 2, self.panel_y + 2,
                           self.panel_w - 14, self.panel_h - 4)
        old_clip = self.screen.get_clip()
        self.screen.set_clip(clip)

        snapshot = list(self.lines)
        for i, line in enumerate(snapshot):
            y = self.panel_y + 8 + i * self.line_h - self.scroll_offset
            if y + self.line_h < self.panel_y:
                continue
            if y > self.panel_y + self.panel_h:
                break
            surf = self.font_mono.render(line.text, True, line.color)
            self.screen.blit(surf, (self.panel_x + 10, y))

        self.screen.set_clip(old_clip)

        # Scrollbar
        total_h = max(1, len(self.lines) * self.line_h)
        sb_x = self.panel_x + self.panel_w - 10
        pygame.draw.rect(self.screen, BG_TERTIARY,
                         (sb_x, self.panel_y + 2, 8, self.panel_h - 4),
                         border_radius=4)
        if total_h > self.panel_h:
            ratio  = self.panel_h / total_h
            bar_h  = max(24, int(self.panel_h * ratio))
            bar_y  = self.panel_y + 2 + int(
                (self.scroll_offset / max(1, self._max_scroll())) * (self.panel_h - bar_h))
            pygame.draw.rect(self.screen, TEXT_MUTED,
                             (sb_x, bar_y, 8, bar_h), border_radius=4)

        # Line count badge
        lc = get_font(12).render(f"{len(self.lines)} lines", True, TEXT_MUTED)
        self.screen.blit(lc, lc.get_rect(right=self.panel_x + self.panel_w - 14,
                                          top=self.panel_y + self.panel_h + 4))

        fh = get_font(12).render(
            "Up/Down  Scroll  Home/End  to navigate   |   ESC or <- Back to return",
            True, TEXT_MUTED)
        self.screen.blit(fh, fh.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 28)))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            if not self.handle_events():
                break
            self.draw()
        return True