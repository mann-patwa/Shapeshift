extends Control

func _on_button_1_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/game.tscn")

func _on_button_2_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/custom_map.tscn")
	
