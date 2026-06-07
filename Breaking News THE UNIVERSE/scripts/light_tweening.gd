extends PointLight2D
class_name FeedbackLight

var current_tween
var must_tween = false

func start_tweening(start_e = .5, end_e = 5, time = .5) -> void:
	if energy != start_e:
		energy = start_e
	must_tween = true
	while must_tween:
		current_tween = get_tree().create_tween()
		current_tween.tween_property(self, "energy", end_e, time)
		current_tween.tween_property(self, "energy", start_e, time)
		await  current_tween.finished

func kill_tween() -> void:
	must_tween = false
	energy = 0
	if current_tween != null:
		current_tween.kill()
		current_tween = null
