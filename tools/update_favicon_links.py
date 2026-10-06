# -*- coding: utf-8 -*-
"""Обновляет ссылки на favicon во всех HTML-страницах сайта (docs/)."""
import os
import re
import io
import sys

SITE = r"C:\Сайт кузовн\docs"
out = io.StringIO()

# старые строки -> новые
BLOCKS = [
    (
        re.compile(
            r'<link rel="icon" href="[^"]*favicon\.ico"[^>]*>\s*'
            r'<link rel="icon" type="image/png" href="[^"]*favicon\.png"[^>]*>\s*'
            r'<link rel="apple-touch-icon" href="[^"]*"[^>]*>'
        ),
        '<link rel="icon" href="{p}favicon.ico" sizes="any">\n'
        '<link rel="icon" type="image/png" sizes="32x32" href="{p}favicon-32.png">\n'
        '<link rel="icon" type="image/png" sizes="16x16" href="{p}favicon-16.png">\n'
        '<link rel="apple-touch-icon" sizes="180x180" href="{p}apple-touch-icon.png">'
    ),
]

# предыдущий вариант (со sizes="32x32" и без type у ico)
BLOCKS.append((
    re.compile(
        r'<link rel="icon" href="[^"]*favicon\.ico"[^>]*>\s*'
        r'<link rel="icon" type="image/png" href="[^"]*favicon\.png"[^>]*>\s*'
        r'<link rel="apple-touch-icon" href="[^"]*"[^>]*>'
    ),
    None  # заполним ниже
))

changed = 0
for root, dirs, files in os.walk(SITE):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(root, fn)
        txt = open(path, encoding="utf-8").read()
        # префикс пути к img: в корне "img/", в подпапках "../img/"
        rel = os.path.relpath(root, SITE)
        prefix = "img/" if rel == "." else "../img/"

        new_txt = txt
        # универсально: заменяем группу из трёх строк про иконки
        pat = re.compile(
            r'[ \t]*<link rel="icon"[^>]*>(?:\s*\n[ \t]*<link rel="(?:icon|apple-touch-icon)"[^>]*>)*',
        )
        m = pat.search(new_txt)
        if m and "favicon" in m.group(0):
            replacement = (
                f'<link rel="icon" href="{prefix}favicon.ico" sizes="any">\n'
                f'<link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png">\n'
                f'<link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16.png">\n'
                f'<link rel="apple-touch-icon" sizes="180x180" href="{prefix}apple-touch-icon.png">'
            )
            new_txt = new_txt[:m.start()] + replacement + new_txt[m.end():]

        if new_txt != txt:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_txt)
            changed += 1
            out.write(f"обновлён {os.path.relpath(path, SITE)}\n")

out.write(f"\nфайлов обновлено: {changed}\n")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())