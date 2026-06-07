extends Minigame

@onready var cursor = $UI/BarBG/Cursor
@onready var bar_bg = $UI/BarBG
@onready var golf_club = $Planet/GolfClub
@onready var planet = $Planet
@onready var black_hole = $BlackHole

var cursor_speed = 1000.0
var cursor_direction = 1
var is_moving = true
var game_over = false

func _ready():
	cursor.position.y = bar_bg.size.y
	
	var gm = get_parent()
	var time_limit = 10.0
	if gm and "current_time" in gm:
		time_limit = gm.current_time
		
	var timer = get_tree().create_timer(time_limit - 0.1)
	timer.timeout.connect(_on_timeout)

func _on_timeout():
	if not game_over:
		game_over = true
		is_moving = false
		cursor.color = Color(1, 0, 0)
		# Fallo genérico por timeout
		var tween = create_tween()
		tween.tween_property(golf_club, "rotation_degrees", 20.0, 0.1)
		tween.tween_property(golf_club, "rotation_degrees", 0.0, 0.2)
		await tween.finished
		emit_signal("lost")

func _process(delta):
	if not is_moving or game_over:
		return
		
	cursor.position.y += cursor_speed * cursor_direction * delta
	
	if cursor.position.y > bar_bg.size.y:
		cursor.position.y = bar_bg.size.y
		cursor_direction = -1
	elif cursor.position.y < 0:
		cursor.position.y = 0
		cursor_direction = 1

func _input(event):
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed):
		if is_moving and not game_over:
			_attempt_shot()

func _attempt_shot():
	is_moving = false
	game_over = true
	
	var cursor_center = cursor.position.y + cursor.size.y / 2.0
	var power = 1.0 - (cursor_center / bar_bg.size.y) # 0.0 to 1.0
	
	# Win condition: power between 0.45 and 0.55 (perfect is 0.5)
	var is_win = abs(power - 0.5) <= 0.075
	
	# Calculate distance: Max power (1.0) goes 1000 pixels. Power 0.5 goes 500 pixels.
	var distance = power * 1000.0
	var target_y = planet.global_position.y - distance
	
	# Animate Swing
	var tween = create_tween()
	# The club swings back more depending on power
	var back_rotation = lerp(20.0, 90.0, power)
	tween.tween_property(golf_club, "rotation_degrees", back_rotation, 0.15)
	
	# The club swings forward
	var follow_through = lerp(-10.0, -60.0, power)
	tween.tween_property(golf_club, "rotation_degrees", follow_through, 0.1)
	
	# Planet flies
	var flight_time = lerp(0.3, 0.6, power)
	tween.parallel().tween_property(planet, "global_position", Vector2(planet.global_position.x, target_y), flight_time).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD).set_delay(0.25)
	
	if is_win:
		tween.parallel().tween_property(planet, "scale", Vector2(0.05, 0.05), flight_time).set_delay(0.25)
		await tween.finished
		emit_signal("point_scored")
		emit_signal("completed")
	else:
		await tween.finished
		emit_signal("lost")
