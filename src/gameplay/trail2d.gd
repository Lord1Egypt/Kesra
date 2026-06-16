extends Line2D
class_name Trail2D

# ✨ Trail2D — simple world-space trail effect for the ball. Uses top_level so it ignores the
# parent's transform and records the parent's absolute position history each frame instead.

@export var max_points: int = 16
var enabled: bool = true

func _ready() -> void:
	top_level = true
	width = 6.0
	default_color = Color(1, 1, 1, 0.5)

func _process(_delta: float) -> void:
	if not enabled or not get_parent():
		return
	add_point(get_parent().global_position)
	while get_point_count() > max_points:
		remove_point(0)
