# ГЕОМЕТРИЯ КУЗОВА — сайт

Кузовной ремонт в Челябинске, ул. Каслинская 1/1.
Телефоны: +7 (922) 632-60-30, +7 (351) 683-12-05. Ежедневно 10:00–20:00.

## Структура

```
geometriya-kuzova/
├─ index.html          — главная: hero, услуги, «Почему мы», галерея работ, процесс, отзывы, FAQ, контакты
├─ privacy.html        — политика конфиденциальности
├─ style.css           — стили (тёмная тема, адаптив)
├─ app.js              — Telegram-форма с фото, фильтр галереи, лайтбокс, кнопка «наверх»
├─ robots.txt
├─ sitemap.xml
├─ img/
│  ├─ logo.jpg / logo-200.jpg / logo-360.jpg  — логотип из группы ВК
│  ├─ favicon.ico / favicon.png               — иконка сайта
│  ├─ og-cover.jpg                            — превью для соцсетей (og:image)
│  └─ works/                                  — 438 фото работ из группы ВК
└─ uslugi/             — 10 страниц услуг (SEO-тексты 600–800 слов + фото примеров)
```

## Галерея работ

Блок `#works` на главной: 18 фото с фильтрами (после ДТП / покраска / коррозия и сварка / бамперы),
клик открывает лайтбокс со ссылкой на исходный пост ВК. Источник — группа
https://vk.com/geometriyakuzova (id 113402547).

## Страницы услуг (10)

| Страница | Тема | Цена |
|---|---|---|
| remont-bamperov.html | Ремонт бамперов и пластика | от 1 000 ₽ |
| lokalnaya-pokraska.html | Локальная покраска элемента | от 5 000 ₽ |
| pokraska-elementa.html | Покраска элемента кузова | от 12 000 ₽ |
| udalenie-korrozii.html | Удаление коррозии | от 1 000 ₽ |
| zhestyanye-raboty.html | Жестяные работы | от 3 000 ₽ |
| zamena-arok.html | Замена арок | от 2 500 ₽ |
| zamena-porogov.html | Замена порогов | от 4 500 ₽ |
| zamena-privarnyh-paneley.html | Замена приварных панелей | от 5 000 ₽ |
| svarochnye-raboty.html | Сварочные работы | от 1 000 ₽ |
| vosstanovlenie-geometrii.html | Восстановление геометрии кузова | от 5 000 ₽ |

Тексты страниц лежат в `../seo/<slug>.html` (HTML-фрагменты, 600–800 слов каждый) и вставляются
в шаблон скриптом `../rebuild_service_pages.py`.

## Что нужно сделать перед публикацией

1. **Яндекс.Метрика:** замените `XXXXXXXX` на номер счётчика в `index.html` (2 места) и `app.js` (1 место).
2. **Telegram-бот:** в `app.js` замените `YOUR_BOT_TOKEN_HERE` и `YOUR_CHAT_ID_HERE`.
   Форма отправляет заявку текстом и приложенные фото через `sendPhoto`.
3. **Домен:** замените `geometriya-kuzova.ru` на реальный (canonical, og:image, Schema.org, sitemap.xml, robots.txt).
4. **Проверить телефоны и ссылки** на 2ГИС/Яндекс.Карты.
5. **Загрузить сайт на хостинг** и отправить sitemap.xml в Яндекс.Вебмастер и Google Search Console.

## Инструменты пересборки (папка site-build)

| Файл | Назначение |
|---|---|
| `fetch_vk_photos.py` | собирает посты и фото из группы ВК (Googlebot UA) в `_vk_catalog_v2.json` |
| `download_vk_photos_v2.py` | скачивает фото в `geometriya-kuzova/img/works/` |
| `rebuild_service_pages.py` | пересобирает 10 страниц услуг из `seo/*.html` |
| `build-service-pages.ps1` | обёртка над `rebuild_service_pages.py` |
| `_verify_site.py` | проверяет битые ссылки, картинки и анкоры |

> **Важно:** `build-site.legacy.ps1` — старый полный генератор. При повторном запуске он затрёт
> галерею, логотип, SEO-тексты и privacy.html. Не запускайте его.

## Как открыть локально

Двойной клик по `index.html` или локальный сервер:

```
python -m http.server 8000 --directory geometriya-kuzova
```

## Как запустить Telegram-бота

1. @BotFather → `/newbot` → получите TOKEN
2. Напишите боту `/start`, откройте `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Найдите `"chat":{"id":XXXXXXXX}` — это CHAT_ID
4. Вставьте TOKEN и CHAT_ID в `app.js`
