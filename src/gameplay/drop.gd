extends Area2D
class_name Drop

# 💎 Drop — falling pickup spawned when a brick breaks. Color-coded by rarity tier.

signal collected(drop_type: String)

const FALL_SPEED: float = 180.0
const DIAMETER: float = 18.0

const RARITY_COLORS: Dictionary = {
	"common": Color("#C0C0C0"),
	"rare": Color("#1E90FF"),
	"epic": Color("#9400D3"),
	"legendary": Color("#FFD700"),
}

const DROP_RARITY: Dictionary = {
	"bronze_coin": "common", "heart": "common", "shield": "common", "speed_up": "common",
	"silver_coin": "rare", "fireball": "rare", "wide_paddle": "rare", "multiball": "rare",
	"magnet": "rare", "slow": "rare",
	"gold_coin": "epic", "rocket": "epic", "laser": "epic", "star": "epic", "bomb": "epic",
	"chaos": "epic",
	"diamond": "legendary", "ankh": "legendary", "whirlwind": "legendary",
	"eye_of_horus": "legendary",
}

@onready var sprite: Sprite2D = $Sprite2D

var drop_type: String = "bronze_coin"

func _ready() -> void:
	add_to_group("drops")
	body_entered.connect(_on_body_entered)
	var rarity: String = DROP_RARITY.get(drop_type, "common")
	sprite.texture = ProceduralTexture.make_circle(int(DIAMETER), Color.WHITE)
	sprite.modulate = RARITY_COLORS.get(rarity, Color.WHITE)

func _process(delta: float) -> void:
	position.y += FALL_SPEED * delta
	if position.y > get_viewport_rect().size.y + 40:
		queue_free()

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("paddle"):
		collected.emit(drop_type)
		queue_free()
