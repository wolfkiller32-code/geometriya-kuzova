#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор блока галереи работ (#works) для index.html.
Источник данных — _vk_catalog_v2.json (посты группы ВК) и img/works/.

Использование:
    python build_works_section.py          # записать works-section.html
    python build_works_section.py --inject # вставить блок в index.html
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))          # .../tools
SITE = os.path.join(os.path.dirname(ROOT), "docs")          # публикуемая папка сайта
OUT_HTML = os.path.join(ROOT, "works-section.html")
INDEX = os.path.join(SITE, "index.html")

# Кураторский список проектов: (номер поста, категории, заголовок, описание, номер фото)
PROJECTS = [
    ("9257", "dtp", "Hyundai Creta после ДТП", "Замена оригинальных дверей, лонжерона и арки, восстановление системы безопасности.", "457249168"),
    ("9254", "dtp pokraska", "Hyundai Elantra", "Замена передних крыльев и покраска с выставлением по заводским зазорам.", "457249161"),
    ("9248", "pokraska bamper", "Audi Q8", "Ремонт и покраска переднего бампера и капота, замена решётки радиатора.", "457249132"),
    ("9210", "pokraska", "Renault Duster", "Полная покраска крыльев, порогов, капота, бамперов и двери + полировка. 12 дней.", "457249017"),
    ("9215", "dtp pokraska", "Renault Duster «перевёртыш»", "Замена повреждённых панелей, ювелирная рихтовка, полная покраска кузова.", "457249033"),
    ("9195", "korroziya dtp", "Mazda 3", "Замена крышки багажника, заднего крыла, наружной арки, задней панели и бампера, лечение коррозии.", "457248961"),
    ("9192", "dtp", "Mercedes S450", "Комплексный кузовной ремонт премиального седана.", "457248928"),
    ("9186", "dtp pokraska", "Hyundai Solaris", "Замена переднего левого крыла, ремонт и покраска передней левой двери — 3 дня.", "457248916"),
    ("9160", "dtp korroziya", "Chevrolet Camaro", "Восстановление геометрии кузова, замена крыла и силовых усилителей, точечная сварка, антикор.", "457248856"),
    ("9177", "pokraska korroziya", "Mercedes C180", "Покраска заднего бампера, удаление коррозии с задних крыльев и покраска — 5 дней.", "457248890"),
    ("9166", "dtp", "Toyota Camry", "Кузовной ремонт и покраска после ДТП, проверка геометрии.", "457248868"),
    ("9163", "korroziya bamper", "Устранение последствий «горе-мастеров»", "Бампер был прикручен саморезом через крыло — переделали по технологии, убрали очаг коррозии.", "457248861"),
    ("9143", "pokraska dtp", "Toyota Camry V70 — до/после", "Комплексный ремонт и покраска за 7 дней, контроль геометрии.", "457248824"),
    ("9139", "pokraska", "JAC JS6, Candy красный", "Покраска задней левой двери в сложный трёхслойный цвет без перехода на соседние элементы.", "457248819"),
    ("9134", "pokraska", "Lexus RX 350", "Ремонт и покраска с подбором белого перламутра — сложный трёхслойный цвет.", "457248811"),
    ("9253", "pokraska", "Итоги лета в цехе", "83 автомобиля, 120 бамперов, 71 дверь, 39 порогов и 7 полных покрасок кузова за сезон.", "457249147"),
    ("9248", "bamper", "Ремонт и покраска бампера", "Подготовка поверхности, ремонт дефектов и покраска с попаданием в цвет кузова.", "457249136"),
    ("9182", "dtp", "Chevrolet Camaro — готов", "Финальная сборка после восстановления геометрии и покраски.", "457248910"),
]

# Стикеры на фото убраны по просьбе заказчика. SEO они не несли —
# текст для поисковиков дают alt, figcaption и data-атрибуты.
# Фильтрация галереи работает по невидимому атрибуту data-cat.

ITEM = """      <figure class="work reveal" data-cat="{cats}" data-full="img/works/_{pid}.jpg" data-title="{title}" data-desc="{desc}" data-link="https://vk.com/wall-113402547_{post}">
        <img src="img/works/_{pid}.jpg" alt="{alt}" loading="lazy" width="{w}" height="{h}">
        <figcaption class="work__cap"><div class="work__title">{title}</div><div class="work__desc">{short}</div></figcaption>
        <span class="work__zoom">⤢</span>
      </figure>"""

HEAD = """<!-- ================== ГАЛЕРЕЯ РАБОТ (источник: группа ВК vk.com/geometriyakuzova) ================== -->
<section class="section" id="works">
  <div class="wrap">
    <div class="works-head reveal">
      <div class="section__head" style="margin-bottom:0">
        <div class="section__tag">Наши работы</div>
        <h2>Наши работы: реальные проекты цеха</h2>
        <p class="section__desc">Кузовной ремонт после ДТП, покраска, восстановление геометрии, сварка и борьба с коррозией. Фотографии из нашего цеха — с реальными сроками и результатом. За сезон вернули в идеальное состояние 83 автомобиля.</p>
      </div>
      <a href="https://vk.com/geometriyakuzova" target="_blank" rel="noopener" class="btn btn--ghost">Все работы во ВКонтакте →</a>
    </div>

    <div class="works-filter reveal" role="tablist" aria-label="Фильтр работ">
      <button type="button" class="is-active" data-filter="all">Все работы</button>
      <button type="button" data-filter="dtp">После ДТП</button>
      <button type="button" data-filter="pokraska">Покраска</button>
      <button type="button" data-filter="korroziya">Коррозия и сварка</button>
      <button type="button" data-filter="bamper">Бамперы и пластик</button>
    </div>

    <div class="works">
{items}
    </div>

    <div style="text-align:center;margin-top:36px" class="reveal">
      <a href="#estimate" class="btn btn--primary btn--lg">Оценить ремонт по фото</a>
      <p style="color:var(--muted);font-size:13.5px;margin-top:14px">Пришлите фото повреждения — рассчитаем стоимость и сроки бесплатно</p>
    </div>
  </div>
</section>

<!-- ================== ЛАЙТБОКС ================== -->
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Просмотр фотографии">
  <button type="button" class="lightbox__close" id="lightboxClose" aria-label="Закрыть">×</button>
  <img class="lightbox__img" id="lightboxImg" src="" alt="">
  <div class="lightbox__cap"><b id="lightboxTitle"></b><div id="lightboxDesc"></div><a class="lightbox__vk" id="lightboxLink" href="#" target="_blank" rel="noopener">Открыть пост во ВКонтакте →</a></div>
</div>
"""


def img_size(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:  # noqa: BLE001
        return (604, 453)


def main():
    items = []
    for i, (post, cats, title, desc, pid) in enumerate(PROJECTS):
        full = "113402547_" + pid
        path = os.path.join(SITE, "img", "works", "_" + full + ".jpg")
        if not os.path.exists(path):
            print("нет файла:", path, file=sys.stderr)
            continue
        w, h = img_size(path)
        short = desc.replace("—", "-")
        short = (short[:52] + "…") if len(short) > 52 else short
        items.append(ITEM.format(cats=cats, pid=full, post=post, title=title, desc=desc,
                                 alt=f"{title} — кузовной ремонт в Челябинске",
                                 short=short, w=w, h=h))

    html = HEAD.format(items="\n\n".join(items))
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"works-section.html: {len(items)} работ")

    if "--inject" in sys.argv:
        page = open(INDEX, encoding="utf-8").read()
        start = page.find("<!-- ================== ГАЛЕРЕЯ РАБОТ")
        end = page.find("<!-- ================== ЛАЙТБОКС ==================")
        if start == -1 or end == -1:
            print("не найдены маркеры для вставки", file=sys.stderr)
            return
        end2 = page.find("</div>", page.find("lightboxLink", end)) + len("</div>")
        new_page = page[:start] + html + page[end2:]
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(new_page)
        print("index.html обновлён")


if __name__ == "__main__":
    main()
