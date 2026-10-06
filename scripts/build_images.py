import os
from PIL import Image

SRC = "/Users/arda/Desktop/NEU giant/source-images"
OUT = "/Users/arda/Desktop/NEU giant/img"
os.makedirs(OUT, exist_ok=True)

# name: (source file, ratio w/h, [output widths], focus_y 0=top 0.5=center 1=bottom, quality)
JOBS = [
    ("hero-montage-schwarz",      "6GIANT.jpg",  16/10, [1200, 640], 0.38, 78),
    ("og-source",                 "6GIANT.jpg",  1200/630, [1200], 0.38, 82),
    ("ueberuns-haupt",            "7GIANT.jpg",  3/4,   [960, 500], 0.5, 80),
    ("ueberuns-detail",           "2GIANT.png",  1/1,   [640, 400], 0.5, 80),
    ("leistung-montage",          "4GIANT.jpg",  3/4,   [900, 480], 0.5, 78),
    ("leistung-geraete",          "10GIANT.jpg", 1/1,   [900, 480], 0.45, 78),
    ("leistung-abbau",            "11GIANT.jpg", 2/3,   [900, 480], 0.5, 78),
    ("leistung-moebel",           "13GIANT.jpg", 1/1,   [900, 480], 0.32, 78),
    ("ablauf-planung",            "8GIANT.jpg",  1/1,   [960, 500], 0.5, 80),
    ("galerie-minimal-weiss",     "3GIANT.jpg",  4/3,   [900, 480], 0.5, 78),
    ("galerie-offenes-regal",     "5GIANT.jpg",  4/3,   [900, 480], 0.5, 78),
    ("galerie-marmor-insel",      "12GIANT.jpg", 4/3,   [900, 480], 0.4, 78),
    ("galerie-pendelleuchten",    "14GIANT.jpg", 4/3,   [900, 480], 0.25, 78),
]

def crop_to_ratio(im, ratio, focus_y=0.5):
    w, h = im.size
    target_w = w
    target_h = round(w / ratio)
    if target_h > h:
        target_h = h
        target_w = round(h * ratio)
    x0 = (w - target_w) // 2
    y0 = int((h - target_h) * focus_y)
    y0 = max(0, min(y0, h - target_h))
    return im.crop((x0, y0, x0 + target_w, y0 + target_h))

for name, src, ratio, widths, focus_y, quality in JOBS:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    cropped = crop_to_ratio(im, ratio, focus_y)
    for w in widths:
        h = round(w / ratio)
        resized = cropped.resize((w, h), Image.LANCZOS)
        out_path = os.path.join(OUT, f"{name}-{w}.webp")
        q = quality
        resized.save(out_path, "WEBP", quality=q, method=6)
        size_kb = os.path.getsize(out_path) / 1024
        # tighten quality if still too big
        while size_kb > 195 and q > 40:
            q -= 8
            resized.save(out_path, "WEBP", quality=q, method=6)
            size_kb = os.path.getsize(out_path) / 1024
        print(f"{out_path}  {w}x{h}  q={q}  {size_kb:.1f}KB")
