import os
from PIL import Image

dest_dir = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_1\tazon"

files = [
    "tazon_vacio.png",
    "tazon_1_4.png",
    "tazon_medio.png",
    "tazon_lleno.png"
]

chroma_color = (212, 10, 247)
tolerance = 60

for file in files:
    path = os.path.join(dest_dir, file)
    if os.path.exists(path):
        img = Image.open(path).convert("RGBA")
        data = img.getdata()
        
        new_data = []
        for item in data:
            # Check if color is close to chroma color
            if (abs(item[0] - chroma_color[0]) < tolerance and
                abs(item[1] - chroma_color[1]) < tolerance and
                abs(item[2] - chroma_color[2]) < tolerance):
                # Replace with transparent
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        img.save(path, "PNG")
        print(f"Processed chroma key for {file}")
    else:
        print(f"Missing {file}")
