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
points = PackedVector2Array(1000, 900, 960, 950)
width = 8.0
default_color = Color(0.6, 0.1, 0.1, 1)

[node name="Wood" type="Polygon2D" parent="SlingshotBase"]
color = Color(0.45, 0.25, 0.1, 1)
polygon = PackedVector2Array(950, 1100, 970, 1100, 965, 970, 1005, 890, 990, 885, 955, 955, 920, 885, 905, 890, 950, 970)

[node name="FrontBand" type="Line2D" parent="SlingshotBase"]
z_index = 2
points = PackedVector2Array(920, 900, 960, 950)
width = 8.0
default_color = Color(0.8, 0.2, 0.2, 1)

[node name="AsteroidSpawnPoint" type="Marker2D" parent="."]
position = Vector2(960, 950)

[node name="PlanetContainer" type="Node2D" parent="."]
"""
with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn_content)


# Update GD script
with open(gd_path, "r", encoding="utf-8") as f:
    gd_code = f.read()

gd_code = gd_code.replace("spawn_point.position = Vector2(960, 800)", "spawn_point.position = Vector2(960, 950)")
gd_code = gd_code.replace("var idle_center = Vector2(960, 800)", "var idle_center = Vector2(960, 950)")

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd_code)

print("Moved slingshot and fixed back band visibility")
