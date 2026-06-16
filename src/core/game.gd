extends Node2D

# 🎮 Game — wires GameManager to the actual play scene. Rounds run back-to-back forever;
# there is no "you win" path, only "you lose all lives".

const BrickScene := preload("res://src/gameplay/brick.tscn")
const DropScene := preload("res://src/gameplay/drop.tscn")
const PaddleScene := preload("res://src/gameplay/paddle.tscn")
const BallScene := preload("res://src/gameplay/ball.tscn")

const BRICK_WIDTH: float = 56.0
const BRICK_HEIGHT: float = 24.0
const GRID_MARGIN_X: float = 16.0
const GRID_MARGIN_TOP: float = 80.0

var gman: Node
var paddle: CharacterBody2D
var ball: RigidBody2D
var bricks_alive: int = 0
var current_round_data: Dictionary = {}

@onready var bricks_container: Node2D = $Bricks
@onready var drops_container: Node2D = $Drops
@onready var camera: Camera2D = $Camera2D

func _ready() -> void:
	gman = get_node("/root/GameManager")
	gman.round_started.connect(_on_round_started)
	gman.game_over.connect(_on_game_over)
	spawn_paddle()
	gman.start_run()
	spawn_ball()

func spawn_paddle() -> void:
	paddle = PaddleScene.instantiate()
	paddle.position = Vector2(get_viewport_rect().size.x / 2.0, get_viewport_rect().size.y - 48)
	add_child(paddle)

func spawn_ball() -> void:
	ball = BallScene.instantiate()
	ball.position = paddle.get_launch_position()
	ball.ball_lost.connect(_on_ball_lost)
	add_child(ball)
	await get_tree().process_frame
	ball.launch(Vector2.UP)

func _on_round_started(round_data: Dictionary) -> void:
	current_round_data = round_data
	clear_round()
	build_grid(round_data.get("grid", []))

func clear_round() -> void:
	for child in bricks_container.get_children():
		child.queue_free()
	for child in drops_container.get_children():
		child.queue_free()

func build_grid(grid: Array) -> void:
	bricks_alive = 0
	var start_x: float = GRID_MARGIN_X + BRICK_WIDTH / 2.0
	for row_idx in range(grid.size()):
		var row: Array = grid[row_idx]
		for col_idx in range(row.size()):
			var cell = row[col_idx]
			if cell == null:
				continue
			var brick: Brick = BrickScene.instantiate()
			bricks_container.add_child(brick)
			brick.position = Vector2(start_x + col_idx * BRICK_WIDTH, GRID_MARGIN_TOP + row_idx * BRICK_HEIGHT)
			brick.configure(cell)
			brick.destroyed.connect(_on_brick_destroyed)
			bricks_alive += 1
	if bricks_alive == 0:
		_advance_round()

func _on_brick_destroyed(brick: Brick) -> void:
	gman.increment_combo()
	gman.add_score(brick.points)
	spawn_score_popup(brick.global_position, brick.points)
	if gman.combo > 0 and gman.combo % 10 == 0:
		shake_camera()
	if randf() < brick.drop_chance:
		spawn_drop(brick.global_position, current_round_data.get("drops_allowed", ["bronze_coin"]))
	bricks_alive -= 1
	if bricks_alive <= 0:
		_advance_round()

func spawn_drop(pos: Vector2, allowed: Array) -> void:
	if allowed.is_empty():
		return
	var drop: Drop = DropScene.instantiate()
	drop.drop_type = allowed[randi() % allowed.size()]
	drop.position = pos
	drop.collected.connect(_on_drop_collected)
	drops_container.add_child(drop)

func _on_drop_collected(drop_type: String) -> void:
	match drop_type:
		"bronze_coin":
			gman.add_coin("bronze", 10)
			gman.add_score(10)
		"silver_coin":
			gman.add_coin("silver", 5)
			gman.add_score(50)
		"gold_coin":
			gman.add_coin("gold", 2)
			gman.add_score(200)
		"diamond":
			gman.add_coin("gem", 1)
			gman.add_score(1000)
		"heart", "ankh":
			gman.add_life()
		"shield":
			gman.powerups_active["shield"] = true
		"wide_paddle":
			paddle.resize(2.0, 10.0)
		"fireball":
			ball.set_ball_type("fire")
		"magnet":
			paddle.activate_magnet(8.0)
		"star":
			gman.powerups_active["star"] = true
			get_tree().create_timer(15.0).timeout.connect(func(): gman.powerups_active.erase("star"))
		_:
			pass

func _on_ball_lost() -> void:
	gman.reset_combo()
	gman.lose_life()
	if gman.lives > 0:
		spawn_ball()

func _advance_round() -> void:
	gman.advance_round()

func _on_game_over() -> void:
	get_tree().change_scene_to_file("res://src/ui/main_menu.tscn")

func spawn_score_popup(pos: Vector2, amount: int) -> void:
	var label := Label.new()
	label.text = "+%d" % amount
	label.position = pos
	add_child(label)
	var tw := create_tween()
	tw.tween_property(label, "position", pos + Vector2(0, -40), 0.6)
	tw.parallel().tween_property(label, "modulate:a", 0.0, 0.6)
	tw.tween_callback(label.queue_free)

func shake_camera(strength: float = 6.0, duration: float = 0.15) -> void:
	var original: Vector2 = camera.position
	var tw := create_tween()
	tw.tween_method(func(_t): camera.position = original + Vector2(randf_range(-strength, strength), randf_range(-strength, strength)), 0.0, 1.0, duration)
	tw.tween_callback(func(): camera.position = original)
