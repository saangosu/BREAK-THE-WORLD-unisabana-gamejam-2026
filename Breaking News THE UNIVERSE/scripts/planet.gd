extends StaticBody2D

signal planet_destroyed(pos, color)

var max_hp = 1
var current_hp = 1
var move_speed = 200.0
var direction = 1
var planet_color = Color.WHITE

func _ready():
	add_to_group("planet")
	planet_color = Color.from_hsv(randf(), randf_range(0.5, 1.0), randf_range(0.8, 1.0))
	$Sprite2D.modulate = planet_color
	direction = 1 if randf() > 0.5 else -1
	move_speed = randf_range(400.0, 750.0)

func _physics_process(delta):
	global_position.x += move_speed * direction * delta
	if global_position.x < 100:
		direction = 1
	elif global_position.x > 1820:
		direction = -1

func take_damage():
	current_hp -= 1
	if current_hp <= 0:
		emit_signal("planet_destroyed", global_position, planet_color)
		queue_free()

func update_visuals():
	pass
