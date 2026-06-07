import re

tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\eggs\eggs.tscn"

with open(tscn_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the texture path for 2_poa2p
content = re.sub(
    r'\[ext_resource type="Texture2D".*?path="res://textures/placeholders/half circle filled\.png" id="2_poa2p"\]',
    '[ext_resource type="Texture2D" path="res://assets/sprites/minigame_1/tazon/tazon_vacio.png" id="2_poa2p"]',
    content
)

# Replace Bowl node
old_bowl = """[node name="Bowl" type="Sprite2D" parent="." unique_id=229170384]
modulate = Color(0.42872298, 0.3166794, 0, 1)
position = Vector2(960.00006, 715.00006)
rotation = -0.7853982
scale = Vector2(6, 6)
texture = ExtResource("2_poa2p")"""

new_bowl = """[node name="Bowl" type="Sprite2D" parent="." unique_id=229170384]
position = Vector2(960, 715)
scale = Vector2(1.5, 1.5)
texture = ExtResource("2_poa2p")"""

content = content.replace(old_bowl, new_bowl)

# Fix children rotation and scale
# For the first CollisionShape2D
old_col1 = """[node name="CollisionShape2D" type="CollisionShape2D" parent="Bowl/Collider" unique_id=246550476]
position = Vector2(0.35355377, -0.58927155)
rotation = 2.3561945
shape = SubResource("CapsuleShape2D_437cf")"""

new_col1 = """[node name="CollisionShape2D" type="CollisionShape2D" parent="Bowl/Collider" unique_id=246550476]
rotation = 1.5708
scale = Vector2(4, 4)
shape = SubResource("CapsuleShape2D_437cf")"""

content = content.replace(old_col1, new_col1)

# For the second CollisionShape2D
old_col2 = """[node name="CollisionShape2D2" type="CollisionShape2D" parent="Bowl/Hitbox" unique_id=780539353]
position = Vector2(0.35355377, -0.5892792)
rotation = 2.3561945
scale = Vector2(0.9999999, 0.9999999)
shape = SubResource("CapsuleShape2D_187s8")"""

new_col2 = """[node name="CollisionShape2D2" type="CollisionShape2D" parent="Bowl/Hitbox" unique_id=780539353]
rotation = 1.5708
scale = Vector2(4, 4)
shape = SubResource("CapsuleShape2D_187s8")"""

content = content.replace(old_col2, new_col2)

with open(tscn_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Bowl in eggs.tscn")
