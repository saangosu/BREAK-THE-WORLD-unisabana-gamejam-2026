extends RigidBody2D

signal asteroid_launched
signal asteroid_destroyed
signal hit_planet

var dragging = false
var start_pos = Vector2()
var max_drag_distance = 200.0
var launch_multiplier = 10.0
var launched = false

func _ready():
	input_pickable = true
	gravity_scale = 0
	linear_velocity = Vector2.ZERO
	contact_monitor = true
	max_contacts_reported = 2
	body_entered.connect(_on_body_entered)
	add_to_group("asteroid")

func _input_event(viewport, event, shape_idx):
	if launched: return
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			dragging = true
			start_pos = global_position

func _process(delta):
	if dragging and not launched:
		if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
			var drag_vec = get_global_mouse_position() - start_pos
			if drag_vec.length() > max_drag_distance:
				drag_vec = drag_vec.normalized() * max_drag_distance
			global_position = start_pos + drag_vec
		else:
			dragging = false
			launch_asteroid()

func launch_asteroid():
	launched = true
	var drag_vec = global_position - start_pos
	var impulse = -drag_vec * launch_multiplier
	apply_central_impulse(impulse)
	emit_signal("asteroid_launched")

func _on_body_entered(body):
	if body.has_method("take_damage"):
		body.take_damage()
		emit_signal("hit_planet")
	emit_signal("asteroid_destroyed")
	queue_free()

func get_sucked():
	emit_signal("asteroid_destroyed")
	queue_free()
