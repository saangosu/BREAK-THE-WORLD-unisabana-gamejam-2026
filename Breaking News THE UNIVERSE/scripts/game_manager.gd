extends Node
class_name GameManager

# constants
const max_time := 10.0
const min_time := 1.0
const max_lives := 3

# onreadies
@onready var current_scene = $CurrentScene
@onready var in_game_ui = $InGameUi
@onready var game_timer = $GameTimer

# dictionaries
var levels := ["res://scenes/eggs/eggs.tscn", "res://scenes/Minijuego3.tscn"]
var user_interfaces := {"main_menu" : "res://scenes/ui/main_menu.tscn"}

# arrays
var current_signals = []

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
	game_timer.minigame_timed_out.connect(lost)

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
	current_scene.queue_free()
	current_scene = new_scene.instantiate()
	get_tree().current_scene.add_child(current_scene)
	return current_scene

func load_main_menu() -> void:
	var menu_scene = switch_current_scene(user_interfaces["main_menu"])
	current_signals.insert(0, menu_scene.start_game)
	current_signals.insert(1, menu_scene.quit)
	current_signals[0].connect(start_game)
	current_signals[1].connect(quit)
	in_game_ui.visible = false

func select_minigame() -> void:
	var level_index = randi_range(0, levels.size() - 1)
	var minigame_scene : Minigame = switch_current_scene(levels[level_index])
	current_signals.insert(0, minigame_scene.completed)
	current_signals.insert(1, minigame_scene.lost)
	current_signals[0].connect(completed)
	current_signals[1].connect(lost)
	game_timer.set_timer(current_time)

func completed() -> void:
	game_timer.stop()
	current_score += 1
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
		load_main_menu()

func start_game() -> void:
	current_lives = 3
	current_time = max_time
	current_score = 0
	in_game_ui.visible = true
	in_game_ui.set_lives_label(current_lives)
	select_minigame()

func quit() -> void:
	get_tree().quit()
