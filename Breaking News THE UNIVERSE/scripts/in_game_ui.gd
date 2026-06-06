extends Control

# functions
func set_lives_label(amount : int) -> void:
	$Lives.text = "LIVES: " + str(amount)

func set_time_label(time : float) -> void:
	$Time.text = "TIME: " + str(int(time))
