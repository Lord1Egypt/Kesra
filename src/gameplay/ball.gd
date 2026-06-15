extends RigidBody2D

# ⚡ Ball — Sun Disc (قرص الشمس)
# كِسرة — Egyptian Brick-Breaker

signal ball_lost()
signal brick_hit(brick_type: String)
signal wall_hit()

const BASE_SPEED: float = 350.0
const MAX_SPEED: float = 800.0
const SPEED_INCREMENT: float = 20.0

var current_speed: float = BASE_SPEED
var ball_type: String = "stone"  # stone, fire, lightning, explosive, void, solar
var trail_enabled: bool = true
var ghost_mode: bool = false  # Pass through bricks (rare)
var explosive: bool = false
var attached: bool = false

@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var sprite: Sprite2D = $Sprite2D
@onready var trail: Trail2D = $Trail2D

func _ready() -> void:
	gravity_scale = 0
	continuous_cd = true
	update_ball_appearance()

func launch(direction: Vector2 = Vector2.UP) -> void:
	attached = false
	linear_velocity = direction * current_speed
	trail.enabled = true

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
	# Maintain constant speed
	if linear_velocity.length() > 0:
		linear_velocity = linear_velocity.normalized() * current_speed

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("bricks"):
		var brick = body as Brick
		if brick:
			brick_hit.emit(brick.type)
			if explosive:
				brick.explode()
			elif ghost_mode:
				brick.hit(1)  # Still hit it, but pass through
			else:
				brick.hit(1)
	elif body.is_in_group("paddle"):
		# Calculate reflection angle based on where ball hit paddle
		var paddle = body as Paddle
		var hit_pos = (global_position.x - paddle.global_position.x) / (paddle.BASE_WIDTH * paddle.width_factor / 2)
		var angle = hit_pos * deg_to_rad(60)
		var new_direction = Vector2(sin(angle), -abs(cos(angle))).normalized()
		linear_velocity = new_direction * current_speed
		var gman = get_node("/root/GameManager")
		if gman:
			gman.increment_combo()

func increase_speed(amount: float = SPEED_INCREMENT) -> void:
	current_speed = min(current_speed + amount, MAX_SPEED)

func decrease_speed(amount: float = SPEED_INCREMENT) -> void:
	current_speed = max(current_speed - amount, BASE_SPEED / 2)

func set_ball_type(type: String) -> void:
	ball_type = type
	match type:
		"fire":
			explosive = false
			ghost_mode = false
			# Fire: burns 3 adjacent bricks automatically
		"lightning":
			explosive = false
			ghost_mode = true  # Passes through bricks
			# But only damages 1
		"explosive":
			explosive = true
			ghost_mode = false
		"void":
			explosive = false
			ghost_mode = true
			# Destroys any brick it touches
		"solar":
			explosive = false
			ghost_mode = true
			# Passes through everything
	update_ball_appearance()

func update_ball_appearance() -> void:
	match ball_type:
		"stone":
			sprite.texture = preload("res://assets/textures/ball_stone.png")
		"fire":
			sprite.texture = preload("res://assets/textures/ball_fire.png")
		"lightning":
			sprite.texture = preload("res://assets/textures/ball_lightning.png")
		"explosive":
			sprite.texture = preload("res://assets/textures/ball_explosive.png")
		"void":
			sprite.texture = preload("res://assets/textures/ball_void.png")
		"solar":
			sprite.texture = preload("res://assets/textures/ball_solar.png")

# Called when ball falls off screen
func _on_visible_on_screen_notifier_2d_screen_exited() -> void:
	if global_position.y > get_viewport_rect().size.y + 50:
		ball_lost.emit()
		queue_free()
