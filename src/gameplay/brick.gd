extends StaticBody2D
class_name Brick

# 🧱 Brick — destructible block, configured at spawn time from LevelGenerator output.
# Rendered with a procedural flat-color texture (no art assets yet) so it works with zero
# asset pipeline; swap the texture generation for a sprite sheet later without touching logic.

signal destroyed(brick: Brick)

const TYPE_COLORS: Dictionary = {
	"mud": Color("#8B4513"),
	"stone": Color("#A9A9A9"),
	"marble": Color("#7CFC00"),
	"granite": Color("#DC143C"),
	"gold": Color("#FFD700"),
	"obsidian": Color("#2F2F2F"),
	"boss": Color("#FF1493"),
}

const BRICK_WIDTH: float = 52.0
const BRICK_HEIGHT: float = 20.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var brick_type: String = "mud"
var hp: int = 1
var max_hp: int = 1
var points: int = 10
var drop_chance: float = 0.1
var boss_name: String = ""

func _ready() -> void:
	add_to_group("bricks")
	if sprite.texture == null:
		sprite.texture = ProceduralTexture.make_rect(int(BRICK_WIDTH), int(BRICK_HEIGHT), Color.WHITE)
	update_visual()

func configure(data: Dictionary) -> void:
	brick_type = data.get("type", "mud")
	hp = data.get("hp", 1)
	max_hp = hp
	points = data.get("points", 10)
	drop_chance = data.get("drop_chance", 0.1)
	boss_name = data.get("boss_name", "")
	if is_inside_tree():
		update_visual()

func update_visual() -> void:
	sprite.modulate = TYPE_COLORS.get(brick_type, Color.WHITE)

func hit(damage: int = 1) -> void:
	hp -= damage
	if hp <= 0:
		break_brick()
	else:
		flash()

func explode() -> void:
	hp = 0
	break_brick()

func flash() -> void:
	var base_color: Color = TYPE_COLORS.get(brick_type, Color.WHITE)
	var tw := create_tween()
	tw.tween_property(sprite, "modulate", Color.WHITE, 0.04)
	tw.tween_property(sprite, "modulate", base_color, 0.08)

func break_brick() -> void:
	spawn_particles()
	destroyed.emit(self)
	queue_free()

func spawn_particles() -> void:
	var particles := CPUParticles2D.new()
	particles.position = global_position
	particles.amount = 12
	particles.lifetime = 0.5
	particles.one_shot = true
	particles.explosiveness = 1.0
	particles.direction = Vector2.UP
	particles.spread = 180.0
	particles.gravity = Vector2(0, 300)
	particles.initial_velocity_min = 40.0
	particles.initial_velocity_max = 120.0
	particles.scale_amount_min = 2.0
	particles.scale_amount_max = 4.0
	particles.color = TYPE_COLORS.get(brick_type, Color.WHITE)
	get_tree().current_scene.add_child(particles)
	particles.emitting = true
	var t := get_tree().create_timer(0.6)
	t.timeout.connect(particles.queue_free)
