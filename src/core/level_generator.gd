extends RefCounted
class_name LevelGenerator

## Procedural infinite round generator. There is no level cap: this is the only path that
## produces playable content. Round N maps to a biome and a cycle:
##   position_in_cycle = ((N-1) % 9) + 1   → which of the 9 worlds this round is themed as
##   cycle              = floor((N-1)/9)+1 → how many full passes over the 9 worlds so far
## Position 8 of every cycle is a boss round; the boss rotates with the cycle number so every
## one of the 9 recurring bosses gets used over a span of 9 cycles, then the rotation repeats
## with higher stats. See ROADMAP.md "Vision" for why this replaces the old finite level list.

const GRID_COLS: int = 8
const BASE_ROWS: int = 5
const MAX_ROWS: int = 10

const BIOMES: Dictionary = {
	1: {"name": "🧪 Scientific", "background": "#0A0A2E", "colors": ["#FFD700", "#FF6B35", "#00D4FF"], "boss": "Imhotep"},
	2: {"name": "🎨 Artistic", "background": "#2E0A2E", "colors": ["#FFD700", "#FF69B4", "#7CFC00"], "boss": "Thoth"},
	3: {"name": "📜 Historical", "background": "#2E1A0A", "colors": ["#DC143C", "#FFD700", "#8B4513"], "boss": "Ramesses II"},
	4: {"name": "🌍 Geographical", "background": "#0A1E2E", "colors": ["#1E90FF", "#7CFC00", "#D4A574"], "boss": "Hapi"},
	5: {"name": "🏛️ Architectural", "background": "#1A1A1A", "colors": ["#D4A574", "#A9A9A9", "#FFD700"], "boss": "Seshat"},
	6: {"name": "☀️ Religious", "background": "#2E2A0A", "colors": ["#FFD700", "#FF6B35", "#DC143C"], "boss": "Ra"},
	7: {"name": "🇪🇬 National", "background": "#0A0A0A", "colors": ["#DC143C", "#FFFFFF", "#000000"], "boss": "Nebty"},
	8: {"name": "📦 Logistical", "background": "#1A1408", "colors": ["#8B4513", "#A9A9A9", "#D4A574"], "boss": "Khufu"},
	9: {"name": "🚀 Space & Rockets", "background": "#000010", "colors": ["#00D4FF", "#FFD700", "#FFFFFF"], "boss": "NARSS Director"},
}

const BRICK_TIERS: Array = [
	{"type": "mud", "hp": 1, "points": 10, "weight": 40.0, "scales": false},
	{"type": "stone", "hp": 2, "points": 20, "weight": 25.0, "scales": false},
	{"type": "marble", "hp": 3, "points": 30, "weight": 15.0, "scales": true},
	{"type": "granite", "hp": 5, "points": 50, "weight": 10.0, "scales": true},
	{"type": "gold", "hp": 1, "points": 100, "weight": 6.0, "scales": false},
	{"type": "obsidian", "hp": 10, "points": 100, "weight": 4.0, "scales": true},
]

static func generate_round(round_number: int) -> Dictionary:
	var cycle: int = int(floor(float(round_number - 1) / 9.0)) + 1
	var position_in_cycle: int = ((round_number - 1) % 9) + 1
	var biome: Dictionary = BIOMES[position_in_cycle]
	var is_boss_round: bool = position_in_cycle == 8
	var difficulty_multiplier: float = 1.0 + (round_number - 1) * 0.04

	var data: Dictionary = {
		"round": round_number,
		"cycle": cycle,
		"biome_index": position_in_cycle,
		"biome_name": biome.name,
		"is_boss_round": is_boss_round,
		"difficulty_multiplier": difficulty_multiplier,
		"theme": {"background": biome.background, "brick_colors": biome.colors},
		"drops_allowed": drop_table_for_round(round_number),
	}

	if is_boss_round:
		var boss_biome_index: int = ((cycle - 1) % 9) + 1
		var appearance: int = int(floor(float(cycle - 1) / 9.0)) + 1
		var boss_biome: Dictionary = BIOMES[boss_biome_index]
		data["boss"] = {"name": boss_biome.boss, "appearance": appearance}
		data["grid"] = generate_boss_grid(boss_biome.boss, appearance)
	else:
		data["grid"] = generate_brick_grid(difficulty_multiplier)

	return data

static func generate_brick_grid(difficulty_multiplier: float) -> Array:
	var rows: int = clampi(BASE_ROWS + int(difficulty_multiplier * 2.0), BASE_ROWS, MAX_ROWS)
	var gap_chance: float = clampf(0.15 - difficulty_multiplier * 0.01, 0.0, 0.15)
	var grid: Array = []
	for _row in range(rows):
		var row: Array = []
		for _col in range(GRID_COLS):
			if randf() < gap_chance:
				row.append(null)
			else:
				row.append(pick_weighted_brick(difficulty_multiplier))
		grid.append(row)
	return grid

static func pick_weighted_brick(difficulty_multiplier: float) -> Dictionary:
	var total_weight: float = 0.0
	var weights: Array = []
	for tier in BRICK_TIERS:
		var w: float = tier.weight
		if tier.scales:
			w *= difficulty_multiplier
		weights.append(w)
		total_weight += w
	var roll: float = randf() * total_weight
	var accumulated: float = 0.0
	for i in range(BRICK_TIERS.size()):
		accumulated += weights[i]
		if roll <= accumulated:
			var tier: Dictionary = BRICK_TIERS[i]
			var hp: int = max(1, int(round(tier.hp * (1.0 if not tier.scales else min(difficulty_multiplier, 3.0)))))
			return {"type": tier.type, "hp": hp, "points": tier.points, "drop_chance": 0.12}
	var fallback: Dictionary = BRICK_TIERS[0]
	return {"type": fallback.type, "hp": fallback.hp, "points": fallback.points, "drop_chance": 0.12}

static func generate_boss_grid(boss_name: String, appearance: int) -> Array:
	var rows: int = 6
	var grid: Array = []
	for _row in range(rows):
		var row: Array = []
		for _col in range(GRID_COLS):
			row.append({
				"type": "boss",
				"hp": 5 * appearance,
				"points": 200 * appearance,
				"drop_chance": 0.5,
				"boss_name": boss_name,
			})
		grid.append(row)
	return grid

static func drop_table_for_round(round_number: int) -> Array:
	var table: Array = ["bronze_coin", "heart", "shield"]
	if round_number >= 5:
		table += ["fireball", "wide_paddle", "multiball", "magnet", "slow"]
	if round_number >= 15:
		table += ["rocket", "laser", "star", "bomb"]
	if round_number >= 30:
		table += ["diamond", "ankh", "eye_of_horus"]
	return table
