# -*- coding: utf-8 -*-
"""
Убирает декоративные стикеры с фотографий галереи.

Стикеры (work__badge: «Премиум», «Коррозия», «ДТП» и т.п.) не несут
SEO-нагрузки — текст для поисковиков дают alt, figcaption и data-атрибуты.
Фильтры продолжают работать: они используют невидимый data-cat.
"""
import io
import os
import re
import sys

SITE = r"C:\Сайт кузовн\docs"
out = io.StringIO()

targets = []
for root, dirs, files in os.walk(SITE):
    for fn in files:
        if fn.endswith(".html"):
            targets.append(os.path.join(root, fn))

total = 0
for path in targets:
    txt = open(path, encoding="utf-8").read()
    # удаляем стикеры вместе с предшествующими пробелами/отступами
    new = re.sub(r'[ \t]*<span class="work__badge">[^<]*</span>', "", txt)
    if new != txt:
        n = len(re.findall(r'<span class="work__badge">', txt))
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        total += n
        out.write(f"{os.path.relpath(path, SITE)}: убрано {n}\n")

out.write(f"\nвсего убрано стикеров: {total}\n")

# проверка: data-cat и подписи на месте (фильтры и SEO не сломаны)
idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
out.write(f"\nпроверка галереи:\n")
out.write(f"  карточек работ:      {len(re.findall(r'class=.work reveal.', idx))}\n")
out.write(f"  data-cat (фильтры):  {len(re.findall(r'data-cat=', idx))}\n")
out.write(f"  figcaption (SEO):    {len(re.findall(r'figcaption class=.work__cap', idx))}\n")
out.write(f"  осталось бейджей:    {len(re.findall(r'work__badge', idx))}\n")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print(out.getvalue())