# Публикация сайта и работа с репозиторием

**Сайт уже опубликован:** https://wolfkiller32-code.github.io/geometriya-kuzova/

Репозиторий: https://github.com/wolfkiller32-code/geometriya-kuzova (публичный)
Ветка: `main`. Сайт лежит **в корне репозитория** — GitHub Pages отдаёт его как есть.

## Как сайт публикуется

GitHub Pages настроен на публикацию из ветки `main`, папка `/ (root)`.
Любой `git push` в `main` автоматически обновляет сайт в интернете (1–2 минуты).

## Как вносить изменения (командная строка)

```powershell
cd "C:\Сайт кузовн"
git add -A
git commit -m "Кратко: что изменили"
git push
```

Пароль вводить не нужно — авторизация настроена через GitHub CLI (`gh auth setup-git`).

Проверить, что всё отправлено: `git status` → должно быть `nothing to commit, working tree clean`.
Через пару минут изменения появятся на https://wolfkiller32-code.github.io/geometriya-kuzova/

## Как откатить неудачное изменение

```powershell
git log --oneline            # посмотреть историю
git revert <хеш-коммита>     # отменить конкретный коммит
git checkout -- <файл>       # отменить правки в файле
```

## Свой домен (необязательно)

Если купите домен (например, `geometriya-kuzova.ru`):
1. В репозитории: **Settings → Pages → Custom domain** → введите домен → Save.
2. У регистратора домена добавьте CNAME-запись: `www` → `wolfkiller32-code.github.io`,
   либо A-записи на IP GitHub Pages (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153).
3. Включите **Enforce HTTPS**.
4. После привязки домена замените `geometriya-kuzova.ru` в файлах сайта на реальный домен.

## Другие варианты хостинга (альтернатива)

### Netlify
1. netlify.com → **Add new site → Import an existing project → GitHub** → `geometriya-kuzova`.
2. **Build command:** пусто, **Publish directory:** `.` (точка — корень репозитория).
3. Deploy → адрес вида `https://имя.netlify.app`.

### Vercel
1. vercel.com → **Add New → Project → Import Git Repository** → `geometriya-kuzova`.
2. **Root Directory:** `.`, Framework Preset: **Other**. Deploy.

### Cloudflare Pages
1. dash.cloudflare.com → **Workers & Pages → Create → Pages → Connect to Git**.
2. **Build output directory:** `.`
Тогда: **Settings → Pages → Source: Deploy from a branch → main → / (root)**.
Учтите: сайт лежит в подпапке, поэтому Pages отдаст корневой `index.html` (старая версия).
Правильнее перенести папку `site-build/geometriya-kuzova/*` в корень репозитория.

## Что заменить перед публикацией

| Что | Где | На что заменить |
|---|---|---|
| Номер счётчика Яндекс.Метрики | `index.html` (2 места), `app.js` (1) | `XXXXXXXX` → ваш номер |
| Токен Telegram-бота | `app.js` | `YOUR_BOT_TOKEN_HERE` |
| ID чата Telegram | `app.js` | `YOUR_CHAT_ID_HERE` |
| Домен | `index.html`, `privacy.html`, `uslugi/*.html`, `sitemap.xml`, `robots.txt` | `geometriya-kuzova.ru` → ваш домен |

После смены домена обновите `sitemap.xml` и отправьте его в Яндекс.Вебмастер и Google Search Console.

## Структура репозитория

```
.
├─ index.html                 # ранняя версия сайта (одним файлом, архив)
└─ site-build/
   ├─ geometriya-kuzova/      # ← АКТУАЛЬНЫЙ САЙТ (публиковать эту папку)
   │  ├─ index.html           # главная с галереей работ
   │  ├─ privacy.html
   │  ├─ style.css, app.js
   │  ├─ robots.txt, sitemap.xml, README.md
   │  ├─ img/                 # логотип, favicon, og-обложка
   │  └─ img/works/           # 438 фото работ из ВК
   ├─ seo/                    # SEO-тексты страниц услуг (600–800 слов)
   ├─ fetch_vk_photos.py      # сбор фото из группы ВК
   ├─ download_vk_photos_v2.py
   ├─ build_works_section.py  # генерация блока галереи
   ├─ rebuild_service_pages.py# пересборка страниц услуг
   ├─ build-service-pages.ps1
   ├─ _verify_site.py         # проверка ссылок и картинок
   └─ REPORT.md               # отчёт по правкам сайта

⚠️ build-site.legacy.ps1 — старый генератор. Не запускать: затрёт галерею,
   логотип, SEO-тексты и privacy.html.
```

## GitHub Desktop

Приложение установлено, но на этом компьютере не запускается (Electron завершается
сразу после старта, в логе — `Failed trying to find Git on PATH`). Рабочая схема —
командная строка GitHub CLI, она уже настроена и проверена.
