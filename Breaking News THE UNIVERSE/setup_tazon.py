import os
import shutil
from PIL import Image

downloads = r"C:\Users\start\Downloads"
dest_dir = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_1\tazon"
os.makedirs(dest_dir, exist_ok=True)

files = {
    "tazon vacio.png": "tazon_vacio.png",
    "tazon 1_4.png": "tazon_1_4.png",
    "tazon medio.png": "tazon_medio.png",
    "tazon lleno.png": "tazon_lleno.png"
}

for src_name, dest_name in files.items():
    src_path = os.path.join(downloads, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        with Image.open(dest_path) as img:
            print(f"{dest_name}: {img.size}")
    else:
        print(f"Missing: {src_path}")
