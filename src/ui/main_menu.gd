extends Control

func _ready() -> void:
	$VBox/StartButton.pressed.connect(_on_start_pressed)

func _on_start_pressed() -> void:
	get_tree().change_scene_to_file("res://src/core/game.tscn")
