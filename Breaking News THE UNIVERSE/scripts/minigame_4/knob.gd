extends Control

signal value_changed(value)

var is_dragging = false
var min_angle = -135.0
var max_angle = 135.0

# Value between 0.0 and 1.0
var current_value = 0.5
var knob_sprite : Polygon2D

func _ready():
	# Create a visual representation of the knob
	knob_sprite = Polygon2D.new()
	var points = PackedVector2Array()
	for i in range(32):
		var a = i * TAU / 32
		points.append(Vector2(cos(a), sin(a)) * 100)
	knob_sprite.polygon = points
	knob_sprite.color = Color(0.3, 0.3, 0.3)
	knob_sprite.position = Vector2(100, 100) # Offset to center of 200x200 control
	
	# Indicator line
	var line = Line2D.new()
	line.add_point(Vector2(0, -20))
	line.add_point(Vector2(0, -90))
	line.width = 10.0
	line.default_color = Color(1, 0, 0)
	knob_sprite.add_child(line)
	
	add_child(knob_sprite)
	
	# Initial rotation
	set_value(current_value)

func _gui_input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				is_dragging = true
			else:
				is_dragging = false
	elif event is InputEventMouseMotion and is_dragging:
		var mouse_pos = get_local_mouse_position() - Vector2(100, 100) # Relative to center
		var angle = rad_to_deg(Vector2(0, -1).angle_to(mouse_pos))
		
		# Clamp angle
		if angle < min_angle: angle = min_angle
		if angle > max_angle: angle = max_angle
		
		# Convert angle to 0.0 - 1.0
		var val = (angle - min_angle) / (max_angle - min_angle)
		set_value(val)
		emit_signal("value_changed", current_value)

func set_value(val: float):
	current_value = clamp(val, 0.0, 1.0)
	var angle = lerp(min_angle, max_angle, current_value)
	knob_sprite.rotation = deg_to_rad(angle)
