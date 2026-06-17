"""
settings.py — all constants for كِسرة
"""
import pygame

W, H   = 480, 720
FPS    = 60
TITLE  = "كِسرة — Egyptian Brick-Breaker"

# Grid
BRICK_COLS  = 8
BRICK_W     = (W - 16) // BRICK_COLS   # 58 px
BRICK_H     = 22
GRID_MARGIN = 8
GRID_TOP    = 88

# Paddle
PADDLE_W     = 100
PADDLE_H     = 16
PADDLE_Y     = H - 60
PADDLE_SPEED = 500
PADDLE_MIN_W = 60
PADDLE_MAX_W = 180

# Ball
BALL_R       = 9
BALL_SPEED   = 420
BALL_MAX_SPD = 700

# ── Palette ───────────────────────────────────────────────────────────────────
C_BG_TOP   = (5,   5, 18)
C_BG_BOT   = (18,  4, 32)
C_GOLD     = (255, 215,  0)
C_GOLD_D   = (180, 130,  0)
C_GOLD_L   = (255, 240, 130)
C_WHITE    = (255, 255, 255)
C_PADDLE   = (190, 155, 55)
C_PADDLE_H = (240, 210, 100)
C_RED      = (200,  40,  40)
C_HEART    = (220,  40,  80)
C_HUD      = (220, 200, 120)
C_DIM      = (100,  90,  70)

# ── Biomes ────────────────────────────────────────────────────────────────────
BIOMES = [
    {"name": "Scientific",    "boss": "Imhotep",         "accent": (0, 220, 255),   "bg_tint": (0, 30, 50)},
    {"name": "Artistic",      "boss": "Thoth",            "accent": (200, 80, 255),  "bg_tint": (25, 0, 45)},
    {"name": "Historical",    "boss": "Ramesses II",      "accent": (255, 80,  60),  "bg_tint": (50, 5,  5)},
    {"name": "Geographical",  "boss": "Hapi",             "accent": (40, 160, 255),  "bg_tint": (0, 20, 55)},
    {"name": "Architectural", "boss": "Seshat",           "accent": (200, 200, 190), "bg_tint": (20, 20, 25)},
    {"name": "Religious",     "boss": "Ra",               "accent": (255, 180,  0),  "bg_tint": (45, 20,  0)},
    {"name": "National",      "boss": "Nebty",            "accent": (255,  60,  60), "bg_tint": (40,  5,  5)},
    {"name": "Logistical",    "boss": "Khufu",            "accent": (190, 130,  60), "bg_tint": (35, 20,  5)},
    {"name": "Space & NARSS", "boss": "NARSS Director",  "accent": (140,  0, 255),  "bg_tint": (10,  0, 40)},
]

# ── Brick tiers ───────────────────────────────────────────────────────────────
BRICK_TIERS = [
    {"name": "mud",      "hp": 1, "pts":  10, "w": 0.34, "color": (139,  90,  43)},
    {"name": "stone",    "hp": 2, "pts":  25, "w": 0.27, "color": (130, 130, 140)},
    {"name": "marble",   "hp": 3, "pts":  50, "w": 0.18, "color": (210, 205, 225)},
    {"name": "granite",  "hp": 4, "pts": 100, "w": 0.11, "color": (100,  80,  70)},
    {"name": "gold",     "hp": 5, "pts": 200, "w": 0.07, "color": (255, 195,   0)},
    {"name": "obsidian", "hp": 6, "pts": 500, "w": 0.03, "color": ( 40,  10,  60)},
]

# ── Drop types ────────────────────────────────────────────────────────────────
DROPS = {
    # common
    "bronze_coin": {"color": (180, 110,  40), "label": "+10",   "rarity": "common"},
    "silver_coin": {"color": (180, 180, 200), "label": "+50",   "rarity": "rare"},
    "gold_coin":   {"color": (255, 215,   0), "label": "+200",  "rarity": "epic"},
    "heart":       {"color": (220,  40,  80), "label": "♥",     "rarity": "rare"},
    "shield":      {"color": ( 80, 160, 255), "label": "🛡",    "rarity": "rare"},
    # paddle power-ups
    "wide":        {"color": (100, 220, 100), "label": "⟺",    "rarity": "rare"},
    "magnet":      {"color": (180,   0, 255), "label": "⚡",    "rarity": "rare"},
    # ball power-ups
    "fireball":    {"color": (255,  80,   0), "label": "🔥",    "rarity": "rare"},
    "slow":        {"color": (200, 200, 255), "label": "❄",     "rarity": "common"},
    "multi_ball":  {"color": (255, 220,  80), "label": "×2",    "rarity": "epic"},
    # offensive
    "bomb":        {"color": (220,  60,  10), "label": "💣",    "rarity": "epic"},
    "rocket":      {"color": (200, 200, 255), "label": "🚀",    "rarity": "epic"},
    # score
    "star":        {"color": (255, 255, 100), "label": "★×2",   "rarity": "epic"},
    "diamond":     {"color": (120, 220, 255), "label": "+1k",   "rarity": "legendary"},
}
