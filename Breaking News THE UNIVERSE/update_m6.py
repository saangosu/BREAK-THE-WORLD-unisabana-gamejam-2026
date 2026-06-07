import os

tscn = """[gd_scene load_steps=7 format=3 uid="uid://minigame6"]

[ext_resource type="Script" path="res://scripts/minigame_6/minigame_6.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/sprites/minigame_2/planeta 2 completo.png" id="2_planet"]
[ext_resource type="Texture2D" path="res://assets/sprites/minigame_2/agujero negro.png" id="3_hole"]

[sub_resource type="Shader" id="Shader_gradient"]
code = "shader_type canvas_item;
void fragment() {
    float t = UV.y;
    vec3 color;
    if (t < 0.5) {
        // Top half: Red to Green
        color = mix(vec3(1.0, 0.0, 0.0), vec3(0.0, 1.0, 0.0), t * 2.0);
    } else {
        // Bottom half: Green to Blue
        color = mix(vec3(0.0, 1.0, 0.0), vec3(0.0, 0.0, 1.0), (t - 0.5) * 2.0);
    }
    COLOR = vec4(color, 1.0);
}
"

[sub_resource type="ShaderMaterial" id="ShaderMaterial_gradient"]
shader = SubResource("Shader_gradient")

[node name="Minigame6" type="Node2D"]
script = ExtResource("1_script")

[node name="Background" type="ColorRect" parent="."]
offset_right = 1920.0
offset_bottom = 1080.0
color = Color(0.05, 0.05, 0.1, 1)
mouse_filter = 2

[node name="BlackHole" type="Sprite2D" parent="."]
position = Vector2(960, 350)
scale = Vector2(0.6, 0.6)
texture = ExtResource("3_hole")

[node name="Pole" type="ColorRect" parent="BlackHole"]
offset_left = -10.0
offset_top = -300.0
offset_right = 10.0
offset_bottom = 0.0
color = Color(0.8, 0.8, 0.8, 1)

[node name="Flag" type="ColorRect" parent="BlackHole/Pole"]
layout_mode = 0
offset_left = 20.0
offset_top = 0.0
offset_right = 150.0
offset_bottom = 80.0
color = Color(1, 0, 0, 1)

[node name="Planet" type="Sprite2D" parent="."]
position = Vector2(960, 850)
scale = Vector2(0.12, 0.12)
texture = ExtResource("2_planet")

[node name="GolfClub" type="ColorRect" parent="Planet"]
offset_left = 600.0
offset_top = -1200.0
offset_right = 700.0
offset_bottom = 300.0
color = Color(0.7, 0.7, 0.7, 1)
pivot_offset = Vector2(50, 1500)

[node name="ClubHead" type="ColorRect" parent="Planet/GolfClub"]
layout_mode = 0
offset_left = -250.0
offset_top = 1400.0
offset_right = 100.0
offset_bottom = 1500.0
color = Color(0.5, 0.5, 0.5, 1)

[node name="UI" type="Control" parent="."]
layout_mode = 3
anchors_preset = 0
offset_right = 1920.0
offset_bottom = 1080.0

[node name="BarBG" type="ColorRect" parent="UI"]
material = SubResource("ShaderMaterial_gradient")
layout_mode = 0
offset_left = 1600.0
offset_top = 140.0
offset_right = 1700.0
offset_bottom = 940.0

[node name="SweetSpotIndicator" type="ColorRect" parent="UI/BarBG"]
layout_mode = 0
offset_left = -20.0
offset_top = 370.0
offset_right = 0.0
offset_bottom = 430.0
color = Color(1, 1, 1, 1)

[node name="SweetSpotIndicator2" type="ColorRect" parent="UI/BarBG"]
layout_mode = 0
offset_left = 100.0
offset_top = 370.0
offset_right = 120.0
offset_bottom = 430.0
color = Color(1, 1, 1, 1)

[node name="Cursor" type="ColorRect" parent="UI/BarBG"]
layout_mode = 0
offset_left = -30.0
offset_top = 0.0
offset_right = 130.0
offset_bottom = 15.0
color = Color(1, 1, 1, 1)
"""

gd = """extends Minigame

@onready var cursor = $UI/BarBG/Cursor
@onready var bar_bg = $UI/BarBG
@onready var golf_club = $Planet/GolfClub
@onready var planet = $Planet
@onready var black_hole = $BlackHole

var cursor_speed = 1000.0
var cursor_direction = 1
var is_moving = true
var game_over = false

func _ready():
	cursor.position.y = bar_bg.size.y

func _process(delta):
	if not is_moving or game_over:
		return
		
	cursor.position.y += cursor_speed * cursor_direction * delta
	
	if cursor.position.y > bar_bg.size.y:
		cursor.position.y = bar_bg.size.y
		cursor_direction = -1
	elif cursor.position.y < 0:
		cursor.position.y = 0
		cursor_direction = 1

func _input(event):
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed):
		if is_moving and not game_over:
			_attempt_shot()

func _attempt_shot():
	is_moving = false
	game_over = true
	
	var cursor_center = cursor.position.y + cursor.size.y / 2.0
	var power = 1.0 - (cursor_center / bar_bg.size.y) # 0.0 to 1.0
	
	# Win condition: power between 0.45 and 0.55 (perfect is 0.5)
	var is_win = abs(power - 0.5) <= 0.075
	
	# Calculate distance: Max power (1.0) goes 1000 pixels. Power 0.5 goes 500 pixels.
	var distance = power * 1000.0
	var target_y = planet.global_position.y - distance
	
	# Animate Swing
	var tween = create_tween()
	# The club swings back more depending on power
	var back_rotation = lerp(20.0, 90.0, power)
	tween.tween_property(golf_club, "rotation_degrees", back_rotation, 0.15)
	
	# The club swings forward
	var follow_through = lerp(-10.0, -60.0, power)
	tween.tween_property(golf_club, "rotation_degrees", follow_through, 0.1)
	
	# Planet flies
	var flight_time = lerp(0.3, 0.6, power)
	tween.parallel().tween_property(planet, "global_position", Vector2(planet.global_position.x, target_y), flight_time).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD).set_delay(0.25)
	
	if is_win:
		tween.parallel().tween_property(planet, "scale", Vector2(0.05, 0.05), flight_time).set_delay(0.25)
		await tween.finished
		emit_signal("point_scored")
		emit_signal("completed")
	else:
		await tween.finished
		emit_signal("lost")
"""

with open("scenes/minigame_6/minigame_6.tscn", "w", encoding="utf-8") as f:
    f.write(tscn)

with open("scripts/minigame_6/minigame_6.gd", "w", encoding="utf-8") as f:
    f.write(gd)

print("Minigame 6 updated.")
