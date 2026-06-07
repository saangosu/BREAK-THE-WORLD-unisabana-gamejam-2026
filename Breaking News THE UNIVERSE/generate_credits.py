import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Text to render
credits_text = """
Programación:

Salem de los Andes González Suárez
Programador senior

Andrés Felipe Rojas Díaz
Programador junior 1

Daniel Suarez Peña
Programador junior 2


Arte:

Carolina Torres Daza
Dirección de arte

Gabriela Vergara Mariño
Asistencia de arte 1

Andrés Felipe Rojas Díaz
Asistente de arte 2


Sonido:

Gabriela Vergara Mariño
Dirección de sonido

Salem de los Andes González Suárez
Asistencia de sonido 1


Agradecimientos:

Hugo Orlando Ureña Naranjo
Universidad de La Sabana
Electronic Arts COL
"""

# Load background
bg_path = r"C:\Users\start\.gemini\antigravity\brain\dea9bbd6-8738-4eab-8e76-1837f56878a3\clean_background_1780851789650.png"
bg_img = Image.open(bg_path).convert("RGB")

# Resize/Crop to 1920x1080
target_w, target_h = 1920, 1080
bg_aspect = bg_img.width / bg_img.height
target_aspect = target_w / target_h

if bg_aspect > target_aspect:
    # bg is wider, scale by height
    new_h = target_h
    new_w = int(bg_aspect * new_h)
    bg_img = bg_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    # crop width
    left = (new_w - target_w) // 2
    bg_img = bg_img.crop((left, 0, left + target_w, target_h))
else:
    # bg is taller, scale by width
    new_w = target_w
    new_h = int(new_w / bg_aspect)
    bg_img = bg_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    # crop height
    top = (new_h - target_h) // 2
    bg_img = bg_img.crop((0, top, target_w, top + target_h))

# Dim background so text is readable
dimmer = Image.new('RGB', (target_w, target_h), (0, 0, 0))
bg_img = Image.blend(bg_img, dimmer, 0.5)

# Try to load a font
try:
    font_title = ImageFont.truetype("arialbd.ttf", 60)
    font_text = ImageFont.truetype("arial.ttf", 40)
except:
    font_title = ImageFont.load_default()
    font_text = ImageFont.load_default()

# Video configuration
fps = 60
duration = 20 # seconds
total_frames = fps * duration

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('creditos.mp4', fourcc, fps, (target_w, target_h))

# Pre-calculate text block height
dummy_draw = ImageDraw.Draw(Image.new('RGB', (10, 10)))
lines = credits_text.strip().split('\n')

text_h = 0
line_heights = []
for line in lines:
    if line.strip() in ["Programación:", "Arte:", "Sonido:", "Agradecimientos:"]:
        bbox = dummy_draw.textbbox((0, 0), line, font=font_title)
        h = bbox[3] - bbox[1] + 30
    else:
        bbox = dummy_draw.textbbox((0, 0), line, font=font_text)
        h = bbox[3] - bbox[1] + 20
    if line.strip() == "":
        h = 40 # empty line height
    line_heights.append(h)
    text_h += h

# Render frames
start_y = target_h
end_y = -text_h

print("Rendering video frames...")
for frame_idx in range(total_frames):
    progress = frame_idx / float(total_frames - 1)
    current_y = start_y + (end_y - start_y) * progress
    
    # Create a copy of the background
    frame_img = bg_img.copy()
    draw = ImageDraw.Draw(frame_img)
    
    y = current_y
    for i, line in enumerate(lines):
        if y > target_h or y + line_heights[i] < 0:
            y += line_heights[i]
            continue
            
        is_title = line.strip() in ["Programación:", "Arte:", "Sonido:", "Agradecimientos:"]
        font = font_title if is_title else font_text
        color = (255, 255, 255) if is_title else (200, 200, 200)
        
        # Draw text centered horizontally
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (target_w - w) // 2
        
        # Shadow
        draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0))
        # Text
        draw.text((x, y), line, font=font, fill=color)
        
        y += line_heights[i]
        
    # Convert RGB PIL image to BGR OpenCV format
    frame_cv = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGB2BGR)
    out.write(frame_cv)
    
    if frame_idx % 100 == 0:
        print(f"Frame {frame_idx}/{total_frames}...")

out.release()
print("Video generated: creditos.mp4")
