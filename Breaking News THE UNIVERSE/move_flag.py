import re

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_6\minigame_6.tscn"
with open(tscn_path, "r", encoding="utf-8") as f:
    tscn = f.read()

# The old pole and flag:
old_flag_str = """[node name="Pole" type="ColorRect" parent="BlackHole"]
offset_left = -80.0
offset_top = -250.0
offset_right = -60.0
offset_bottom = 0.0
color = Color(0.8, 0.8, 0.8, 1)

[node name="Flag" type="Polygon2D" parent="BlackHole/Pole"]
color = Color(1, 0, 0, 1)
polygon = PackedVector2Array(20, 0, 130, 20, 20, 60)"""

new_flag_str = """[node name="FlagGroup" type="Node2D" parent="BlackHole"]
position = Vector2(400, 150)
rotation = 2.35619

[node name="Pole" type="ColorRect" parent="BlackHole/FlagGroup"]
offset_left = -4.0
offset_top = -200.0
offset_right = 4.0
offset_bottom = 0.0
color = Color(0.9, 0.9, 0.9, 1)

[node name="Flag" type="Polygon2D" parent="BlackHole/FlagGroup"]
color = Color(1, 0, 0, 1)
polygon = PackedVector2Array(-4, -200, -120, -170, -4, -130)"""

if old_flag_str in tscn:
    tscn = tscn.replace(old_flag_str, new_flag_str)
    with open(tscn_path, "w", encoding="utf-8") as f:
        f.write(tscn)
    print("Flag moved successfully!")
else:
    print("Could not find the old flag string.")
