extends RigidBody2D
class_name Asteroid

signal asteroid_launched
signal asteroid_destroyed
signal hit_planet

var dragging = false
var start_pos = Vector2()
var max_drag_distance = 200.0
var launch_multiplier = 15.0
var launched = false

const sfx_whoosh = preload("res://sounds/minigame_2/Asteroide/whoosh.mp3")
const sfx_impact = preload("res://sounds/minigame_2/Asteroide/impacto_de_roca.mp3")
const sfx_drag = preload("res://sounds/minigame_2/Asteroide/jalar.mp3")

var drag_player: AudioStreamPlayer = null

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
			
			# Play drag sound
			if is_instance_valid(drag_player):
				drag_player.stop()
				drag_player.queue_free()
			drag_player = AudioStreamPlayer.new()
			drag_player.stream = sfx_drag
			drag_player.volume_db = -6.0
			get_tree().current_scene.add_child(drag_player)
			drag_player.play()
			drag_player.finished.connect(drag_player.queue_free)

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

func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func launch_asteroid():
	launched = true
	var drag_vec = global_position - start_pos
	var impulse = -drag_vec * launch_multiplier
	apply_central_impulse(impulse)
	
	# Stop drag sound if it's still playing
	if is_instance_valid(drag_player):
		drag_player.stop()
		drag_player.queue_free()
		
	play_sound(sfx_whoosh, 4.0)
	emit_signal("asteroid_launched")

func _on_body_entered(body):
	if body.has_method("take_damage"):
		body.take_damage()
		play_sound(sfx_impact, -16.0)
		emit_signal("hit_planet")
	emit_signal("asteroid_destroyed")
	queue_free()

func get_sucked():
	emit_signal("asteroid_destroyed")
	queue_free()
