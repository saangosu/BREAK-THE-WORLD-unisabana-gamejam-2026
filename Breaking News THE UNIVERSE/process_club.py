from PIL import Image
import math
import os

img_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_6\palo_de_golf_cropped.png"
out_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_6\palo_de_golf_vertical.png"
img = Image.open(img_path)

# If it's 1173x333, it's horizontal. Rotate it to be vertical.
# Let's assume handle is on the left, head on the right.
# Rotating -90 puts handle at the top, head at the bottom.
# If handle was on the right, it will be upside down. We can rotate 90.
# Let's rotate -90 for now.
img_vertical = img.rotate(-90, expand=True)
img_vertical.save(out_path)

w, h = img_vertical.size
print(f"Vertical image size: {w}x{h}")

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_6\minigame_6.tscn"
with open(tscn_path, "r", encoding="utf-8") as f:
    tscn = f.read()

import re

# Update Texture to use vertical
tscn = tscn.replace('path="res://assets/sprites/minigame_6/palo_de_golf.png"', 'path="res://assets/sprites/minigame_6/palo_de_golf_vertical.png"')

# The new h is 1173. The offset should be Vector2(0, h/2) so the top is at the pivot.
# We also probably need to increase the scale since it was scaled based on 1620, but the club itself is 1173.
# The original club placeholder was 1500 pixels tall.
scale = 1500.0 / h

# Find the scale and offset and update them
def replace_offset(match):
    return f'offset = Vector2(0, {h/2.0:.1f})'

tscn = re.sub(r'offset = Vector2\([0-9.-]+, [0-9.-]+\)', replace_offset, tscn)

def replace_scale(match):
    return f'scale = Vector2({scale:.3f}, {scale:.3f})'

tscn = re.sub(r'scale = Vector2\([0-9.-]+, [0-9.-]+\)\ntexture = ExtResource\("4_club"\)', 
              lambda m: replace_scale(m) + '\ntexture = ExtResource("4_club")', tscn)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(tscn)

print("Scene updated with vertical club image.")
