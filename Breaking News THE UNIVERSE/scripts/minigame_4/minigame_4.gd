extends Minigame

@onready var target_wave = $TargetWave
@onready var player_wave = $PlayerWave
@onready var planet = $Planet
@onready var ok_button = $OKButton

const sfx_frequency = preload("res://sounds/minigame_4/Frecuencia/frecuencia.mp3")
const sfx_impact = preload("res://sounds/minigame_4/impacto_de_roca/impacto_de_roca.mp3")
const sfx_win = preload("res://sounds/minigame_4/Foleys/gano.mp3")
const sfx_lose = preload("res://sounds/minigame_4/Foleys/perdiste.mp3")
const sfx_click = preload("res://sounds/minigame_4/click/click.mp3")

var target_frequency : float
var player_frequency : float
var target_amplitude : float
var player_amplitude : float

var match_tolerance_freq = 0.04
var match_tolerance_amp = 8.0
var game_over = false

var frequency_player : AudioStreamPlayer

func _ready():
	target_frequency = randf_range(0.2, 0.8)
	target_amplitude = randf_range(50.0, 110.0)
	
	player_frequency = 0.5
	player_amplitude = 125.0
	
	update_wave(target_wave, target_frequency, target_amplitude, Color(1, 0, 0, 0.5))
	update_wave(player_wave, player_frequency, player_amplitude, Color(0, 1, 0, 0.8))
	
	var knob_freq = $KnobFreq
	knob_freq.value_changed.connect(_on_knob_freq_changed)
	
	var knob_amp = $KnobAmp
	knob_amp.value_changed.connect(_on_knob_amp_changed)
	
	ok_button.pressed.connect(_on_ok_pressed)
	
	# Play looping frequency hum/buzz
	frequency_player = AudioStreamPlayer.new()
	frequency_player.stream = sfx_frequency
	if frequency_player.stream is AudioStreamMP3:
		frequency_player.stream.loop = true
	frequency_player.volume_db = lerp(-32.0, -14.0, 0.5) # Initial volume based on default knob position
	frequency_player.pitch_scale = 1.0 # Center pitch for 0.5 frequency knob value
	add_child(frequency_player)
	frequency_player.play()
	
	# Connect to game timer timeout for lose SFX
	var game_manager = get_parent()
	if game_manager and game_manager.has_node("GameTimer"):
		var game_timer = game_manager.get_node("GameTimer")
		game_timer.minigame_timed_out.connect(_on_timeout)

func check_light() -> void:
	var prev_light_state = $OK_Light.visible
	var light_state = check_frequency_match()
	if prev_light_state != light_state:
		play_sound(sfx_click, -3.0)
	$OK_Light.visible = light_state
	if light_state == true:
		$OK_Light.start_tweening(1, 10, .25)
	else:
		$OK_Light.kill_tween()

func _on_knob_freq_changed(value):
	if game_over: return
	player_frequency = lerp(0.1, 0.9, value)
	update_wave(player_wave, player_frequency, player_amplitude, Color(0, 1, 0, 0.8))
	if frequency_player:
		# Map knob frequency to pitch_scale dynamically
		frequency_player.pitch_scale = lerp(0.5, 1.5, value)
	check_light()

func _on_knob_amp_changed(value):
	if game_over: return
	player_amplitude = lerp(50.0, 110.0, value)
	update_wave(player_wave, player_frequency, player_amplitude, Color(0, 1, 0, 0.8))
	if frequency_player:
		# Map knob amplitude to volume_db dynamically
		frequency_player.volume_db = lerp(-32.0, -14.0, value)
	check_light()

func check_frequency_match() -> bool:
	var freq_match = abs(target_frequency - player_frequency) < match_tolerance_freq
	var amp_match = abs(target_amplitude - player_amplitude) < match_tolerance_amp
	
	if freq_match and amp_match:
		return true
	else:
		return false

func _on_ok_pressed():
	if game_over: return
	
	play_sound(sfx_click, -6.0)
	
	var can_win = check_frequency_match()
	
	if can_win:
		win_game()
	else:
		var gm = get_parent()
		if gm and "current_lives" in gm and gm.current_lives <= 1:
			if frequency_player:
				frequency_player.stop()
			play_sound(sfx_lose, -2.0)
		emit_signal("life_lost")
		# Agitar el boton o dar feedback visual
		var tween = create_tween()
		var original_pos = ok_button.position
		tween.tween_property(ok_button, "position", original_pos + Vector2(10, 0), 0.05)
		tween.tween_property(ok_button, "position", original_pos - Vector2(10, 0), 0.05)
		tween.tween_property(ok_button, "position", original_pos, 0.05)

func update_wave(line: Line2D, freq: float, amp: float, color: Color):
	line.clear_points()
	line.default_color = color
	line.width = 10.0
	
	var points = 100
	var width = 800.0
	
	for i in range(points):
		var x = (i / float(points - 1)) * width - (width / 2.0)
		var t = float(i) / points
		var y = sin(t * TAU * (freq * 10.0)) * amp
		line.add_point(Vector2(x, y))

var time_passed = 0.0
func _process(delta):
	if game_over: return
	
	time_passed += delta * 0.5
	animate_wave(target_wave, target_frequency, target_amplitude)
	animate_wave(player_wave, player_frequency, player_amplitude)

func animate_wave(line: Line2D, freq: float, amp: float):
	var points = 100
	var width = 800.0
	
	for i in range(points):
		var x = (i / float(points - 1)) * width - (width / 2.0)
		var t = float(i) / points
		var y = sin(t * TAU * (freq * 10.0) + time_passed * 10.0) * amp
		line.set_point_position(i, Vector2(x, y))

var tex_broken = preload("res://assets/sprites/minigame_4/IMG_1510.png")

func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func win_game():
	game_over = true
	emit_signal("point_scored")
	
	if frequency_player:
		frequency_player.stop()
	play_sound(sfx_impact, -15.0) # Rock impact sound (explosion)
	play_sound(sfx_win, -2.0) # Win foley
	
	# "Explotar" el planeta
	planet.texture = tex_broken
	var particles = CPUParticles2D.new()
	particles.position = planet.position
	particles.emitting = true
	particles.one_shot = true
	particles.amount = 50
	particles.explosiveness = 1.0
	particles.spread = 180.0
	particles.gravity = Vector2(0, 0)
	particles.initial_velocity_min = 200.0
	particles.initial_velocity_max = 500.0
	particles.scale_amount_min = 10.0
	particles.scale_amount_max = 30.0
	particles.color = Color(0.8, 0.2, 0.2)
	add_child(particles)
	
	await get_tree().create_timer(1.5).timeout
	emit_signal("completed")

func _on_timeout() -> void:
	if not game_over:
		if frequency_player:
			frequency_player.stop()
		play_sound(sfx_lose, -2.0)
