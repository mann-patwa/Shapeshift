extends Area2D

@onready var game_manager = %GameManager
const COIN = preload("res://assets/sounds/coin.wav")

func _on_body_entered(_body: Node2D) -> void:
	# Play the coin sound effect with reduced volume
	play_sound(COIN, -15.0)
	
	# Add point to the game manager
	
	# Remove the coin from the scene
	queue_free()

# Helper method to create and play a sound effect
func play_sound(audio_stream, volume_db = -500.0):
	# Create a new AudioStreamPlayer
	var audio_player = AudioStreamPlayer.new()
	
	# Set the stream to our coin sound
	audio_player.stream = audio_stream
	
	# Set the volume (in decibels, negative values make it quieter)
	audio_player.volume_db = volume_db
	
	# Add it to the scene tree
	get_tree().root.add_child(audio_player)
	
	# Connect to the finished signal to remove the player after playing
	audio_player.finished.connect(func(): audio_player.queue_free())
	
	# Play the sound
	audio_player.play()
