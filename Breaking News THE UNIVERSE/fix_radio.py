import re

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_4\minigame_4.tscn"

with open(tscn_path, "r", encoding="utf-8") as f:
    content = f.read()

# Restore planet resource and add radio resource
# Currently line 5 is: [ext_resource type="Texture2D" path="res://assets/sprites/minigame_4/sonido.png" id="3_tex"]
content = content.replace(
    '[ext_resource type="Texture2D" path="res://assets/sprites/minigame_4/sonido.png" id="3_tex"]',
    '[ext_resource type="Texture2D" path="res://assets/sprites/minigame_4/IMG_1508.png" id="3_tex"]\n[ext_resource type="Texture2D" path="res://assets/sprites/minigame_4/sonido.png" id="radio_tex"]'
)

# Add RadioConsole node
radio_node = """
[node name="RadioConsole" type="Sprite2D" parent="."]
position = Vector2(960, 700)
texture = ExtResource("radio_tex")
"""

content = content.replace('[node name="TargetWave" type="Line2D" parent="."]', radio_node + '\n[node name="TargetWave" type="Line2D" parent="."]')

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Restored planet and added radio console")
