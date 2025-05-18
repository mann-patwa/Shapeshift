extends Area2D

signal level_completed

func _on_body_entered(body: Node2D) -> void:
	print("Entered by: ", body.name)

	if body.is_in_group("player"):  # Make sure your player is in the 'player' group
		emit_signal("level_completed")
