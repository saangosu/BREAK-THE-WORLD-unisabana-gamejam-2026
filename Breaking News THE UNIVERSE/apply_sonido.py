import os
import shutil

src = r"C:\Users\start\Downloads\sonido-removebg-preview.png"
dst = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_4\sonido.png"
tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_4\minigame_4.tscn"

# Ensure target directory exists
os.makedirs(os.path.dirname(dst), exist_ok=True)

if os.path.exists(src):
    shutil.copy2(src, dst)
    print(f"Copied {src} to {dst}")
    
    with open(tscn_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    content = content.replace("res://assets/sprites/minigame_4/IMG_1508.png", "res://assets/sprites/minigame_4/sonido.png")
    
    with open(tscn_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Updated minigame_4.tscn to use sonido.png")
else:
    print(f"Could not find {src}")
