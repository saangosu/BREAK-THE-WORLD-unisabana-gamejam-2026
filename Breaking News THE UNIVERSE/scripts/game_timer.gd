extends Timer

# constants
const update_time : float = 0.5
# variables 
var current_time : float
# signals
signal minigame_timed_out
signal must_update_label

#funcs
func set_timer(start_time) -> void:
	current_time = start_time
	must_update_label.emit(floor(current_time))
	start(update_time)

func update_current_time() -> void:
	current_time -= .5
	# checking if the time is an int
	if floor(current_time) == current_time:
		must_update_label.emit(current_time)
	if current_time > 0:
		start(update_time)
	else:
		minigame_timed_out.emit()

#connections
func _on_timeout() -> void:
	update_current_time()
