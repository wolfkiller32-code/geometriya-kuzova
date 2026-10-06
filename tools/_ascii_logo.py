# -*- coding: utf-8 -*-
"""Отрисовка логотипа в ASCII, чтобы понять его содержимое без просмотра картинки."""
import io, sys
from PIL import Image, ImageOps

LOGO = r"C:\Сайт кузовн\docs\img\logo.jpg"
im = Image.open(LOGO).convert("L")
W = 76
H = int(W * im.size[1] / im.size[0] * 0.5)   # поправка на пропорции символа
im = im.resize((W, H))

px = list(im.getdata())
chars = " .:-=+*#%@"
out = io.StringIO()
out.write(f"логотип {Image.open(LOGO).size}, отрисовка {W}x{H}\n")
out.write("тёмное -> пробел, светлое -> @\n\n")
for y in range(H):
    row = ""
    for x in range(W):
        v = px[y * W + x]
        row += chars[min(len(chars) - 1, v * len(chars) // 256)]
    out.write(row + "\n")

# инверсия: показать тёмные элементы на светлом
out.write("\n--- ИНВЕРСИЯ (тёмные элементы видны как @) ---\n")
inv = ImageOps.invert(Image.open(LOGO).convert("L")).resize((W, H))
px2 = list(inv.getdata())
for y in range(H):
    row = ""
    for x in range(W):
        v = px2[y * W + x]
        row += chars[min(len(chars) - 1, v * len(chars) // 256)]
    out.write(row + "\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())