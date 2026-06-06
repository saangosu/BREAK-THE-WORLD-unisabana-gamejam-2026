extends RigidBody2D
class_name EggShred

var random_y : float
var random_x : float
var count = 5

func _ready() -> void:
	random_y = randf_range(-20, 0) * 30
	random_x = randf_range(-10, 10)
	rotation = randi_range(-360, 360)
	angular_velocity = randf_range(-5, 5)

func _process(_delta: float) -> void:
	if count > 0:
		apply_impulse(Vector2(random_x, random_y))
		count -= 1

func _on_visible_on_screen_notifier_2d_screen_exited() -> void:
	queue_free()
