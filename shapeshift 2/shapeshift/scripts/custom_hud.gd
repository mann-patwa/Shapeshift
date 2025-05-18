extends CanvasLayer

var elapsed_time := 0.0
var is_running := true  # flag to control timer

func _process(delta):
	if is_running:
		elapsed_time += delta
		$TimerLabel.text = format_time(elapsed_time)

func format_time(seconds: float) -> String:
	var mins := int(seconds) / 60
	var secs := int(seconds) % 60
	var millis := int((seconds - int(seconds)) * 100)
	return "%02d:%02d.%02d" % [mins, secs, millis]

# Call this to stop the timer
func stop_timer():
	is_running = false
