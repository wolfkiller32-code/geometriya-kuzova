# -*- coding: utf-8 -*-
"""
Favicon из графического знака логотипа ВК.

Логотип (720x720) состоит из:
  - графического знака  : x=202..506, y=124..418
  - текста «ГЕОМЕТРИЯ»  : y=449..498
  - текста «КУЗОВА»     : y=519..569
Текст на 16x16 нечитаем, поэтому в иконку идёт только знак.

Знак в логотипе светлый на тёмном фоне. Чтобы иконка не выглядела
пустым листом на тёмной панели браузера, знак рисуется тёмным
(фирменный графит #14161A) на фирменной оранжевой подложке (#FF6B1A).
"""
import io
import os
import sys
from PIL import Image, ImageDraw, ImageFilter

SITE = r"C:\Сайт кузовн\docs"
IMG = os.path.join(SITE, "img")
LOGO = os.path.join(IMG, "logo.jpg")

# границы графического знака в логотипе
SIGN_BOX = (202, 124, 506, 418)
GRAPHITE = (20, 22, 26)      # #14161A — фон сайта
ACCENT = (255, 107, 26)      # #FF6B1A — акцент сайта
PAD_RATIO = 0.13             # отступ знака от края
CORNER_RATIO = 0.22          # скругление иконки


def build(size: int, sharpen: bool = False) -> Image.Image:
    ss = size * 8                                   # супер-сэмплинг
    logo = Image.open(LOGO).convert("L")
    sign = logo.crop(SIGN_BOX)

    # квадратный канвас, знак вписан по ширине
    inner = int(ss * (1 - 2 * PAD_RATIO))
    sign = sign.resize((inner, int(inner * sign.size[1] / sign.size[0])), Image.LANCZOS)

    # маска знака: светлые пиксели логотипа -> непрозрачные
    mask = sign.point(lambda v: 0 if v < 70 else min(255, int((v - 70) * 255 / 120)))
    # утолщаем штрихи, чтобы знак читался на 16-32px
    thicken = max(1, int(ss / 190))
    mask = mask.filter(ImageFilter.MaxFilter(thicken * 2 + 1))

    canvas = Image.new("RGB", (ss, ss), ACCENT)
    # знак по центру, цветом графит
    solid = Image.new("RGB", sign.size, GRAPHITE)
    ox = (ss - sign.size[0]) // 2
    oy = (ss - sign.size[1]) // 2
    canvas.paste(solid, (ox, oy), mask)

    # скругление подложки
    alpha = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(alpha).rounded_rectangle(
        [0, 0, ss - 1, ss - 1], radius=int(ss * CORNER_RATIO), fill=255)

    out = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    out.paste(canvas, (0, 0), alpha)
    out = out.resize((size, size), Image.LANCZOS)
    if sharpen:
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    return out


def ascii_preview(im: Image.Image, w: int = 46) -> str:
    g = im.convert("L")
    h = max(1, int(w * g.size[1] / g.size[0] * 0.5))
    g = g.resize((w, h))
    px = list(g.getdata())
    chars = " .:-=+*#%@"
    lines = []
    for y in range(h):
        lines.append("".join(chars[min(9, px[y * w + x] * 10 // 256)] for x in range(w)))
    return "\n".join(lines)


def main():
    out = io.StringIO()
    sizes = {
        "favicon-16.png": (16, False),
        "favicon-32.png": (32, False),
        "favicon-48.png": (48, True),
        "favicon-64.png": (64, True),
        "apple-touch-icon.png": (180, True),
    }
    for name, (s, sharp) in sizes.items():
        im = build(s, sharp)
        im.save(os.path.join(IMG, name))
        out.write(f"создан {name} ({s}x{s})\n")

    build(48, True).save(os.path.join(IMG, "favicon.ico"), format="ICO",
                         sizes=[(16, 16), (32, 32), (48, 48)])
    out.write("создан favicon.ico (16, 32, 48)\n")
    build(64, True).save(os.path.join(IMG, "favicon.png"))
    out.write("создан favicon.png (64x64)\n")

    # контроль качества
    for s in (16, 32):
        im = build(s)
        rgb = im.convert("RGB")
        px = list(rgb.getdata())
        lum = [0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in px]
        accent_px = sum(1 for c in px if c[0] > 180 and c[1] < 140) / len(px)
        graphite_px = sum(1 for c in px if max(c) < 80) / len(px)
        out.write(f"\n{s}x{s}: средняя яркость {sum(lum)/len(lum):.0f}, "
                  f"оранжевых {accent_px:.0%}, тёмных(знак) {graphite_px:.0%}")
        if s == 32:
            out.write("\n\nвид 32x32:\n" + ascii_preview(im))

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print(out.getvalue())


if __name__ == "__main__":
    main()