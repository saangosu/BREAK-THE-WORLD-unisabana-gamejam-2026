from PIL import Image
import os

folder = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_4"
images = ["IMG_1508.png", "IMG_1509.png", "IMG_1510.png"]

for img_name in images:
    path = os.path.join(folder, img_name)
    if not os.path.exists(path):
        continue
    
    img = Image.open(path).convert("RGBA")
    datas = img.getdata()
    
    # Let's take the pixel at (0,0) as the background color
    bg_color = img.getpixel((0, 0))
    
    # We'll use a tolerance to catch variations in the green
    tolerance = 80
    new_data = []
    
    for item in datas:
        r, g, b, a = item
        # If the pixel is close to the background green
        if abs(r - bg_color[0]) < tolerance and abs(g - bg_color[1]) < tolerance and abs(b - bg_color[2]) < tolerance:
            # Calculate a smooth alpha for antialiasing
            dist = max(abs(r - bg_color[0]), abs(g - bg_color[1]), abs(b - bg_color[2]))
            if dist < tolerance - 20:
                new_data.append((r, g, b, 0)) # fully transparent
            else:
                # Semi transparent edge
                alpha = int(((dist - (tolerance - 20)) / 20.0) * 255)
                new_data.append((r, g, b, alpha))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(path, "PNG")
    print(f"Removed green background from {img_name}")
