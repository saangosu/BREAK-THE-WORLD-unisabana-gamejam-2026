extends SceneTree

func _init():
	var root = Node2D.new()
	root.name = "Minigame4"
	root.set_script(load("res://scripts/minigame_4/minigame_4.gd"))
	
	var bg = ColorRect.new()
	bg.name = "Background"
	bg.color = Color(0.05, 0.05, 0.1)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.size = Vector2(1920, 1080)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(bg)
	bg.owner = root
	
	var planet = Polygon2D.new()
	planet.name = "Planet"
	planet.position = Vector2(960, 400)
	var points = PackedVector2Array()
	for i in range(32):
		var a = i * TAU / 32
		points.append(Vector2(cos(a), sin(a)) * 150)
	planet.polygon = points
	planet.color = Color(0.8, 0.2, 0.2)
	root.add_child(planet)
	planet.owner = root
	
	var target_wave = Line2D.new()
	target_wave.name = "TargetWave"
	target_wave.position = Vector2(960, 400)
	root.add_child(target_wave)
	target_wave.owner = root
	
	var player_wave = Line2D.new()
	player_wave.name = "PlayerWave"
	player_wave.position = Vector2(960, 400)
	root.add_child(player_wave)
	player_wave.owner = root
	
	var knob = Control.new()
	knob.name = "Knob"
	knob.position = Vector2(960 - 100, 850 - 100)
	knob.custom_minimum_size = Vector2(200, 200)
	knob.size = Vector2(200, 200)
	knob.set_script(load("res://scripts/minigame_4/knob.gd"))
	root.add_child(knob)
	knob.owner = root
	
	var packed = PackedScene.new()
	packed.pack(root)
	ResourceSaver.save(packed, "res://scenes/minigame_4/minigame_4.tscn")
	print("Minigame 4 generado!")
	quit()
