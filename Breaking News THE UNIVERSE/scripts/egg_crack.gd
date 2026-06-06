extends RigidBody2D
class_name EggPlanet

# signals
signal cracked
signal selected

# onreadies
@onready var hurtbox : Area2D = $Hurtbox
@onready var visible_notifier := $VisibleOnScreenNotifier2D

# vars
var is_selected : bool = false
var can_select : bool = true
var impulsed : int = 10
var impacts : int = 0

# built in
func _ready() -> void:
	hurtbox.input_event.connect(clicked)
	hurtbox.area_entered.connect(collided)

func _physics_process(_delta: float) -> void:
	if is_selected:
		var direction = -(global_position - get_global_mouse_position())
		linear_velocity = direction.normalized() * direction.length() * 8
	elif is_selected != true && impulsed > 0 && impacts > 2:
		apply_impulse(Vector2(0, impulsed * -15))
		impulsed -= 1
		gravity_scale = (-impulsed + 10.0)/10.0 * 2.0

# functions
func clicked(_viewport : Viewport, event : InputEvent, _shape_idx) -> void:
	# checking event type
	if event.is_action_pressed("click") && impacts < 3 && can_select:
		is_selected = true

func check_impacts() -> void:
	if impacts >= 3:
		crack()

func collided(area : Area2D) -> void:
	impacts += 1
	check_impacts()

func crack() -> void:
	$Complete.visible = false
	$Cracked.visible = true
	is_selected = false
	selected.emit(false)
	cracked.emit()
	set_collision_layer_value(0, false)
	set_collision_mask_value(1, false)

func freeze() -> void:
	gravity_scale = 0
