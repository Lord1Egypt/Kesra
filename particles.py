"""
particles.py — lightweight particle system
"""
import pygame
import random
import math


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "r", "color", "gravity")

    def __init__(self, x, y, color, speed=120, r=4, life=0.6, gravity=180):
        angle = random.uniform(0, math.pi * 2)
        spd   = random.uniform(speed * 0.4, speed)
        self.x  = float(x)
        self.y  = float(y)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd
        self.life     = life + random.uniform(-0.1, 0.1)
        self.max_life = self.life
        self.r        = r + random.uniform(-1, 1)
        self.color    = color
        self.gravity  = gravity

    def update(self, dt: float) -> bool:
        self.life -= dt
        self.vx  *= 0.94
        self.vy  += self.gravity * dt
        self.x   += self.vx * dt
        self.y   += self.vy * dt
        return self.life > 0

    def draw(self, surf: pygame.Surface) -> None:
        t  = max(0.0, self.life / self.max_life)
        a  = int(255 * t)
        r  = max(1, int(self.r * (0.5 + 0.5 * t)))
        s  = pygame.Surface((r * 2 + 1, r * 2 + 1), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color[:3], a), (r, r), r)
        surf.blit(s, (int(self.x) - r, int(self.y) - r))


class ParticleSystem:
    def __init__(self):
        self._particles: list[Particle] = []

    def burst(self, x, y, color, n=14, speed=160, r=4, life=0.55, gravity=250):
        for _ in range(n):
            self._particles.append(Particle(x, y, color, speed, r, life, gravity))

    def spark(self, x, y, color, n=6, speed=80):
        for _ in range(n):
            self._particles.append(Particle(x, y, color, speed, r=2, life=0.35, gravity=100))

    def update(self, dt: float) -> None:
        self._particles = [p for p in self._particles if p.update(dt)]

    def draw(self, surf: pygame.Surface) -> None:
        for p in self._particles:
            p.draw(surf)

    def clear(self) -> None:
        self._particles.clear()


class FloatText:
    """Rising score / message popup."""
    __slots__ = ("text", "x", "y", "vy", "life", "max_life", "color", "font")

    def __init__(self, text: str, x: int, y: int, color: tuple,
                 font: pygame.font.Font, life: float = 0.9):
        self.text = text
        self.x    = float(x)
        self.y    = float(y)
        self.vy   = -60.0
        self.life = self.max_life = life
        self.color = color
        self.font  = font

    def update(self, dt: float) -> bool:
        self.life -= dt
        self.y   += self.vy * dt
        self.vy  *= 0.96
        return self.life > 0

    def draw(self, surf: pygame.Surface) -> None:
        t   = max(0.0, self.life / self.max_life)
        a   = int(255 * t)
        img = self.font.render(self.text, True, self.color)
        s   = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        s.blit(img, (0, 0))
        s.set_alpha(a)
        surf.blit(s, (int(self.x) - img.get_width() // 2, int(self.y)))


class FloatTextSystem:
    def __init__(self):
        self._items: list[FloatText] = []

    def add(self, text, x, y, color, font, life=0.9):
        self._items.append(FloatText(text, x, y, color, font, life))

    def update(self, dt):
        self._items = [i for i in self._items if i.update(dt)]

    def draw(self, surf):
        for i in self._items:
            i.draw(surf)


# ── Expanding shockwave ring ──────────────────────────────────────────────────
class Ring:
    __slots__ = ("x", "y", "r", "max_r", "life", "max_life", "color", "width")

    def __init__(self, x, y, color, max_r=60, life=0.45, width=3):
        self.x = x;  self.y = y
        self.r = 4.0;  self.max_r = float(max_r)
        self.life = self.max_life = life
        self.color = color;  self.width = width

    def update(self, dt):
        self.life -= dt
        self.r += (self.max_r - self.r) * min(1.0, dt * 6)
        return self.life > 0

    def draw(self, surf):
        t = max(0.0, self.life / self.max_life)
        a = int(220 * t)
        s = pygame.Surface((int(self.r)*2+4, int(self.r)*2+4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color[:3], a),
                           (int(self.r)+2, int(self.r)+2), int(self.r), self.width)
        surf.blit(s, (int(self.x)-int(self.r)-2, int(self.y)-int(self.r)-2))


class RingSystem:
    def __init__(self):
        self._rings: list[Ring] = []

    def add(self, x, y, color, max_r=60, life=0.45, width=3):
        self._rings.append(Ring(x, y, color, max_r, life, width))

    def update(self, dt):
        self._rings = [r for r in self._rings if r.update(dt)]

    def draw(self, surf):
        for r in self._rings:
            r.draw(surf)


# ── Ambient dreamy sparkles ───────────────────────────────────────────────────
class AmbientSparkle:
    __slots__ = ("x", "y", "vy", "vx", "life", "max_life", "r", "color")

    def __init__(self, screen_w, screen_h, accent_color):
        self.x = random.uniform(0, screen_w)
        self.y = random.uniform(screen_h * 0.3, screen_h)
        self.vx = random.uniform(-12, 12)
        self.vy = random.uniform(-25, -8)
        self.r  = random.uniform(1.5, 3.5)
        t = random.random()
        r = int(accent_color[0] * t + 255 * (1-t))
        g = int(accent_color[1] * t + 215 * (1-t))
        b = int(accent_color[2] * t + 0   * (1-t))
        self.color = (min(255,r), min(255,g), min(255,b))
        self.life = self.max_life = random.uniform(1.5, 3.5)

    def update(self, dt):
        self.life -= dt
        self.x   += self.vx * dt
        self.y   += self.vy * dt
        self.vx  *= 0.99
        return self.life > 0

    def draw(self, surf):
        t = max(0.0, self.life / self.max_life)
        a = int(160 * math.sin(t * math.pi))
        r = max(1, int(self.r * t))
        s = pygame.Surface((r*2+1, r*2+1), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, a), (r, r), r)
        surf.blit(s, (int(self.x)-r, int(self.y)-r))


class AmbientSystem:
    MAX_SPARKLES = 35

    def __init__(self, screen_w, screen_h):
        self._w = screen_w;  self._h = screen_h
        self._sparkles: list[AmbientSparkle] = []
        self._accent = (255, 215, 0)
        self._t = 0.0

    def set_accent(self, color):
        self._accent = color

    def update(self, dt):
        self._t += dt
        self._sparkles = [s for s in self._sparkles if s.update(dt)]
        if len(self._sparkles) < self.MAX_SPARKLES and random.random() < dt * 12:
            self._sparkles.append(AmbientSparkle(self._w, self._h, self._accent))

    def draw(self, surf):
        for s in self._sparkles:
            s.draw(surf)
