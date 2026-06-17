"""
achievements.py — data-driven achievement definitions.

Each achievement is a dict with:
  id    — stable key stored in the save file
  name  — short title shown in the toast / list
  desc  — one-line description
  check — predicate over a flat "snapshot" dict assembled by
          GameState.check_achievements() (lifetime stats + current-run values)

Snapshot keys available to predicates:
  bricks_total, drops_total, best_combo, boss_clears, max_balls  (lifetime)
  score, round, best_round                                       (current/best)
  combo, balls, is_boss_clear                                    (event context)
"""

ACHIEVEMENTS = [
    {"id": "first_brick",      "name": "First Crack",     "desc": "Break your first brick",
     "check": lambda s: s["bricks_total"] >= 1},
    {"id": "first_drop",       "name": "Finders Keepers", "desc": "Collect your first drop",
     "check": lambda s: s["drops_total"] >= 1},
    {"id": "combo_8",          "name": "Combo Starter",   "desc": "Reach an ×8 combo",
     "check": lambda s: s["best_combo"] >= 8},
    {"id": "combo_16",         "name": "Combo King",      "desc": "Reach an ×16 combo",
     "check": lambda s: s["best_combo"] >= 16},
    {"id": "combo_32",         "name": "Unstoppable",     "desc": "Reach an ×32 combo",
     "check": lambda s: s["best_combo"] >= 32},
    {"id": "round_5",          "name": "Apprentice",      "desc": "Reach round 5",
     "check": lambda s: s["best_round"] >= 5},
    {"id": "round_10",         "name": "Archaeologist",   "desc": "Reach round 10 (clear a full cycle)",
     "check": lambda s: s["best_round"] >= 10},
    {"id": "round_18",         "name": "Pharaoh",         "desc": "Reach round 18",
     "check": lambda s: s["best_round"] >= 18},
    {"id": "round_27",         "name": "Legend",          "desc": "Reach round 27 (three cycles)",
     "check": lambda s: s["best_round"] >= 27},
    {"id": "bricks_100",       "name": "Stonebreaker",    "desc": "Break 100 bricks (lifetime)",
     "check": lambda s: s["bricks_total"] >= 100},
    {"id": "bricks_1000",      "name": "Demolisher",      "desc": "Break 1,000 bricks (lifetime)",
     "check": lambda s: s["bricks_total"] >= 1000},
    {"id": "score_10k",        "name": "High Roller",     "desc": "Score 10,000 in a single run",
     "check": lambda s: s["score"] >= 10000},
    {"id": "boss_slayer",      "name": "Boss Slayer",     "desc": "Clear a boss round",
     "check": lambda s: s["boss_clears"] >= 1},
    {"id": "ball_storm",       "name": "Ball Storm",      "desc": "Have 4+ balls at once",
     "check": lambda s: s["max_balls"] >= 4},
]

TOTAL = len(ACHIEVEMENTS)
