# -*- coding: utf-8 -*-
"""Анализ структуры логотипа: карта яркости 8x8, поиск светлых зон (текста)."""
import io, sys
from PIL import Image

LOGO = r"C:\Сайт кузовн\img\logo.jpg"
im = Image.open(LOGO).convert("RGB")
w, h = im.size
out = io.StringIO()
out.write(f"логотип: {w}x{h}\n\n")

small = im.resize((8, 8))
px = list(small.getdata())
out.write("карта яркости 8x8 (0=чёрный, 9=белый):\n")
for y in range(8):
    row = ""
    for x in range(8):
        c = px[y * 8 + x]
        lum = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
        row += str(min(9, int(lum / 26))) + " "
    out.write("  " + row + "\n")

# карта насыщенности (оранжевые акценты?)
out.write("\nкарта 'оранжевости' (R заметно больше B):\n")
for y in range(8):
    row = ""
    for x in range(8):
        c = px[y * 8 + x]
        row += ("O" if c[0] > c[2] + 40 else ".") + " "
    out.write("  " + row + "\n")

# зоны: центр, низ, верх
def stat(box, name):
    crop = im.crop(box).resize((20, 20))
    p = list(crop.getdata())
    lum = [0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in p]
    bright = sum(1 for l in lum if l > 150) / len(lum)
    out.write(f"{name}: ярких пикселей {bright:.0%}, средняя яркость {sum(lum)/len(lum):.0f}\n")

stat((0, 0, w, h // 3), "верхняя треть")
stat((0, h // 3, w, 2 * h // 3), "центральная треть")
stat((0, 2 * h // 3, w, h), "нижняя треть")
stat((w // 4, h // 4, 3 * w // 4, 3 * h // 4), "центральный квадрат")

# сколько всего светлых пикселей на разных порогах
full = im.resize((200, 200))
fp = list(full.getdata())
fl = [0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in fp]
for t in (100, 140, 170, 200):
    out.write(f"пикселей ярче {t}: {sum(1 for l in fl if l > t)/len(fl):.1%}\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())