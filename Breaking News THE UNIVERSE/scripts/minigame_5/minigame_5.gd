extends Minigame

@onready var moon = $Moon
@onready var progress_bar = $ProgressBar
@onready var particles = $CheeseParticles
@onready var feedback_arrow_down = $FeedbackArrowDown
@onready var feedback_arrow_up = $FeedbackArrowUp

const sfx_grater = preload("res://sounds/minigame_5/Rallador/rallador.mp3")
const sfx_win = preload("res://sounds/minigame_5/Foleys/gano.mp3")
const sfx_lose = preload("res://sounds/minigame_5/Foleys/perdiste.mp3")

var is_grating = false
var progress = 0.0
var required_distance = 10000.0 # lowered distance slightly for testing

var is_game_over = false

var grater_left_bound = 800.0
var grater_right_bound = 1120.0

var initial_scale = 0.25

var BGM_player : AudioStreamPlayer
var grater_player : AudioStreamPlayer
var last_motion_time = 0.0

func set_arrows() -> void:
	feedback_arrow_down.start_tweening()
	feedback_arrow_up.start_tweening(-feedback_arrow_down.movement_range, .5)
	feedback_arrow_down.visible = true
	feedback_arrow_up.visible = true

func _ready():
	progress_bar.max_value = 100
	progress_bar.value = 0
	moon.scale = Vector2(initial_scale, initial_scale)
	moon.position = Vector2(960, 540)
	
	call_deferred("set_arrows")
	
	# Play looping background music
	var bgm = load("res://sounds/minigame_5/musica_de_fondo/pol-star-way-short.wav")
	if bgm:
		if bgm is AudioStreamWAV:
			bgm.loop_mode = AudioStreamWAV.LOOP_FORWARD
		BGM_player = AudioStreamPlayer.new()
		BGM_player.stream = bgm
		BGM_player.volume_db = -18.0 # Adjusted BGM volume
		add_child(BGM_player)
		BGM_player.play()
		
	# Instantiate grater sound player
	grater_player = AudioStreamPlayer.new()
	grater_player.stream = sfx_grater
	if grater_player.stream is AudioStreamMP3:
		grater_player.stream.loop = true
	grater_player.volume_db = -1.0 # Raised volume for clarity
	grater_player.pitch_scale = 0.75 # Lowered pitch/speed to match dragging motion
	add_child(grater_player)
	
	var gm = get_parent()
	var time_limit = 10.0
	if gm and "current_time" in gm:
		time_limit = gm.current_time
		
	var timer = get_tree().create_timer(time_limit - 0.1)
	timer.timeout.connect(_on_timeout)

func _on_timeout():
	if not is_game_over:
		is_game_over = true
		if BGM_player:
			BGM_player.stop()
		if grater_player:
			grater_player.stop()
		play_sound(sfx_lose, -2.0)
		emit_signal("lost")

func _process(delta):
	if is_game_over:
		if grater_player and grater_player.playing:
			grater_player.stop()
		return
	
	# Stop grater sound if there's no mouse motion for 0.15 seconds
	if grater_player and grater_player.playing:
		last_motion_time += delta
		if last_motion_time > 0.15 or not is_grating:
			grater_player.stop()
			particles.emitting = false

func _input(event):
	if is_game_over: return
	
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			is_grating = true
		else:
			is_grating = false
			particles.emitting = false
			if grater_player and grater_player.playing:
				grater_player.stop()
			
	if is_grating and event is InputEventMouseMotion:
		moon.position += event.relative
		moon.position.y = clamp(moon.position.y, 140, 940)
		
		# Check walls
		if moon.position.x < grater_left_bound or moon.position.x > grater_right_bound:
			_hit_wall()
			return
			
		particles.position = moon.position + Vector2(0, 50)
		
		if abs(event.relative.y) > 0:
			particles.emitting = true
			last_motion_time = 0.0 # Reset motion timer
			if grater_player and not grater_player.playing:
				grater_player.play()
			progress += abs(event.relative.y)
			var pct = min((progress / required_distance) * 100.0, 100.0)
			progress_bar.value = pct
			
			# Make moon thinner
			moon.scale.x = lerp(initial_scale, 0.02, progress / required_distance)
			
			if pct >= 100.0:
				_win()
		else:
			particles.emitting = false

func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func _hit_wall():
	is_grating = false
	particles.emitting = false
	if grater_player and grater_player.playing:
		grater_player.stop()
	moon.position.x = 960
	
	var gm = get_parent()
	if gm and "current_lives" in gm and gm.current_lives <= 1:
		if BGM_player:
			BGM_player.stop()
		play_sound(sfx_lose, -2.0)
	emit_signal("life_lost")

func _win():
	is_game_over = true
	stop_timer.emit()
	particles.emitting = false
	if grater_player and grater_player.playing:
		grater_player.stop()
	if BGM_player:
		BGM_player.stop()
	play_sound(sfx_win, -2.0)
	
	var tween = create_tween()
	tween.tween_property(moon, "scale", Vector2(0, 0), 0.2)
	await tween.finished
	emit_signal("point_scored")
	emit_signal("completed")
