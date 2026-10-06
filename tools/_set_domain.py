# -*- coding: utf-8 -*-
"""Заменяет временный домен geometriya-kuzova.ru на реальный адрес GitHub Pages."""
import os
import io
import sys

ROOT = r"C:\Сайт кузовн"
OLD = "https://geometriya-kuzova.ru"
NEW = "https://wolfkiller32-code.github.io/geometriya-kuzova"

out = io.StringIO()
targets = []
for r, d, f in os.walk(ROOT):
    parts = r.split(os.sep)
    if ".git" in parts or "tools" in parts:
        continue
    for x in f:
        if x.endswith((".html", ".xml", ".txt")):
            targets.append(os.path.join(r, x))

changed = 0
total = 0
for p in targets:
    t = open(p, encoding="utf-8").read()
    n = t.count(OLD)
    if n:
        t = t.replace(OLD, NEW)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(t)
        changed += 1
        total += n
        out.write(f"{os.path.relpath(p, ROOT)}: {n} замен\n")

out.write(f"\nФайлов изменено: {changed}, замен: {total}\n")

# проверка остатка
left = 0
for p in targets:
    left += open(p, encoding="utf-8").read().count("geometriya-kuzova.ru")
out.write(f"Осталось вхождений старого домена: {left}\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())