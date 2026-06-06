extends Minigame

var black_hole_scene = preload("res://scenes/minigame_2/black_hole.tscn")
var asteroid_scene = preload("res://scenes/minigame_2/asteroid.tscn")
var planet_scene = preload("res://scenes/minigame_2/planet.tscn")

@onready var spawn_point = $AsteroidSpawnPoint
@onready var planet_container = $PlanetContainer

var current_asteroid = null

func _ready():
	# Centro inferior de la pantalla (1920x1080)
	spawn_point.position = Vector2(960, 800)
	spawn_asteroid()
	
	# Spawneamos 3 planetas al mismo tiempo en diferentes alturas
	spawn_planet(Vector2(400, 150))
	spawn_planet(Vector2(960, 350))
	spawn_planet(Vector2(1400, 550))

func spawn_asteroid():
	current_asteroid = asteroid_scene.instantiate()
	current_asteroid.global_position = spawn_point.global_position
	current_asteroid.asteroid_launched.connect(_on_asteroid_launched)
	current_asteroid.asteroid_destroyed.connect(_on_asteroid_destroyed)
	add_child(current_asteroid)

func _on_asteroid_launched():
	await get_tree().create_timer(4.0).timeout
	if is_instance_valid(current_asteroid):
		current_asteroid.queue_free()
		spawn_asteroid()

func _on_asteroid_destroyed():
	if is_instance_valid(current_asteroid):
		current_asteroid.queue_free()
	spawn_asteroid()

func spawn_planet(pos: Vector2):
	var planet = planet_scene.instantiate()
	planet.global_position = pos
	planet.planet_destroyed.connect(_on_planet_destroyed)
	planet_container.add_child(planet)

func _on_planet_destroyed(pos: Vector2):
	var bh = black_hole_scene.instantiate()
	bh.global_position = pos
	add_child(bh)
