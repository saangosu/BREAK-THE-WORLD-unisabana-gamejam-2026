import os
from PIL import Image

dest_dir = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_1\tazon"

files = [
    "tazon_vacio.png",
    "tazon_1_4.png",
    "tazon_medio.png",
    "tazon_lleno.png"
]

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
ANCHOR_X = 250
ANCHOR_Y = 450

for file in files:
    path = os.path.join(dest_dir, file)
    if os.path.exists(path):
        img = Image.open(path).convert("RGBA")
        
        # Get bounding box of non-transparent pixels
        # getbbox() works on the alpha channel if we split it
        alpha = img.split()[3]
        bbox = alpha.getbbox()
        
        if bbox:
            # Crop to exactly the non-transparent area
            cropped = img.crop(bbox)
            
            # The bottom center of the cropped image
            crop_w = cropped.width
            crop_h = cropped.height
            
            # We want the bottom center of 'cropped' to be at (ANCHOR_X, ANCHOR_Y)
            paste_x = ANCHOR_X - (crop_w // 2)
            paste_y = ANCHOR_Y - crop_h
            
            # Create new canvas
            canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0,0,0,0))
            canvas.paste(cropped, (paste_x, paste_y))
            
            canvas.save(path, "PNG")
            print(f"Aligned and saved {file}")
        else:
            print(f"{file} is completely transparent?")
    else:
        print(f"Missing {file}")
