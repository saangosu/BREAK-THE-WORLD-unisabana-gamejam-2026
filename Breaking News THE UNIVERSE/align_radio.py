import re
from PIL import Image

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_4\minigame_4.tscn"
img_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_4\sonido.png"

# We don't know the exact knob positions inside the image, but we can guess it based on the screenshot.
# The radio has a big white screen on top, and a control panel below.
# If Radio is at 960, 650 with scale 1.0 (currently).
# Let's scale it to 2.0 to make it bigger, and position it at 960, 700.
# Then we place waves at 960, 600.
# Knobs around 720, 800 and 1200, 800.

with open(tscn_path, "r", encoding="utf-8") as f:
    content = f.read()

# Scale and move radio
radio_node = """[node name="RadioConsole" type="Sprite2D" parent="."]
position = Vector2(960, 750)
scale = Vector2(1.5, 1.5)
texture = ExtResource("radio_tex")"""
content = re.sub(r'\[node name="RadioConsole".*?texture = ExtResource\("radio_tex"\)', radio_node, content, flags=re.DOTALL)

# Move waves to fit the screen
content = re.sub(r'\[node name="TargetWave" type="Line2D" parent="\." unique_id=1896961605\]\nposition = Vector2\(\d+, \d+\)', 
                 '[node name="TargetWave" type="Line2D" parent="." unique_id=1896961605]\nposition = Vector2(960, 620)', content)
content = re.sub(r'\[node name="PlayerWave" type="Line2D" parent="\." unique_id=813977682\]\nposition = Vector2\(\d+, \d+\)', 
                 '[node name="PlayerWave" type="Line2D" parent="." unique_id=813977682]\nposition = Vector2(960, 620)', content)

# Modify the game's knobs so they can be repositioned easily from Editor by the user, but give them a better default
# The current knobs are Controls. We will scale them and move them.
# KnobFreq at 600, 750 -> Let's move to 720, 800 and scale 0.5
content = re.sub(r'\[node name="KnobFreq" type="Control" parent="\." unique_id=1409786609\]\ncustom_minimum_size = Vector2\(200, 200\)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = \d+\.\d+\noffset_top = \d+\.\d+\noffset_right = \d+\.\d+\noffset_bottom = \d+\.\d+',
                 '[node name="KnobFreq" type="Control" parent="." unique_id=1409786609]\ncustom_minimum_size = Vector2(200, 200)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = 680.0\noffset_top = 800.0\noffset_right = 880.0\noffset_bottom = 1000.0\nscale = Vector2(0.6, 0.6)', content)

content = re.sub(r'\[node name="KnobAmp" type="Control" parent="\." unique_id=143609267\]\ncustom_minimum_size = Vector2\(200, 200\)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = \d+\.\d+\noffset_top = \d+\.\d+\noffset_right = \d+\.\d+\noffset_bottom = \d+\.\d+',
                 '[node name="KnobAmp" type="Control" parent="." unique_id=143609267]\ncustom_minimum_size = Vector2(200, 200)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = 1120.0\noffset_top = 800.0\noffset_right = 1320.0\noffset_bottom = 1000.0\nscale = Vector2(0.6, 0.6)', content)

# Modify OKButton to be invisible but over the text
content = re.sub(r'\[node name="OKButton" type="Button" parent="\." unique_id=144942119\]\noffset_left = \d+\.\d+\noffset_top = \d+\.\d+\noffset_right = \d+\.\d+\noffset_bottom = \d+\.\d+\ntheme_override_font_sizes/font_size = \d+\ntext = "OK"',
                 '[node name="OKButton" type="Button" parent="." unique_id=144942119]\nmodulate = Color(1, 1, 1, 0)\noffset_left = 900.0\noffset_top = 820.0\noffset_right = 1020.0\noffset_bottom = 880.0\nflat = true', content)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated positions")
