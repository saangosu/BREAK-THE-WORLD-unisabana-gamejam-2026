extends Area2D

var pull_force = 1500.0

func _ready():
	gravity_space_override = Area2D.SPACE_OVERRIDE_DISABLED

func _physics_process(delta):
	var bodies = get_overlapping_bodies()
	for body in bodies:
		if body.is_in_group("asteroid") and body is RigidBody2D:
			if "launched" in body and not body.launched:
				continue
			var direction = global_position - body.global_position
			var distance = direction.length()
			if distance < 50.0:
				if body.has_method("get_sucked"):
					body.get_sucked()
			elif distance > 10.0:
				direction = direction.normalized()
				var force = direction * pull_force
				body.apply_central_force(force)
