import os

tscn = """[gd_scene load_steps=9 format=3 uid="uid://minigame6"]

[ext_resource type="Script" path="res://scripts/minigame_6/minigame_6.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/sprites/minigame_2/planeta 2 completo.png" id="2_planet"]
[ext_resource type="Texture2D" path="res://assets/sprites/minigame_2/agujero negro.png" id="3_hole"]

[sub_resource type="Shader" id="Shader_power"]
code = "shader_type canvas_item;
void fragment() {
    float t = UV.y;
    vec3 color;
    if (t < 0.5) {
        color = mix(vec3(1.0, 0.0, 0.0), vec3(0.0, 1.0, 0.0), t * 2.0);
    } else {
        color = mix(vec3(0.0, 1.0, 0.0), vec3(0.0, 0.0, 1.0), (t - 0.5) * 2.0);
    }
    COLOR = vec4(color, 1.0);
}
"

[sub_resource type="ShaderMaterial" id="ShaderMaterial_power"]
shader = SubResource("Shader_power")

[sub_resource type="Shader" id="Shader_dir"]
code = "shader_type canvas_item;
void fragment() {
    float t = UV.x;
    vec3 color;
    if (t < 0.5) {
        color = mix(vec3(1.0, 0.0, 0.0), vec3(0.0, 1.0, 0.0), t * 2.0);
    } else {
        color = mix(vec3(0.0, 1.0, 0.0), vec3(1.0, 0.0, 0.0), (t - 0.5) * 2.0);
    }
    COLOR = vec4(color, 1.0);
}
"

[sub_resource type="ShaderMaterial" id="ShaderMaterial_dir"]
shader = SubResource("Shader_dir")

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
offset_left = -80.0
offset_top = -250.0
offset_right = -60.0
offset_bottom = 0.0
color = Color(0.8, 0.8, 0.8, 1)

[node name="Flag" type="Polygon2D" parent="BlackHole/Pole"]
color = Color(1, 0, 0, 1)
polygon = PackedVector2Array(20, 0, 130, 20, 20, 60)

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
material = SubResource("ShaderMaterial_power")
layout_mode = 0
offset_left = 1600.0
offset_top = 140.0
offset_right = 1700.0
offset_bottom = 940.0

[node name="Border" type="ReferenceRect" parent="UI/BarBG"]
layout_mode = 0
offset_left = -5.0
offset_top = -5.0
offset_right = 105.0
offset_bottom = 805.0
border_color = Color(1, 1, 1, 1)
border_width = 5.0
editor_only = false

[node name="SweetSpotIndicator" type="Polygon2D" parent="UI/BarBG"]
position = Vector2(-20, 400)
color = Color(1, 1, 1, 1)
polygon = PackedVector2Array(0, -15, 20, 0, 0, 15)

[node name="SweetSpotIndicator2" type="Polygon2D" parent="UI/BarBG"]
position = Vector2(120, 400)
color = Color(1, 1, 1, 1)
polygon = PackedVector2Array(0, -15, -20, 0, 0, 15)

[node name="Cursor" type="ColorRect" parent="UI/BarBG"]
layout_mode = 0
offset_left = -10.0
offset_top = 0.0
offset_right = 110.0
offset_bottom = 10.0
color = Color(1, 1, 1, 1)

[node name="DirBarBG" type="ColorRect" parent="UI"]
material = SubResource("ShaderMaterial_dir")
layout_mode = 0
offset_left = 660.0
offset_top = 950.0
offset_right = 1260.0
offset_bottom = 1000.0
visible = false

[node name="Border" type="ReferenceRect" parent="UI/DirBarBG"]
layout_mode = 0
offset_left = -5.0
offset_top = -5.0
offset_right = 605.0
offset_bottom = 55.0
border_color = Color(1, 1, 1, 1)
border_width = 5.0
editor_only = false

[node name="SweetSpotIndicator" type="Polygon2D" parent="UI/DirBarBG"]
position = Vector2(300, -20)
color = Color(1, 1, 1, 1)
polygon = PackedVector2Array(-15, 0, 15, 0, 0, 20)

[node name="SweetSpotIndicator2" type="Polygon2D" parent="UI/DirBarBG"]
position = Vector2(300, 70)
color = Color(1, 1, 1, 1)
polygon = PackedVector2Array(-15, 0, 15, 0, 0, -20)

[node name="DirCursor" type="ColorRect" parent="UI/DirBarBG"]
layout_mode = 0
offset_left = 0.0
offset_top = -10.0
offset_right = 10.0
offset_bottom = 60.0
color = Color(1, 1, 1, 1)
"""

gd = """extends Minigame

@onready var cursor_power = $UI/BarBG/Cursor
@onready var bar_power = $UI/BarBG

@onready var cursor_dir = $UI/DirBarBG/DirCursor
@onready var bar_dir = $UI/DirBarBG

@onready var golf_club = $Planet/GolfClub
@onready var planet = $Planet
@onready var black_hole = $BlackHole

var cursor_speed_power = 900.0
var cursor_speed_dir = 900.0

var power_dir_y = 1
var dir_dir_x = 1

enum State { POWER, DIRECTION, SHOOTING, DONE }
var current_state = State.POWER

var stored_power = 0.5
var stored_direction = 0.5

func _ready():
	cursor_power.position.y = bar_power.size.y
	cursor_dir.position.x = 0
	bar_dir.visible = false
	
	var gm = get_parent()
	var time_limit = 10.0
	if gm and "current_time" in gm:
		time_limit = gm.current_time
		
	var timer = get_tree().create_timer(time_limit - 0.1)
	timer.timeout.connect(_on_timeout)

func _on_timeout():
	if current_state != State.SHOOTING and current_state != State.DONE:
		current_state = State.DONE
		cursor_power.color = Color(1, 0, 0)
		if bar_dir.visible:
			cursor_dir.color = Color(1, 0, 0)
		var tween = create_tween()
		tween.tween_property(golf_club, "rotation_degrees", 20.0, 0.1)
		tween.tween_property(golf_club, "rotation_degrees", 0.0, 0.2)
		await tween.finished
		emit_signal("lost")

func _process(delta):
	if current_state == State.POWER:
		cursor_power.position.y += cursor_speed_power * power_dir_y * delta
		if cursor_power.position.y > bar_power.size.y:
			cursor_power.position.y = bar_power.size.y
			power_dir_y = -1
		elif cursor_power.position.y < 0:
			cursor_power.position.y = 0
			power_dir_y = 1
			
	elif current_state == State.DIRECTION:
		cursor_dir.position.x += cursor_speed_dir * dir_dir_x * delta
		if cursor_dir.position.x > bar_dir.size.x:
			cursor_dir.position.x = bar_dir.size.x
			dir_dir_x = -1
		elif cursor_dir.position.x < 0:
			cursor_dir.position.x = 0
			dir_dir_x = 1

func _input(event):
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed):
		if current_state == State.POWER:
			_lock_power()
		elif current_state == State.DIRECTION:
			_lock_direction()

func _lock_power():
	current_state = State.DIRECTION
	var cursor_center = cursor_power.position.y + cursor_power.size.y / 2.0
	stored_power = 1.0 - (cursor_center / bar_power.size.y) # 0.0 a 1.0
	bar_dir.visible = true

func _lock_direction():
	current_state = State.SHOOTING
	var cursor_center = cursor_dir.position.x + cursor_dir.size.x / 2.0
	stored_direction = cursor_center / bar_dir.size.x # 0.0 a 1.0 (0.5 es el centro)
	_attempt_shot()

func _attempt_shot():
	current_state = State.DONE
	
	var power_perfect = abs(stored_power - 0.5) <= 0.08
	var dir_perfect = abs(stored_direction - 0.5) <= 0.08
	var is_win = power_perfect and dir_perfect
	
	# Calculate target
	var distance_y = stored_power * 1000.0
	var target_y = planet.global_position.y - distance_y
	
	var offset_x = (stored_direction - 0.5) * 1200.0
	var target_x = planet.global_position.x + offset_x
	
	var tween = create_tween()
	var back_rotation = lerp(20.0, 90.0, stored_power)
	tween.tween_property(golf_club, "rotation_degrees", back_rotation, 0.15)
	
	var follow_through = lerp(-10.0, -60.0, stored_power)
	tween.tween_property(golf_club, "rotation_degrees", follow_through, 0.1)
	
	var flight_time = lerp(0.3, 0.6, stored_power)
	tween.parallel().tween_property(planet, "global_position", Vector2(target_x, target_y), flight_time).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD).set_delay(0.25)
	
	if is_win:
		tween.parallel().tween_property(planet, "scale", Vector2(0.05, 0.05), flight_time).set_delay(0.25)
		await tween.finished
		emit_signal("point_scored")
		emit_signal("completed")
	else:
		if not power_perfect:
			cursor_power.color = Color(1,0,0)
		if not dir_perfect:
			cursor_dir.color = Color(1,0,0)
		await tween.finished
		emit_signal("lost")
"""

with open("scenes/minigame_6/minigame_6.tscn", "w", encoding="utf-8") as f:
    f.write(tscn)

with open("scripts/minigame_6/minigame_6.gd", "w", encoding="utf-8") as f:
    f.write(gd)

print("Minigame 6 updated with double mechanics.")
