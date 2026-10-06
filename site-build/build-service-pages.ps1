# ============================================================
#  ГЕОМЕТРИЯ КУЗОВА — пересборка страниц услуг
# ============================================================
#  ВАЖНО: этот скрипт пересобирает ТОЛЬКО страницы услуг
#  (geometriya-kuzova/uslugi/*.html) из SEO-текстов в папке seo\.
#  Главную страницу (index.html) он НЕ трогает — она содержит
#  галерею работ и правится вручную.
#
#  Старый полный генератор сохранён как build-site.legacy.ps1
#  и НЕ должен запускаться повторно: он затрёт галерею, логотип,
#  SEO-тексты и privacy.html.
# ============================================================
$ErrorActionPreference = "Stop"

$py = "C:\Users\vyazi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path $py)) { $py = "python" }

& $py "$PSScriptRoot\rebuild_service_pages.py"

Write-Host ""
Write-Host "Страницы услуг пересобраны из seo\*.html" -ForegroundColor Green
Write-Host "Проверка ссылок:  $py $PSScriptRoot\_verify_site.py" -ForegroundColor Cyan
