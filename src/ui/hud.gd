extends CanvasLayer

# 📊 HUD — score / lives / round / biome / combo. Instanced as a child of game.tscn.

@onready var score_label: Label = $VBox/ScoreLabel
@onready var lives_label: Label = $VBox/LivesLabel
@onready var round_label: Label = $VBox/RoundLabel
@onready var combo_label: Label = $VBox/ComboLabel

var gman: Node

func _ready() -> void:
	gman = get_node("/root/GameManager")
	gman.score_updated.connect(_on_score_updated)
	gman.lives_updated.connect(_on_lives_updated)
	gman.round_started.connect(_on_round_started)
	gman.combo_updated.connect(_on_combo_updated)
	_on_score_updated(gman.score)
	_on_lives_updated(gman.lives)
	_on_combo_updated(gman.combo)

func _on_score_updated(score: int) -> void:
	score_label.text = "Score: %d" % score

func _on_lives_updated(lives: int) -> void:
	lives_label.text = "❤️ x%d" % lives

func _on_round_started(round_data: Dictionary) -> void:
	round_label.text = "Round %d  •  Cycle %d  •  %s" % [
		round_data.get("round", 1),
		round_data.get("cycle", 1),
		round_data.get("biome_name", ""),
	]
	if round_data.get("is_boss_round", false):
		round_label.text += "  •  🏆 BOSS: %s" % round_data.get("boss", {}).get("name", "?")

func _on_combo_updated(combo: int) -> void:
	combo_label.visible = combo > 1
	combo_label.text = "Combo x%d" % combo
