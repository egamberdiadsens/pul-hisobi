"""Ilova ikonkasi va splash ekranni yaratadi (GitHub Actions ichida ishlaydi)."""
import glob
import os
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
GREEN = (15, 107, 74)
GOLD = (242, 190, 72)
WHITE = (255, 255, 255)


def draw_mark(d, cx, cy, s):
    # uchta ustun (statistika) va tepasida tanga
    w = s * 0.16
    gap = s * 0.08
    heights = [0.34, 0.52, 0.70]
    base = cy + s * 0.36
    x0 = cx - (3 * w + 2 * gap) / 2
    for i, h in enumerate(heights):
        x = x0 + i * (w + gap)
        d.rounded_rectangle([x, base - s * h, x + w, base], radius=w * 0.3, fill=WHITE)
    r = s * 0.15
    ccx, ccy = cx - s * 0.22, cy - s * 0.24
    d.ellipse([ccx - r, ccy - r, ccx + r, ccy + r], fill=GOLD)


def icon(size, round_=False, fg_only=False):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if fg_only:
        s = S * 0.42
    else:
        if round_:
            d.ellipse([0, 0, S - 1, S - 1], fill=GREEN)
        else:
            d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.22, fill=GREEN)
        s = S * 0.62
    draw_mark(d, S / 2, S / 2, s)
    return im.resize((size, size), Image.LANCZOS)


for k, m in {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}.items():
    folder = f"{RES}/mipmap-{k}"
    os.makedirs(folder, exist_ok=True)
    icon(int(48 * m)).save(f"{folder}/ic_launcher.png")
    icon(int(48 * m), round_=True).save(f"{folder}/ic_launcher_round.png")
    icon(int(108 * m), fg_only=True).save(f"{folder}/ic_launcher_foreground.png")

for f in glob.glob(f"{RES}/drawable*/splash.png"):
    w, h = Image.open(f).size
    im = Image.new("RGB", (w, h), GREEN)
    ic = icon(int(min(w, h) * 0.28), fg_only=True)
    im.paste(ic, ((w - ic.width) // 2, (h - ic.height) // 2), ic)
    im.save(f)

bg = f"{RES}/values/ic_launcher_background.xml"
with open(bg) as fh:
    txt = fh.read()
with open(bg, "w") as fh:
    fh.write(txt.replace("#FFFFFF", "#0F6B4A"))
print("Ikonkalar tayyor")
