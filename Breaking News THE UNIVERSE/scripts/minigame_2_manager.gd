extends Minigame

var black_hole_scene = preload("res://scenes/minigame_2/black_hole.tscn")
var asteroid_scene = preload("res://scenes/minigame_2/asteroid.tscn")
var planet_scene = preload("res://scenes/minigame_2/planet.tscn")

@onready var spawn_point = $AsteroidSpawnPoint
@onready var planet_container = $PlanetContainer

var current_asteroid = null
var current_time = 20.0
var lives = 3
var planets_to_destroy = 3
var game_over = false
var hit_something = false

var timer_label: Label
var lives_label: Label
var status_label: Label

func _ready():
	setup_ui()
	
	# Centro inferior de la pantalla (1920x1080)
	spawn_point.position = Vector2(960, 800)
	spawn_asteroid()
	
	# Spawneamos 3 planetas al mismo tiempo en diferentes alturas
	spawn_planet(Vector2(400, 150))
	spawn_planet(Vector2(960, 350))
	spawn_planet(Vector2(1400, 550))

func setup_ui():
	var canvas = CanvasLayer.new()
	add_child(canvas)
	
	timer_label = Label.new()
	timer_label.position = Vector2(50, 50)
	timer_label.add_theme_font_size_override("font_size", 40)
	canvas.add_child(timer_label)
	
	lives_label = Label.new()
	lives_label.position = Vector2(1650, 50)
	lives_label.add_theme_font_size_override("font_size", 40)
	canvas.add_child(lives_label)
	
	status_label = Label.new()
	status_label.position = Vector2(0, 500)
	status_label.size = Vector2(1920, 200)
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status_label.add_theme_font_size_override("font_size", 100)
	status_label.text = ""
	canvas.add_child(status_label)

func _process(delta):
	if game_over:
		return
		
	current_time -= delta
	if current_time <= 0:
		current_time = 0
		timer_label.text = "Tiempo: %.1f" % current_time
		win_game("¡SE ACABÓ EL TIEMPO!")
	
	timer_label.text = "Tiempo: %.1f" % current_time
	lives_label.text = "Vidas: %d" % lives

func spawn_asteroid():
	if game_over: return
	
	hit_something = false
	current_asteroid = asteroid_scene.instantiate()
	current_asteroid.global_position = spawn_point.global_position
	current_asteroid.asteroid_launched.connect(_on_asteroid_launched)
	current_asteroid.asteroid_destroyed.connect(_on_asteroid_destroyed)
	current_asteroid.hit_planet.connect(_on_hit_planet)
	add_child(current_asteroid)

func _on_asteroid_launched():
	var launched_asteroid = current_asteroid
	await get_tree().create_timer(1.5).timeout
	if is_instance_valid(launched_asteroid) and not game_over:
		launched_asteroid.emit_signal("asteroid_destroyed")
		launched_asteroid.queue_free()

func _on_hit_planet():
	hit_something = true

func _on_asteroid_destroyed():
	if game_over: return
	
	if not hit_something:
		lives -= 1
		lives_label.text = "Vidas: %d" % lives
		if lives <= 0:
			lose_game("¡SIN VIDAS!")
			return
			
	# If we hit something, or we still have lives, spawn another
	spawn_asteroid()

func spawn_planet(pos: Vector2):
	var planet = planet_scene.instantiate()
	planet.global_position = pos
	planet.planet_destroyed.connect(_on_planet_destroyed)
	planet_container.add_child(planet)

func _on_planet_destroyed(pos: Vector2):
	emit_signal("point_scored")
	var bh = black_hole_scene.instantiate()
	bh.global_position = pos
	add_child(bh)
	
	planets_to_destroy -= 1
	if planets_to_destroy <= 0:
		win_game("¡NIVEL COMPLETADO!")

func win_game(reason: String):
	game_over = true
	status_label.text = reason
	status_label.modulate = Color(0, 1, 0) # Verde
	
	if is_instance_valid(current_asteroid):
		current_asteroid.queue_free()
	for p in get_tree().get_nodes_in_group("planet"):
		p.move_speed = 0
		
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
		
	await get_tree().create_timer(2.0).timeout
	emit_signal("lost")
