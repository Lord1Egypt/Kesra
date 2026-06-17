"""
state.py — shared game state (score, lives, combo, round)
"""
import storage
from achievements import ACHIEVEMENTS


class GameState:
    MAX_LIVES = 5
    SPEEDS = [0.5, 1.0, 1.5, 2.0]

    def __init__(self):
        self.reset()
        self.best_score = 0
        self.best_round = 1
        self.auto_play  = False
        self.speed_idx  = 1        # index into SPEEDS; default 1.0×
        self.god_mode   = False    # Konami easter egg — session-only, not persisted
        self.load_persistent()

    @property
    def speed(self) -> float:
        return self.SPEEDS[self.speed_idx]

    # ── persistence ─────────────────────────────────────────────────────────────
    def load_persistent(self) -> None:
        d = storage.load()
        self.best_score = int(d.get("best_score", self.best_score))
        self.best_round = int(d.get("best_round", self.best_round))
        self.auto_play  = bool(d.get("auto_play", self.auto_play))
        si = int(d.get("speed_idx", self.speed_idx))
        self.speed_idx  = si if 0 <= si < len(self.SPEEDS) else 1
        self.muted      = bool(d.get("muted", False))
        self.tut_done   = bool(d.get("tut_done", False))
        self.unlocked   = set(d.get("unlocked", []))
        self.stats = {
            "bricks_total": int(d.get("bricks_total", 0)),
            "drops_total":  int(d.get("drops_total", 0)),
            "best_combo":   int(d.get("best_combo", 0)),
            "boss_clears":  int(d.get("boss_clears", 0)),
            "max_balls":    int(d.get("max_balls", 0)),
        }

    def save_persistent(self) -> None:
        storage.save({
            "best_score": self.best_score,
            "best_round": self.best_round,
            "auto_play":  self.auto_play,
            "speed_idx":  self.speed_idx,
            "muted":      self.muted,
            "tut_done":   self.tut_done,
            "unlocked":   sorted(self.unlocked),
            **self.stats,
        })

    # ── achievements ────────────────────────────────────────────────────────────
    def check_achievements(self, **ctx) -> list:
        """Evaluate all locked achievements against current stats; persist + return new."""
        snap = dict(self.stats)
        snap["score"]      = self.score
        snap["round"]      = self.round
        snap["best_round"] = self.best_round
        snap.update(ctx)
        newly = []
        for a in ACHIEVEMENTS:
            if a["id"] not in self.unlocked and a["check"](snap):
                self.unlocked.add(a["id"])
                newly.append(a)
        if newly:
            self.save_persistent()
        return newly

    def record_brick(self) -> list:
        self.stats["bricks_total"] += 1
        return self.check_achievements()

    def record_drop(self) -> list:
        self.stats["drops_total"] += 1
        return self.check_achievements()

    def record_combo(self, c: int) -> list:
        self.stats["best_combo"] = max(self.stats["best_combo"], c)
        return self.check_achievements(combo=c)

    def record_balls(self, n: int) -> list:
        self.stats["max_balls"] = max(self.stats["max_balls"], n)
        return self.check_achievements(balls=n)

    def record_round_clear(self, cleared_round: int, is_boss: bool) -> list:
        if is_boss:
            self.stats["boss_clears"] += 1
        return self.check_achievements(round=cleared_round, is_boss_clear=is_boss)

    def reset(self):
        self.score  = 0
        self.lives  = 3
        self.round  = 1
        self.combo  = 0
        self.mult   = 1.0     # score multiplier (star power-up)
        self.star_t = 0.0     # seconds remaining on ×2 star multiplier
        self.coins  = {"bronze": 0, "silver": 0, "gold": 0, "gem": 0}
        self.powerups: dict[str, bool] = {}

    def update_timers(self, dt: float) -> None:
        if self.star_t > 0:
            self.star_t = max(0.0, self.star_t - dt)
            if self.star_t <= 0:
                self.mult = 1.0

    def add_score(self, pts: int) -> int:
        earned = int(pts * self.mult * (1 + self.combo * 0.05))
        self.score     += earned
        self.best_score = max(self.best_score, self.score)
        return earned

    def add_combo(self) -> None:
        self.combo += 1

    def reset_combo(self) -> None:
        self.combo = 0

    def lose_life(self) -> None:
        if not self.powerups.get("shield"):
            self.lives -= 1
        self.powerups.pop("shield", None)
        self.reset_combo()

    def add_life(self) -> None:
        self.lives = min(self.MAX_LIVES, self.lives + 1)

    def next_round(self) -> None:
        self.round     += 1
        self.best_round = max(self.best_round, self.round)

    @property
    def game_over(self) -> bool:
        return self.lives <= 0
