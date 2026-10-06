# -*- coding: utf-8 -*-
"""
Готовит фоновый водяной знак из логотипа.

Исходник: JPEG 2560x2560 с логотипом на тёмно-синем фоне (RGB 1,14,30).
Такой файл как фон не годится: тёмно-синий квадрат будет заметен
на графитовом фоне сайта (#14161A) как чужеродное пятно.

Решение: фон -> прозрачность, логотип -> светлые штрихи с заданной
максимальной непрозрачностью. Получается деликатный водяной знак,
который лежит на существующем фоне, не перекрывая контент.
"""
import io
import os
import sys
from PIL import Image

SRC = r"C:\Users\vyazi\Downloads\6UW-M2z7u8-Qvk-kTM8dJ18fSxqGevGENwpvAROp3JbqisO6b0PcAbdECA0I7HSp-iA5EzMKcKnC1aZpFrq8qM37.jpg"
OUT_DIR = r"C:\Сайт кузовн\docs\img"
SIZE = 1400               # итоговый размер квадрата (px)
MAX_ALPHA = 44            # максимальная непрозрачность (≈17%) — заметно, но не мешает
LOGO_RGB = (255, 255, 255)  # цвет штрихов


def main():
    out = io.StringIO()
    im = Image.open(SRC).convert("L")

    # альфа = яркость: тёмный фон (≈20) -> 0, светлый логотип (≈200) -> max
    LO, HI = 45, 190
    alpha = im.point(lambda v: 0 if v <= LO else (
        MAX_ALPHA if v >= HI else int((v - LO) * MAX_ALPHA / (HI - LO))))

    rgba = Image.new("RGBA", im.size, LOGO_RGB + (0,))
    rgba.putalpha(alpha)
    rgba = rgba.resize((SIZE, SIZE), Image.LANCZOS)

    dst = os.path.join(OUT_DIR, "bg-watermark.png")
    rgba.save(dst, optimize=True)
    out.write(f"создан bg-watermark.png: {SIZE}x{SIZE}, "
              f"{os.path.getsize(dst)/1024:.0f} КБ\n")

    # контроль: прозрачность и «вес» знака
    a = list(rgba.getdata())
    opaque = sum(1 for c in a if c[3] > 0) / len(a)
    avg_alpha = sum(c[3] for c in a) / len(a)
    out.write(f"пикселей со штрихами: {opaque:.1%}\n")
    out.write(f"средняя непрозрачность: {avg_alpha:.1f}/255 "
              f"(макс {MAX_ALPHA})\n")

    # как это будет выглядеть поверх фона сайта #14161A
    bg = (20, 22, 26)
    sample = []
    for c in a:
        al = c[3] / 255
        r = int(bg[0] * (1 - al) + LOGO_RGB[0] * al)
        g = int(bg[1] * (1 - al) + LOGO_RGB[1] * al)
        b = int(bg[2] * (1 - al) + LOGO_RGB[2] * al)
        sample.append((r, g, b))
    dark = [c for c in sample if sum(c) < 200]
    bright = [c for c in sample if sum(c) > 250]
    out.write(f"\nповерх фона #14161A:\n")
    out.write(f"  максимум штриха: RGB {max(sample, key=sum)}\n")
    out.write(f"  фон остаётся: RGB {bg}\n")

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print(out.getvalue())


if __name__ == "__main__":
    main()