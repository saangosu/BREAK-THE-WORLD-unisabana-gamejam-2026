from PIL import Image
import os

path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\textures\art\Luna.png"

if os.path.exists(path):
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    
    # We assume pixel (0,0) is the background color
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
    print("Removed background from Luna.png")
else:
    print("Luna.png not found at", path)
