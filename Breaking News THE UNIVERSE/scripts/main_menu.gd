extends Node2D

# signals
signal start_game
signal quit

func _on_start_button_pressed() -> void:
	start_game.emit()

func _on_quit_button_pressed() -> void:
	quit.emit()
