"""
state.py — shared game state (score, lives, combo, round)
"""


class GameState:
    MAX_LIVES = 5
    SPEEDS = [0.5, 1.0, 1.5, 2.0]

    def __init__(self):
        self.reset()
        self.best_score = 0
        self.best_round = 1
        self.auto_play  = False
        self.speed_idx  = 1        # index into SPEEDS; default 1.0×

    @property
    def speed(self) -> float:
        return self.SPEEDS[self.speed_idx]

    def reset(self):
        self.score  = 0
        self.lives  = 3
        self.round  = 1
        self.combo  = 0
        self.mult   = 1.0     # score multiplier (star power-up)
        self.coins  = {"bronze": 0, "silver": 0, "gold": 0, "gem": 0}
        self.powerups: dict[str, bool] = {}

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
