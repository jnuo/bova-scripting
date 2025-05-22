#!/usr/bin/env python3
"""
make_widescreen.py – batch-convert images to 1920×1080 transparent canvases,
saving the results in ./image_results/
"""

from pathlib import Path
from PIL import Image

SRC_DIR      = Path("images")            # where your source files live
DEST_DIR     = Path("image_results")     # all PNG outputs go here
TARGET_SIZE  = (1920, 1080)              # (width, height)
IMAGE_TYPES  = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".gif"}

def process_image(src_path: Path) -> None:
    """Open one image, centre it on a 1920×1080 transparent canvas, save to DEST_DIR."""
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size

    # 1. Shrink if bigger than target canvas
    if w > TARGET_SIZE[0] or h > TARGET_SIZE[1]:
        im.thumbnail(TARGET_SIZE, Image.LANCZOS)
        w, h = im.size

    # 2. Create transparent canvas + paste
    canvas = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))
    offset_x = (TARGET_SIZE[0] - w) // 2
    offset_y = (TARGET_SIZE[1] - h) // 2
    canvas.paste(im, (offset_x, offset_y), im)

    # 3. Build destination file path
    out_path = DEST_DIR / src_path.with_suffix(".png").name

    # 4. Save
    canvas.save(out_path, "PNG")
    print(f"✓ {src_path.name}  →  {out_path}")

def main():
    if not SRC_DIR.exists():
        raise SystemExit(f"Source folder {SRC_DIR} not found.")

    DEST_DIR.mkdir(exist_ok=True)

    images = [p for p in SRC_DIR.iterdir() if p.suffix.lower() in IMAGE_TYPES]
    if not images:
        raise SystemExit(f"No image files found in {SRC_DIR}")

    for img_path in images:
        try:
            process_image(img_path)
        except Exception as exc:
            print(f"✗ {img_path.name}  –  skipped ({exc})")

if __name__ == "__main__":
    main()