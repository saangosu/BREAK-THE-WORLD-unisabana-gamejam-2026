extends Node2D
class_name FeedbackArrow

var tweening : bool
var current_tween : Tween
var movement_range = 50

func _ready() -> void:
	self.visibility_changed.connect(set_tween)
	set_tween()

func set_tween() -> void:
	if visible:
		if tweening != true: start_tweening()
	else:
		kill_tween()

func start_tweening(offset = 0.0, delay = 0.0) -> void:
	tweening = true
	$Sprite2D.position = Vector2(0, offset)
	await get_tree().create_timer(delay).timeout
	while tweening:
		current_tween = get_tree().create_tween()
		current_tween.tween_property($Sprite2D, "position", Vector2(0, movement_range), .5)\
		.set_ease(Tween.EASE_IN_OUT)\
		.set_trans(Tween.TRANS_SINE)
		current_tween.tween_property($Sprite2D, "position", Vector2(0, -movement_range), .5)\
		.set_ease(Tween.EASE_IN_OUT)\
		.set_trans(Tween.TRANS_SINE)
		await  current_tween.finished

func kill_tween() -> void:
	$Sprite2D.position = Vector2.ZERO
	tweening = false
	if current_tween != null:
		current_tween.kill()
		current_tween = null
