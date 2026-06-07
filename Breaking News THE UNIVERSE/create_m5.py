import os

# Create dirs
os.makedirs(r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_5", exist_ok=True)
os.makedirs(r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\minigame_5", exist_ok=True)

gd_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\minigame_5\minigame_5.gd"
gd_content = """extends Minigame

@onready var moon = $Moon
@onready var progress_bar = $ProgressBar

var is_grating = false
var progress = 0.0
var required_distance = 15000.0 # Adjust for difficulty

var is_game_over = false

func _ready():
    progress_bar.max_value = 100
    progress_bar.value = 0
    
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
            
    if is_grating and event is InputEventMouseMotion:
        moon.position.y += event.relative.y
        moon.position.y = clamp(moon.position.y, 200, 800)
        
        progress += abs(event.relative.y)
        var pct = min((progress / required_distance) * 100.0, 100.0)
        progress_bar.value = pct
        
        if pct >= 100.0:
            _win()

func _win():
    is_game_over = true
    var tween = create_tween()
    tween.tween_property(moon, "scale", Vector2(0, 0), 0.2)
    await tween.finished
    emit_signal("point_scored")
    emit_signal("completed")
"""

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd_content)

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_5\minigame_5.tscn"
tscn_content = """[gd_scene load_steps=3 format=3 uid="uid://minigame5"]

[ext_resource type="Script" path="res://scripts/minigame_5/minigame_5.gd" id="1_script"]

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

[node name="Grater" type="ColorRect" parent="."]
offset_left = 760.0
offset_top = 100.0
offset_right = 1160.0
offset_bottom = 980.0
color = Color(0.6, 0.6, 0.65, 1)
mouse_filter = 2

[node name="GraterHoles" type="ColorRect" parent="Grater"]
layout_mode = 0
offset_left = 40.0
offset_top = 40.0
offset_right = 360.0
offset_bottom = 840.0
color = Color(0.3, 0.3, 0.35, 1)
mouse_filter = 2

[node name="ProgressBar" type="ProgressBar" parent="."]
offset_left = 1300.0
offset_top = 100.0
offset_right = 1400.0
offset_bottom = 980.0
theme_override_styles/background = SubResource("StyleBoxFlat_bg")
theme_override_styles/fill = SubResource("StyleBoxFlat_fill")
fill_mode = 3
show_percentage = false

[node name="Moon" type="Polygon2D" parent="."]
position = Vector2(960, 540)
color = Color(1, 0.9, 0.6, 1)
polygon = PackedVector2Array(0, -120, 85, -85, 120, 0, 85, 85, 0, 120, -85, 85, -120, 0, -85, -85)
"""

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn_content)

# Update game_manager.gd
gm_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\game_manager.gd"
with open(gm_path, "r", encoding="utf-8") as f:
    gm = f.read()

# Add minigame_5 to levels array
if '"res://scenes/minigame_5/minigame_5.tscn"' not in gm:
    gm = gm.replace(
        '"res://scenes/minigame_6/minigame_6.tscn"', 
        '"res://scenes/minigame_6/minigame_6.tscn", "res://scenes/minigame_5/minigame_5.tscn"'
    )
    with open(gm_path, "w", encoding="utf-8") as f:
        f.write(gm)
        
print("Minigame 5 created and registered!")
