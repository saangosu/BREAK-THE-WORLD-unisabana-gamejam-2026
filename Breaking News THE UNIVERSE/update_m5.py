import os

gd_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\minigame_5\minigame_5.gd"
gd_content = """extends Minigame

@onready var moon = $Moon
@onready var progress_bar = $ProgressBar
@onready var particles = $CheeseParticles

var is_grating = false
var progress = 0.0
var required_distance = 10000.0 # lowered distance slightly for testing

var is_game_over = false

var grater_left_bound = 800.0
var grater_right_bound = 1120.0

var initial_scale = 0.25

func _ready():
    progress_bar.max_value = 100
    progress_bar.value = 0
    moon.scale = Vector2(initial_scale, initial_scale)
    moon.position = Vector2(960, 540)
    
    var gm = get_parent()
    var time_limit = 10.0
    if gm and "current_time" in gm:
        time_limit = gm.current_time
        
    var timer = get_tree().create_timer(time_limit - 0.1)
    timer.timeout.connect(_on_timeout)

func _on_timeout():
    if not is_game_over:
        is_game_over = true
        emit_signal("lost")

func _input(event):
    if is_game_over: return
    
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if event.pressed:
            is_grating = true
        else:
            is_grating = false
            particles.emitting = false
            
    if is_grating and event is InputEventMouseMotion:
        moon.position += event.relative
        moon.position.y = clamp(moon.position.y, 140, 940)
        
        # Check walls
        if moon.position.x < grater_left_bound or moon.position.x > grater_right_bound:
            _hit_wall()
            return
            
        particles.position = moon.position + Vector2(0, 50)
        
        if abs(event.relative.y) > 0:
            particles.emitting = true
            progress += abs(event.relative.y)
            var pct = min((progress / required_distance) * 100.0, 100.0)
            progress_bar.value = pct
            
            # Make moon thinner
            moon.scale.x = lerp(initial_scale, 0.02, progress / required_distance)
            
            if pct >= 100.0:
                _win()
        else:
            particles.emitting = false

func _hit_wall():
    is_grating = false
    particles.emitting = false
    moon.position.x = 960
    emit_signal("life_lost")

func _win():
    is_game_over = true
    particles.emitting = false
    var tween = create_tween()
    tween.tween_property(moon, "scale", Vector2(0, 0), 0.2)
    await tween.finished
    emit_signal("point_scored")
    emit_signal("completed")
"""

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd_content)


tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_5\minigame_5.tscn"

# Create holes string
holes_str = ""
idx = 1
for x in range(60, 340, 60):
    for y in range(60, 800, 60):
        holes_str += f"""[node name="Hole_{idx}" type="ColorRect" parent="GraterFrame/GraterHolesBG"]
layout_mode = 0
offset_left = {x - 10}.0
offset_top = {y - 10}.0
offset_right = {x + 10}.0
offset_bottom = {y + 10}.0
color = Color(0.1, 0.1, 0.1, 1)
mouse_filter = 2

"""
        idx += 1


tscn_content = f"""[gd_scene load_steps=4 format=3 uid="uid://minigame5"]

[ext_resource type="Script" path="res://scripts/minigame_5/minigame_5.gd" id="1_script"]
[ext_resource type="Texture2D" uid="uid://bvlan7jb7dn1" path="res://textures/art/Luna.png" id="2_moon"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_bg"]
bg_color = Color(0.2, 0.2, 0.2, 1)

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_fill"]
bg_color = Color(1, 0.8, 0.2, 1)

[node name="Minigame5" type="Node2D"]
script = ExtResource("1_script")

[node name="Background" type="ColorRect" parent="."]
offset_right = 1920.0
offset_bottom = 1080.0
color = Color(0.1, 0.05, 0.15, 1)
mouse_filter = 2

[node name="GraterFrame" type="ColorRect" parent="."]
offset_left = 760.0
offset_top = 100.0
offset_right = 1160.0
offset_bottom = 980.0
color = Color(0.65, 0.65, 0.7, 1)
mouse_filter = 2

[node name="GraterHolesBG" type="ColorRect" parent="GraterFrame"]
layout_mode = 0
offset_left = 40.0
offset_top = 40.0
offset_right = 360.0
offset_bottom = 840.0
color = Color(0.3, 0.3, 0.35, 1)
mouse_filter = 2

{holes_str}

[node name="ProgressBar" type="ProgressBar" parent="."]
offset_left = 1300.0
offset_top = 100.0
offset_right = 1400.0
offset_bottom = 980.0
theme_override_styles/background = SubResource("StyleBoxFlat_bg")
theme_override_styles/fill = SubResource("StyleBoxFlat_fill")
fill_mode = 3
show_percentage = false

[node name="CheeseParticles" type="CPUParticles2D" parent="."]
position = Vector2(960, 540)
emitting = false
amount = 60
lifetime = 1.0
emission_shape = 3
emission_rect_extents = Vector2(60, 20)
direction = Vector2(0, 1)
spread = 20.0
gravity = Vector2(0, 1200)
initial_velocity_min = 100.0
initial_velocity_max = 300.0
scale_amount_min = 8.0
scale_amount_max = 16.0
color = Color(1, 0.9, 0.2, 1)

[node name="Moon" type="Sprite2D" parent="."]
position = Vector2(960, 540)
scale = Vector2(0.25, 0.25)
texture = ExtResource("2_moon")
"""

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn_content)

print("Updated minigame 5 with textures, grater visuals, particles and walls!")
