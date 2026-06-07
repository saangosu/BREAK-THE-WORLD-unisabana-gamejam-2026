extends Minigame

@onready var cursor_power = $UI/BarBG/Cursor
@onready var bar_power = $UI/BarBG

@onready var cursor_dir = $UI/DirBarBG/DirCursor
@onready var bar_dir = $UI/DirBarBG

@onready var golf_club = $GolfClub
@onready var planet = $Planet
@onready var black_hole = $BlackHole

const sfx_whoosh = preload("res://sounds/minigame_6/palo_de_golf/whoosh_palo.mp3")
const sfx_impact = preload("res://sounds/minigame_6/Planeta/palo_pegando_pelota.mp3")
const sfx_black_hole = preload("res://sounds/minigame_6/agujero_negro/agujero_negro.mp3")
const sfx_win = preload("res://sounds/minigame_6/Foleys/gano.mp3")
const sfx_lose = preload("res://sounds/minigame_6/Foleys/perdiste.mp3")

var cursor_speed_power = 1800.0
var cursor_speed_dir = 1800.0

var power_dir_y = 1
var dir_dir_x = 1

enum State { POWER, DIRECTION, SHOOTING, DONE }
var current_state = State.POWER

var stored_power = 0.5
var stored_direction = 0.5

var black_hole_player : AudioStreamPlayer = null

func _ready():
	cursor_power.position.y = bar_power.size.y
	cursor_dir.position.x = 0
	bar_dir.visible = false
	
	var gm = get_parent()
	var time_limit = 10.0
	if gm and "current_time" in gm:
		time_limit = gm.current_time
		
	var timer = get_tree().create_timer(time_limit - 0.1)
	timer.timeout.connect(_on_timeout)

func _on_timeout():
	if current_state != State.SHOOTING and current_state != State.DONE:
		current_state = State.DONE
		cursor_power.color = Color(1, 0, 0)
		if bar_dir.visible:
			cursor_dir.color = Color(1, 0, 0)
		var tween = create_tween()
		tween.tween_property(golf_club, "rotation_degrees", 90.0, 0.1)
		tween.tween_property(golf_club, "rotation_degrees", -45.0, 0.05)
		await tween.finished
		play_sound(sfx_lose, -2.0)
		emit_signal("lost")

func _process(delta):
	if current_state == State.POWER:
		cursor_power.position.y += cursor_speed_power * power_dir_y * delta
		if cursor_power.position.y > bar_power.size.y:
			cursor_power.position.y = bar_power.size.y
			power_dir_y = -1
		elif cursor_power.position.y < 0:
			cursor_power.position.y = 0
			power_dir_y = 1
			
	elif current_state == State.DIRECTION:
		cursor_dir.position.x += cursor_speed_dir * dir_dir_x * delta
		if cursor_dir.position.x > bar_dir.size.x:
			cursor_dir.position.x = bar_dir.size.x
			dir_dir_x = -1
		elif cursor_dir.position.x < 0:
			cursor_dir.position.x = 0
			dir_dir_x = 1

func _input(event):
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed):
		if current_state == State.POWER:
			_lock_power()
		elif current_state == State.DIRECTION:
			_lock_direction()

func _lock_power():
	current_state = State.DIRECTION
	var cursor_center = cursor_power.position.y + cursor_power.size.y / 2.0
	stored_power = 1.0 - (cursor_center / bar_power.size.y) # 0.0 a 1.0
	bar_dir.visible = true

func _lock_direction():
	current_state = State.SHOOTING
	var cursor_center = cursor_dir.position.x + cursor_dir.size.x / 2.0
	stored_direction = cursor_center / bar_dir.size.x # 0.0 a 1.0 (0.5 es el centro)
	_attempt_shot()

func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func _attempt_shot():
	current_state = State.DONE
	
	var power_perfect = abs(stored_power - 0.5) <= 0.20
	var dir_perfect = abs(stored_direction - 0.5) <= 0.20
	var is_win = power_perfect and dir_perfect
	
	# Calculate target
	var distance_y = stored_power * 1000.0
	var target_y = planet.global_position.y - distance_y
	
	var offset_x = (stored_direction - 0.5) * 1200.0
	var target_x = planet.global_position.x + offset_x
	
	if is_win:
		target_x = black_hole.global_position.x
		target_y = black_hole.global_position.y
	
	var tween = create_tween()
	var back_rotation = lerp(10.0, 90.0, stored_power)
	tween.tween_property(golf_club, "rotation_degrees", back_rotation, 0.15)
	
	# Play whoosh sound when forward swing starts
	tween.tween_callback(func(): play_sound(sfx_whoosh, -4.0))
	
	var follow_through = -45.0
	tween.tween_property(golf_club, "rotation_degrees", follow_through, 0.1)
	
	# Play contact sound when hit occurs
	tween.tween_callback(func(): play_sound(sfx_impact, -4.0))
	
	var flight_time = lerp(0.3, 0.6, stored_power)
	tween.parallel().tween_property(planet, "global_position", Vector2(target_x, target_y), flight_time).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD).set_delay(0.25)
	
	if is_win:
		tween.parallel().tween_property(planet, "scale", Vector2(0.05, 0.05), flight_time).set_delay(0.25)
		await tween.finished
		
		# Play black hole sink sound (starts at 2.0s to jump directly to the wind section)
		black_hole_player = AudioStreamPlayer.new()
		black_hole_player.stream = sfx_black_hole
		black_hole_player.volume_db = -4.0
		add_child(black_hole_player)
		black_hole_player.play(2.0)
		
		planet.texture = load("res://assets/sprites/minigame_2/Planeta 2 destruido.png")
		planet.scale = Vector2(0.12, 0.12) # Hacemos un pop para que se vea la destrucción
		var final_tween = create_tween()
		final_tween.tween_property(planet, "modulate", Color(1, 1, 1, 0), 0.8)
		await final_tween.finished
		
		# Wait an additional 0.4s to let the sound play a bit longer before level transition
		await get_tree().create_timer(0.4).timeout
		
		# Stop black hole sound when level ends
		if is_instance_valid(black_hole_player):
			black_hole_player.stop()
			black_hole_player.queue_free()
		
		# Play win foley sound
		play_sound(sfx_win, -2.0)
		
		emit_signal("point_scored")
		emit_signal("completed")
	else:
		if not power_perfect:
			cursor_power.color = Color(1,0,0)
		if not dir_perfect:
			cursor_dir.color = Color(1,0,0)
		await tween.finished
		
		# Play lose foley sound
		play_sound(sfx_lose, -2.0)
		
		emit_signal("lost")

func _exit_tree() -> void:
	if is_instance_valid(black_hole_player):
		black_hole_player.stop()
