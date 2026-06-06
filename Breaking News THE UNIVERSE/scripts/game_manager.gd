extends Node
class_name GameManager

# constants
const max_time := 10.0
const min_time := 1.0
const max_lives := 3

# onreadies
@onready var current_scene = $CurrentScene

# dictionaries
var levels := ["res://scenes/eggs/eggs.tscn"]
var user_interfaces := {"main_menu" : "res://scenes/main_menu.tscn"}

# arrays
var current_signals = []

# variables
var current_lives : int
var current_time : float
var current_score : int

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
	current_scene.queue_free()
	current_scene = new_scene.instantiate()
	current_signals.insert(0, current_scene.start_game)
	current_signals.insert(1, current_scene.quit)
	current_signals[0].connect(start_game)
	current_signals[1].connect(quit)
	get_tree().current_scene.add_child(current_scene)

func select_minigame() -> void:
	var game_index = randi_range(0, levels.size() - 1)
	

func start_game() -> void:
	current_lives = 3
	current_time = max_time
	current_score = 0
	select_minigame()

func quit() -> void:
	get_tree().quit()
