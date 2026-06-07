import re

eggs_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\eggs\eggs.tscn"
m3_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\Minijuego3.tscn"

# Eggs
with open(eggs_path, "r", encoding="utf-8") as f:
    content = f.read()

res_ext = '\n[ext_resource type="Texture2D" path="res://assets/backgrounds/fondo_1.png" id="bg_tex"]\n'
content = content.replace("[gd_scene", "[gd_scene" + res_ext)

bg_node = """
[node name="Background" type="TextureRect" parent="."]
z_index = -10
offset_right = 1920.0
offset_bottom = 1080.0
mouse_filter = 2
texture = ExtResource("bg_tex")
expand_mode = 1
stretch_mode = 6
modulate = Color(0.5, 0.5, 0.5, 1)
"""
content = content.replace('script = ExtResource("1_8u3g3")', 'script = ExtResource("1_8u3g3")' + bg_node)

with open(eggs_path, "w", encoding="utf-8") as f:
    f.write(content)

# M3
with open(m3_path, "r", encoding="utf-8") as f:
    content = f.read()

res_ext = '\n[ext_resource type="Texture2D" path="res://assets/backgrounds/fondo_3.png" id="bg_tex"]\n'
content = content.replace("[gd_scene", "[gd_scene" + res_ext)

bg_node = """
[node name="Background" type="TextureRect" parent="."]
z_index = -10
offset_right = 1920.0
offset_bottom = 1080.0
mouse_filter = 2
texture = ExtResource("bg_tex")
expand_mode = 1
stretch_mode = 6
modulate = Color(0.5, 0.5, 0.5, 1)
"""
# find script or first node
content = content.replace('script = ExtResource("1_mgr")', 'script = ExtResource("1_mgr")' + bg_node)

with open(m3_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed backgrounds for eggs and minijuego3")
