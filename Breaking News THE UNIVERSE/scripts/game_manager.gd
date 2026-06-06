extends Node
class_name GameManager

# constants
const max_time := 10.0
const min_time := 1.0
const max_lives := 3

# onreadies
@onready var current_scene = $CurrentScene

# dictionaries
var levels := ["res://scenes/eggs/eggs.tscn", "res://scenes/minigame_2/minigame_2.tscn"]
var user_interfaces := {"main_menu" : "res://scenes/main_menu.tscn"}

# arrays
var current_signals = []

# variables
var current_lives : int
var current_time : float
var current_score : int
var unplayed_levels : Array

# built_in
func _ready() -> void:
	load_main_menu()

# funcs
func clear_connections() -> void:
	for signal_variant : Signal in current_signals:
		var signal_connections = signal_variant.get_connections()
		for connection in signal_connections:
			signal_variant.disconnect(connection.callable)

func load_main_menu() -> void:
	var new_scene : PackedScene = load(user_interfaces["main_menu"])
	if current_scene:
		current_scene.queue_free()
	current_scene = new_scene.instantiate()
	
	current_signals.clear()
	current_signals.append(current_scene.start_game)
	current_signals.append(current_scene.quit)
	current_signals[0].connect(start_game)
	current_signals[1].connect(quit)
	
	add_child(current_scene)

func select_minigame() -> void:
	if unplayed_levels.is_empty():
		show_final_score()
		return
		
	var game_index = randi_range(0, unplayed_levels.size() - 1)
	var minigame_scene = load(unplayed_levels[game_index])
	unplayed_levels.remove_at(game_index)
	
	if current_scene:
		current_scene.queue_free()
		
	current_scene = minigame_scene.instantiate()
	
	# Detectamos si es un Minigame y conectamos sus señales
	if current_scene is Minigame:
		current_scene.completed.connect(_on_minigame_completed)
		current_scene.lost.connect(_on_minigame_lost)
		if current_scene.has_signal("point_scored"):
			current_scene.point_scored.connect(_on_minigame_point_scored)
		
	add_child(current_scene)

func show_final_score() -> void:
	if current_scene:
		current_scene.queue_free()
		current_scene = null
		
	var canvas = CanvasLayer.new()
	add_child(canvas)
	current_scene = canvas # Assign canvas to current_scene so it gets cleaned up later
	
	var label = Label.new()
	# The score can be much higher than the number of levels now
	label.text = "¡JUEGO TERMINADO!\n\nPlanetas Rotos: " + str(current_score)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 100)
	label.size = Vector2(1920, 1080)
	canvas.add_child(label)
	
	await get_tree().create_timer(4.0).timeout
	load_main_menu()

func _on_minigame_point_scored():
	current_score += 1

func _on_minigame_completed():
	select_minigame()

func _on_minigame_lost():
	load_main_menu()

func start_game() -> void:
	current_lives = 3
	current_time = max_time
	current_score = 0
	unplayed_levels = levels.duplicate()
	select_minigame()

func quit() -> void:
	get_tree().quit()
