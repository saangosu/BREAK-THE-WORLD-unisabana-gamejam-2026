import os
import shutil

src = r"C:\Users\start\Downloads\Palo de golf.png"
dst_dir = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_6"

os.makedirs(dst_dir, exist_ok=True)
dst = os.path.join(dst_dir, "palo_de_golf.png")
shutil.copy(src, dst)

# Read image to get dimensions
from PIL import Image
img = Image.open(dst)
w, h = img.size

print(f"Image imported: {w}x{h}")

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_6\minigame_6.tscn"
with open(tscn_path, "r", encoding="utf-8") as f:
    tscn = f.read()

# Add ExtResource for the club
lines = tscn.split('\n')
insert_idx = 0
for i, line in enumerate(lines):
    if line.startswith("[ext_resource") and "agujero negro.png" in line:
        insert_idx = i + 1
        break

ext_resource = f'[ext_resource type="Texture2D" path="res://assets/sprites/minigame_6/palo_de_golf.png" id="4_club"]'
lines.insert(insert_idx, ext_resource)

tscn = '\n'.join(lines)

old_club = """[node name="GolfClub" type="ColorRect" parent="Planet"]
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
color = Color(0.5, 0.5, 0.5, 1)"""

# The club handle should be the pivot.
# We'll guess the handle is at the top. Top is `y = -h/2` from center.
# So we need to shift the sprite down by `h/2`.
# Also the Club image might need scaling. We will add a scale so it fits the scene.
# The previous club was 1500 pixels tall (from -1200 to 300).
# So scale = 1500 / h
scale = 1500.0 / h

new_club = f"""[node name="GolfClub" type="Sprite2D" parent="Planet"]
position = Vector2(650, 300)
scale = Vector2({scale:.3f}, {scale:.3f})
texture = ExtResource("4_club")
offset = Vector2(0, {h/2.0:.1f})"""

tscn = tscn.replace(old_club, new_club)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn)

print("Scene updated with GolfClub sprite.")
