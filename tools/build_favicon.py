# -*- coding: utf-8 -*-
"""
Готовит favicon из логотипа ВК.

Проблема: логотип тёмный (средний RGB 26,37,48) — на тёмной панели вкладок
браузера сливается и выглядит как пустой лист.

Решение: оранжевая подложка (фирменный акцент #FF6B1A) со скруглёнными
углами + логотип с отступом. Такой значок заметен и на светлой, и на тёмной
панели вкладок.

Создаёт: favicon.ico (16+32+48), favicon-16/32/48/64.png,
apple-touch-icon.png (180x180).
"""
import os
import sys
from PIL import Image, ImageDraw

SITE = r"C:\Сайт кузовн\docs"
IMG = os.path.join(SITE, "img")
LOGO = os.path.join(IMG, "logo.jpg")
ACCENT = (255, 107, 26)      # #FF6B1A — акцент сайта
PAD_RATIO = 0.11             # отступ логотипа внутрь


def rounded_logo(size: int) -> Image.Image:
    """Квадратная иконка: оранжевый фон со скруглением + логотип по центру."""
    ss = size * 4                     # супер-сэмплинг для гладких краёв
    canvas = Image.new("RGB", (ss, ss), ACCENT)
    logo = Image.open(LOGO).convert("RGB")
    pad = int(ss * PAD_RATIO)
    inner = ss - pad * 2
    logo = logo.resize((inner, inner), Image.LANCZOS)
    # сам логотип тоже со скруглением, чтобы не смотрелся «квадратом в квадрате»
    mask = Image.new("L", (inner, inner), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, inner - 1, inner - 1],
                                           radius=int(inner * 0.16), fill=255)
    canvas.paste(logo, (pad, pad), mask)

    # скругление самого значка
    outer = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(outer).rounded_rectangle([0, 0, ss - 1, ss - 1],
                                            radius=int(ss * 0.22), fill=255)
    result = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    result.paste(canvas, (0, 0), outer)
    return result.resize((size, size), Image.LANCZOS)


def main():
    sizes = {
        "favicon-16.png": 16,
        "favicon-32.png": 32,
        "favicon-48.png": 48,
        "favicon-64.png": 64,
        "apple-touch-icon.png": 180,
    }
    for name, s in sizes.items():
        rounded_logo(s).save(os.path.join(IMG, name))
        print("создан", name, f"{s}x{s}")

    # многоразмерный .ico — браузер сам выберет подходящий
    ico_main = rounded_logo(48)
    ico_main.save(os.path.join(IMG, "favicon.ico"), format="ICO",
                  sizes=[(16, 16), (32, 32), (48, 48)])
    print("создан favicon.ico (16, 32, 48)")

    # совместимость: favicon.png = 64
    rounded_logo(64).save(os.path.join(IMG, "favicon.png"))
    print("создан favicon.png (64x64)")

    # контроль: яркость значка
    px = list(rounded_logo(16).convert("RGB").getdata())
    lum = [0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in px]
    print(f"\nконтроль: средняя яркость значка {sum(lum)/len(lum):.0f} "
          f"(было 36 у тёмного логотипа)")
    print(f"ярких пикселей: {sum(1 for l in lum if l > 140)/len(lum):.0%}")


if __name__ == "__main__":
    main()