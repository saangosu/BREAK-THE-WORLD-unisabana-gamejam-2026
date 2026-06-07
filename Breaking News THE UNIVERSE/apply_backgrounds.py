import os
import shutil
import re

src_dir = r"C:\Users\start\Downloads"
dest_dir = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\backgrounds"
os.makedirs(dest_dir, exist_ok=True)

for i in range(1, 7):
    src = os.path.join(src_dir, f"Fondo {i}.png")
    dst = os.path.join(dest_dir, f"fondo_{i}.png")
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied Fondo {i}.png")
    else:
        print(f"Not found: {src}")

scenes = [
    (r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\eggs\eggs.tscn", 1),
    (r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_2\minigame_2.tscn", 2),
    (r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\Minijuego3.tscn", 3),
    (r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_4\minigame_4.tscn", 4),
    (r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_5\minigame_5.tscn", 5),
    (r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_6\minigame_6.tscn", 6),
]

for tscn_path, bg_idx in scenes:
    if not os.path.exists(tscn_path):
        print(f"Scene not found: {tscn_path}")
        continue
        
    with open(tscn_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Inject ExtResource if not present
    res_path = f"res://assets/backgrounds/fondo_{bg_idx}.png"
    if res_path not in content:
        # Find the last ext_resource
        ext_res_matches = list(re.finditer(r'\[ext_resource.*?\]', content))
        if ext_res_matches:
            last_ext = ext_res_matches[-1]
            # Use id "bg_texture"
            new_ext = f'\n[ext_resource type="Texture2D" path="{res_path}" id="bg_texture"]\n'
            content = content[:last_ext.end()] + new_ext + content[last_ext.end():]
        else:
            # no ext_resource found, add after gd_scene
            new_ext = f'\n[ext_resource type="Texture2D" path="{res_path}" id="bg_texture"]\n'
            content = content.replace("[gd_scene", "[gd_scene" + new_ext)
            
    # 2. Replace the Background node
    # It might be ColorRect or TextureRect already.
    # Let's find the Background block
    bg_pattern = r'\[node name="Background"[^\]]*\].*?(?=\n\[node)'
    bg_replacement = f"""[node name="Background" type="TextureRect" parent="."]
z_index = -10
offset_right = 1920.0
offset_bottom = 1080.0
mouse_filter = 2
texture = ExtResource("bg_texture")
expand_mode = 1
stretch_mode = 6
modulate = Color(0.5, 0.5, 0.5, 1)
"""
    
    new_content = re.sub(bg_pattern, bg_replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        # If it couldn't find the pattern (maybe no background node?)
        print(f"Warning: Could not replace Background node in {tscn_path}")
    else:
        with open(tscn_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {tscn_path} with fondo_{bg_idx}.png")
