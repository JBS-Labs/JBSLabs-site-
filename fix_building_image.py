#!/usr/bin/env python3
"""Remove black background from building.png and resize to 80%."""
import sys
import os

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image

# Path to building.png (nested: MIND MENDR GITHUB PAGE_files/Images/building.png)
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, "MIND MENDR GITHUB PAGE_files", "Images")
img_path = os.path.join(images_dir, "building.png")

if not os.path.isfile(img_path):
    print(f"Image not found: {img_path}", file=sys.stderr)
    sys.exit(1)

img = Image.open(img_path).convert("RGBA")
w, h = img.size
data = img.getdata()

# Replace near-black pixels with transparent. Threshold: pixels with R,G,B all <= 40 become transparent.
new_data = []
for item in data:
    r, g, b, a = item
    if r <= 40 and g <= 40 and b <= 40:
        new_data.append((255, 255, 255, 0))  # transparent
    else:
        new_data.append(item)

img.putdata(new_data)

# Resize to 80%
new_w = int(w * 0.8)
new_h = int(h * 0.8)
img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

img.save(img_path, "PNG")
print("Done: black removed and image resized to 80%.")
