from PIL import Image
import os

folder = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_2"
images = ["planeta 2 completo.png", "Planeta 2 destruido.png"]

for img_name in images:
    path = os.path.join(folder, img_name)
    if not os.path.exists(path):
        continue
    
    img = Image.open(path).convert("RGBA")
    
    # Use get_flattened_data to avoid deprecation warning
    # Pillow 14 deprecates getdata(). Let's just use getdata() for now but suppress warning, or just iterate over x,y
    width, height = img.size
    
    bg_color = img.getpixel((0, 0))
    tolerance = 80
    
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if abs(r - bg_color[0]) < tolerance and abs(g - bg_color[1]) < tolerance and abs(b - bg_color[2]) < tolerance:
                dist = max(abs(r - bg_color[0]), abs(g - bg_color[1]), abs(b - bg_color[2]))
                if dist < tolerance - 20:
                    pixels[x, y] = (r, g, b, 0)
                else:
                    alpha = int(((dist - (tolerance - 20)) / 20.0) * 255)
                    pixels[x, y] = (r, g, b, alpha)

    img.save(path, "PNG")
    print(f"Removed green background from {img_name}")
