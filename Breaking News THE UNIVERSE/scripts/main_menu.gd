extends Node2D

# signals
signal start_game
signal quit
signal credits_requested

func _ready():
	var music = $MenuMusic
	if music.stream is AudioStreamMP3:
		music.stream.loop = true

func _on_start_button_pressed() -> void:
	start_game.emit()

func _on_quit_button_pressed() -> void:
	quit.emit()

func _on_credits_button_pressed() -> void:
	credits_requested.emit()
