# -*- coding: utf-8 -*-
"""Анализ картинки-логотипа для фона: форма, прозрачность фона, контраст."""
import io, sys
from PIL import Image

SRC = r"C:\Users\vyazi\Downloads\6UW-M2z7u8-Qvk-kTM8dJ18fSxqGevGENwpvAROp3JbqisO6b0PcAbdECA0I7HSp-iA5EzMKcKnC1aZpFrq8qM37.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
out = io.StringIO()
out.write(f"картинка {W}x{H}\n")

px = im.load()
def lum(c):
    return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]

# общая яркость
full = im.resize((200, 200))
fp = list(full.getdata())
fl = [lum(c) for c in fp]
out.write(f"средняя яркость: {sum(fl)/len(fl):.0f} | min {min(fl):.0f} | max {max(fl):.0f}\n")
out.write(f"доля тёмных (<60): {sum(1 for v in fl if v<60)/len(fl):.0%}\n")
out.write(f"доля светлых (>160): {sum(1 for v in fl if v>160)/len(fl):.0%}\n")

# углы — понять фон
for name, box in [("лев.верх", (0,0,200,200)), ("прав.верх", (W-200,0,W,200)),
                  ("лев.низ", (0,H-200,200,H)), ("прав.низ", (W-200,H-200,W,H)),
                  ("центр", (W//2-150,H//2-150,W//2+150,H//2+150))]:
    crop = im.crop(box)
    p = list(crop.resize((30,30)).getdata())
    l = [lum(c) for c in p]
    avg = tuple(sum(c[i] for c in p)//len(p) for i in range(3))
    out.write(f"{name}: средняя яркость {sum(l)/len(l):.0f}, средний RGB {avg}\n")

# ASCII-отрисовка
out.write("\n--- отрисовка (светлое -> @) ---\n")
AW = 84
AH = int(AW * H / W * 0.5)
small = im.convert("L").resize((AW, AH))
sp = list(small.getdata())
chars = " .:-=+*#%@"
for y in range(AH):
    out.write("".join(chars[min(9, sp[y*AW+x]*10//256)] for x in range(AW)) + "\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())