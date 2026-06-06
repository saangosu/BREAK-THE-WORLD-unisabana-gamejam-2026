extends Node2D
class_name EggsLevel

# signals
signal completed

# OnReadies
@onready var egg_1 = $Egg1
@onready var egg_2 = $Egg2
@onready var egg_3 = $Egg3

# constants
const winning_goal = 3

# variables
var level_score = 0

# built in
func _ready() -> void:
	egg_1.cracked.connect(increase_score)
	egg_2.cracked.connect(increase_score)
	egg_3.cracked.connect(increase_score)

# functions
func increase_score() -> void:
	level_score += 1
	if level_score == winning_goal:
		completed.emit()
