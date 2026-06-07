extends RigidBody2D
class_name EggPlanet

# signals
signal cracked
signal selected

# exported
@export var shred_base : PackedScene

# onreadies
@onready var hurtbox : Area2D = $Hurtbox

# vars
var is_selected : bool = false
var can_select : bool = true
var impacts : int = 0
var last_position : Vector2
var last_speed : Vector2
var last_speed_count = 0

# constants
const egg_crack_one := "res://textures/art/egg_crack_1.png"
const egg_crack_two := "res://textures/art/egg_crack_2.png"
const shreds_crack_two := ["res://textures/art/egg_crack_2_shatter_1.png", "res://textures/art/egg_crack_2_shatter_2.png", "res://textures/art/egg_crack_2_shatter_3.png", "res://textures/art/egg_crack_2_shatter_4.png", "res://textures/art/egg_crack_2_shatter_5.png", "res://textures/art/egg_crack_2_shatter_6.png", "res://textures/art/egg_crack_2_shatter_7.png"]
const shreds_crack_three := ["res://textures/art/egg_crack_3_shatter_1.png", "res://textures/art/egg_crack_3_shatter_2.png", "res://textures/art/egg_crack_3_shatter_3.png"]

const sfx_crack = preload("res://sounds/minigame_1/huevo_planeta/huevo_agrietandose.mp3")
const sfx_break = preload("res://sounds/minigame_1/huevo_planeta/huevo_roto.wav")

# built in
func _ready() -> void:
	hurtbox.input_event.connect(clicked)
	hurtbox.area_entered.connect(collided)

func _physics_process(_delta: float) -> void:
	if is_selected:
		var direction = -(global_position - get_global_mouse_position())
		linear_velocity = direction.normalized() * direction.length() * 8
		last_speed_count += 1
		if last_position == null:
			last_position = global_position
		if last_speed_count == 3:
			last_speed = (global_position - last_position) / _delta * 3
			last_speed_count = 0
			last_position = global_position

# functions
func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func clicked(_viewport : Viewport, event : InputEvent, _shape_idx) -> void:
	# checking event type
	if event.is_action_pressed("click") && impacts < 3 && can_select:
		is_selected = true
		selected.emit(true, name)

func check_impacts() -> void:
	match impacts:
		3:
			play_sound(sfx_break, -2.0)
			for texture in shreds_crack_two:
				create_shreds(texture)
			for texture in shreds_crack_three:
				create_shreds(texture)
			crack()
		2:
			play_sound(sfx_crack, -2.0)
			for texture in shreds_crack_two:
				create_shreds(texture)
			$Sprite.texture = load(egg_crack_two)
		1:
			play_sound(sfx_crack, -2.0)
			$Sprite.texture = load(egg_crack_one)

func collided(_area : Area2D) -> void:
	if last_speed.length() > 15000: # gotta hit hard >:C
		impacts += 1
		check_impacts()

func crack() -> void:
	$Sprite.visible = false
	is_selected = false
	selected.emit(false, name)
	cracked.emit()
	freeze()

func create_shreds(texture : String) -> void:
	var shred = shred_base.instantiate()
	var sprite : Sprite2D = shred.find_child("Sprite")
	sprite.texture = load(texture)
	sprite.scale = $Sprite.scale / 2
	sprite.modulate = $Sprite.modulate
	shred.global_position = global_position
	get_tree().current_scene.call_deferred("add_child", shred)

func switch_can_select(can : bool, egg_name : String) -> void:
	if name != egg_name && impacts < 3:
		can_select = can

func freeze() -> void:
	set_collision_layer_value(2, false)
	set_collision_mask_value(1, false)
	gravity_scale = 0
