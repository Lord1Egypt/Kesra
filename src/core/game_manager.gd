extends Node2D

# 🎮 Game Manager — Core game state controller
# كِسرة — Egyptian Brick-Breaker

signal score_updated(score: int)
signal lives_updated(lives: int)
signal level_loaded(level_data: Dictionary)
signal game_over()
signal level_complete()

enum GameMode { STORY, ENDLESS, CHALLENGE, TOURNAMENT, PUZZLE }
enum Difficulty { EASY, NORMAL, HARD, NIGHTMARE, HELL }

var game_mode: GameMode = GameMode.STORY
var difficulty: Difficulty = Difficulty.NORMAL

var current_world: int = 1
var current_level: int = 1
var score: int = 0
var lives: int = 3
var max_lives: int = 9
var combo: int = 0
var max_combo: int = 0

var coins: Dictionary = {
	"bronze": 0,
	"silver": 0,
	"gold": 0,
	"gem": 0
}

var powerups_active: Dictionary = {}
var achievements_unlocked: Array = []
var save_data: Dictionary = {}

# Paddle upgrades
var paddle_level: int = 1
var ball_level: int = 1
var rockets_unlocked: Array = ["scarab"]

# World names
const WORLD_NAMES: Dictionary = {
	1: "🧪 Scientific",
	2: "🎨 Artistic", 
	3: "📜 Historical",
	4: "🌍 Geographical",
	5: "🏛️ Architectural",
	6: "☀️ Religious",
	7: "🇪🇬 National",
	8: "📦 Logistical",
	9: "🚀 Space & Rockets"
}

func _ready() -> void:
	load_save_data()

func start_game() -> void:
	score = 0
	lives = 3
	combo = 0
	current_world = 1
	current_level = 1
	load_level(current_world, current_level)

func load_level(world: int, level: int) -> void:
	var level_path = "res://levels/world_%d/level_%d.json" % [world, level]
	var file = FileAccess.open(level_path, FileAccess.READ)
	if file:
		var json = JSON.new()
		var data = json.parse_string(file.get_as_text())
		level_loaded.emit(data)
	else:
		push_error("Level not found: ", level_path)

func add_score(points: int) -> void:
	var multiplier = 1
	if powerups_active.has("star"):
		multiplier = 2
	score += points * multiplier * max(1, combo)
	score_updated.emit(score)

func lose_life() -> void:
	if powerups_active.has("shield"):
		powerups_active.erase("shield")
		return
	lives -= 1
	lives_updated.emit(lives)
	if lives <= 0:
		game_over.emit()

func add_life() -> void:
	lives = min(lives + 1, max_lives)
	lives_updated.emit(lives)

func increment_combo() -> void:
	combo += 1
	max_combo = max(max_combo, combo)

func reset_combo() -> void:
	combo = 0

func add_coin(type: String, amount: int = 1) -> void:
	if coins.has(type):
		coins[type] += amount

func spend_coin(type: String, amount: int) -> bool:
	if coins.has(type) and coins[type] >= amount:
		coins[type] -= amount
		return true
	return false

func save_save_data() -> void:
	var save_dict = {
		"score": score,
		"lives": lives,
		"current_world": current_world,
		"current_level": current_level,
		"coins": coins,
		"paddle_level": paddle_level,
		"ball_level": ball_level,
		"rockets_unlocked": rockets_unlocked,
		"achievements": achievements_unlocked
	}
	var save_file = FileAccess.open("user://save_data/save.save", FileAccess.WRITE)
	if save_file:
		var json = JSON.new()
		save_file.store_line(json.stringify(save_dict))

func load_save_data() -> void:
	var save_file = FileAccess.open("user://save_data/save.save", FileAccess.READ)
	if save_file:
		var json = JSON.new()
		var data = json.parse_string(save_file.get_as_text())
		if data:
			score = data.get("score", 0)
			lives = data.get("lives", 3)
			current_world = data.get("current_world", 1)
			current_level = data.get("current_level", 1)
			coins = data.get("coins", {"bronze": 0, "silver": 0, "gold": 0, "gem": 0})
			paddle_level = data.get("paddle_level", 1)
			ball_level = data.get("ball_level", 1)
			rockets_unlocked = data.get("rockets_unlocked", ["scarab"])
			achievements_unlocked = data.get("achievements", [])
