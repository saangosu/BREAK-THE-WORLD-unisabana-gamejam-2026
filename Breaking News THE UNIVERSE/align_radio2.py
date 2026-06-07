import re

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_4\minigame_4.tscn"

with open(tscn_path, "r", encoding="utf-8") as f:
    content = f.read()

# Scale and move radio to 2.5
radio_node = """[node name="RadioConsole" type="Sprite2D" parent="."]
position = Vector2(960, 780)
scale = Vector2(2.5, 2.5)
texture = ExtResource("radio_tex")"""
content = re.sub(r'\[node name="RadioConsole".*?texture = ExtResource\("radio_tex"\)', radio_node, content, flags=re.DOTALL)

# Move waves to fit the screen
content = re.sub(r'\[node name="TargetWave" type="Line2D" parent="\." unique_id=1896961605\]\nposition = Vector2\(\d+, \d+\)', 
                 '[node name="TargetWave" type="Line2D" parent="." unique_id=1896961605]\nposition = Vector2(960, 680)', content)
content = re.sub(r'\[node name="PlayerWave" type="Line2D" parent="\." unique_id=813977682\]\nposition = Vector2\(\d+, \d+\)', 
                 '[node name="PlayerWave" type="Line2D" parent="." unique_id=813977682]\nposition = Vector2(960, 680)', content)

# Adjust knobs for scale 2.5
# Previously at scale 1.5, knobs were at roughly 680 and 1120. Center is 960.
# Delta was 280 and 160.
# At scale 2.5, they will be 2.5/1.5 = 1.66 times further from the center of the radio.
# Or just guess: Center is 960. Radio width is larger. Let's put them at 600 and 1320.
content = re.sub(r'\[node name="KnobFreq" type="Control" parent="\." unique_id=1409786609\].*?scale = Vector2\(\d+\.\d+, \d+\.\d+\)',
                 '[node name="KnobFreq" type="Control" parent="." unique_id=1409786609]\ncustom_minimum_size = Vector2(200, 200)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = 600.0\noffset_top = 840.0\noffset_right = 800.0\noffset_bottom = 1040.0\nscale = Vector2(0.8, 0.8)', content, flags=re.DOTALL)

content = re.sub(r'\[node name="KnobAmp" type="Control" parent="\." unique_id=143609267\].*?scale = Vector2\(\d+\.\d+, \d+\.\d+\)',
                 '[node name="KnobAmp" type="Control" parent="." unique_id=143609267]\ncustom_minimum_size = Vector2(200, 200)\nlayout_mode = 3\nanchors_preset = 0\noffset_left = 1140.0\noffset_top = 840.0\noffset_right = 1340.0\noffset_bottom = 1040.0\nscale = Vector2(0.8, 0.8)', content, flags=re.DOTALL)

# Modify OKButton
content = re.sub(r'\[node name="OKButton" type="Button" parent="\." unique_id=144942119\].*?flat = true',
                 '[node name="OKButton" type="Button" parent="." unique_id=144942119]\nmodulate = Color(1, 1, 1, 0)\noffset_left = 890.0\noffset_top = 860.0\noffset_right = 1030.0\noffset_bottom = 920.0\nflat = true', content, flags=re.DOTALL)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated positions again")
