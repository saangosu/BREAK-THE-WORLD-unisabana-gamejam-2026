extends StaticBody2D

signal planet_destroyed(pos)

var max_hp = 1
var current_hp = 1
var move_speed = 200.0
var direction = 1

func _ready():
	add_to_group("planet")
	update_visuals()
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
	update_visuals()
	if current_hp <= 0:
		emit_signal("planet_destroyed", global_position)
		queue_free()

func update_visuals():
	var sprite = $Polygon2D
	if sprite:
		if current_hp > 3:
			sprite.color = Color(0.2, 0.8, 0.2) # Verde
		elif current_hp > 1:
			sprite.color = Color(0.8, 0.8, 0.2) # Amarillo
		else:
			sprite.color = Color(0.8, 0.2, 0.2) # Rojo
