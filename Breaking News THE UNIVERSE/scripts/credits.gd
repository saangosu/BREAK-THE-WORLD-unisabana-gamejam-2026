extends Control

signal finished

@onready var label = $ScrollContainer/CreditsLabel
var scroll_speed = 100.0 # pixels per second

func _ready():
	var music = $MenuMusic
	if music and music.stream is AudioStreamMP3:
		music.stream.loop = true

func _process(delta):
	label.position.y -= scroll_speed * delta
	if label.position.y < -label.size.y - 100:
		_on_finished()

func _on_return_button_pressed():
	_on_finished()

func _on_finished():
	finished.emit()
