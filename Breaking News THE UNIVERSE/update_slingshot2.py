import re

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
points = PackedVector2Array(1060, 780, 960, 850)
width = 8.0
default_color = Color(0.1, 0.7, 0.9, 1)

[node name="MetalBase" type="Polygon2D" parent="SlingshotBase"]
color = Color(0.75, 0.8, 0.9, 1)
polygon = PackedVector2Array(940, 1080, 980, 1080, 970, 900, 1080, 790, 1060, 780, 960, 870, 860, 780, 840, 790, 950, 900)

[node name="MetalAccents" type="Polygon2D" parent="SlingshotBase"]
color = Color(0.4, 0.45, 0.55, 1)
polygon = PackedVector2Array(950, 1080, 970, 1080, 965, 910, 1060, 810, 1050, 800, 960, 880, 870, 800, 860, 810, 955, 910)

[node name="FrontBand" type="Line2D" parent="SlingshotBase"]
z_index = 2
points = PackedVector2Array(860, 780, 960, 850)
width = 8.0
default_color = Color(0.2, 0.9, 1.0, 1)

[node name="AsteroidSpawnPoint" type="Marker2D" parent="."]
position = Vector2(960, 850)

[node name="PlanetContainer" type="Node2D" parent="."]
"""
with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn_content)

# Update GD script
with open(gd_path, "r", encoding="utf-8") as f:
    gd_code = f.read()

# Update positions
gd_code = gd_code.replace("Vector2(960, 950)", "Vector2(960, 850)")
gd_code = gd_code.replace("Vector2(920, 750)", "Vector2(860, 780)")
gd_code = gd_code.replace("Vector2(1000, 750)", "Vector2(1060, 780)")

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd_code)

print("Updated to space aesthetic, wider and higher")
