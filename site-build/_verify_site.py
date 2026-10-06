# -*- coding: utf-8 -*-
"""Проверка сайта: битые ссылки, картинки, анкоры, объём текста."""
import os, re, io, sys
from urllib.parse import urlparse, unquote

SITE = r"C:\Сайт кузовн\site-build\geometriya-kuzova"
out = io.StringIO()

html_files = []
for r, d, f in os.walk(SITE):
    for x in f:
        if x.endswith(".html"):
            html_files.append(os.path.join(r, x))

errors = []
ok_links = 0

# карта id по файлам
ids = {}
for hf in html_files:
    txt = open(hf, encoding="utf-8").read()
    ids[os.path.normpath(hf)] = set(re.findall(r'id="([^"]+)"', txt))

for hf in html_files:
    rel = os.path.relpath(hf, SITE)
    txt = open(hf, encoding="utf-8").read()
    base = os.path.dirname(hf)

    # ссылки
    for m in re.finditer(r'href="([^"]+)"', txt):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
            continue
        if href.startswith("#"):
            if len(href) > 1 and href[1:] not in ids.get(os.path.normpath(hf), set()):
                errors.append(f"{rel}: анкор {href} не найден на этой странице")
            continue
        # относительная ссылка
        path_part = href.split("#")[0]
        anchor = href.split("#")[1] if "#" in href else None
        if not path_part:
            continue
        target = os.path.normpath(os.path.join(base, unquote(path_part)))
        if not os.path.exists(target):
            errors.append(f"{rel}: битая ссылка {href}")
        else:
            ok_links += 1
            if anchor and os.path.normpath(target) in ids and anchor not in ids[os.path.normpath(target)]:
                errors.append(f"{rel}: анкор #{anchor} отсутствует в {os.path.relpath(target, SITE)}")

    # картинки
    for m in re.finditer(r'(?:src|data-full)="([^"]+)"', txt):
        src = m.group(1)
        if src.startswith(("http://", "https://", "data:")):
            continue
        if not src:
            continue
        target = os.path.normpath(os.path.join(base, unquote(src)))
        if not os.path.exists(target):
            errors.append(f"{rel}: нет файла изображения {src}")

out.write(f"HTML-файлов: {len(html_files)}\n")
out.write(f"Проверено внутренних ссылок (успешно): {ok_links}\n")
out.write(f"Ошибок: {len(errors)}\n")
for e in errors[:60]:
    out.write("  ✗ " + e + "\n")
if not errors:
    out.write("  ✓ битых ссылок и картинок не найдено\n")
sys.stderr.buffer.write(out.getvalue().encode("utf-8", "replace"))