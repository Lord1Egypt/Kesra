"""
scenes.py — Menu, Play, GameOver scene classes
"""
import pygame
import math
import random
from settings import *
from state import GameState
from entities import Ball, Paddle, Brick, Drop
from levelgen import generate_round
from particles import ParticleSystem, FloatTextSystem, RingSystem, AmbientSystem
import gfx
from rtl import ar


# ── shared starfield ──────────────────────────────────────────────────────────
def _make_stars(n=220) -> list:
    stars = []
    for _ in range(n):
        x  = random.randint(0, W)
        y  = random.randint(0, H)
        r  = random.choice([1, 1, 1, 2])
        b  = random.randint(120, 255)
        stars.append((x, y, r, b))
    return stars


STARS = _make_stars()
_bg_cache: dict = {}


def get_bg(biome_i: int) -> pygame.Surface:
    if biome_i not in _bg_cache:
        accent = BIOMES[biome_i]["bg_tint"]
        _bg_cache[biome_i] = gfx.build_bg(W, H, C_BG_TOP, C_BG_BOT, accent, STARS)
    return _bg_cache[biome_i]


# ── fonts ─────────────────────────────────────────────────────────────────────
def _fonts():
    _cairo = "assets/fonts/Cairo.ttf"
    import os
    if os.path.exists(_cairo):
        big    = pygame.font.Font(_cairo, 52)
        med    = pygame.font.Font(_cairo, 30)
        small  = pygame.font.Font(_cairo, 20)
        tiny   = pygame.font.Font(_cairo, 15)
        arabic = pygame.font.Font(_cairo, 72)
        pop    = pygame.font.Font(_cairo, 24)
    else:
        big    = pygame.font.SysFont("arial", 52, bold=True)
        med    = pygame.font.SysFont("arial", 28, bold=True)
        small  = pygame.font.SysFont("arial", 18)
        tiny   = pygame.font.SysFont("arial", 14)
        arabic = pygame.font.SysFont("tahoma,arial", 64, bold=True)
        pop    = pygame.font.SysFont("arial", 22, bold=True)
    return big, med, small, tiny, arabic, pop


# ── MENU ──────────────────────────────────────────────────────────────────────
class MenuScene:
    _SPEED_LABELS = ["½×", "1×", "1.5×", "2×"]

    def __init__(self, gs: GameState):
        self.gs    = gs
        self.t     = 0.0
        self.f_big, self.f_med, self.f_sm, self.f_tiny, self.f_ar, _ = _fonts()
        self._bg   = get_bg(0)

    # ── button rects ──────────────────────────────────────────────────────────
    def _btn_play(self):   return pygame.Rect(W // 2 - 110, H // 2 + 30, 220, 48)
    def _btn_auto(self):   return pygame.Rect(W // 2 - 110, H // 2 + 88, 220, 38)
    def _speed_rects(self):
        rects = []
        sw, sh, gap = 50, 30, 6
        total = len(GameState.SPEEDS) * sw + (len(GameState.SPEEDS) - 1) * gap
        x0 = W // 2 - total // 2
        y0 = H // 2 + 138
        for i in range(len(GameState.SPEEDS)):
            rects.append(pygame.Rect(x0 + i * (sw + gap), y0, sw, sh))
        return rects

    def update(self, dt: float, events: list) -> str | None:
        self.t += dt
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return "play"
                if ev.key == pygame.K_ESCAPE:
                    return "quit"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                if self._btn_play().collidepoint(mx, my):
                    self.gs.auto_play = False
                    return "play"
                if self._btn_auto().collidepoint(mx, my):
                    self.gs.auto_play = True
                    return "play"
                for i, r in enumerate(self._speed_rects()):
                    if r.collidepoint(mx, my):
                        self.gs.speed_idx = i
        return None

    def draw(self, surf: pygame.Surface) -> None:
        surf.blit(self._bg, (0, 0))
        self._draw_pyramids(surf)

        t = self.t
        for y_off in (-160, -80):
            line_s = pygame.Surface((W, 2), pygame.SRCALPHA)
            pulse  = int(40 + 40 * math.sin(t * 1.5))
            line_s.fill((255, 215, 0, pulse))
            surf.blit(line_s, (0, H // 2 + y_off))

        # Title
        gfx.draw_glow(surf, (W // 2, H // 2 - 110), 90, C_GOLD, alpha=120)
        title = self.f_ar.render(ar("كِسرة"), True, C_GOLD)
        surf.blit(title, title.get_rect(center=(W // 2, H // 2 - 110)))

        sub = self.f_med.render("Egyptian Brick-Breaker", True, C_GOLD_D)
        surf.blit(sub, sub.get_rect(center=(W // 2, H // 2 - 48)))

        tag = self.f_sm.render(ar('"محصلتش قبل كده ولا هتحصل"'), True, (160, 140, 100))
        surf.blit(tag, tag.get_rect(center=(W // 2, H // 2 - 10)))

        if self.gs.best_score > 0:
            bs = self.f_sm.render(
                f"Best  {self.gs.best_score:,}   Round {self.gs.best_round}", True, C_DIM)
            surf.blit(bs, bs.get_rect(center=(W // 2, H // 2 + 14)))

        # ── PLAY button ──────────────────────────────────────────────────────
        pulse = 0.5 + 0.5 * math.sin(t * 2.5)
        btn   = self._btn_play()
        bcol  = tuple(int(C_GOLD_D[i] + (C_GOLD[i] - C_GOLD_D[i]) * pulse) for i in range(3))
        pygame.draw.rect(surf, bcol, btn, border_radius=8)
        pygame.draw.rect(surf, C_GOLD, btn, 2, border_radius=8)
        gfx.draw_glow(surf, btn.center, 55, C_GOLD, alpha=int(80 * pulse))
        surf.blit(self.f_med.render("▶  PLAY", True, (10, 5, 0)),
                  self.f_med.render("▶  PLAY", True, C_GOLD).get_rect(center=btn.center))

        # ── AUTO PLAY button ─────────────────────────────────────────────────
        abtn  = self._btn_auto()
        acol  = (0, 180, 120) if self.gs.auto_play else (30, 30, 50)
        abord = (0, 255, 160) if self.gs.auto_play else (80, 80, 100)
        pygame.draw.rect(surf, acol, abtn, border_radius=6)
        pygame.draw.rect(surf, abord, abtn, 2, border_radius=6)
        albl  = self.f_sm.render("🤖  AUTO PLAY", True, (230, 255, 230) if self.gs.auto_play else C_DIM)
        surf.blit(albl, albl.get_rect(center=abtn.center))

        # ── SPEED tabs ───────────────────────────────────────────────────────
        spd_lbl = self.f_tiny.render("SPEED", True, C_DIM)
        surf.blit(spd_lbl, spd_lbl.get_rect(center=(W // 2, H // 2 + 130)))
        for i, r in enumerate(self._speed_rects()):
            active = (i == self.gs.speed_idx)
            col  = C_GOLD if active else (40, 35, 20)
            bord = C_GOLD if active else (80, 70, 40)
            pygame.draw.rect(surf, col, r, border_radius=4)
            pygame.draw.rect(surf, bord, r, 1, border_radius=4)
            lc   = (10, 5, 0) if active else C_DIM
            lbl  = self.f_tiny.render(self._SPEED_LABELS[i], True, lc)
            surf.blit(lbl, lbl.get_rect(center=r.center))

        hint = self.f_tiny.render("← → / drag to move  |  SPACE to launch  |  ESC to quit", True, C_DIM)
        surf.blit(hint, hint.get_rect(center=(W // 2, H - 24)))

    def _draw_pyramids(self, surf: pygame.Surface) -> None:
        t   = self.t * 0.4
        bob = int(4 * math.sin(t))
        col = (80, 60, 20)
        pts = [(18, H - 40 + bob), (70, H - 140 + bob), (122, H - 40 + bob)]
        pygame.draw.polygon(surf, col, pts)
        pygame.draw.polygon(surf, C_GOLD_D, pts, 1)
        pts = [(W - 18, H - 40 + bob), (W - 70, H - 140 + bob), (W - 122, H - 40 + bob)]
        pygame.draw.polygon(surf, col, pts)
        pygame.draw.polygon(surf, C_GOLD_D, pts, 1)


# ── GAME OVER ─────────────────────────────────────────────────────────────────
class GameOverScene:
    def __init__(self, gs: GameState):
        self.gs  = gs
        self.t   = 0.0
        self.f_big, self.f_med, self.f_sm, self.f_tiny, _, _ = _fonts()

    def update(self, dt: float, events: list) -> str | None:
        self.t += dt
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_r):
                    return "restart"
                if ev.key == pygame.K_ESCAPE:
                    return "menu"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                return "restart"
        return None

    def draw(self, surf: pygame.Surface) -> None:
        # Dark overlay
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 10, 200))
        surf.blit(ov, (0, 0))

        cx, cy = W // 2, H // 2
        # red glow
        gfx.draw_glow(surf, (cx, cy - 80), 100, C_RED, alpha=100)

        go = self.f_big.render("GAME OVER", True, C_RED)
        surf.blit(go, go.get_rect(center=(cx, cy - 80)))

        sc = self.f_med.render(f"Score: {self.gs.score:,}", True, C_GOLD)
        surf.blit(sc, sc.get_rect(center=(cx, cy - 20)))

        rnd = self.f_med.render(f"Round: {self.gs.round}  |  Cycle: {(self.gs.round-1)//9+1}", True, C_HUD)
        surf.blit(rnd, rnd.get_rect(center=(cx, cy + 20)))

        if self.gs.score >= self.gs.best_score and self.gs.score > 0:
            new = self.f_med.render("✦ NEW BEST! ✦", True, C_GOLD)
            surf.blit(new, new.get_rect(center=(cx, cy + 60)))

        pulse = 0.5 + 0.5 * math.sin(self.t * 3)
        v     = int(80 + 80 * pulse)
        rcol  = (v, v, v)
        restart = self.f_sm.render("SPACE / click to play again  |  ESC for menu", True, rcol)
        surf.blit(restart, restart.get_rect(center=(cx, cy + 110)))


# ── PLAY ──────────────────────────────────────────────────────────────────────
class PlayScene:
    def __init__(self, gs: GameState):
        self.gs        = gs
        self.gs.reset()
        self.t         = 0.0
        self._shake    = 0.0
        self._shake_v  = pygame.Vector2(0, 0)
        self.particles = ParticleSystem()
        self.floats    = FloatTextSystem()
        self.rings     = RingSystem()
        self.ambient   = AmbientSystem(W, H)
        self.f_big, self.f_med, self.f_sm, self.f_tiny, self.f_ar, self.f_pop = _fonts()
        self._round_data: dict = {}
        self._biome_i  = 0
        self._bg       = get_bg(0)

        # entities
        self.bricks: list[Brick] = []
        self.drops:  list[Drop]  = []
        self.paddle  = Paddle(W / 2, PADDLE_Y)
        self.ball: Ball | None   = None

        # round-transition flash
        self._flash   = 0.0
        self._flash_c = (255, 255, 255)

        self._announce: str  = ""
        self._announce_t: float = 0.0

        # auto-play state
        self._auto_launch_t = 0.6   # seconds before auto-launch after attach
        self._auto_launch_timer = 0.0

        self._start_round()

    # ── round management ──────────────────────────────────────────────────────
    def _start_round(self) -> None:
        data           = generate_round(self.gs.round)
        self._round_data = data
        self._biome_i  = data["biome_i"]
        self._bg       = get_bg(self._biome_i)
        biome          = data["biome"]
        accent         = biome["accent"]

        self.bricks    = []
        for row, row_data in enumerate(data["grid"]):
            for col, cell in enumerate(row_data):
                if cell is not None:
                    self.bricks.append(Brick(col, row, cell))

        self.drops     = []
        self.particles.clear()
        self.rings     = RingSystem()
        self.ambient.set_accent(biome["accent"])
        self._spawn_ball(accent)

        # biome flash
        self._flash   = 0.6
        self._flash_c = accent
        label         = f"Round {self.gs.round}  —  {biome['name']}"
        if data["is_boss"]:
            label     = f"⚡ BOSS — {biome['boss']} ⚡"
        self._announce   = label
        self._announce_t = 2.5

    def _spawn_ball(self, accent: tuple) -> None:
        self.ball = Ball(self.paddle.rect.centerx,
                         self.paddle.rect.top - BALL_R - 1,
                         color=accent)
        self.ball.attached = True

    # ── update ────────────────────────────────────────────────────────────────
    def update(self, dt: float, events: list) -> str | None:
        self.t += dt

        for ev in events:
            if ev.type == pygame.KEYDOWN:
                self.paddle.on_keydown(ev.key)
                if ev.key == pygame.K_ESCAPE:
                    return "menu"
                if ev.key == pygame.K_SPACE and self.ball and self.ball.attached:
                    self.ball.launch(random.uniform(-80, -100))
            elif ev.type == pygame.KEYUP:
                self.paddle.on_keyup(ev.key)
            elif ev.type == pygame.FINGERMOTION:
                # touch drag on web/mobile — move paddle to finger x
                tx = int(ev.x * W)
                self.paddle.x = max(0.0, min(W - self.paddle.w, tx - self.paddle.w / 2))
            elif ev.type == pygame.FINGERDOWN:
                if self.ball and self.ball.attached:
                    self.ball.launch(random.uniform(-80, -100))

        if self.gs.auto_play:
            self._run_ai(dt)
        else:
            keys = pygame.key.get_pressed()
            self.paddle.update(dt, keys, W)
            # mouse / touch control
            mx, _ = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                self.paddle.x = max(0.0, min(W - self.paddle.w, mx - self.paddle.w / 2))

        # keep attached ball on paddle
        if self.ball and self.ball.attached:
            self.ball.x = self.paddle.rect.centerx
            self.ball.y = self.paddle.rect.top - BALL_R - 1
            if not self.gs.auto_play and pygame.mouse.get_pressed()[0]:
                self.ball.launch(random.uniform(-80, -100))

        if self.ball:
            result = self.ball.update(dt, W, H)
            self._check_collisions()
            if result == "lost":
                self._on_ball_lost()

        for brick in self.bricks:
            brick.update(dt)

        for drop in self.drops:
            drop.update(dt, H)
            if drop.alive and drop.rect.colliderect(self.paddle.rect):
                self._collect_drop(drop)
                drop.alive = False

        self.drops    = [d for d in self.drops if d.alive]
        self.particles.update(dt)
        self.floats.update(dt)
        self.rings.update(dt)
        self.ambient.update(dt)

        self._flash      = max(0.0, self._flash - dt * 2.5)
        self._announce_t = max(0.0, self._announce_t - dt)
        self._shake      = max(0.0, self._shake - dt * 4)

        if self.gs.game_over:
            return "game_over"
        return None

    # ── collision ─────────────────────────────────────────────────────────────
    def _check_collisions(self) -> None:
        if not self.ball or self.ball.attached:
            return
        b = self.ball

        # paddle
        if b.vy > 0 and b.overlaps_rect(self.paddle.rect):
            b.bounce_off_paddle(self.paddle.rect)
            self.paddle.on_ball_hit()
            self.gs.add_combo()
            self.particles.spark(b.x, b.y, b.color, n=5, speed=60)

        # bricks
        hit_this_frame = False
        for brick in self.bricks:
            if not brick.alive:
                continue
            if b.overlaps_rect(brick.rect):
                if not b.fireball or not hit_this_frame:
                    b.bounce_off_brick(brick.rect)
                    hit_this_frame = True
                pts  = self.gs.add_score(brick.pts)
                kill = brick.hit(2 if b.fireball else 1)
                self.particles.spark(b.x, b.y, brick.color, n=4)
                if kill:
                    self._on_brick_killed(brick, pts)
                else:
                    # hit-but-not-killed: small ring + spark
                    self.rings.add(brick.rect.centerx, brick.rect.centery,
                                   brick.color, max_r=30, life=0.25, width=2)

        self.bricks = [br for br in self.bricks if br.alive]

        if not self.bricks:
            self._next_round()

    def _on_brick_killed(self, brick: Brick, pts: int) -> None:
        cx, cy = brick.rect.centerx, brick.rect.centery
        # big particle burst
        self.particles.burst(cx, cy, brick.color, n=22, speed=220, r=5, life=0.65)
        # second burst of white sparks
        self.particles.burst(cx, cy, (255, 255, 255), n=8, speed=160, r=2, life=0.35, gravity=120)
        # expanding shockwave rings (two rings for depth)
        self.rings.add(cx, cy, brick.color, max_r=55, life=0.45, width=3)
        self.rings.add(cx, cy, (255, 255, 255), max_r=30, life=0.25, width=1)
        # score popup with glow
        self.floats.add(f"+{pts:,}", cx, brick.rect.top - 4, brick.color, self.f_pop)
        c = self.gs.combo
        if c and c % 8 == 0:
            self._shake = 0.30
            # dramatic combo: full-width gold flash + text
            self._flash   = 0.18
            self._flash_c = C_GOLD
            self.floats.add(f"✦ x{c} COMBO! ✦", W // 2, H // 3,
                            C_GOLD, self.f_med, life=1.4)
            self.rings.add(W // 2, H // 2, C_GOLD, max_r=200, life=0.6, width=4)
        # maybe drop
        import random as _r
        if _r.random() < brick.drop_ch:
            allowed = self._round_data.get("drops", ["bronze_coin"])
            t = allowed[_r.randint(0, len(allowed) - 1)]
            self.drops.append(Drop(brick.rect.centerx, brick.rect.centery, t, self.f_tiny))

    def _on_ball_lost(self) -> None:
        self.gs.reset_combo()
        self.gs.lose_life()
        accent = self._round_data["biome"]["accent"]
        self.particles.burst(self.ball.x, H - 40, (200, 60, 60), n=25, speed=140, r=4)
        self._flash   = 0.3
        self._flash_c = (180, 30, 30)
        if not self.gs.game_over:
            self._spawn_ball(accent)

    def _collect_drop(self, drop: Drop) -> None:
        self.particles.burst(*drop.rect.center, drop.color, n=10, speed=100, r=3)
        t = drop.type
        if t == "bronze_coin":
            self.gs.add_score(10)
        elif t == "silver_coin":
            self.gs.add_score(50)
        elif t == "gold_coin":
            self.gs.add_score(200)
        elif t == "heart":
            self.gs.add_life()
            self.floats.add("♥ +1 LIFE", W // 2, H // 2, C_HEART, self.f_med, 1.5)
        elif t == "shield":
            self.gs.powerups["shield"] = True
            self.floats.add("🛡 SHIELD", W // 2, H // 2, (80, 160, 255), self.f_med, 1.5)
        elif t == "wide":
            self.paddle.resize(1.4, 8.0)
            self.floats.add("⟺ WIDE", W // 2, H // 2, (100, 220, 100), self.f_med, 1.5)
        elif t == "fireball" and self.ball:
            self.ball.fireball = True
            self.floats.add("🔥 FIREBALL", W // 2, H // 2, (255, 80, 0), self.f_med, 1.5)
        elif t == "magnet":
            self.paddle.activate_magnet(8.0)
            self.floats.add("⚡ MAGNET", W // 2, H // 2, (180, 0, 255), self.f_med, 1.5)
        elif t == "slow" and self.ball:
            self.ball.speed = max(200, self.ball.speed * 0.75)
            self.floats.add("❄ SLOW", W // 2, H // 2, (200, 200, 255), self.f_med, 1.5)

    def _next_round(self) -> None:
        self.gs.next_round()
        self._start_round()

    # ── auto-play AI ──────────────────────────────────────────────────────────
    def _run_ai(self, dt: float) -> None:
        if not self.ball:
            return
        if self.ball.attached:
            self._auto_launch_timer += dt
            # track ball to center of paddle while attached
            self.paddle.x = max(0.0, min(W - self.paddle.w,
                                         self.ball.x - self.paddle.w / 2))
            if self._auto_launch_timer >= self._auto_launch_t:
                self._auto_launch_timer = 0.0
                self.ball.launch(random.uniform(-75, -105))
            return
        # track ball x with slight imperfection so it's not perfect
        target_x = self.ball.x - self.paddle.w / 2 + random.uniform(-8, 8)
        self.paddle.x += (target_x - self.paddle.x) * min(1.0, dt * 9)
        self.paddle.x  = max(0.0, min(W - self.paddle.w, self.paddle.x))

    # ── draw ──────────────────────────────────────────────────────────────────
    def draw(self, surf: pygame.Surface) -> None:
        shake_x = shake_y = 0
        if self._shake > 0:
            s = self._shake * 8
            shake_x = random.randint(int(-s), int(s))
            shake_y = random.randint(int(-s), int(s))

        # temp surface so we can shake the whole scene
        scene = pygame.Surface((W, H))
        scene.blit(self._bg, (0, 0))

        # ambient dreamy sparkles (behind everything)
        self.ambient.draw(scene)

        # subtle center glow in biome accent color
        biome_accent = self._round_data.get("biome", {}).get("accent", C_GOLD)
        pulse = 0.5 + 0.5 * math.sin(self.t * 1.2)
        gfx.draw_glow(scene, (W // 2, H // 2), int(120 + 20 * pulse),
                      biome_accent, alpha=int(22 + 10 * pulse))

        for brick in self.bricks:
            brick.draw(scene)

        self.rings.draw(scene)

        for drop in self.drops:
            drop.draw(scene)

        self.particles.draw(scene)

        if self.ball:
            self.ball.draw(scene, self.t)

        self.paddle.draw(scene)

        self.floats.draw(scene)
        self._draw_hud(scene)

        # biome entry flash
        if self._flash > 0:
            t  = self._flash
            fl = pygame.Surface((W, H), pygame.SRCALPHA)
            fl.fill((*self._flash_c, int(min(255, t * 280))))
            scene.blit(fl, (0, 0))

        # round announce
        if self._announce_t > 0:
            t  = min(1.0, self._announce_t)
            a  = int(255 * t)
            an = self.f_med.render(self._announce, True, C_GOLD)
            s  = pygame.Surface(an.get_size(), pygame.SRCALPHA)
            s.blit(an, (0, 0))
            s.set_alpha(a)
            scene.blit(s, s.get_rect(center=(W // 2, 52)))

        surf.blit(scene, (shake_x, shake_y))

    def _draw_hud(self, surf: pygame.Surface) -> None:
        # score
        sc = self.f_med.render(f"{self.gs.score:,}", True, C_GOLD)
        surf.blit(sc, (10, 10))

        # combo
        if self.gs.combo > 1:
            co = self.f_sm.render(f"x{self.gs.combo}", True, C_GOLD_L)
            surf.blit(co, (10, 40))

        # lives (hearts)
        for i in range(GameState.MAX_LIVES):
            filled = i < self.gs.lives
            gfx.draw_heart(surf, W - 18 - i * 26, 20, 14, filled)

        # biome name (bottom)
        biome = self._round_data.get("biome", {})
        name  = biome.get("name", "")
        rnd   = self.gs.round
        cycle = (rnd - 1) // 9 + 1
        info  = self.f_tiny.render(f"Round {rnd}  ·  Cycle {cycle}  ·  {name}", True, C_DIM)
        surf.blit(info, info.get_rect(center=(W // 2, H - 14)))

        # shield indicator
        if self.gs.powerups.get("shield"):
            sh = self.f_tiny.render("🛡 SHIELD", True, (80, 160, 255))
            surf.blit(sh, (10, H - 28))

        # speed + auto-play pill (top-right, below hearts)
        spd_str = GameState.SPEEDS[self.gs.speed_idx]
        spd_lbl = ("AUTO " if self.gs.auto_play else "") + f"{spd_str}×"
        spd_col = (0, 255, 160) if self.gs.auto_play else C_GOLD_D
        spd_surf = self.f_tiny.render(spd_lbl, True, spd_col)
        surf.blit(spd_surf, spd_surf.get_rect(topright=(W - 10, 36)))
