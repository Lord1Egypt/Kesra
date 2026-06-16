"""
gfx.py — drawing primitives: glow, gradient, 3-D bricks, ball, paddle
"""
import pygame
import math


# ── pre-baked glow cache ──────────────────────────────────────────────────────
_glow_cache: dict = {}


def glow_surf(radius: int, color: tuple, max_alpha: int = 160) -> pygame.Surface:
    key = (radius, color, max_alpha)
    if key in _glow_cache:
        return _glow_cache[key]
    size = radius * 4
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size // 2
    r, g, b = color[:3]
    for r_ in range(radius * 2, 0, -2):
        t = r_ / (radius * 2)
        a = int(max_alpha * (1 - t) ** 1.5)
        pygame.draw.circle(s, (r, g, b, a), (cx, cy), r_)
    _glow_cache[key] = s
    return s


def draw_glow(surf: pygame.Surface, pos: tuple, radius: int,
              color: tuple, alpha: int = 160) -> None:
    s = glow_surf(radius, color, alpha)
    ox = pos[0] - s.get_width() // 2
    oy = pos[1] - s.get_height() // 2
    surf.blit(s, (ox, oy), special_flags=pygame.BLEND_ALPHA_SDL2)


def _lerp_color(a: tuple, b: tuple, t: float) -> tuple:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_gradient_rect(surf: pygame.Surface, rect: pygame.Rect,
                       top: tuple, bot: tuple) -> None:
    if rect.height <= 0:
        return
    for dy in range(rect.height):
        t = dy / max(1, rect.height - 1)
        pygame.draw.line(surf, _lerp_color(top, bot, t),
                         (rect.x, rect.y + dy), (rect.right - 1, rect.y + dy))


def build_bg(w: int, h: int, top: tuple, bot: tuple,
             accent: tuple, stars: list) -> pygame.Surface:
    """Pre-render background for a biome.  Returns a static Surface."""
    s = pygame.Surface((w, h))
    # vertical gradient
    for y in range(h):
        t = y / (h - 1)
        base = _lerp_color(top, bot, t)
        # blend in accent tint towards the top
        blend_t = max(0.0, 1.0 - t * 2)
        c = _lerp_color(base, tuple(min(255, base[i] + accent[i]) for i in range(3)), blend_t * 0.18)
        pygame.draw.line(s, c, (0, y), (w - 1, y))
    # stars
    for (sx, sy, sr, sb) in stars:
        col = (min(255, sb), min(255, sb), min(255, int(sb * 0.85) + 20))
        pygame.draw.circle(s, col, (sx, sy), sr)
    return s


# ── 3-D brick drawing ─────────────────────────────────────────────────────────
def _lighten(c: tuple, amt: int) -> tuple:
    return tuple(min(255, v + amt) for v in c[:3])


def _darken(c: tuple, amt: int) -> tuple:
    return tuple(max(0, v - amt) for v in c[:3])


def draw_brick(surf: pygame.Surface, rect: pygame.Rect, color: tuple,
               hp: int, max_hp: int, glow_col: tuple | None = None) -> None:
    if rect.width < 4 or rect.height < 4:
        return
    # fill
    pygame.draw.rect(surf, color, rect, border_radius=3)
    # top highlight
    hi = _lighten(color, 70)
    pygame.draw.rect(surf, hi, pygame.Rect(rect.x + 2, rect.y + 1, rect.w - 4, 4), border_radius=2)
    # bottom shadow
    sh = _darken(color, 55)
    pygame.draw.rect(surf, sh, pygame.Rect(rect.x + 2, rect.bottom - 4, rect.w - 4, 3), border_radius=2)
    # border
    pygame.draw.rect(surf, sh, rect, 1, border_radius=3)

    # damage cracks
    if max_hp > 1 and hp < max_hp:
        damage = 1.0 - hp / max_hp
        crack_col = (*_darken(color, 80), 180)
        cx, cy = rect.centerx, rect.centery
        n_cracks = int(damage * 4) + 1
        for i in range(n_cracks):
            angle = (i / n_cracks) * math.pi + damage * 0.5
            dx = int(math.cos(angle) * rect.w * 0.38)
            dy = int(math.sin(angle) * rect.h * 0.38)
            cs = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            pygame.draw.line(cs, crack_col, (rect.w // 2, rect.h // 2),
                             (rect.w // 2 + dx, rect.h // 2 + dy), 1)
            surf.blit(cs, rect.topleft)

    # optional glow for special bricks (gold / obsidian)
    if glow_col:
        draw_glow(surf, rect.center, max(rect.w, rect.h) // 2, glow_col, alpha=60)


def draw_paddle(surf: pygame.Surface, rect: pygame.Rect,
                color: tuple, shimmer_t: float = 0.0) -> None:
    # body gradient
    hi = _lighten(color, 80)
    sh = _darken(color, 50)
    draw_gradient_rect(surf, rect, hi, color)
    # bottom shadow strip
    pygame.draw.rect(surf, sh, pygame.Rect(rect.x, rect.bottom - 4, rect.w, 4), border_radius=2)
    # border
    pygame.draw.rect(surf, _darken(color, 70), rect, 1, border_radius=4)
    # shimmer highlight (slides across on ball hit)
    if shimmer_t > 0:
        sx = rect.x + int(shimmer_t * rect.w)
        sw = 24
        hs = pygame.Surface((sw, rect.h), pygame.SRCALPHA)
        alpha = int(200 * math.sin(shimmer_t * math.pi))
        hs.fill((255, 255, 255, alpha))
        surf.blit(hs, (sx - sw // 2, rect.y))
    pygame.draw.rect(surf, (0, 0, 0, 0), rect, 0, border_radius=4)  # clip corners
    pygame.draw.rect(surf, _darken(color, 70), rect, 1, border_radius=4)


def draw_ball(surf: pygame.Surface, pos: tuple, radius: int,
              color: tuple, trail: list) -> None:
    n = len(trail)
    for i, (tx, ty) in enumerate(trail):
        t = i / max(1, n)
        a = int(180 * t ** 1.4)
        r = max(2, int(radius * 0.65 * t))
        ts = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(ts, (*color[:3], a), (r + 1, r + 1), r)
        surf.blit(ts, (int(tx) - r - 1, int(ty) - r - 1))
    draw_glow(surf, pos, radius + 6, color, alpha=140)
    pygame.draw.circle(surf, (255, 255, 255), (int(pos[0]), int(pos[1])), radius)
    pygame.draw.circle(surf, color, (int(pos[0]), int(pos[1])), radius, 2)


def draw_ball_rainbow(surf: pygame.Surface, pos: tuple, radius: int,
                      color: tuple, rainbow_trail: list) -> None:
    """Trail where each (x, y, col) has its own color — dream/rainbow effect."""
    n = len(rainbow_trail)
    for i, (tx, ty, tc) in enumerate(rainbow_trail):
        t  = i / max(1, n)
        a  = int(210 * t ** 1.2)
        r  = max(2, int(radius * 0.7 * t))
        ts = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(ts, (*tc[:3], a), (r + 1, r + 1), r)
        surf.blit(ts, (int(tx) - r - 1, int(ty) - r - 1))
    # outer glow (biome accent)
    draw_glow(surf, pos, radius + 8, color, alpha=150)
    # secondary glow (white, smaller, ethereal)
    draw_glow(surf, pos, radius + 3, (255, 255, 255), alpha=100)
    # core
    pygame.draw.circle(surf, (255, 255, 255), (int(pos[0]), int(pos[1])), radius)
    pygame.draw.circle(surf, color, (int(pos[0]), int(pos[1])), radius, 2)


def draw_drop(surf: pygame.Surface, rect: pygame.Rect, color: tuple, label: str,
              font: pygame.font.Font) -> None:
    # pill shape
    pygame.draw.rect(surf, color, rect, border_radius=8)
    pygame.draw.rect(surf, _lighten(color, 60), rect, 1, border_radius=8)
    # label
    txt = font.render(label, True, (255, 255, 255))
    surf.blit(txt, txt.get_rect(center=rect.center))


# ── HUD helpers ───────────────────────────────────────────────────────────────
def draw_heart(surf: pygame.Surface, cx: int, cy: int, size: int,
               filled: bool) -> None:
    color = (220, 40, 80) if filled else (80, 40, 50)
    # simple heart via two circles + triangle
    r = size // 2
    pygame.draw.circle(surf, color, (cx - r // 2, cy - r // 3), r // 2)
    pygame.draw.circle(surf, color, (cx + r // 2, cy - r // 3), r // 2)
    pts = [(cx - r, cy - r // 4), (cx + r, cy - r // 4), (cx, cy + r)]
    pygame.draw.polygon(surf, color, pts)
