
extends CanvasLayer

@onready var timer_label = $TimerLabel
@onready var message_label = $MessageLabel
@onready var game_timer = $GameTimer
var time_elapsed := 0.0

func _process(delta):
	time_elapsed += delta
	@warning_ignore("integer_division")
	var minutes = int(time_elapsed) / 60
	var seconds = int(time_elapsed) % 60
	var milliseconds = int((time_elapsed - int(time_elapsed)) * 1000)
	timer_label.text = "%02d:%02d:%03d" % [minutes, seconds, milliseconds]


func stop_timer():
	game_timer.stop()
	set_process(false)  # Stop counting time
	message_label.text = "You finished the game!"


func _on_finishblock_level_completed() -> void:
	stop_timer()
