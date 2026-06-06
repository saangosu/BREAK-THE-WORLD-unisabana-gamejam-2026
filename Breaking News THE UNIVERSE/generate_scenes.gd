extends SceneTree

func _init():
	create_asteroid_scene()
	create_planet_scene()
	create_black_hole_scene()
	create_main_scene()
	print("Todas las escenas generadas correctamente!")
	quit()

func create_circle_polygon(radius: float) -> PackedVector2Array:
	var points = PackedVector2Array()
	var segments = 32
	for i in range(segments):
		var angle = i * TAU / segments
		points.append(Vector2(cos(angle), sin(angle)) * radius)
	return points

func create_asteroid_scene():
	var root = RigidBody2D.new()
	root.name = "Asteroid"
	root.set_script(load("res://scenes/minigame_2/asteroid.gd"))
	
	var poly = Polygon2D.new()
	poly.name = "Polygon2D"
	poly.polygon = create_circle_polygon(30.0)
	poly.color = Color(0.5, 0.5, 0.5)
	root.add_child(poly)
	poly.owner = root
	
	var coll = CollisionShape2D.new()
	coll.name = "CollisionShape2D"
	var shape = CircleShape2D.new()
	shape.radius = 30.0
	coll.shape = shape
	root.add_child(coll)
	coll.owner = root
	
	var packed = PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, "res://scenes/minigame_2/asteroid.tscn")

func create_planet_scene():
	var root = StaticBody2D.new()
	root.name = "Planet"
	root.set_script(load("res://scenes/minigame_2/planet.gd"))
	
	var poly = Polygon2D.new()
	poly.name = "Polygon2D"
	poly.polygon = create_circle_polygon(100.0)
	poly.color = Color(0.2, 0.8, 0.2)
	root.add_child(poly)
	poly.owner = root
	
	var coll = CollisionShape2D.new()
	coll.name = "CollisionShape2D"
	var shape = CircleShape2D.new()
	shape.radius = 100.0
	coll.shape = shape
	root.add_child(coll)
	coll.owner = root
	
	var packed = PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, "res://scenes/minigame_2/planet.tscn")

func create_black_hole_scene():
	var root = Area2D.new()
	root.name = "BlackHole"
	root.set_script(load("res://scenes/minigame_2/black_hole.gd"))
	
	var poly = Polygon2D.new()
	poly.name = "Polygon2D"
	poly.polygon = create_circle_polygon(60.0)
	poly.color = Color(0.0, 0.0, 0.0)
	root.add_child(poly)
	poly.owner = root
	
	var coll = CollisionShape2D.new()
	coll.name = "CollisionShape2D"
	var shape = CircleShape2D.new()
	shape.radius = 400.0
	coll.shape = shape
	root.add_child(coll)
	coll.owner = root
	
	var packed = PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, "res://scenes/minigame_2/black_hole.tscn")

func create_main_scene():
	var root = Node2D.new()
	root.name = "Minigame2"
	root.set_script(load("res://scenes/minigame_2/minigame_2_manager.gd"))
	
	var bg = ColorRect.new()
	bg.name = "Background"
	bg.color = Color(0.1, 0.1, 0.2)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.size = Vector2(1920, 1080)
	root.add_child(bg)
	bg.owner = root
	
	var spawn = Marker2D.new()
	spawn.name = "AsteroidSpawnPoint"
	spawn.position = Vector2(300, 540)
	root.add_child(spawn)
	spawn.owner = root
	
	var p_container = Node2D.new()
	p_container.name = "PlanetContainer"
	root.add_child(p_container)
	p_container.owner = root
	
	var packed = PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, "res://scenes/minigame_2/minigame_2.tscn")
