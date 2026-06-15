extends CharacterBody2D

# 🏏 Paddle — Solar Barque (مركب الشمس)
# كِسرة — Egyptian Brick-Breaker

signal paddle_resized(width_factor: float)
signal powerup_activated(powerup_type: String)

const BASE_WIDTH: float = 128.0
const SPEED: float = 600.0
const MARGIN: float = 16.0

var width_factor: float = 1.0
var paddle_color: Color = Color("#D4A574")
var glow_enabled: bool = false
var sticky: bool = false
var has_ball: bool = true  # Ball attached to paddle
var fire_effect: bool = false

@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var sprite: Sprite2D = $Sprite2D
@onready var screen_size: Vector2 = get_viewport_rect().size

func _ready() -> void:
	update_paddle_size()
	
func _physics_process(delta: float) -> void:
	var direction = Input.get_axis("ui_left", "ui_right")
	velocity.x = direction * SPEED
	move_and_slide()
	
	# Clamp to screen
	var half_width = (BASE_WIDTH * width_factor) / 2
	global_position.x = clamp(global_position.x, MARGIN + half_width, screen_size.x - MARGIN - half_width)

func update_paddle_size() -> void:
	var new_width = BASE_WIDTH * width_factor
	collision_shape.shape.size.x = new_width
	sprite.scale.x = width_factor
	paddle_resized.emit(width_factor)

func resize(width_multiplier: float, duration: float = 10.0) -> void:
	width_factor = width_multiplier
	update_paddle_size()
	if duration > 0:
		await get_tree().create_timer(duration).timeout
		width_factor = 1.0
		update_paddle_size()

func activate_sticky(attached_ball: Node2D) -> void:
	sticky = true
	has_ball = true
	attached_ball.global_position = global_position + Vector2(0, -32)

func release_ball() -> void:
	sticky = false
	has_ball = false

func activate_fire(duration: float = 15.0) -> void:
	fire_effect = true
	sprite.modulate = Color("#FF4500")
	await get_tree().create_timer(duration).timeout
	fire_effect = false
	sprite.modulate = Color.WHITE

func activate_magnet(duration: float = 8.0) -> void:
	# Magnet effect — pulls coins toward player
	glow_enabled = true
	sprite.modulate = Color.MAGENTA
	await get_tree().create_timer(duration).timeout
	glow_enabled = false
	sprite.modulate = Color.WHITE

func get_launch_position() -> Vector2:
	return global_position + Vector2(0, -32)
