# -*- coding: utf-8 -*-
"""Извлекает графический знак из логотипа и показывает его форму (ASCII)."""
import io, sys
from PIL import Image

LOGO = r"C:\Сайт кузовн\docs\img\logo.jpg"
im = Image.open(LOGO).convert("L")

# знак: x=202..506, y=124..418 -> берём с запасом и делаем квадрат
X0, Y0, X1, Y1 = 184, 101, 524, 441
sign = im.crop((X0, Y0, X1, Y1))
print(f"знак: {sign.size}")

W = 68
H = int(W * sign.size[1] / sign.size[0] * 0.5)
small = sign.resize((W, H))
px = list(small.getdata())
chars = " .:-=+*#%@"
out = io.StringIO()
out.write("ЗНАК (светлое -> @):\n")
for y in range(H):
    out.write("".join(chars[min(9, px[y*W+x] * 10 // 256)] for x in range(W)) + "\n")

# порог: сколько пикселей выше разных уровней
full = list(sign.getdata())
for t in (60, 90, 120, 150):
    out.write(f"\nпикселей ярче {t}: {sum(1 for v in full if v > t)/len(full):.1%}")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())