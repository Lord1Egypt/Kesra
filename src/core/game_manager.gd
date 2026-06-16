extends Node

# 🎮 Game Manager — Core game state controller (autoload singleton)
# كِسرة — Egyptian Brick-Breaker. Infinite mode: there is no level cap, only a monotonically
# increasing round counter. See LevelGenerator for how round → biome/cycle/boss is derived.

signal score_updated(score: int)
signal lives_updated(lives: int)
signal round_started(round_data: Dictionary)
signal combo_updated(combo: int)
signal game_over()

enum GameMode { ENDLESS, CHALLENGE, TOURNAMENT, PUZZLE }
enum Difficulty { EASY, NORMAL, HARD, NIGHTMARE, HELL }

var game_mode: GameMode = GameMode.ENDLESS
var difficulty: Difficulty = Difficulty.NORMAL

var current_round: int = 1
var best_round: int = 1
var score: int = 0
var best_score: int = 0
var lives: int = 3
var max_lives: int = 9
var combo: int = 0
var max_combo: int = 0

var coins: Dictionary = {
	"bronze": 0,
	"silver": 0,
	"gold": 0,
	"gem": 0,
}

var powerups_active: Dictionary = {}
var achievements_unlocked: Array = []

var paddle_level: int = 1
var ball_level: int = 1
var rockets_unlocked: Array = ["scarab"]

func _ready() -> void:
	load_save_data()

func start_run() -> void:
	score = 0
	lives = 3
	combo = 0
	current_round = 1
	powerups_active.clear()
	start_round()

func start_round() -> void:
	var round_data: Dictionary = LevelGenerator.generate_round(current_round)
	round_started.emit(round_data)

func advance_round() -> void:
	current_round += 1
	best_round = max(best_round, current_round)
	start_round()

func add_score(points: int) -> void:
	var multiplier: int = 1
	if powerups_active.has("star"):
		multiplier = 2
	score += points * multiplier * max(1, combo)
	best_score = max(best_score, score)
	score_updated.emit(score)

func lose_life() -> void:
	if powerups_active.has("shield"):
		powerups_active.erase("shield")
		return
	lives -= 1
	lives_updated.emit(lives)
	if lives <= 0:
		save_save_data()
		game_over.emit()

func add_life() -> void:
	lives = min(lives + 1, max_lives)
	lives_updated.emit(lives)

func increment_combo() -> void:
	combo += 1
	max_combo = max(max_combo, combo)
	combo_updated.emit(combo)

func reset_combo() -> void:
	combo = 0
	combo_updated.emit(combo)

func add_coin(type: String, amount: int = 1) -> void:
	if coins.has(type):
		coins[type] += amount

func spend_coin(type: String, amount: int) -> bool:
	if coins.has(type) and coins[type] >= amount:
		coins[type] -= amount
		return true
	return false

func save_save_data() -> void:
	var save_dict: Dictionary = {
		"best_score": best_score,
		"best_round": best_round,
		"coins": coins,
		"paddle_level": paddle_level,
		"ball_level": ball_level,
		"rockets_unlocked": rockets_unlocked,
		"achievements": achievements_unlocked,
	}
	DirAccess.make_dir_recursive_absolute("user://save_data")
	var save_file := FileAccess.open("user://save_data/save.save", FileAccess.WRITE)
	if save_file:
		var json := JSON.new()
		save_file.store_line(json.stringify(save_dict))

func load_save_data() -> void:
	var save_file := FileAccess.open("user://save_data/save.save", FileAccess.READ)
	if save_file:
		var json := JSON.new()
		var data = json.parse_string(save_file.get_as_text())
		if data:
			best_score = data.get("best_score", 0)
			best_round = data.get("best_round", 1)
			coins = data.get("coins", {"bronze": 0, "silver": 0, "gold": 0, "gem": 0})
			paddle_level = data.get("paddle_level", 1)
			ball_level = data.get("ball_level", 1)
			rockets_unlocked = data.get("rockets_unlocked", ["scarab"])
			achievements_unlocked = data.get("achievements", [])
