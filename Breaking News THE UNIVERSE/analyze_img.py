from PIL import Image

img_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\assets\sprites\minigame_6\palo_de_golf.png"
img = Image.open(img_path)

# Find bounding box of non-transparent pixels
bbox = img.getbbox()
print(f"Original size: {img.size}")
print(f"Bounding box (left, upper, right, lower): {bbox}")

if bbox:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    print(f"Content size: {w}x{h}")
    # Crop to content and save to see if that helps
    cropped = img.crop(bbox)
    cropped.save(img_path.replace(".png", "_cropped.png"))
    print("Cropped image saved as palo_de_golf_cropped.png")
else:
    print("Image is entirely transparent!")
