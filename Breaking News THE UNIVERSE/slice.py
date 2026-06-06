from PIL import Image
import os

path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_2\Planeta 2 destruido.png"
if os.path.exists(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    
    # We will slice into a 3x3 grid for more fragments
    rows, cols = 3, 3
    w_step = w // cols
    h_step = h // rows
    
    count = 0
    for i in range(rows):
        for j in range(cols):
            box = (j * w_step, i * h_step, (j + 1) * w_step, (i + 1) * h_step)
            frag = img.crop(box)
            
            # Check if fragment is completely transparent to avoid useless fragments
            extrema = frag.getextrema()
            if extrema[3][1] > 0: # Max alpha > 0
                out_path = path.replace(".png", f"_frag_{count}.png")
                frag.save(out_path)
                count += 1
                
    print(f"Generated {count} fragments")
else:
    print("Image not found")
