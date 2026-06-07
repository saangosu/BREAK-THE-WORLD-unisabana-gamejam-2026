import re

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_4\minigame_4.tscn"

with open(tscn_path, "r", encoding="utf-8") as f:
    content = f.read()

# Scale and move radio to 1.9 (calculated to fit the 800px wave width into the white screen portion)
radio_node = """[node name="RadioConsole" type="Sprite2D" parent="."]
position = Vector2(960, 750)
scale = Vector2(1.9, 1.9)
texture = ExtResource("radio_tex")"""
content = re.sub(r'\[node name="RadioConsole".*?texture = ExtResource\("radio_tex"\)', radio_node, content, flags=re.DOTALL)

# Move waves to center of the white screen (approx y=660)
content = re.sub(r'\[node name="TargetWave" type="Line2D" parent="\." unique_id=1896961605\]\nposition = Vector2\(\d+, \d+\)', 
                 '[node name="TargetWave" type="Line2D" parent="." unique_id=1896961605]\nposition = Vector2(960, 660)', content)
content = re.sub(r'\[node name="PlayerWave" type="Line2D" parent="\." unique_id=813977682\]\nposition = Vector2\(\d+, \d+\)', 
                 '[node name="PlayerWave" type="Line2D" parent="." unique_id=813977682]\nposition = Vector2(960, 660)', content)

# Adjust knobs for scale 1.9 and set pivot_offset so scaling keeps them centered.
# Left knob center approx: X=580, Y=840
# Since size is 200x200, offset is X-100, Y-100
content = re.sub(r'\[node name="KnobFreq" type="Control" parent="\." unique_id=1409786609\].*?scale = Vector2\(\d+\.\d+, \d+\.\d+\)',
                 '[node name="KnobFreq" type="Control" parent="." unique_id=1409786609]\ncustom_minimum_size = Vector2(200, 200)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = 480.0\noffset_top = 740.0\noffset_right = 680.0\noffset_bottom = 940.0\npivot_offset = Vector2(100, 100)\nscale = Vector2(0.65, 0.65)', content, flags=re.DOTALL)

# Right knob center approx: X=1340, Y=840
content = re.sub(r'\[node name="KnobAmp" type="Control" parent="\." unique_id=143609267\].*?scale = Vector2\(\d+\.\d+, \d+\.\d+\)',
                 '[node name="KnobAmp" type="Control" parent="." unique_id=143609267]\ncustom_minimum_size = Vector2(200, 200)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = 1240.0\noffset_top = 740.0\noffset_right = 1440.0\noffset_bottom = 940.0\npivot_offset = Vector2(100, 100)\nscale = Vector2(0.65, 0.65)', content, flags=re.DOTALL)

# Modify OKButton
content = re.sub(r'\[node name="OKButton" type="Button" parent="\." unique_id=144942119\].*?flat = true',
                 '[node name="OKButton" type="Button" parent="." unique_id=144942119]\nmodulate = Color(1, 1, 1, 0)\noffset_left = 890.0\noffset_top = 840.0\noffset_right = 1030.0\noffset_bottom = 890.0\nflat = true', content, flags=re.DOTALL)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated positions optimally")
