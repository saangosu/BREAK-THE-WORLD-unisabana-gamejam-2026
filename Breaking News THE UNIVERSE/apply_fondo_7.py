import os
import shutil

src = r"C:\Users\start\Downloads\Fondo 7.png"
dst = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\backgrounds\fondo_7.png"
tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\minigame_5\minigame_5.tscn"

# Wait, the file might be named 'Fondo 7.png' or 'fondo 7.png' or 'fondo 7.jpg'. Let's search for it.
found_src = None
for f in os.listdir(r"C:\Users\start\Downloads"):
    if f.lower().startswith("fondo 7"):
        found_src = os.path.join(r"C:\Users\start\Downloads", f)
        break

if found_src:
    shutil.copy2(found_src, dst)
    print(f"Copied {found_src} to {dst}")
    
    with open(tscn_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    content = content.replace("res://assets/backgrounds/fondo_6.png", "res://assets/backgrounds/fondo_7.png")
    
    with open(tscn_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Updated minigame_5.tscn to use fondo_7.png")
else:
    print("Could not find Fondo 7 in Downloads folder.")
