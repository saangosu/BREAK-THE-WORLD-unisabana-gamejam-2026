import os

os.makedirs("scenes/minigame_6", exist_ok=True)
os.makedirs("scripts/minigame_6", exist_ok=True)

tscn = """[gd_scene load_steps=5 format=3 uid="uid://minigame6"]

[ext_resource type="Script" path="res://scripts/minigame_6/minigame_6.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/sprites/minigame_2/planeta 2 completo.png" id="2_planet"]
[ext_resource type="Texture2D" path="res://assets/sprites/minigame_2/agujero negro.png" id="3_hole"]

[node name="Minigame6" type="Node2D"]
script = ExtResource("1_script")

[node name="Background" type="ColorRect" parent="."]
offset_right = 1920.0
offset_bottom = 1080.0
color = Color(0.05, 0.05, 0.1, 1)
mouse_filter = 2

[node name="BlackHole" type="Sprite2D" parent="."]
position = Vector2(960, 200)
scale = Vector2(0.3, 0.3)
texture = ExtResource("3_hole")

[node name="Planet" type="Sprite2D" parent="."]
position = Vector2(960, 750)
scale = Vector2(0.5, 0.5)
texture = ExtResource("2_planet")

[node name="GolfClub" type="ColorRect" parent="Planet"]
offset_left = 150.0
offset_top = -200.0
offset_right = 180.0
offset_bottom = 150.0
color = Color(0.7, 0.7, 0.7, 1)
pivot_offset = Vector2(15, 350)

[node name="ClubHead" type="ColorRect" parent="Planet/GolfClub"]
layout_mode = 0
offset_left = -60.0
offset_top = 320.0
offset_right = 30.0
offset_bottom = 350.0
color = Color(0.5, 0.5, 0.5, 1)

[node name="UI" type="Control" parent="."]
layout_mode = 3
anchors_preset = 0
offset_top = 900.0
offset_right = 1920.0
offset_bottom = 1080.0

[node name="BarBG" type="ColorRect" parent="UI"]
layout_mode = 0
offset_left = 460.0
offset_top = 50.0
offset_right = 1460.0
offset_bottom = 100.0
color = Color(0.2, 0.2, 0.2, 1)

[node name="SweetSpot" type="ColorRect" parent="UI/BarBG"]
layout_mode = 0
offset_left = 450.0
offset_right = 550.0
offset_bottom = 50.0
color = Color(0, 1, 0, 1)

[node name="Cursor" type="ColorRect" parent="UI/BarBG"]
layout_mode = 0
offset_left = 0.0
offset_top = -10.0
offset_right = 10.0
offset_bottom = 60.0
color = Color(1, 1, 1, 1)
"""

gd = """extends Minigame

@onready var cursor = $UI/BarBG/Cursor
@onready var sweet_spot = $UI/BarBG/SweetSpot
@onready var bar_bg = $UI/BarBG
@onready var golf_club = $Planet/GolfClub
@onready var planet = $Planet
@onready var black_hole = $BlackHole

var cursor_speed = 1200.0
var cursor_direction = 1
var is_moving = true
var game_over = false

func _ready():
	cursor.position.x = 0

func _process(delta):
	if not is_moving or game_over:
		return
		
	cursor.position.x += cursor_speed * cursor_direction * delta
	
	if cursor.position.x > bar_bg.size.x:
		cursor.position.x = bar_bg.size.x
		cursor_direction = -1
	elif cursor.position.x < 0:
		cursor.position.x = 0
		cursor_direction = 1

func _input(event):
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed):
		if is_moving and not game_over:
			_attempt_shot()

func _attempt_shot():
	is_moving = false
	
	var cursor_center = cursor.position.x + cursor.size.x / 2.0
	var spot_left = sweet_spot.position.x
	var spot_right = sweet_spot.position.x + sweet_spot.size.x
	
	if cursor_center >= spot_left and cursor_center <= spot_right:
		_win_shot()
	else:
		_fail_shot()

func _win_shot():
	game_over = true
	var tween = create_tween()
	# Swing back, then forward
	tween.tween_property(golf_club, "rotation_degrees", 60.0, 0.1)
	tween.tween_property(golf_club, "rotation_degrees", -30.0, 0.1)
	
	# Planet flies
	tween.parallel().tween_property(planet, "global_position", black_hole.global_position, 0.5).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD).set_delay(0.2)
	tween.parallel().tween_property(planet, "scale", Vector2(0.1, 0.1), 0.5).set_delay(0.2)
	
	emit_signal("point_scored")
	await tween.finished
	emit_signal("completed")

func _fail_shot():
	var tween = create_tween()
	tween.tween_property(golf_club, "rotation_degrees", 30.0, 0.1)
	tween.tween_property(golf_club, "rotation_degrees", -15.0, 0.2)
	tween.tween_property(golf_club, "rotation_degrees", 0.0, 0.2)
	
	cursor.color = Color(1, 0, 0)
	await get_tree().create_timer(0.8).timeout
	
	if not game_over:
		cursor.color = Color(1, 1, 1)
		is_moving = true
"""

with open("scenes/minigame_6/minigame_6.tscn", "w", encoding="utf-8") as f:
    f.write(tscn)

with open("scripts/minigame_6/minigame_6.gd", "w", encoding="utf-8") as f:
    f.write(gd)

print("Minigame 6 created successfully.")
