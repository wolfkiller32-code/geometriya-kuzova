# -*- coding: utf-8 -*-
"""
Пересборка 10 страниц услуг:
 - SEO-статья из site-build/seo/<slug>.html (600–800 слов)
 - блок «Примеры работ» с фото из img/works/
 - логотип из ВК, favicon, og-теги, актуальные VK-ссылки и второй телефон
Запуск: python rebuild_service_pages.py
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "geometriya-kuzova")
SEO = os.path.join(ROOT, "seo")
USLUGI = os.path.join(SITE, "uslugi")

SERVICES = [
    dict(slug="remont-bamperov", h1="Ремонт бамперов и пластика",
         title="Ремонт бампера в Челябинске — от 1 000 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Ремонт и пайка бамперов в Челябинске. Восстановление креплений, покраска в цвет кузова. ул. Каслинская 1/1. Тел: +7 (922) 632-60-30.",
         price="от 1 000 ₽", time="1–2 дня",
         lead="Паяем трещины, восстанавливаем крепления, красим в цвет кузова. Не всегда нужно покупать новый бампер — часто дешевле отремонтировать.",
         photos=[("457249136", "Ремонт и покраска бампера"), ("457249132", "Audi Q8: бампер и капот"), ("457248861", "Бампер после «горе-мастеров»")]),
    dict(slug="lokalnaya-pokraska", h1="Локальная покраска элемента",
         title="Локальная покраска автомобиля в Челябинске — от 5 000 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Локальная покраска элемента в Челябинске без полной покраски. Точный подбор цвета, выкрас на пробнике. ул. Каслинская 1/1.",
         price="от 5 000 ₽", time="1 день",
         lead="Устраняем небольшие дефекты без полной покраски элемента — быстро, аккуратно и без риска несовпадения оттенка.",
         photos=[("457249161", "Hyundai Elantra: покраска с подбором"), ("457248819", "JAC JS6: Candy красный без перехода"), ("457248811", "Lexus RX 350: белый перламутр")]),
    dict(slug="pokraska-elementa", h1="Покраска элемента кузова",
         title="Покраска элемента кузова в Челябинске — от 12 000 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Покраска элементов кузова автомобиля в Челябинске. Подбор краски по коду, выкрас на пробнике, гарантия. ул. Каслинская 1/1.",
         price="от 12 000 ₽", time="2–3 дня",
         lead="Полное обновление внешнего вида одного или нескольких элементов кузова с подбором краски по коду и выкрасом на пробнике.",
         photos=[("457249132", "Audi Q8: бампер и капот"), ("457248819", "JAC JS6: сложный трёхслойный цвет"), ("457248890", "Mercedes C180: покраска бампера"), ("457249161", "Hyundai Elantra: крылья")]),
    dict(slug="udalenie-korrozii", h1="Удаление коррозии",
         title="Удаление ржавчины и коррозии кузова в Челябинске | ГЕОМЕТРИЯ КУЗОВА",
         desc="Удаление коррозии автомобиля в Челябинске. Остановим ржавчину, обработаем скрытые полости, защитим кузов. ул. Каслинская 1/1.",
         price="от 1 000 ₽", time="1–2 дня",
         lead="Останавливаем ржавчину и защищаем кузов от дальнейшего разрушения. Зачистка до металла, преобразователи, антикор и покраска.",
         photos=[("457248961", "Mazda 3: коррозия крыла и арки"), ("457248890", "Mercedes C180: коррозия задних крыльев"), ("457248861", "Очаг коррозии после некачественного ремонта")]),
    dict(slug="zhestyanye-raboty", h1="Жестяные работы",
         title="Жестяные работы по кузову в Челябинске — от 3 000 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Жестяные работы: восстановление формы кузова после вмятин и деформаций. Рихтовка, споттер, минимум шпатли. ул. Каслинская 1/1.",
         price="от 3 000 ₽", time="от 1 дня",
         lead="Восстанавливаем форму кузова после вмятин и деформаций. Вытягиваем металл, а не маскируем его шпатлёвкой.",
         photos=[("457248856", "Chevrolet Camaro: кузовные работы"), ("457249033", "Renault Duster: рихтовка панелей"), ("457249168", "Hyundai Creta: восстановление после ДТП")]),
    dict(slug="zamena-arok", h1="Замена арок",
         title="Замена арок автомобиля в Челябинске — от 2 500 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Замена колесных арок в Челябинске. Вырезка коррозии, вваривание ремвставок, антикор и покраска. ул. Каслинская 1/1.",
         price="от 2 500 ₽", time="от 2 дней",
         lead="Вернём целостность и эстетику колёсных арок. Вырезаем ржавые участки, ввариваем новые, обрабатываем антикором и красим.",
         photos=[("457248961", "Mazda 3: замена наружной арки"), ("457249168", "Hyundai Creta: арка и лонжерон"), ("457249033", "Renault Duster: восстановление панелей")]),
    dict(slug="zamena-porogov", h1="Замена порогов",
         title="Замена порогов автомобиля в Челябинске — от 4 500 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Замена порогов кузова в Челябинске. Частичная и полная замена, сварка, антикоррозийная обработка, покраска.",
         price="от 4 500 ₽", time="от 2 дней",
         lead="Полная или частичная замена порогов с обработкой скрытых полостей антикором, герметизацией швов и покраской.",
         photos=[("457248961", "Mazda 3: ремонт нижней части кузова"), ("457249033", "Renault Duster: панели и пороги"), ("457248856", "Chevrolet Camaro: силовые элементы")]),
    dict(slug="zamena-privarnyh-paneley", h1="Замена приварных панелей",
         title="Замена приварных панелей кузова в Челябинске | ГЕОМЕТРИЯ КУЗОВА",
         desc="Замена приварных панелей автомобиля в Челябинске. Соблюдение заводских точек сварки, контроль геометрии, антикор.",
         price="от 5 000 ₽", time="от 3 дней",
         lead="Профессиональная замена приварных элементов кузова с соблюдением заводских технологий, зазоров и антикоррозийной обработкой.",
         photos=[("457248856", "Chevrolet Camaro: крыло и усилители"), ("457249168", "Hyundai Creta: двери и лонжерон"), ("457248961", "Mazda 3: задняя панель и крыло")]),
    dict(slug="svarochnye-raboty", h1="Сварочные работы",
         title="Сварочные работы по кузову в Челябинске — от 1 000 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Сварочные работы кузова автомобиля в Челябинске. Полуавтомат, аргон, точечная сварка, антикор швов. ул. Каслинская 1/1.",
         price="от 1 000 ₽", time="от 1 дня",
         lead="Полуавтомат, аргон, точечная сварка. Выполняем любые сварочные работы по кузову с антикоррозийной обработкой швов.",
         photos=[("457248856", "Chevrolet Camaro: точечная сварка"), ("457248861", "Ремонт после некачественной сварки"), ("457249168", "Hyundai Creta: сварные работы")]),
    dict(slug="vosstanovlenie-geometrii", h1="Восстановление геометрии кузова",
         title="Восстановление геометрии кузова в Челябинске — от 5 000 ₽ | ГЕОМЕТРИЯ КУЗОВА",
         desc="Восстановление геометрии кузова на стапеле в Челябинске. Вернём заводские параметры после ДТП. ул. Каслинская 1/1.",
         price="от 5 000 ₽", time="от 3 дней",
         lead="На стапеле вернём вашему автомобилю заводские параметры кузова после серьёзного ДТП с контролем контрольных точек.",
         photos=[("457248856", "Chevrolet Camaro: геометрия кузова"), ("457249168", "Hyundai Creta: удар в бок и столб"), ("457249033", "Renault Duster «перевёртыш»")]),
]

PAGE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0E1013">
<script>document.documentElement.classList.add('js');</script>
<link rel="icon" href="../img/favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" href="../img/favicon.png">
<link rel="apple-touch-icon" href="../img/logo-200.jpg">
<link rel="canonical" href="https://geometriya-kuzova.ru/uslugi/{slug}.html">
<link rel="stylesheet" href="../style.css">
<meta property="og:title" content="{h1} в Челябинске — ГЕОМЕТРИЯ КУЗОВА">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:locale" content="ru_RU">
<meta property="og:image" content="https://geometriya-kuzova.ru/img/og-cover.jpg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Главная","item":"https://geometriya-kuzova.ru/"}},{{"@type":"ListItem","position":2,"name":"Услуги","item":"https://geometriya-kuzova.ru/#services"}},{{"@type":"ListItem","position":3,"name":"{h1}","item":"https://geometriya-kuzova.ru/uslugi/{slug}.html"}}]}}
</script>
</head>
<body>

<header class="header">
  <div class="wrap header__inner">
    <a href="../index.html" class="logo"><img src="../img/logo-200.jpg" alt="Логотип ГЕОМЕТРИЯ КУЗОВА" class="logo__img" width="38" height="38">ГЕОМЕТРИЯ КУЗОВА</a>
    <nav class="nav">
      <a href="../index.html#services">Услуги</a>
      <a href="../index.html#works">Работы</a>
      <a href="../index.html#process">Процесс</a>
      <a href="../index.html#reviews">Отзывы</a>
      <a href="../index.html#contacts">Контакты</a>
    </nav>
    <div class="header__right">
      <a href="tel:+79226326030" class="header__phone">+7 (922) 632-60-30</a>
      <a href="../index.html#estimate" class="btn btn--primary">Оценить ремонт</a>
    </div>
  </div>
</header>

<nav class="breadcrumbs" aria-label="Хлебные крошки">
  <div class="wrap">
    <ol>
      <li><a href="../index.html">Главная</a></li>
      <li><a href="../index.html#services">Услуги</a></li>
      <li aria-current="page">{h1}</li>
    </ol>
  </div>
</nav>

<section class="hero" style="padding:56px 0 40px">
  <div class="wrap" style="max-width:820px">
    <div class="eyebrow">Челябинск · ул. Каслинская 1/1</div>
    <h1>{h1} <span class="accent">в Челябинске</span></h1>
    <p class="hero__sub">{lead}</p>
    <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:32px">
      <a href="tel:+79226326030" class="btn btn--primary btn--lg">+7 (922) 632-60-30</a>
      <a href="../index.html#estimate" class="btn btn--ghost btn--lg">Оценить по фото</a>
    </div>
    <div style="display:flex;gap:28px;flex-wrap:wrap;padding:20px 24px;background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius)">
      <div><div style="font-size:12px;color:var(--muted);margin-bottom:4px">Стоимость</div><div style="font-size:22px;font-weight:800">{price}</div></div>
      <div><div style="font-size:12px;color:var(--muted);margin-bottom:4px">Срок</div><div style="font-size:22px;font-weight:800">{time}</div></div>
      <div><div style="font-size:12px;color:var(--muted);margin-bottom:4px">Адрес</div><div style="font-size:15px;font-weight:600">ул. Каслинская, 1/1</div></div>
      <div><div style="font-size:12px;color:var(--muted);margin-bottom:4px">Режим</div><div style="font-size:15px;font-weight:600">ежедневно 10:00–20:00</div></div>
    </div>
  </div>
</section>

<section class="section" style="border-top:0;padding:36px 0 48px">
  <div class="wrap" style="max-width:820px">
    <h2>Что входит в услугу</h2>
    <ul style="list-style:none;display:flex;flex-direction:column;gap:14px;margin-top:24px;font-size:16px;color:var(--metal);line-height:1.65">
      <li>✓ Бесплатная дефектовка и точная смета</li>
      <li>✓ Работа с металлом и пластиком любой сложности</li>
      <li>✓ Подбор краски по коду с выкрасом на пробнике</li>
      <li>✓ Фотоотчёт на каждом этапе работ</li>
      <li>✓ Гарантия на все виды работ</li>
      <li>✓ Работаем с наличными и безналичным расчётом</li>
    </ul>
  </div>
</section>

{photos_section}

{seo}

<section class="section">
  <div class="wrap" style="max-width:820px">
    <h2>Как мы работаем</h2>
    <div class="process" style="grid-template-columns:repeat(2,1fr);margin-top:32px">
      <div class="step"><h3>Заявка и фото</h3><p>Присылаете фото повреждения — получаете предварительную оценку.</p><span class="step__time">15 минут</span></div>
      <div class="step"><h3>Осмотр и смета</h3><p>Проводим дефектовку, согласовываем работы и финальную стоимость.</p><span class="step__time">30–60 минут</span></div>
      <div class="step"><h3>Работы</h3><p>Выполняем по этапам, отправляем фотоотчёт на связи.</p><span class="step__time">{time}</span></div>
      <div class="step"><h3>Выдача</h3><p>Проверяете результат, подписываете акт, получаете гарантию.</p><span class="step__time">30 минут</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap" style="max-width:820px">
    <div style="background:var(--graphite-2);border:1px solid var(--line);border-radius:20px;padding:44px;text-align:center">
      <h2 style="margin-bottom:16px">Запишитесь на бесплатную оценку</h2>
      <p style="color:var(--metal);margin-bottom:26px">Пришлите фото повреждения — рассчитаем стоимость и сроки. Или позвоните: +7 (922) 632-60-30, +7 (351) 683-12-05.</p>
      <a href="tel:+79226326030" class="btn btn--primary btn--lg">Позвонить: +7 (922) 632-60-30</a>
      <a href="../index.html#estimate" class="btn btn--ghost btn--lg" style="margin-left:10px">Оценить по фото</a>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <div class="logo"><img src="../img/logo-200.jpg" alt="Логотип ГЕОМЕТРИЯ КУЗОВА" class="logo__img" width="34" height="34">ГЕОМЕТРИЯ КУЗОВА</div>
        <p class="footer__desc">Кузовной ремонт легковых автомобилей в Челябинске. ул. Каслинская, 1/1. Ежедневно 10:00–20:00.</p>
      </div>
      <div>
        <h4>Услуги</h4>
        <ul>
          <li><a href="remont-bamperov.html">Ремонт бамперов</a></li>
          <li><a href="pokraska-elementa.html">Покраска элементов</a></li>
          <li><a href="zhestyanye-raboty.html">Жестяные работы</a></li>
          <li><a href="svarochnye-raboty.html">Сварочные работы</a></li>
          <li><a href="vosstanovlenie-geometrii.html">Восстановление геометрии</a></li>
        </ul>
      </div>
      <div>
        <h4>Контакты</h4>
        <ul>
          <li><a href="tel:+79226326030">+7 (922) 632-60-30</a></li>
          <li><a href="tel:+73516831205">+7 (351) 683-12-05</a></li>
          <li><a href="https://vk.com/geometriyakuzova" target="_blank" rel="noopener">Группа ВКонтакте</a></li>
          <li><a href="../index.html#works">Наши работы</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 ГЕОМЕТРИЯ КУЗОВА. Все права защищены.</span>
      <span><a href="../index.html">Вернуться на главную</a> · <a href="../privacy.html">Политика конфиденциальности</a></span>
    </div>
  </div>
</footer>

<script src="../app.js"></script>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Просмотр фотографии">
  <button type="button" class="lightbox__close" id="lightboxClose" aria-label="Закрыть">×</button>
  <img class="lightbox__img" id="lightboxImg" src="" alt="">
  <div class="lightbox__cap"><b id="lightboxTitle"></b><div id="lightboxDesc"></div><a class="lightbox__vk" id="lightboxLink" href="#" target="_blank" rel="noopener">Открыть группу во ВКонтакте →</a></div>
</div>
</body>
</html>
"""

PHOTOS_TMPL = """<section class="section" style="padding:0 0 48px">
  <div class="wrap" style="max-width:820px">
    <h2>Примеры работ по направлению</h2>
    <p class="section__desc" style="margin-bottom:22px">Фотографии из нашего цеха. Больше проектов — в <a href="../index.html#works" style="color:var(--accent)">галерее работ</a> и в <a href="https://vk.com/geometriyakuzova" target="_blank" rel="noopener" style="color:var(--accent)">группе ВКонтакте</a>.</p>
    <div class="works works--service">
{items}
    </div>
  </div>
</section>"""

PHOTO_ITEM = """      <figure class="work reveal" data-cat="all" data-full="../img/works/_{pid}.jpg" data-title="{cap}" data-desc="{cap} — ГЕОМЕТРИЯ КУЗОВА, Челябинск" data-link="https://vk.com/geometriyakuzova">
        <img src="../img/works/_{pid}.jpg" alt="{cap} — {h1} в Челябинске" loading="lazy">
        <figcaption class="work__cap"><div class="work__title">{cap}</div></figcaption>
        <span class="work__zoom">⤢</span>
      </figure>"""


def main():
    for s in SERVICES:
        seo_path = os.path.join(SEO, s["slug"] + ".html")
        if not os.path.exists(seo_path):
            print("НЕТ SEO-файла:", seo_path)
            continue
        seo = open(seo_path, encoding="utf-8").read().strip()

        items = "\n".join(
            PHOTO_ITEM.format(pid="113402547_" + pid, cap=cap, h1=s["h1"]) for pid, cap in s["photos"]
            if os.path.exists(os.path.join(SITE, "img", "works", "_113402547_" + pid + ".jpg"))
        )
        photos_section = PHOTOS_TMPL.format(items=items) if items else ""

        html = PAGE.format(**{k: v for k, v in s.items() if k != "photos"},
                            photos_section=photos_section, seo=seo)
        with open(os.path.join(USLUGI, s["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"OK {s['slug']}.html — фото: {items.count('<figure')}")


if __name__ == "__main__":
    main()
