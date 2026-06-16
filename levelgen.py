"""
levelgen.py — procedural infinite round generator
Same biome/cycle/difficulty logic as the original GDScript version.
"""
import random
from settings import BIOMES, BRICK_TIERS, BRICK_COLS, DROPS


def generate_round(round_number: int) -> dict:
    cycle    = (round_number - 1) // 9 + 1
    biome_i  = (round_number - 1) % 9            # 0-based index
    biome    = BIOMES[biome_i]
    is_boss  = ((round_number - 1) % 9) == 7     # every 8th slot (0-indexed)
    diff     = 1.0 + (round_number - 1) * 0.04   # +4% per round

    base_rows = min(5 + (round_number - 1) // 3, 10)

    grid = _make_grid(base_rows, diff, biome, is_boss, cycle)

    # drops unlock progressively
    drops = ["bronze_coin"]
    if round_number >= 5:
        drops += ["silver_coin", "heart"]
    if round_number >= 15:
        drops += ["gold_coin", "shield", "wide"]
    if round_number >= 30:
        drops += ["fireball", "magnet", "slow"]

    return {
        "round":    round_number,
        "cycle":    cycle,
        "biome":    biome,
        "biome_i":  biome_i,
        "is_boss":  is_boss,
        "diff":     diff,
        "grid":     grid,
        "drops":    drops,
    }


def _make_grid(rows: int, diff: float, biome: dict,
               is_boss: bool, cycle: int) -> list[list[dict | None]]:
    if is_boss:
        return _boss_grid(biome, cycle, diff)
    return _normal_grid(rows, diff)


def _normal_grid(rows: int, diff: float) -> list[list[dict | None]]:
    grid = []
    for row in range(rows):
        row_list = []
        for col in range(BRICK_COLS):
            if random.random() < 0.12:      # ~12% empty cells for variety
                row_list.append(None)
            else:
                tier = _pick_tier(diff, row / max(1, rows - 1))
                row_list.append(_brick_cell(tier, diff))
        grid.append(row_list)
    return grid


def _boss_grid(biome: dict, cycle: int, diff: float) -> list[list[dict | None]]:
    """Fixed 6-row health-scaled boss grid."""
    scaled_hp = max(1, round(3 * cycle))
    boss_tier = {
        "name":    biome["boss"],
        "hp":      scaled_hp,
        "max_hp":  scaled_hp,
        "pts":     500 * cycle,
        "color":   (255, 215, 0),
        "is_boss": True,
        "drop_chance": 0.8,
    }
    # a dense 6×8 grid of gold bricks scaled by cycle
    grid = []
    for _ in range(6):
        row = []
        for _ in range(BRICK_COLS):
            row.append(dict(boss_tier))
        grid.append(row)
    return grid


def _pick_tier(diff: float, row_depth: float) -> dict:
    """Higher rows (further from player) tend to have harder bricks."""
    weights = []
    for i, t in enumerate(BRICK_TIERS):
        w = t["w"] * (1.0 + row_depth * i * 0.3) * (1.0 + (diff - 1.0) * i * 0.15)
        weights.append(w)
    total = sum(weights)
    r = random.uniform(0, total)
    acc = 0.0
    for t, w in zip(BRICK_TIERS, weights):
        acc += w
        if r <= acc:
            return t
    return BRICK_TIERS[-1]


def _brick_cell(tier: dict, diff: float) -> dict:
    hp = max(1, round(tier["hp"] * (1.0 + (diff - 1.0) * 0.3)))
    return {
        "name":        tier["name"],
        "hp":          hp,
        "max_hp":      hp,
        "pts":         int(tier["pts"] * diff),
        "color":       tier["color"],
        "is_boss":     False,
        "drop_chance": 0.08 + (diff - 1.0) * 0.005,
    }
