extends RigidBody2D

# ⚡ Ball — Sun Disc (قرص الشمس)
# كِسرة — Egyptian Brick-Breaker

signal ball_lost()
signal brick_hit(brick_type: String)
signal wall_hit()

const BASE_SPEED: float = 350.0
const MAX_SPEED: float = 800.0
const SPEED_INCREMENT: float = 20.0
const DIAMETER: float = 24.0

const TYPE_COLORS: Dictionary = {
	"stone": Color("#A9A9A9"),
	"fire": Color("#FF4500"),
	"lightning": Color("#FFFF00"),
	"explosive": Color("#FF0000"),
	"void": Color("#2F2F2F"),
	"solar": Color("#FFD700"),
}

var current_speed: float = BASE_SPEED
var ball_type: String = "stone"  # stone, fire, lightning, explosive, void, solar
var ghost_mode: bool = false  # Pass through bricks (rare)
var explosive: bool = false
var attached: bool = false

@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var sprite: Sprite2D = $Sprite2D
@onready var trail: Trail2D = $Trail2D

func _ready() -> void:
	gravity_scale = 0
	continuous_cd = RigidBody2D.CCD_MODE_CAST_SHAPE
	if sprite.texture == null:
		sprite.texture = ProceduralTexture.make_circle(int(DIAMETER), Color.WHITE)
	body_entered.connect(_on_body_entered)
	update_ball_appearance()

func _process(_delta: float) -> void:
	if global_position.y > get_viewport_rect().size.y + 50:
		ball_lost.emit()
		queue_free()

func launch(direction: Vector2 = Vector2.UP) -> void:
	attached = false
	linear_velocity = direction * current_speed
	trail.enabled = true

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
	if linear_velocity.length() > 0:
		linear_velocity = linear_velocity.normalized() * current_speed

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("bricks"):
		var brick := body as Brick
		if brick:
			brick_hit.emit(brick.brick_type)
			if explosive:
				brick.explode()
			else:
				brick.hit(1)
	elif body.is_in_group("paddle"):
		var paddle := body as CharacterBody2D
		var hit_pos: float = (global_position.x - paddle.global_position.x) / (paddle.BASE_WIDTH * paddle.width_factor / 2.0)
		var angle: float = clampf(hit_pos, -1.0, 1.0) * deg_to_rad(60)
		var new_direction := Vector2(sin(angle), -abs(cos(angle))).normalized()
		linear_velocity = new_direction * current_speed
		var gman := get_node("/root/GameManager")
		if gman:
			gman.increment_combo()
	else:
		wall_hit.emit()

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
		"lightning":
			explosive = false
			ghost_mode = true
		"explosive":
			explosive = true
			ghost_mode = false
		"void":
			explosive = false
			ghost_mode = true
		"solar":
			explosive = false
			ghost_mode = true
	update_ball_appearance()

func update_ball_appearance() -> void:
	sprite.modulate = TYPE_COLORS.get(ball_type, Color.WHITE)
