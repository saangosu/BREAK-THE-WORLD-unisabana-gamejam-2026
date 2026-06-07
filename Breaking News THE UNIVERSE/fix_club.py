from PIL import Image
import math
import os

img_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_6\palo_de_golf.png"
img = Image.open(img_path).convert("RGBA")

data = img.getdata()
new_data = []

# Detect chroma green. Usually something like R<100, G>150, B<100.
# We will use a color distance approach. Typical chroma green is roughly (0, 255, 0).
# Let's say if green is the dominant color and difference between G and max(R, B) is large.
for item in data:
    r, g, b, a = item
    if g > 150 and g > r * 1.5 and g > b * 1.5:
        new_data.append((255, 255, 255, 0))
    else:
        # Check if it's very close to pure green
        if r < 80 and g > 150 and b < 80:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

img.putdata(new_data)
img.save(img_path)
print("Chroma key removed.")

# Now update the scale in tscn
tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_6\minigame_6.tscn"
with open(tscn_path, "r", encoding="utf-8") as f:
    tscn = f.read()

import re
# We look for:
# [node name="GolfClub" type="Sprite2D" parent="Planet"]
# position = ...
# scale = Vector2(0.694, 0.694)
def replace_scale(match):
    # match.group(1) is the x scale, match.group(2) is the y scale
    sx = float(match.group(1)) * 2.5 # Make it 2.5x larger
    sy = float(match.group(2)) * 2.5
    return f'scale = Vector2({sx:.3f}, {sy:.3f})'

tscn = re.sub(r'scale = Vector2\(([0-9.]+), ([0-9.]+)\)\ntexture = ExtResource\("4_club"\)', 
              lambda m: replace_scale(m) + '\ntexture = ExtResource("4_club")', tscn)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn)

print("Scene updated with larger scale.")
