# -*- coding: utf-8 -*-
"""Готовит logo, favicon, og-image из скачанного аватара ВК."""
import os
from PIL import Image

SRC = r"C:\Сайт кузовн\site-build\geometriya-kuzova\img\logo.jpg"
IMG = r"C:\Сайт кузовн\site-build\geometriya-kuzova\img"

im = Image.open(SRC).convert("RGB")
print("logo size:", im.size, "mode:", im.mode)

# favicon.ico (32px) и favicon.png (64px) в корень сайта
fav_ico = im.resize((32, 32), Image.LANCZOS)
fav_png = im.resize((64, 64), Image.LANCZOS)
fav_ico.save(os.path.join(IMG, "favicon.ico"), format="ICO", sizes=[(32, 32)])
fav_png.save(os.path.join(IMG, "favicon.png"))

# og-image 1200x630 (с обрезкой по центру)
og = im.resize((1200, 1200), Image.LANCZOS)
left = (1200 - 1200) // 2
top = (1200 - 630) // 2
og_crop = og.crop((0, top, 1200, top + 630))
og_crop.save(os.path.join(IMG, "og-cover.jpg"), quality=90)

# анализ палитры (чтобы понять, тёмный/светлый логотип)
small = im.resize((50, 50))
px = list(small.getdata())
avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
print("average color:", avg)
# гистограмма яркости
lum = [0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] for p in px]
dark = sum(1 for l in lum if l < 100) / len(lum)
light = sum(1 for l in lum if l > 155) / len(lum)
print(f"dark px: {dark:.0%}, light px: {light:.0%}")

# сохраняем версии 200 и 360 для логотипа в шапке
for size in (200, 360):
    v = im.resize((size, size), Image.LANCZOS)
    v.save(os.path.join(IMG, f"logo-{size}.jpg"), quality=88)
print("done")