extends Minigame

var black_hole_scene = preload("res://scenes/minigame_2/black_hole.tscn")
var asteroid_scene = preload("res://scenes/minigame_2/asteroid.tscn")
var planet_scene = preload("res://scenes/minigame_2/planet.tscn")

@onready var spawn_point = $AsteroidSpawnPoint
@onready var planet_container = $PlanetContainer

var current_asteroid = null
var planets_to_destroy = 3
var game_over = false
var hit_something = false

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
