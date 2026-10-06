# -*- coding: utf-8 -*-
"""Точный анализ логотипа: профиль строк/столбцов, поиск графического знака и текста."""
import io, sys
from PIL import Image

LOGO = r"C:\Сайт кузовн\docs\img\logo.jpg"
im = Image.open(LOGO).convert("RGB")
W, H = im.size
px = im.load()

def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

# профиль по строкам: доля «светлых» пикселей (контент) и средняя яркость
out = io.StringIO()
out.write(f"логотип {W}x{H}\n\n")
out.write("строка | светлых% | средн.ярк | полоса\n")
rows = []
for y in range(H):
    vals = [lum(px[x, y]) for x in range(0, W, 4)]
    light = sum(1 for v in vals if v > 120) / len(vals)
    avg = sum(vals) / len(vals)
    rows.append((y, light, avg))

# ищем пустые полосы (границы между блоками)
in_block = False
blocks = []
for y, light, avg in rows:
    content = light > 0.02
    if content and not in_block:
        start = y; in_block = True
    elif not content and in_block:
        blocks.append((start, y)); in_block = False
if in_block:
    blocks.append((start, H))

out.write("\nнайдено блоков контента по вертикали:\n")
for i, (a, b) in enumerate(blocks):
    out.write(f"  блок {i}: y={a}..{b} (высота {b-a}, {100*(b-a)/H:.1f}% от логотипа)\n")

# для каждого блока — горизонтальные границы
for i, (a, b) in enumerate(blocks):
    xs = []
    for y in range(a, b, 2):
        for x in range(W):
            if lum(px[x, y]) > 120:
                xs.append(x)
                break
    xs2 = []
    for y in range(a, b, 2):
        for x in range(W - 1, -1, -1):
            if lum(px[x, y]) > 120:
                xs2.append(x)
                break
    if xs:
        out.write(f"  блок {i}: x={min(xs)}..{max(xs2)}  ширина {max(xs2)-min(xs)}\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())