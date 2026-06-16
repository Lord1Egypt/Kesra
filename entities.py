"""
entities.py — Ball, Paddle, Brick, Drop
"""
import pygame
import math
import random
from collections import deque
from settings import *
import gfx


def _hsv(h: float, s: float, v: float) -> tuple:
    """HSV → RGB tuple (0-255 each). h in [0,1]."""
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s);  q = v * (1 - f * s);  t = v * (1 - (1 - f) * s)
    segs = [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)]
    r, g, b = segs[i % 6]
    return (int(r*255), int(g*255), int(b*255))


# ── Ball ──────────────────────────────────────────────────────────────────────
class Ball:
    MAX_TRAIL = 22

    def __init__(self, x: float, y: float, color: tuple = (255, 215, 0)):
        self.x  = x
        self.y  = y
        self.vx = 0.0
        self.vy = 0.0
        self.r  = BALL_R
        self.color       = color
        self.speed       = float(BALL_SPEED)
        self.alive       = True
        self.attached    = True          # waiting for launch
        self.fireball    = False
        self.trail: deque[tuple[float, float]] = deque(maxlen=self.MAX_TRAIL)
        # impact flash
        self._flash      = 0.0          # seconds remaining

    # ── physics ───────────────────────────────────────────────────────────────
    def launch(self, angle_deg: float = -70.0) -> None:
        a = math.radians(angle_deg)
        self.vx = math.cos(a) * self.speed
        self.vy = math.sin(a) * self.speed
        self.attached = False

    def update(self, dt: float, screen_w: int, screen_h: int) -> str:
        """Returns 'lost' if fell off-bottom, else 'ok'."""
        if self.attached:
            return "ok"
        self.trail.append((self.x, self.y))
        self.x += self.vx * dt
        self.y += self.vy * dt

        # clamp speed
        spd = math.hypot(self.vx, self.vy)
        if spd > 0:
            factor = self.speed / spd
            self.vx *= factor
            self.vy *= factor

        # wall bounces
        if self.x - self.r < 0:
            self.x = self.r;  self.vx = abs(self.vx)
        if self.x + self.r > screen_w:
            self.x = screen_w - self.r;  self.vx = -abs(self.vx)
        if self.y - self.r < 0:
            self.y = self.r;  self.vy = abs(self.vy)

        self._flash = max(0.0, self._flash - dt)

        if self.y - self.r > screen_h:
            self.alive = False
            return "lost"
        return "ok"

    def bounce_off_paddle(self, paddle_rect: pygame.Rect) -> None:
        hit = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
        hit = max(-0.95, min(0.95, hit))
        angle = hit * math.radians(65)
        self.vx = math.sin(angle) * self.speed
        self.vy = -abs(math.cos(angle)) * self.speed
        self._flash = 0.12

    def bounce_off_brick(self, brick_rect: pygame.Rect) -> None:
        # determine which side was hit
        dx = self.x - brick_rect.centerx
        dy = self.y - brick_rect.centery
        half_w = brick_rect.width / 2 + self.r
        half_h = brick_rect.height / 2 + self.r
        overlap_x = half_w - abs(dx)
        overlap_y = half_h - abs(dy)
        if overlap_x < overlap_y:
            self.vx = math.copysign(abs(self.vx), dx)
            self.x  = brick_rect.centerx + math.copysign(half_w, dx)
        else:
            self.vy = math.copysign(abs(self.vy), dy)
            self.y  = brick_rect.centery + math.copysign(half_h, dy)
        self._flash = 0.06

    def overlaps_rect(self, rect: pygame.Rect) -> bool:
        cx = max(rect.left, min(self.x, rect.right))
        cy = max(rect.top,  min(self.y, rect.bottom))
        return (self.x - cx) ** 2 + (self.y - cy) ** 2 < self.r ** 2

    def draw(self, surf: pygame.Surface, game_t: float = 0.0) -> None:
        col = (255, 140, 0) if self.fireball else self.color
        # rainbow cycling trail
        trail_list = list(self.trail)
        rainbow_trail = []
        n = len(trail_list)
        for i, pos in enumerate(trail_list):
            if self.fireball:
                hue = (game_t * 0.4 + i / max(1, n) * 0.3) % 1.0
                tc  = _hsv(hue, 1.0, 1.0)
            else:
                hue = (game_t * 0.2 + i / max(1, n) * 0.5) % 1.0
                tc  = _hsv(hue, 0.6, 1.0)
            rainbow_trail.append((*pos, tc))
        gfx.draw_ball_rainbow(surf, (self.x, self.y), self.r, col, rainbow_trail)
        if self._flash > 0:
            t  = self._flash / 0.12
            hs = pygame.Surface((self.r * 6, self.r * 6), pygame.SRCALPHA)
            pygame.draw.circle(hs, (255, 255, 255, int(200 * t)),
                               (self.r * 3, self.r * 3), self.r * 3)
            surf.blit(hs, (int(self.x) - self.r * 3, int(self.y) - self.r * 3))


# ── Paddle ────────────────────────────────────────────────────────────────────
class Paddle:
    _LEFT_KEYS  = (pygame.K_LEFT, pygame.K_a)
    _RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)

    def __init__(self, cx: float, y: float):
        self.w   = float(PADDLE_W)
        self.h   = float(PADDLE_H)
        self.x   = cx - self.w / 2
        self.y   = float(y)
        self.vx  = 0.0
        self.color      = C_PADDLE
        # power-up state
        self.magnet     = False
        self.magnet_t   = 0.0
        self._shimmer   = 0.0
        # event-based key tracking (reliable in Pygbag/browser)
        self._held: set = set()

    def on_keydown(self, key: int) -> None:
        self._held.add(key)

    def on_keyup(self, key: int) -> None:
        self._held.discard(key)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    @property
    def centerx(self) -> float:
        return self.x + self.w / 2

    def update(self, dt: float, keys, screen_w: int) -> None:
        speed = PADDLE_SPEED
        left  = any(k in self._held for k in self._LEFT_KEYS) or \
                any(keys[k] for k in self._LEFT_KEYS)
        right = any(k in self._held for k in self._RIGHT_KEYS) or \
                any(keys[k] for k in self._RIGHT_KEYS)
        if left:
            self.x -= speed * dt
        if right:
            self.x += speed * dt
        self.x = max(0.0, min(screen_w - self.w, self.x))

        if self.magnet_t > 0:
            self.magnet_t -= dt
            if self.magnet_t <= 0:
                self.magnet = False

        self._shimmer = max(0.0, self._shimmer - dt * 2.5)

    def on_ball_hit(self) -> None:
        self._shimmer = 1.0

    def resize(self, factor: float, duration: float = 8.0) -> None:
        self.w = max(PADDLE_MIN_W, min(PADDLE_MAX_W, self.w * factor))
        self.x = max(0, self.x)

    def activate_magnet(self, duration: float = 8.0) -> None:
        self.magnet   = True
        self.magnet_t = duration

    def draw(self, surf: pygame.Surface) -> None:
        col = (80, 160, 255) if self.magnet else self.color
        gfx.draw_paddle(surf, self.rect, col, self._shimmer)
        if self.magnet:
            gfx.draw_glow(surf, self.rect.center, int(self.w // 2), (80, 160, 255), alpha=80)


# ── Brick ─────────────────────────────────────────────────────────────────────
class Brick:
    def __init__(self, col: int, row: int, data: dict):
        self.col = col
        self.row = row
        self.rect = pygame.Rect(
            GRID_MARGIN + col * BRICK_W,
            GRID_TOP    + row * BRICK_H,
            BRICK_W - 2, BRICK_H - 2,
        )
        self.hp      = data["hp"]
        self.max_hp  = data["max_hp"]
        self.pts     = data["pts"]
        self.color   = tuple(data["color"])
        self.is_boss = data.get("is_boss", False)
        self.drop_ch = data.get("drop_chance", 0.08)
        self.alive   = True
        self._hit_t  = 0.0    # white-flash timer

    def hit(self, dmg: int = 1) -> bool:
        """Returns True if destroyed."""
        self.hp -= dmg
        self._hit_t = 0.12
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def update(self, dt: float) -> None:
        self._hit_t = max(0.0, self._hit_t - dt)

    def draw(self, surf: pygame.Surface) -> None:
        col = self.color
        if self._hit_t > 0:
            t   = self._hit_t / 0.12
            col = tuple(int(c + (255 - c) * t * 0.7) for c in self.color)
        glow = (255, 215, 0) if self.is_boss else (
               (255, 100, 0) if self.color == (255, 195, 0) else None)
        gfx.draw_brick(surf, self.rect, col, self.hp, self.max_hp, glow)


# ── Drop ──────────────────────────────────────────────────────────────────────
class Drop:
    SIZE   = (32, 18)
    SPEED  = 130

    def __init__(self, x: float, y: float, drop_type: str, font: pygame.font.Font):
        self.x    = x
        self.y    = float(y)
        self.type = drop_type
        self.font = font
        from settings import DROPS
        info      = DROPS.get(drop_type, {"color": (200, 200, 200), "label": "?"})
        self.color = info["color"]
        self.label = info["label"]
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x) - self.SIZE[0] // 2,
                           int(self.y) - self.SIZE[1] // 2,
                           *self.SIZE)

    def update(self, dt: float, screen_h: int) -> None:
        self.y += self.SPEED * dt
        if self.y > screen_h + 30:
            self.alive = False

    def draw(self, surf: pygame.Surface) -> None:
        gfx.draw_drop(surf, self.rect, self.color, self.label, self.font)
        gfx.draw_glow(surf, self.rect.center, 14, self.color, alpha=90)
