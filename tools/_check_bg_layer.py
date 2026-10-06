# -*- coding: utf-8 -*-
"""Проверка фонового слоя: где знак виден, где его закрывают карточки."""
import io, re, sys, os

CSS = r"C:\Сайт кузовн\docs\style.css"
css = open(CSS, encoding="utf-8").read()
out = io.StringIO()

# 1. проверка наличия ключевых правил
checks = {
    "html с фоном": r"html\{[^}]*background-color:var\(--graphite\)",
    "body::before fix": r"body::before\{[^}]*position:fixed",
    "знак по центру": r"body::before\{[^}]*background-position:center center",
    "z-index:-1": r"body::before\{[^}]*z-index:-1",
    "pointer-events:none": r"body::before\{[^}]*pointer-events:none",
    "размер в vmin": r"background-size:min\(78vmin",
    "контент выше (z-index:1)": r"\.breadcrumbs,.hero,\.section,\.footer,\.trust\{position:relative;z-index:1\}",
    "картинка знака": r"url\(\"img/bg-watermark\.png\"\)",
}
for name, pat in checks.items():
    out.write(f"  {'✓' if re.search(pat, css, re.S) else '✗'} {name}\n")

# 2. элементы с непрозрачным фоном, которые могут закрыть знак
out.write("\nБлоки с собственным фоном (закрывают знак под собой):\n")
for m in re.finditer(r"([.#][\w-]+(?:\s*,[^\{]*?)?)\{([^}]*background[^}]*)\}", css):
    sel = m.group(1).strip()[:60]
    body = m.group(2)
    if "graphite-2" in body or "linear-gradient" in body:
        out.write(f"  {sel}\n")

# 3. наличие файла
img = r"C:\Сайт кузовн\docs\img\bg-watermark.png"
out.write(f"\nфайл фона: {'✓ ' + str(os.path.getsize(img)//1024) + ' КБ' if os.path.exists(img) else '✗ НЕТ'}")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())