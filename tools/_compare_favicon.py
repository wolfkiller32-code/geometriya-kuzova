# -*- coding: utf-8 -*-
"""Сравнение вариантов favicon: только знак vs весь логотип. Печать ASCII для оценки."""
import io, sys
from PIL import Image, ImageDraw

LOGO = r"C:\Сайт кузовн\docs\img\logo.jpg"
GRAPHITE = (20, 22, 26)
ACCENT = (255, 107, 26)

def preview(im, w=50):
    g = im.convert("L")
    h = max(1, int(w * g.size[1] / g.size[0] * 0.5))
    g = g.resize((w, h))
    px = list(g.getdata())
    chars = " .:-=+*#%@"
    return "\n".join("".join(chars[min(9, px[y*w+x]*10//256)] for x in range(w)) for y in range(h))

def make(crop_box, size, pad=0.13, corner=0.22, thr=55):
    ss = size * 8
    logo = Image.open(LOGO).convert("L")
    art = logo.crop(crop_box) if crop_box else logo
    inner = int(ss * (1 - 2*pad))
    art = art.resize((inner, int(inner*art.size[1]/art.size[0])), Image.LANCZOS)
    mask = art.point(lambda v: 0 if v < thr else min(255, int((v-thr)*255/(200-thr))))
    canvas = Image.new("RGB", (ss, ss), ACCENT)
    solid = Image.new("RGB", art.size, GRAPHITE)
    canvas.paste(solid, ((ss-art.size[0])//2, (ss-art.size[1])//2), mask)
    alpha = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(alpha).rounded_rectangle([0,0,ss-1,ss-1], radius=int(ss*corner), fill=255)
    out = Image.new("RGBA", (ss, ss), (0,0,0,0))
    out.paste(canvas, (0,0), alpha)
    return out.resize((size, size), Image.LANCZOS)

SIGN = (202, 124, 506, 418)      # только графический знак
FULL = None                       # весь логотип

out = io.StringIO()
for label, box, thr in [("ЗНАК (thr=55)", SIGN, 55), ("ЗНАК (thr=90, жирнее)", SIGN, 90), ("ВЕСЬ ЛОГОТИП", FULL, 55)]:
    out.write("=" * 60 + f"\n{label}\n" + "=" * 60 + "\n")
    for s in (16, 32):
        im = make(box, s, thr=thr)
        px = list(im.convert("RGB").getdata())
        dark = sum(1 for c in px if max(c) < 90) / len(px)
        out.write(f"\n{s}x{s}: тёмных(рисунок) {dark:.0%}\n")
        out.write(preview(im) + "\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())