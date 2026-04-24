#!/usr/bin/env python3
"""Remove only the outer black rectangle from MM-logo.png; keep black inside the logo."""
import sys
import os

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image

def is_black(pixel, threshold=40):
    r, g, b = pixel[0], pixel[1], pixel[2]
    return r <= threshold and g <= threshold and b <= threshold

def is_dark(pixel, threshold=85):
    """Dark background (black or dark purple) for shrinking the 'black square'."""
    r, g, b = pixel[0], pixel[1], pixel[2]
    return r <= threshold and g <= threshold and b <= threshold

script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, "MIND MENDR GITHUB PAGE_files", "Images")
img_path = os.path.join(images_dir, "MM-logo.png")

if not os.path.isfile(img_path):
    print(f"Image not found: {img_path}", file=sys.stderr)
    sys.exit(1)

img = Image.open(img_path).convert("RGBA")
w, h = img.size
pixels = img.load()

# Find bounding box of non-black, non-transparent content (the actual logo)
left, right = w, 0
top, bottom = h, 0
for y in range(h):
    for x in range(w):
        p = pixels[x, y]
        if p[3] > 128 and not is_black(p):
            left = min(left, x)
            right = max(right, x)
            top = min(top, y)
            bottom = max(bottom, y)

# Add a small margin so we don't clip the logo edge
margin = 2
left = max(0, left - margin)
right = min(w - 1, right + margin)
top = max(0, top - margin)
bottom = min(h - 1, bottom + margin)

# Only make transparent: pixels that are black AND outside the logo bounds
for y in range(h):
    for x in range(w):
        if is_black(pixels[x, y]) and (x < left or x > right or y < top or y > bottom):
            pixels[x, y] = (255, 255, 255, 0)

# Shrink the black square by 20%: keep only the inner 80% (centered), rest of black -> transparent
box_w = right - left + 1
box_h = bottom - top + 1
inner_left = int(left + 0.1 * box_w)
inner_right = int(right - 0.1 * box_w)
inner_top = int(top + 0.1 * box_h)
inner_bottom = int(bottom - 0.1 * box_h)

for y in range(h):
    for x in range(w):
        if left <= x <= right and top <= y <= bottom and is_dark(pixels[x, y]):
            if x < inner_left or x > inner_right or y < inner_top or y > inner_bottom:
                pixels[x, y] = (255, 255, 255, 0)

img.save(img_path, "PNG")
print("Done: outer black removed; black square reduced by 20%; image size unchanged.")
