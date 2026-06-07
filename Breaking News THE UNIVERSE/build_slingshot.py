import os

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_2\minigame_2.tscn"
gd_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\minigame_2_manager.gd"

# Update TSCN
tscn_content = """[gd_scene load_steps=2 format=3 uid="uid://bs0wprtx8ukj3"]

[ext_resource type="Script" path="res://scripts/minigame_2_manager.gd" id="1_mgr"]

[node name="Minigame2" type="Node2D"]
script = ExtResource("1_mgr")

[node name="Background" type="ColorRect" parent="."]
offset_right = 1920.0
offset_bottom = 1080.0
mouse_filter = 2
color = Color(0.1, 0.1, 0.2, 1)

[node name="SlingshotBase" type="Node2D" parent="."]

[node name="BackBand" type="Line2D" parent="SlingshotBase"]
z_index = -1
points = PackedVector2Array(1000, 750, 960, 800)
width = 8.0
default_color = Color(0.6, 0.1, 0.1, 1)

[node name="Wood" type="Polygon2D" parent="SlingshotBase"]
color = Color(0.45, 0.25, 0.1, 1)
polygon = PackedVector2Array(950, 950, 970, 950, 965, 820, 1005, 740, 990, 735, 955, 805, 920, 735, 905, 740, 950, 820)

[node name="FrontBand" type="Line2D" parent="SlingshotBase"]
z_index = 2
points = PackedVector2Array(920, 750, 960, 800)
width = 8.0
default_color = Color(0.8, 0.2, 0.2, 1)

[node name="AsteroidSpawnPoint" type="Marker2D" parent="."]
position = Vector2(960, 800)

[node name="PlanetContainer" type="Node2D" parent="."]
"""
with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn_content)

# Update GD script
with open(gd_path, "r", encoding="utf-8") as f:
    gd_code = f.read()

import re

# Add onready variables
if "var back_band" not in gd_code:
    injection = """@onready var spawn_point = $AsteroidSpawnPoint
@onready var planet_container = $PlanetContainer
@onready var front_band = $SlingshotBase/FrontBand
@onready var back_band = $SlingshotBase/BackBand

var band_left_prong = Vector2(920, 750)
var band_right_prong = Vector2(1000, 750)
var idle_center = Vector2(960, 800)
"""
    gd_code = re.sub(r"@onready var spawn_point = \$AsteroidSpawnPoint\n@onready var planet_container = \$PlanetContainer\n", injection, gd_code)

# Add _process logic
if "func _process(" not in gd_code:
    process_func = """
func _process(delta):
	if is_instance_valid(current_asteroid):
		if not current_asteroid.launched:
			front_band.visible = true
			back_band.visible = true
			# La goma persigue al asteroide
			front_band.set_point_position(1, current_asteroid.global_position)
			back_band.set_point_position(1, current_asteroid.global_position)
		else:
			# Si ya se lanzó, esconder bandas temporalmente
			front_band.visible = false
			back_band.visible = false
	else:
		front_band.visible = false
		back_band.visible = false
"""
    gd_code += process_func

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd_code)

print("Slingshot graphics and manager process updated!")
