extends Node
class_name GameManager

# constants
const max_time := 10.0
const min_time := 3.0
const max_lives := 3

# onreadies
@onready var current_scene = $CurrentScene
@onready var in_game_ui = $InGameUi
@onready var game_timer = $GameTimer

# dictionaries
var levels := ["res://scenes/eggs/eggs.tscn", "res://scenes/minigame_2/minigame_2.tscn", "res://scenes/Minijuego3/Minijuego3.tscn", "res://scenes/minigame_4/minigame_4.tscn", "res://scenes/minigame_6/minigame_6.tscn", "res://scenes/minigame_5/minigame_5.tscn"]
var user_interfaces := {"main_menu" : "res://scenes/ui/main_menu.tscn"}

# arrays
var current_signals = []
var unplayed_levels : Array

# variables
var current_lives : int
var current_time : float
var current_score : int

# built_in
func _ready() -> void:
	# loading main menu
	load_main_menu()
	# connecting signals
	game_timer.must_update_label.connect(in_game_ui.set_time_label)
	game_timer.minigame_timed_out.connect(completed)

# funcs
func clear_connections() -> void:
	for signal_variant : Signal in current_signals:
		var signal_connections = signal_variant.get_connections()
		for connection in signal_connections:
			signal_variant.disconnect(connection.callable)
	current_signals.clear()

func switch_current_scene(path : String):
	var new_scene : PackedScene = load(path)
	clear_connections()
	if current_scene:
		current_scene.queue_free()
	current_scene = new_scene.instantiate()
	get_tree().current_scene.add_child(current_scene)
	get_tree().current_scene.move_child(current_scene, 0)
	return current_scene

func load_main_menu() -> void:
	var menu_scene = switch_current_scene(user_interfaces["main_menu"])
	current_signals.insert(0, menu_scene.start_game)
	current_signals.insert(1, menu_scene.quit)
	current_signals[0].connect(start_game)
	current_signals[1].connect(quit)
	in_game_ui.visible = false
	game_timer.stop()

func select_minigame() -> void:
	if unplayed_levels.is_empty():
		unplayed_levels = levels.duplicate()
		
	var level_index = randi_range(0, unplayed_levels.size() - 1)
	var minigame_scene : Minigame = switch_current_scene(unplayed_levels[level_index])
	unplayed_levels.remove_at(level_index)
	
	current_signals.insert(0, minigame_scene.completed)
	current_signals.insert(1, minigame_scene.lost)
	current_signals[0].connect(completed)
	current_signals[1].connect(lost)
	
	if minigame_scene.has_signal("point_scored"):
		var point_sig = minigame_scene.point_scored
		current_signals.append(point_sig)
		point_sig.connect(_on_minigame_point_scored)
		
	if minigame_scene.has_signal("life_lost"):
		var life_sig = minigame_scene.life_lost
		current_signals.append(life_sig)
		life_sig.connect(_on_life_lost)
		
	game_timer.set_timer(current_time)

func show_final_score() -> void:
	game_timer.stop()
	in_game_ui.visible = false
	if current_scene:
		current_scene.queue_free()
		current_scene = null
		
	var canvas = CanvasLayer.new()
	add_child(canvas)
	current_scene = canvas
	
	var label = Label.new()
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

func _on_life_lost():
	current_lives -= 1
	in_game_ui.set_lives_label(current_lives)
	if current_lives <= 0:
		lost()

func completed() -> void:
	game_timer.stop()
	if current_time > min_time:
		current_time -= .5
	else:
		current_time = min_time
	await get_tree().create_timer(1).timeout
	select_minigame()

func lost() -> void:
	game_timer.stop()
	await get_tree().create_timer(1).timeout
	current_lives -= 1
	in_game_ui.set_lives_label(current_lives)
	if current_lives > 0:
		select_minigame()
	else:
		show_final_score()

func start_game() -> void:
	current_lives = 3
	current_time = max_time
	current_score = 0
	unplayed_levels = levels.duplicate()
	in_game_ui.visible = true
	in_game_ui.set_lives_label(current_lives)
	select_minigame()

func quit() -> void:
	get_tree().quit()
