import re

# 1. Update minigame_6.tscn
tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_6\minigame_6.tscn"
with open(tscn_path, "r", encoding="utf-8") as f:
    tscn = f.read()

# Find GolfClub and replace its position
# Currently it's:
# [node name="GolfClub" type="Sprite2D" parent="Planet"]
# position = Vector2(650, 300)
# scale = ...
# texture = ExtResource("4_club")
# offset = Vector2(0, 586.5)

# We want: position = Vector2(-1060, -1060), rotation = -0.785398
def replace_position(match):
    return 'position = Vector2(-1060, -1060)\nrotation = -0.785398'

tscn = re.sub(r'position = Vector2\([0-9.-]+, [0-9.-]+\)', replace_position, tscn, count=1)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn)


# 2. Update minigame_6.gd swing animation
gd_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\minigame_6\minigame_6.gd"
with open(gd_path, "r", encoding="utf-8") as f:
    gd = f.read()

# Replace swing logic
old_back = 'var back_rotation = lerp(20.0, 90.0, stored_power)'
new_back = 'var back_rotation = lerp(-60.0, -130.0, stored_power)'

old_follow = 'var follow_through = lerp(-10.0, -60.0, stored_power)'
new_follow = 'var follow_through = lerp(0.0, 45.0, stored_power)'

gd = gd.replace(old_back, new_back)
gd = gd.replace(old_follow, new_follow)

# Also fix the timeout swing
old_timeout_1 = 'tween.tween_property(golf_club, "rotation_degrees", 20.0, 0.1)'
new_timeout_1 = 'tween.tween_property(golf_club, "rotation_degrees", -60.0, 0.1)'
old_timeout_2 = 'tween.tween_property(golf_club, "rotation_degrees", 0.0, 0.2)'
new_timeout_2 = 'tween.tween_property(golf_club, "rotation_degrees", -45.0, 0.2)'

gd = gd.replace(old_timeout_1, new_timeout_1)
gd = gd.replace(old_timeout_2, new_timeout_2)

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd)

print("Club repositioned and animations updated.")
