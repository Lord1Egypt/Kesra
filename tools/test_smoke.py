#!/usr/bin/env python3
"""
test_smoke.py — headless smoke test for Kesra (Python + Pygame edition).

Runs the whole game with the dummy SDL drivers (no display/audio) and asserts the
core systems never crash and behave correctly. Exits 0 on success, non-zero on any
failure — used by CI (`.github/workflows/ci-cd.yml`) and safe to run locally:

    python3 tools/test_smoke.py
"""
import os
import sys
import tempfile

# headless + isolated save file BEFORE importing pygame / game modules
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
os.chdir(tempfile.mkdtemp(prefix="kesra_test_"))

import pygame                       # noqa: E402
pygame.init()
pygame.display.set_mode((480, 720))

from state import GameState         # noqa: E402
from scenes import MenuScene, PlayScene, GameOverScene  # noqa: E402
from entities import Drop, Brick    # noqa: E402
from achievements import TOTAL      # noqa: E402

SCREEN = pygame.Surface((480, 720))
_passed = 0


def ok(label: str) -> None:
    global _passed
    _passed += 1
    print(f"  ✓ {label}")


# ── 1. Menu ──────────────────────────────────────────────────────────────────
gs = GameState()
m = MenuScene(gs)
m.update(0.016, [])
m.draw(SCREEN)
m.show_ach = True
m.update(0.016, [])
m.draw(SCREEN)            # achievements panel path
ok("Menu (incl. achievements panel) renders")

# ── 2. Play: launch, inject every drop type, run frames ──────────────────────
p = PlayScene(gs)
DROPS = ["bronze_coin", "silver_coin", "gold_coin", "diamond", "heart", "shield",
         "wide", "fireball", "magnet", "slow", "multi_ball", "star", "bomb", "rocket"]
p._launch_all_attached()
for i in range(450):
    if i % 12 == 0 and DROPS:
        p.drops.append(Drop(p.paddle.centerx, p.paddle.y - 30, DROPS.pop(0), p.f_tiny))
    res = p.update(0.016, [])
    p.draw(SCREEN)
    if res == "game_over":
        break
assert not DROPS, f"not all drops were collected: {DROPS}"
ok("Play loop + every drop type collected")

# ── 3. Pause → resume / restart ──────────────────────────────────────────────
esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
p.update(0.016, [esc])
assert p.paused, "ESC should pause"
click_resume = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=p._pause_buttons()["resume"].center)
p.update(0.016, [click_resume])
assert not p.paused, "clicking resume should unpause"
p.update(0.016, [esc])
r = p.update(0.016, [pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                        pos=p._pause_buttons()["restart"].center)])
assert r == "restart", f"expected 'restart', got {r!r}"
ok("Pause menu: resume + restart")

# ── 4. Area-effect drops ─────────────────────────────────────────────────────
p2 = PlayScene(gs)
before = len(p2.bricks)
p2._detonate_bomb()
p2._fire_rocket()
assert len(p2.bricks) < before, "bomb+rocket destroyed nothing"
ok("Bomb + rocket destroy bricks")

# ── 5. Multi-ball cap ────────────────────────────────────────────────────────
p3 = PlayScene(gs)
p3._launch_all_attached()
for _ in range(12):
    p3._spawn_multiball()
assert len(p3.balls) <= PlayScene.MAX_BALLS, f"ball cap exceeded: {len(p3.balls)}"
ok(f"Multi-ball respects cap ({len(p3.balls)} ≤ {PlayScene.MAX_BALLS})")

# ── 6. Special bricks (explosive chain / gift / cursed) ──────────────────────
p4 = PlayScene(gs)
p4.bricks = []
for rr in range(3):
    for cc in range(3):
        p4.bricks.append(Brick(cc, rr, {"name": "mud", "hp": 1, "max_hp": 1, "pts": 10,
                                        "color": (139, 90, 43), "is_boss": False,
                                        "drop_chance": 0.0, "special": "explosive"}))
center = next(b for b in p4.bricks if b.col == 1 and b.row == 1)
center.alive = False
n0 = len(p4.bricks)
p4._on_brick_killed(center, 10)
p4.bricks = [b for b in p4.bricks if b.alive]
assert len(p4.bricks) < n0, "explosive chain destroyed nothing"

w0 = p4.paddle.w
cb = Brick(0, 0, {"name": "mud", "hp": 1, "max_hp": 1, "pts": 10, "color": (139, 90, 43),
                  "is_boss": False, "drop_chance": 0.0, "special": "cursed"})
cb.alive = False
p4._on_brick_killed(cb, 10)
assert p4.paddle.w < w0, "cursed brick did not shrink paddle"
ok("Special bricks: explosive chain + cursed shrink")

# ── 7. Achievements unlock + persistence ─────────────────────────────────────
gs2 = GameState()
gs2.record_brick()
gs2.record_combo(16)
gs2.best_round = 10
gs2.record_round_clear(8, True)
gs2.record_balls(5)
assert {"first_brick", "combo_16", "boss_slayer", "ball_storm"} <= gs2.unlocked
gs2.save_persistent()
gs3 = GameState()
assert gs3.unlocked == gs2.unlocked, "unlocked set did not persist"
assert gs3.stats["bricks_total"] == gs2.stats["bricks_total"], "stats did not persist"
ok(f"Achievements unlock + persist ({len(gs3.unlocked)}/{TOTAL})")

# ── 8. Boss round ────────────────────────────────────────────────────────────
gsb = GameState()
gsb.round = 8
pb = PlayScene(gsb)
pb.gs.round = 8
pb._start_round()
assert pb._round_data["is_boss"], "round 8 should be a boss round"
for _ in range(300):
    pb.update(0.016, [])
    pb.draw(SCREEN)
ok("Boss round generates + plays")

# ── 9. Auto-play soak (round transitions, no crash) ──────────────────────────
gsa = GameState()
gsa.auto_play = True
pa = PlayScene(gsa)
overs = 0
for _ in range(6000):
    if pa.update(0.016, []) == "game_over":
        overs += 1
        gsa.reset(); gsa.auto_play = True
        pa = PlayScene(gsa)
    pa.draw(SCREEN)
ok(f"6k-frame auto-play soak (game-overs handled: {overs})")

# ── 10. GameOver scene ───────────────────────────────────────────────────────
gs.lives = 0
go = GameOverScene(gs)
go.update(0.016, [])
go.draw(SCREEN)
ok("GameOver scene renders")

# ── 11. Audio synthesis + playback (dummy driver) ────────────────────────────
import audio  # noqa: E402
audio.init()
for _name in ("paddle", "coin", "power", "combo", "lose", "clear", "over", "boom"):
    audio.play(_name)
for _c in (0, 8, 16, 99):
    audio.play_brick(_c)
audio.set_muted(True)
audio.play("paddle")          # muted → no-op, must not raise
audio.set_muted(False)
ok("Audio synthesis + playback (no crash)")

print(f"\nALL SMOKE TESTS PASSED ({_passed} checks)")
sys.exit(0)
