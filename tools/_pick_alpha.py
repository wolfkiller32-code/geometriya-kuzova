# -*- coding: utf-8 -*-
"""Подбор пары: цвет приглушённого текста + прозрачность знака (WCAG >= 4.5)."""
import io, sys

def lin(v):
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def contrast(c1, c2):
    l1 = 0.2126*lin(c1[0]) + 0.7152*lin(c1[1]) + 0.0722*lin(c1[2])
    l2 = 0.2126*lin(c2[0]) + 0.7152*lin(c2[1]) + 0.0722*lin(c2[2])
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

bg = (20, 22, 26)
WHITE = (255, 255, 255)

candidates = {
    "#7A8290 (текущий)": (122, 130, 144),
    "#858E9C": (133, 142, 156),
    "#8E97A6": (142, 151, 166),
    "#949DAB": (148, 157, 171),
    "#9AA3B1": (154, 163, 177),
}

out = io.StringIO()
out.write("Для каждого цвета подписей: базовая читаемость и допустимая прозрачность знака\n")
out.write("=" * 92 + "\n")
for name, col in candidates.items():
    base = contrast(col, bg)
    # ищем максимальную альфу, при которой контраст >= 4.5
    safe = 0
    for a in range(4, 80, 2):
        al = a / 255
        br = tuple(int(bg[i]*(1-al) + WHITE[i]*al) for i in range(3))
        if contrast(col, br) >= 4.5:
            safe = a
        else:
            break
    verdict = "не подходит" if base < 4.5 else ("запас мал" if safe < 14 else "ок")
    out.write(f"{name:22} база {base:4.1f}:1 | безопасная альфа до {safe:2}/255 "
              f"({safe/255*100:3.0f}%) | {verdict}\n")

out.write("\n" + "=" * 92 + "\n")
out.write("Проверка выбранного варианта: #8E97A6 + альфа 22\n")
col = (142, 151, 166)
al = 22 / 255
br = tuple(int(bg[i]*(1-al) + WHITE[i]*al) for i in range(3))
out.write(f"  штрих над фоном: {br}\n")
for label, c in [("белый #FFFFFF", (255,255,255)), ("основной #D4D9E0", (212,217,224)),
                 ("металл #A8B0BD", (168,176,189)), ("подписи #8E97A6", col)]:
    out.write(f"  {label:22} на фоне {contrast(c,bg):4.1f}:1 | на знаке {contrast(c,br):4.1f}:1\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())