extends Minigame
class_name EggsLevel

# OnReadies
@onready var egg_1 = $Egg1
@onready var egg_2 = $Egg2
@onready var egg_3 = $Egg3

# constants
const winning_goal = 3

# variables
var level_score = 0
var eggs : Array = []

var game_over = false

var status_label: Label

# built in
func _ready() -> void:
	setup_ui()
	eggs.insert(0, egg_1)
	eggs.insert(1, egg_2)
	eggs.insert(2, egg_3)
	for egg in eggs.size():
		eggs[egg].cracked.connect(increase_score)
		eggs[egg].selected.connect(egg_selected)

func setup_ui():
	var canvas = CanvasLayer.new()
	add_child(canvas)
	
	status_label = Label.new()
	status_label.position = Vector2(0, 500)
	status_label.size = Vector2(1920, 200)
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status_label.add_theme_font_size_override("font_size", 100)
	status_label.text = ""
	canvas.add_child(status_label)

# functions
func egg_selected(selected : bool, selected_egg : String) -> void:
	for egg in eggs.size():
		if is_instance_valid(eggs[egg]):
			eggs[egg].switch_can_select(!selected, selected_egg)

func increase_score() -> void:
	emit_signal("point_scored")
	level_score += 1
	print('new score: ', level_score)
	if level_score == winning_goal:
		win_game("¡NIVEL COMPLETADO!")

func win_game(reason: String):
	if game_over: return
	game_over = true
	status_label.text = reason
	status_label.modulate = Color(0, 1, 0) # Verde
	
	await get_tree().create_timer(2.0).timeout
	emit_signal("completed")
