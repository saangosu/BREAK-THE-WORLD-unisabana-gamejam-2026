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

# built in
func _ready() -> void:
	eggs.insert(0, egg_1)
	eggs.insert(1, egg_2)
	eggs.insert(2, egg_3)
	for egg in eggs.size():
		eggs[egg].cracked.connect(increase_score)
		eggs[egg].selected.connect(egg_selected)

# functions
func egg_selected(selected : bool, selected_egg : String) -> void:
	for egg in eggs.size():
		eggs[egg].switch_can_select(!selected, selected_egg)

func increase_score() -> void:
	level_score += 1
	print('new score: ', level_score)
	if level_score == winning_goal:
		completed.emit()
