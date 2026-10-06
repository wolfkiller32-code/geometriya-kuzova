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
SIZE = 1800               # исходник для чёткости на больших экранах
MAX_ALPHA = 22            # непрозрачность ≈9%: знак бледный, но текст читаем
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

    # ---- проверка читаемости текста поверх знака ----
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    def contrast(c1, c2):
        l1 = 0.2126*lin(c1[0]) + 0.7152*lin(c1[1]) + 0.0722*lin(c1[2])
        l2 = 0.2126*lin(c2[0]) + 0.7152*lin(c2[1]) + 0.0722*lin(c2[2])
        hi, lo = max(l1, l2), min(l1, l2)
        return (hi + 0.05) / (lo + 0.05)

    bg = (20, 22, 26)
    # самый светлый штрих знака поверх фона
    al = MAX_ALPHA / 255
    brightest = tuple(int(bg[i] * (1 - al) + LOGO_RGB[i] * al) for i in range(3))

    out.write(f"\nфон {bg} -> штрих {brightest}\n")
    out.write("\nчитаемость текста поверх знака (WCAG, нужно ≥4.5 для тела):\n")
    for label, col in [("белый текст #FFFFFF", (255, 255, 255)),
                       ("основной текст #D4D9E0", (212, 217, 224)),
                       ("приглушённый #A8B0BD", (168, 176, 189)),
                       ("подписи #7A8290", (122, 130, 144))]:
        bg_c = contrast(col, bg)
        worst = contrast(col, brightest)
        mark = "OK" if worst >= 4.5 else ("на грани" if worst >= 3 else "риск")
        out.write(f"  {label}: на фоне {bg_c:.1f}:1 -> на знаке {worst:.1f}:1 [{mark}]\n")

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print(out.getvalue())


if __name__ == "__main__":
    main()