from PIL import Image
import os

folder = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_2"

# 1. Process Agujero Negro (Remove Green Background)
bh_path = os.path.join(folder, "agujero negro.png")
if os.path.exists(bh_path):
    img = Image.open(bh_path).convert("RGBA")
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
    img.save(bh_path, "PNG")
    print("Processed agujero negro.png")

# 2. Process Asteroide (Remove Green Background and Fire Outline)
ast_path = os.path.join(folder, "Asteroide.png")
if os.path.exists(ast_path):
    img = Image.open(ast_path).convert("RGBA")
    width, height = img.size
    bg_color = img.getpixel((0, 0))
    
    # Check if bg is actually green
    is_green_bg = (bg_color[1] > bg_color[0] + 30) and (bg_color[1] > bg_color[2] + 30)
    
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Remove green bg
            if is_green_bg and a > 0:
                if abs(r - bg_color[0]) < 80 and abs(g - bg_color[1]) < 80 and abs(b - bg_color[2]) < 80:
                    pixels[x, y] = (r, g, b, 0)
                    continue
                    
            # Remove fire outline (bright red/orange/yellow)
            if a > 0:
                # Fire is typically very high Red, high/med Green, low Blue
                if r > 180 and g > 80 and b < 100 and r > b + 50:
                    # Fade it out based on how "fiery" it is to make a soft edge
                    pixels[x, y] = (r, g, b, 0)

    img.save(ast_path, "PNG")
    print("Processed Asteroide.png")
