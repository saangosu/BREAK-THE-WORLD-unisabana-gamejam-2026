extends Minigame

var black_hole_scene = preload("res://scenes/minigame_2/black_hole.tscn")
var asteroid_scene = preload("res://scenes/minigame_2/asteroid.tscn")
var planet_scene = preload("res://scenes/minigame_2/planet.tscn")

const sfx_win = preload("res://sounds/minigame_2/Foleys/gano.mp3")
const sfx_lose = preload("res://sounds/minigame_2/Foleys/perdiste.mp3")

@onready var spawn_point = $AsteroidSpawnPoint
@onready var planet_container = $PlanetContainer
@onready var front_band = $SlingshotBase/FrontBand
@onready var back_band = $SlingshotBase/BackBand

var band_left_prong = Vector2(860, 780)
var band_right_prong = Vector2(1060, 780)
var idle_center = Vector2(960, 850)

var current_asteroid = null
var planets_to_destroy = 3
var game_over = false
var hit_something = false

var status_label: Label
var BGM_player : AudioStreamPlayer

func _ready():
	setup_ui()
	
	# Centro inferior de la pantalla (1920x1080)
	spawn_point.position = Vector2(960, 850)
	spawn_asteroid()
	
	# Spawneamos 3 planetas al mismo tiempo en diferentes alturas
	spawn_planet(Vector2(400, 150))
	spawn_planet(Vector2(960, 350))
	spawn_planet(Vector2(1400, 550))
	
	# Play looping background music
	var bgm = load("res://sounds/minigame_2/musica_de_fondo/musica_de_fondo.wav")
	if bgm:
		if bgm is AudioStreamWAV:
			bgm.loop_mode = AudioStreamWAV.LOOP_FORWARD
		BGM_player = AudioStreamPlayer.new()
		BGM_player.stream = bgm
		BGM_player.volume_db = -12.0 # Balanced volume
		add_child(BGM_player)
		BGM_player.play()
		
	# Connect to game timer timeout for lose SFX
	var game_manager = get_parent()
	if game_manager and game_manager.has_node("GameTimer"):
		var game_timer = game_manager.get_node("GameTimer")
		game_timer.minigame_timed_out.connect(_on_timeout)

func setup_ui():
	var canvas = CanvasLayer.new()
	add_child(canvas)
	
	status_label = Label.new()
	status_label.position = Vector2(0, 500)
	status_label.size = Vector2(1920, 200)
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status_label.add_theme_font_size_override("font_size", 100)
	status_label.text = ""
	canvas.add_child(status_label)

func spawn_asteroid():
	if game_over: return
	
	hit_something = false
	current_asteroid = asteroid_scene.instantiate()
	current_asteroid.global_position = spawn_point.global_position
	current_asteroid.asteroid_launched.connect(_on_asteroid_launched)
	current_asteroid.asteroid_destroyed.connect(_on_asteroid_destroyed)
	current_asteroid.hit_planet.connect(_on_hit_planet)
	call_deferred("add_child", current_asteroid)

func _on_asteroid_launched():
	var launched_asteroid : Asteroid = current_asteroid
	var on_screen_notifier : VisibleOnScreenNotifier2D = launched_asteroid.find_child("VisibleOnScreenNotifier2D")
	await on_screen_notifier.screen_exited
	if is_instance_valid(launched_asteroid) and not game_over:
		launched_asteroid.emit_signal("asteroid_destroyed")
		launched_asteroid.queue_free()

func _on_hit_planet():
	hit_something = true

func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func _on_asteroid_destroyed():
	if game_over: return
	
	if not hit_something:
		var gm = get_parent()
		if gm and "current_lives" in gm and gm.current_lives <= 1:
			if BGM_player:
				BGM_player.stop()
			play_sound(sfx_lose, -2.0)
		emit_signal("life_lost")
		spawn_asteroid()
		return
			
	# If we hit something, or we still have lives, spawn another
	spawn_asteroid()

func spawn_planet(pos: Vector2):
	var planet = planet_scene.instantiate()
	planet.global_position = pos
	planet.planet_destroyed.connect(_on_planet_destroyed)
	planet_container.add_child(planet)

func _on_planet_destroyed(pos: Vector2, p_color: Color):
	emit_signal("point_scored")
	
	# Restos volando (Fragmentos)
	for i in range(9):
		var particles = CPUParticles2D.new()
		var tex = load("res://assets/sprites/minigame_2/Planeta 2 destruido_frag_" + str(i) + ".png")
		if tex:
			particles.texture = tex
			particles.emission_shape = CPUParticles2D.EMISSION_SHAPE_POINT
			particles.spread = 180.0
			particles.gravity = Vector2(0, 0)
			particles.initial_velocity_min = 300.0
			particles.initial_velocity_max = 700.0
			particles.scale_amount_min = 0.05
			particles.scale_amount_max = 0.05
			particles.color = p_color
			particles.explosiveness = 1.0
			particles.amount = 1
			particles.one_shot = true
			particles.lifetime = 1.5
			particles.global_position = pos
			call_deferred("add_child", particles)
	
	# Agujero Negro
	var bh = black_hole_scene.instantiate()
	bh.global_position = pos
	bh.get_node("Sprite2D").modulate = p_color
	call_deferred("add_child", bh)
	
	planets_to_destroy -= 1
	if planets_to_destroy <= 0:
		win_game("¡NIVEL COMPLETADO!")

func win_game(reason: String):
	game_over = true
	stop_timer.emit()
	status_label.text = reason
	status_label.modulate = Color(0, 1, 0) # Verde
	
	if is_instance_valid(current_asteroid):
		current_asteroid.queue_free()
	for p in get_tree().get_nodes_in_group("planet"):
		p.move_speed = 0
		
	if BGM_player:
		BGM_player.stop()
	play_sound(sfx_win, -2.0)
		
	await get_tree().create_timer(2.0).timeout
	emit_signal("completed")

func lose_game(reason: String):
	game_over = true
	status_label.text = reason
	status_label.modulate = Color(1, 0, 0) # Rojo
	
	if is_instance_valid(current_asteroid):
		current_asteroid.queue_free()
	for p in get_tree().get_nodes_in_group("planet"):
		p.move_speed = 0
		
	if BGM_player:
		BGM_player.stop()
	play_sound(sfx_lose, -2.0)
		
	await get_tree().create_timer(2.0).timeout
	emit_signal("lost")

func _on_timeout() -> void:
	if not game_over:
		if BGM_player:
			BGM_player.stop()
		play_sound(sfx_lose, -2.0)

func _process(_delta):
	if is_instance_valid(current_asteroid):
		if not current_asteroid.launched:
			front_band.visible = true
			back_band.visible = true
			# La goma persigue al asteroide
			front_band.set_point_position(1, current_asteroid.global_position)
			back_band.set_point_position(1, current_asteroid.global_position)
		else:
			# Si ya se lanzó, esconder bandas temporalmente
			front_band.visible = false
			back_band.visible = false
	else:
		front_band.visible = false
		back_band.visible = false
