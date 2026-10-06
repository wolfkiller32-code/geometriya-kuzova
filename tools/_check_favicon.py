# -*- coding: utf-8 -*-
"""Диагностика favicon: валидность, размеры, содержимое."""
import io, os, sys
from PIL import Image

IMG = r"C:\Сайт кузовн\img"
out = io.StringIO()

for name in ["favicon.ico", "favicon.png", "logo.jpg", "logo-200.jpg"]:
    p = os.path.join(IMG, name)
    out.write(f"=== {name} ({os.path.getsize(p)} байт) ===\n")
    try:
        im = Image.open(p)
        out.write(f"  формат={im.format} режим={im.mode} размер={im.size}\n")
        if name.endswith(".ico"):
            out.write(f"  встроенных размеров: {getattr(im, 'info', {}).get('sizes', 'н/д')}\n")
        rgb = im.convert("RGB")
        small = rgb.resize((16, 16))
        px = list(small.getdata())
        avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
        lum = [0.299*c[0] + 0.587*c[1] + 0.114*c[2] for c in px]
        out.write(f"  средний цвет RGB={avg}\n")
        out.write(f"  яркость: min={min(lum):.0f} max={max(lum):.0f} avg={sum(lum)/len(lum):.0f}\n")
        white = sum(1 for l in lum if l > 240) / len(lum)
        dark = sum(1 for l in lum if l < 40) / len(lum)
        out.write(f"  доля белых пикселей={white:.0%}, почти чёрных={dark:.0%}\n")
        # alpha
        if im.mode in ("RGBA", "LA"):
            a = list(im.convert("RGBA").resize((16,16)).getdata())
            trans = sum(1 for c in a if c[3] < 20) / len(a)
            out.write(f"  прозрачных пикселей={trans:.0%}\n")
    except Exception as e:
        out.write(f"  ОШИБКА: {e}\n")
    out.write("\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())