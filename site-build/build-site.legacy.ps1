﻿$ErrorActionPreference = "Stop"

$root = "geometriya-kuzova"
$uslugi = Join-Path $root "uslugi"
New-Item -ItemType Directory -Force -Path $uslugi | Out-Null

# ============================================================
# style.css
# ============================================================
$css = @'
:root{
  --graphite:#14161A; --graphite-2:#1C1F26; --graphite-3:#262A33;
  --line:#2E333D; --metal:#A8B0BD; --muted:#7A8290;
  --white:#FFFFFF; --accent:#FF6B1A;
  --radius:14px; --radius-sm:10px; --max:1200px;
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--graphite);color:var(--white);line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer;border:none}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}

.header{position:sticky;top:0;z-index:100;background:rgba(20,22,26,.85);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.header__inner{display:flex;align-items:center;justify-content:space-between;height:72px;gap:24px}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;letter-spacing:-.3px}
.logo__mark{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--accent),#FF9A4D);display:grid;place-items:center;font-size:16px;font-weight:800;color:#14161A}
.nav{display:flex;gap:28px;font-size:15px;color:var(--metal)}
.nav a{transition:color .2s}
.nav a:hover{color:var(--white)}
.header__right{display:flex;align-items:center;gap:16px}
.header__phone{font-weight:600;font-size:15px;white-space:nowrap;transition:color .2s}
.header__phone:hover{color:var(--accent)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:13px 24px;border-radius:var(--radius-sm);font-size:15px;font-weight:600;transition:transform .15s,background .2s,box-shadow .2s;white-space:nowrap}
.btn--primary{background:var(--accent);color:#14161A}
.btn--primary:hover{background:#FF7D33;transform:translateY(-1px);box-shadow:0 8px 24px rgba(255,107,26,.3)}
.btn--ghost{background:transparent;color:var(--white);border:1px solid var(--line)}
.btn--ghost:hover{border-color:var(--metal);background:rgba(255,255,255,.04)}
.btn--lg{padding:17px 34px;font-size:16px}

.breadcrumbs{padding:16px 0;font-size:13.5px;color:var(--muted)}
.breadcrumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.breadcrumbs li{display:flex;align-items:center;gap:8px}
.breadcrumbs li:not(:last-child)::after{content:"→";color:var(--line);font-size:12px}
.breadcrumbs a{color:var(--metal);transition:color .2s}
.breadcrumbs a:hover{color:var(--accent)}
.breadcrumbs [aria-current="page"]{color:var(--white);font-weight:500}

.hero{position:relative;padding:80px 0 90px;overflow:hidden}
.hero::before{content:"";position:absolute;top:-30%;right:-15%;width:800px;height:800px;border-radius:50%;background:radial-gradient(circle,rgba(255,107,26,.12),transparent 65%);pointer-events:none}
.hero__grid{display:grid;grid-template-columns:1.15fr .85fr;gap:60px;align-items:center;position:relative}
.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:99px;background:rgba(255,107,26,.1);border:1px solid rgba(255,107,26,.25);color:var(--accent);font-size:13px;font-weight:600;margin-bottom:24px}
.eyebrow::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent)}
h1{font-size:clamp(34px,4.6vw,58px);line-height:1.08;font-weight:800;letter-spacing:-1.5px;margin-bottom:22px}
h1 .accent{color:var(--accent)}
.hero__sub{font-size:17px;color:var(--metal);max-width:520px;margin-bottom:34px;line-height:1.6}
.hero__cta{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:38px}
.hero__stats{display:flex;gap:40px;flex-wrap:wrap}
.stat__num{font-size:26px;font-weight:800;letter-spacing:-.5px}
.stat__num span{color:var(--accent)}
.stat__label{font-size:13px;color:var(--muted);margin-top:2px}

.hero__card{background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius);padding:28px;position:relative}
.hero__card h3{font-size:17px;margin-bottom:6px;font-weight:700}
.hero__card p{font-size:14px;color:var(--muted);margin-bottom:20px}
.field{margin-bottom:14px}
.field label{display:block;font-size:13px;color:var(--metal);margin-bottom:6px}
.field input,.field select,.field textarea{width:100%;padding:12px 14px;border-radius:var(--radius-sm);background:var(--graphite);border:1px solid var(--line);color:var(--white);font-size:15px;font-family:inherit;transition:border-color .2s,box-shadow .2s}
.field input:focus,.field select:focus,.field textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,107,26,.12)}
.field textarea{resize:vertical;min-height:70px}
.field select{appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='%237A8290' d='M6 8 0 0h12z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center}
.upload{display:flex;align-items:center;gap:12px;padding:14px;border:1.5px dashed var(--line);border-radius:var(--radius-sm);color:var(--muted);font-size:14px;cursor:pointer;transition:border-color .2s,background .2s}
.upload:hover{border-color:var(--accent);background:rgba(255,107,26,.04)}
.upload input{display:none}
.upload__icon{width:34px;height:34px;border-radius:8px;background:var(--graphite-3);display:grid;place-items:center;flex-shrink:0;color:var(--accent)}
.hero__card .btn{width:100%;margin-top:8px}
.form__note{font-size:12px;color:var(--muted);text-align:center;margin-top:12px}

.section{padding:90px 0;border-top:1px solid var(--line)}
.section__head{max-width:640px;margin-bottom:52px}
.section__tag{font-size:13px;color:var(--accent);font-weight:600;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px}
h2{font-size:clamp(26px,3.2vw,40px);line-height:1.15;font-weight:800;letter-spacing:-1px;margin-bottom:16px}
.section__desc{color:var(--metal);font-size:16px}

.services{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.service{background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius);padding:28px;transition:border-color .25s,transform .25s;position:relative;overflow:hidden}
.service:hover{border-color:#3E4552;transform:translateY(-3px)}
.service__icon{width:44px;height:44px;border-radius:11px;background:linear-gradient(135deg,rgba(255,107,26,.15),rgba(255,107,26,.05));border:1px solid rgba(255,107,26,.25);display:grid;place-items:center;margin-bottom:18px;font-size:20px}
.service h3{font-size:18px;margin-bottom:10px;font-weight:700;letter-spacing:-.3px}
.service p{font-size:14.5px;color:var(--metal);line-height:1.6;margin-bottom:18px}
.service__meta{display:flex;justify-content:space-between;align-items:center;padding-top:16px;border-top:1px solid var(--line);font-size:13px}
.service__price{font-weight:700;color:var(--white)}
.service__time{color:var(--muted)}
.service a.link{display:inline-flex;align-items:center;gap:6px;margin-top:12px;font-size:14px;color:var(--accent);font-weight:600;transition:gap .2s}
.service a.link:hover{gap:10px}
.service a.link::after{content:"→"}

.ba{position:relative;border-radius:var(--radius);overflow:hidden;aspect-ratio:16/10;user-select:none;touch-action:none;border:1px solid var(--line);background:var(--graphite-2);cursor:ew-resize}
.ba__layer{position:absolute;inset:0;display:grid;place-items:center}
.ba__before{background:repeating-linear-gradient(45deg,rgba(255,255,255,.02) 0 12px,transparent 12px 24px),linear-gradient(140deg,#2A2119,#1A1A1F 60%,#0F1114)}
.ba__after{background:radial-gradient(ellipse at 40% 35%,rgba(255,107,26,.18),transparent 55%),linear-gradient(140deg,#1F2733,#14171C 60%,#0F1114);clip-path:inset(0 50% 0 0)}
.ba__label{position:absolute;top:16px;padding:6px 14px;border-radius:99px;font-size:12px;font-weight:700;letter-spacing:1px;backdrop-filter:blur(8px)}
.ba__before .ba__label{left:16px;background:rgba(120,120,120,.35);color:#E6E6E6}
.ba__after .ba__label{right:16px;background:rgba(255,107,26,.9);color:#14161A}
.ba__ph{color:#525A68;font-size:13px;text-align:center;line-height:1.6;padding:20px;max-width:280px}
.ba__ph b{color:#8A93A3;display:block;font-size:15px;margin-bottom:6px;font-weight:600}
.ba__handle{position:absolute;top:0;bottom:0;left:50%;width:2px;background:var(--accent);transform:translateX(-50%);pointer-events:none;box-shadow:0 0 20px rgba(255,107,26,.6)}
.ba__grip{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:var(--accent);display:grid;place-items:center;color:#14161A;font-weight:700;font-size:16px;box-shadow:0 6px 20px rgba(0,0,0,.5)}
.ba__caption{position:absolute;bottom:0;left:0;right:0;padding:16px 20px;background:linear-gradient(transparent,rgba(10,11,13,.92));font-size:14px;display:flex;justify-content:space-between;align-items:flex-end;gap:16px;pointer-events:none}
.ba__caption strong{font-weight:600}
.ba__caption span{color:var(--muted);font-size:13px;white-space:nowrap}
.ba-grid{display:grid;grid-template-columns:2fr 1fr;gap:20px}
.ba-side{display:flex;flex-direction:column;gap:20px}

.process{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;counter-reset:step}
.step{position:relative;padding:26px 22px 22px;background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius)}
.step::before{counter-increment:step;content:"0" counter(step);position:absolute;top:-14px;left:22px;font-size:13px;font-weight:800;letter-spacing:1px;background:var(--accent);color:#14161A;padding:4px 10px;border-radius:6px}
.step h3{font-size:16px;margin:10px 0 8px;font-weight:700}
.step p{font-size:14px;color:var(--metal);line-height:1.6}
.step__time{display:block;margin-top:14px;font-size:12.5px;color:var(--accent);font-weight:600}

.guarantees{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.guarantee{display:flex;gap:16px;padding:24px;background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius)}
.guarantee__icon{width:40px;height:40px;flex-shrink:0;border-radius:10px;background:rgba(255,107,26,.1);border:1px solid rgba(255,107,26,.2);display:grid;place-items:center;font-size:18px}
.guarantee h3{font-size:15.5px;margin-bottom:6px;font-weight:700}
.guarantee p{font-size:14px;color:var(--metal);line-height:1.6}

.reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.review{background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius);padding:26px;display:flex;flex-direction:column}
.review__stars{color:var(--accent);font-size:15px;margin-bottom:14px;letter-spacing:2px}
.review__text{font-size:15px;color:#D4D9E0;line-height:1.65;flex:1;margin-bottom:20px}
.review__author{display:flex;align-items:center;gap:12px;padding-top:18px;border-top:1px solid var(--line)}
.review__avatar{width:38px;height:38px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,var(--graphite-3),#333944);display:grid;place-items:center;font-weight:700;font-size:14px;color:var(--metal)}
.review__name{font-size:14px;font-weight:600}
.review__car{font-size:12.5px;color:var(--muted)}

.faq{max-width:820px;margin:0 auto}
.faq details{background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius-sm);margin-bottom:12px;overflow:hidden;transition:border-color .2s}
.faq details[open]{border-color:#3E4552}
.faq summary{padding:20px 24px;cursor:pointer;list-style:none;font-size:16px;font-weight:600;display:flex;justify-content:space-between;align-items:center;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:22px;color:var(--accent);font-weight:400;transition:transform .25s;flex-shrink:0}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq__body{padding:0 24px 22px;color:var(--metal);font-size:15px;line-height:1.7}

.cta{background:linear-gradient(140deg,var(--graphite-2),#191C22);border:1px solid var(--line);border-radius:20px;padding:56px;display:grid;grid-template-columns:1fr 1fr;gap:52px;align-items:center;position:relative;overflow:hidden}
.cta::before{content:"";position:absolute;top:-50%;left:-10%;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(255,107,26,.1),transparent 65%)}
.cta__content{position:relative}
.cta h2{margin-bottom:16px}
.cta p{color:var(--metal);margin-bottom:28px;font-size:16px}
.cta__contacts{display:flex;flex-direction:column;gap:14px;position:relative}
.cta__item{display:flex;align-items:center;gap:14px;padding:16px 20px;background:var(--graphite);border:1px solid var(--line);border-radius:var(--radius-sm);transition:border-color .2s}
.cta__item:hover{border-color:var(--accent)}
.cta__item-icon{width:36px;height:36px;border-radius:9px;background:var(--graphite-3);display:grid;place-items:center;flex-shrink:0}
.cta__item-label{font-size:12.5px;color:var(--muted)}
.cta__item-value{font-size:15.5px;font-weight:600}

.footer{border-top:1px solid var(--line);padding:48px 0 90px;margin-top:20px}
.footer__grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:40px;margin-bottom:36px}
.footer__desc{color:var(--muted);font-size:14px;line-height:1.7;margin-top:16px;max-width:320px}
.footer h4{font-size:14px;margin-bottom:16px;font-weight:700}
.footer ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer ul a{font-size:14px;color:var(--metal);transition:color .2s}
.footer ul a:hover{color:var(--accent)}
.footer__bottom{padding-top:24px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted)}

.mobile-bar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:99;background:rgba(20,22,26,.96);backdrop-filter:blur(14px);border-top:1px solid var(--line);padding:12px 16px;gap:12px}
.mobile-bar .btn{flex:1;padding:14px}

.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.reveal.in{opacity:1;transform:none}

@media(max-width:1024px){
  .hero__grid{grid-template-columns:1fr;gap:44px}
  .hero__card{max-width:520px}
  .services,.guarantees,.reviews{grid-template-columns:repeat(2,1fr)}
  .process{grid-template-columns:repeat(2,1fr)}
  .ba-grid{grid-template-columns:1fr}
  .cta{grid-template-columns:1fr;gap:36px;padding:40px}
  .footer__grid{grid-template-columns:1fr 1fr}
  .nav{display:none}
}
@media(max-width:680px){
  .wrap{padding:0 18px}
  .section{padding:64px 0}
  .services,.guarantees,.reviews,.process{grid-template-columns:1fr}
  .hero{padding:52px 0 64px}
  .hero__stats{gap:28px}
  .header__phone{display:none}
  .header .btn{display:none}
  .mobile-bar{display:flex}
  body{padding-bottom:70px}
  .cta{padding:30px 24px;border-radius:16px}
  .footer__grid{grid-template-columns:1fr;gap:32px}
  .footer{padding-bottom:40px}
  .ba{aspect-ratio:4/3}
}
'@
Set-Content -Path (Join-Path $root "style.css") -Value $css -Encoding UTF8

# ============================================================
# app.js
# ============================================================
$js = @'
// ================== TELEGRAM LEAD FORM ==================
// ИНСТРУКЦИЯ:
// 1. Создайте бота через @BotFather, получите TOKEN
// 2. Напишите боту /start, откройте:
//    https://api.telegram.org/bot<TOKEN>/getUpdates
// 3. Найдите "chat":{"id":XXXXXXXX} — это CHAT_ID
// 4. Замените значения ниже:
const TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE';
const TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID_HERE';
const YM_COUNTER_ID = 'XXXXXXXX'; // номер счётчика Яндекс.Метрики

window.sendToTelegram = async function(event) {
  event.preventDefault();
  const form = document.getElementById('leadForm');
  const btn = form.querySelector('.btn');
  const originalText = btn.textContent;
  btn.textContent = 'Отправляем...';
  btn.disabled = true;

  const name = form.querySelector('[name="name"]').value;
  const phone = form.querySelector('[name="phone"]').value;
  const service = form.querySelector('[name="service"]').value;

  const message = '🔔 Новая заявка с сайта\n━━━━━━━━━━━━━━━━\n👤 Имя: ' + name +
                  '\n📞 Телефон: ' + phone + '\n🛠 Услуга: ' + service;

  try {
    const response = await fetch('https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text: message, parse_mode: 'HTML' })
    });
    if (response.ok) {
      btn.textContent = 'Заявка отправлена ✓';
      btn.style.background = '#2BA84A';
      if (typeof ym === 'function') ym(YM_COUNTER_ID, 'reachGoal', 'lead_form_submit');
      form.reset();
      setTimeout(() => { btn.textContent = originalText; btn.style.background=''; btn.disabled=false; }, 4000);
    } else { throw new Error('err'); }
  } catch (e) {
    btn.textContent = 'Ошибка. Попробуйте ещё раз';
    btn.style.background = '#E53E3E';
    btn.disabled = false;
    setTimeout(() => { btn.textContent = originalText; btn.style.background=''; }, 3000);
  }
  return false;
};

// ================== BEFORE / AFTER SLIDER ==================
document.querySelectorAll('[data-ba]').forEach(ba => {
  const top = ba.querySelector('.ba__after');
  const handle = ba.querySelector('.ba__handle');
  let dragging = false;
  const setPos = (clientX) => {
    const rect = ba.getBoundingClientRect();
    let x = (clientX - rect.left) / rect.width;
    x = Math.max(0.02, Math.min(0.98, x));
    top.style.clipPath = 'inset(0 ' + (100 - x*100) + '% 0 0)';
    handle.style.left = (x*100) + '%';
  };
  ba.addEventListener('pointerdown', e => { dragging = true; setPos(e.clientX); ba.setPointerCapture(e.pointerId); });
  ba.addEventListener('pointermove', e => { if (dragging) setPos(e.clientX); });
  ba.addEventListener('pointerup', () => dragging = false);
  ba.addEventListener('pointercancel', () => dragging = false);
});

// ================== REVEAL ON SCROLL ==================
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach((el, i) => {
  el.style.transitionDelay = ((i % 3) * 80) + 'ms';
  io.observe(el);
});

// ================== SMOOTH ANCHORS ==================
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id === '#' || id.length < 2) return;
    const target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    const y = target.getBoundingClientRect().top + window.pageYOffset - 80;
    window.scrollTo({ top: y, behavior: 'smooth' });
  });
});
'@
Set-Content -Path (Join-Path $root "app.js") -Value $js -Encoding UTF8

# ============================================================
# index.html
# ============================================================
$index = @'
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Кузовной ремонт в Челябинске — ГЕОМЕТРИЯ КУЗОВА | ул. Каслинская 1/1</title>
<meta name="description" content="Кузовной ремонт в Челябинске: покраска, жестяные работы, сварка, восстановление геометрии, ремонт бамперов. ул. Каслинская 1/1. Тел: +7 (922) 632-60-30. Бесплатная оценка по фото.">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0E1013">
<link rel="canonical" href="https://geometriya-kuzova.ru/">
<link rel="stylesheet" href="style.css">
<meta property="og:title" content="Кузовной ремонт в Челябинске — ГЕОМЕТРИЯ КУЗОВА">
<meta property="og:description" content="Полный цикл кузовного ремонта и покраски. ул. Каслинская 1/1.">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
    m[i].l=1*new Date();
    for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
    k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
    (window, document,'script','https://mc.yandex.ru/metrika/tag.js', 'ym');
    ym('XXXXXXXX', 'init', {clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/XXXXXXXX" style="position:absolute; left:-9999px;" alt=""></div></noscript>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AutoBodyShop","name":"ГЕОМЕТРИЯ КУЗОВА","telephone":"+7 (922) 632-60-30","priceRange":"$$","address":{"@type":"PostalAddress","streetAddress":"ул. Каслинская, 1/1","addressLocality":"Челябинск","addressCountry":"RU"},"sameAs":["https://vk.ru/geometriyakuzova","https://2gis.ru/chelyabinsk/firm/70000001114689029","https://yandex.ru/maps/-/CXeXa0mg","https://www.instagram.com/geometriya_kuzova"],"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"10:00","closes":"20:00"}}
</script>
</head>
<body>

<header class="header">
  <div class="wrap header__inner">
    <a href="/" class="logo"><span class="logo__mark">Г</span>ГЕОМЕТРИЯ КУЗОВА</a>
    <nav class="nav">
      <a href="#services">Услуги</a>
      <a href="#works">Работы</a>
      <a href="#process">Процесс</a>
      <a href="#reviews">Отзывы</a>
      <a href="#contacts">Контакты</a>
    </nav>
    <div class="header__right">
      <a href="tel:+79226326030" class="header__phone">+7 (922) 632-60-30</a>
      <a href="#estimate" class="btn btn--primary">Оценить ремонт</a>
    </div>
  </div>
</header>

<nav class="breadcrumbs" aria-label="Хлебные крошки">
  <div class="wrap"><ol><li aria-current="page">Главная</li></ol></div>
</nav>

<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <div class="eyebrow">Кузовной ремонт в Челябинске · ул. Каслинская 1/1</div>
      <h1>Вернём вашему автомобилю <span class="accent">заводскую геометрию</span> и безупречный вид.</h1>
      <p class="hero__sub">Полный цикл кузовного ремонта и покраски любой сложности. Ремонт бамперов, удаление коррозии, жестяные и сварочные работы, восстановление геометрии. Бесплатная консультация и оценка стоимости.</p>
      <div class="hero__cta">
        <a href="#estimate" class="btn btn--primary btn--lg">Рассчитать по фото</a>
        <a href="#works" class="btn btn--ghost btn--lg">Смотреть работы</a>
      </div>
      <div class="hero__stats">
        <div class="stat"><div class="stat__num">10<span>+ лет</span></div><div class="stat__label">опыт работы</div></div>
        <div class="stat"><div class="stat__num">700<span> м²</span></div><div class="stat__label">современный кузовной цех</div></div>
        <div class="stat"><div class="stat__num">4.8<span> / 5</span></div><div class="stat__label">рейтинг на 2ГИС и Яндекс</div></div>
      </div>
    </div>

    <div class="hero__card" id="estimate">
      <h3>Бесплатная оценка по фото</h3>
      <p>Пришлите фото повреждения — вернёмся с расчётом стоимости и сроков.</p>
      <form id="leadForm" onsubmit="return sendToTelegram(event)">
        <div class="field">
          <label for="svc">Что нужно сделать</label>
          <select id="svc" name="service">
            <option value="Ремонт бампера и пластика">Ремонт бампера и пластика</option>
            <option value="Локальная покраска элемента">Локальная покраска элемента</option>
            <option value="Покраска элемента">Покраска элемента</option>
            <option value="Удаление коррозии">Удаление коррозии</option>
            <option value="Жестяные работы">Жестяные работы</option>
            <option value="Замена арок / порогов">Замена арок / порогов</option>
            <option value="Замена приварных панелей">Замена приварных панелей</option>
            <option value="Сварочные работы">Сварочные работы</option>
            <option value="Восстановление геометрии">Восстановление геометрии</option>
          </select>
        </div>
        <div class="field"><label for="name">Имя</label><input type="text" id="name" name="name" placeholder="Как к вам обращаться" required></div>
        <div class="field"><label for="phone">Телефон</label><input type="tel" id="phone" name="phone" placeholder="+7 (___) ___-__-__" required></div>
        <label class="upload"><input type="file" id="photo" accept="image/*" multiple><span class="upload__icon">📷</span><span>Прикрепить фото повреждения</span></label>
        <button type="submit" class="btn btn--primary">Получить расчёт</button>
      </form>
      <p class="form__note">Нажимая кнопку, вы соглашаетесь с политикой конфиденциальности</p>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="section__head reveal">
      <div class="section__tag">Услуги</div>
      <h2>Полный цикл кузовных работ</h2>
      <p class="section__desc">От локальной покраски до восстановления геометрии после серьёзного ДТП — на одном участке.</p>
    </div>
    <div class="services">
      <div class="service reveal"><div class="service__icon">🛠</div><h3>Ремонт бамперов и пластика</h3><p>От мелких трещин до серьёзных повреждений — вернём вашим пластиковым элементам первозданный вид.</p><div class="service__meta"><span class="service__price">от 1 000 ₽</span><span class="service__time">1–2 дня</span></div><a class="link" href="uslugi/remont-bamperov.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">🎨</div><h3>Локальная покраска элемента</h3><p>Идеальное решение для устранения небольших дефектов без полной покраски.</p><div class="service__meta"><span class="service__price">от 5 000 ₽</span><span class="service__time">1 день</span></div><a class="link" href="uslugi/lokalnaya-pokraska.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">✨</div><h3>Покраска элемента</h3><p>Полное обновление внешнего вида одного или нескольких элементов кузова.</p><div class="service__meta"><span class="service__price">от 12 000 ₽</span><span class="service__time">2–3 дня</span></div><a class="link" href="uslugi/pokraska-elementa.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">🔧</div><h3>Удаление коррозии</h3><p>Остановим ржавчину и защитим ваш автомобиль от дальнейшего разрушения.</p><div class="service__meta"><span class="service__price">от 1 000 ₽</span><span class="service__time">1–2 дня</span></div><a class="link" href="uslugi/udalenie-korrozii.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">💪</div><h3>Жестяные работы</h3><p>Восстановим форму кузова после вмятин и деформаций.</p><div class="service__meta"><span class="service__price">от 3 000 ₽</span><span class="service__time">от 1 дня</span></div><a class="link" href="uslugi/zhestyanye-raboty.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">🔩</div><h3>Замена арок и порогов</h3><p>Вернём целостность и эстетику колесных арок и нижней части кузова.</p><div class="service__meta"><span class="service__price">от 2 500 ₽</span><span class="service__time">от 2 дней</span></div><a class="link" href="uslugi/zamena-arok.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">⚙️</div><h3>Замена приварных панелей</h3><p>Профессиональная замена любых приварных элементов кузова.</p><div class="service__meta"><span class="service__price">от 5 000 ₽</span><span class="service__time">от 3 дней</span></div><a class="link" href="uslugi/zamena-privarnyh-paneley.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">🔥</div><h3>Сварочные работы</h3><p>Качественное выполнение любых сварочных работ для восстановления кузова.</p><div class="service__meta"><span class="service__price">от 1 000 ₽</span><span class="service__time">от 1 дня</span></div><a class="link" href="uslugi/svarochnye-raboty.html">Подробнее об услуге</a></div>
      <div class="service reveal"><div class="service__icon">📐</div><h3>Восстановление геометрии</h3><p>Вернём вашему автомобилю идеальные заводские параметры кузова на стапеле.</p><div class="service__meta"><span class="service__price">от 5 000 ₽</span><span class="service__time">от 3 дней</span></div><a class="link" href="uslugi/vosstanovlenie-geometrii.html">Подробнее об услуге</a></div>
    </div>
  </div>
</section>

<section class="section" id="process">
  <div class="wrap">
    <div class="section__head reveal"><div class="section__tag">Процесс</div><h2>Как проходит ремонт</h2></div>
    <div class="process">
      <div class="step reveal"><h3>Заявка и фото</h3><p>Присылаете фото повреждения — получаете предварительный расчёт.</p><span class="step__time">15 минут</span></div>
      <div class="step reveal"><h3>Осмотр и смета</h3><p>Проводим дефектовку, согласовываем перечень работ и стоимость.</p><span class="step__time">30–60 минут</span></div>
      <div class="step reveal"><h3>Ремонт</h3><p>Геометрия → кузов → покраска → сборка. Отправляем фото на этапах.</p><span class="step__time">от 1 дня</span></div>
      <div class="step reveal"><h3>Выдача</h3><p>Проверяете результат, подписываете акт. Гарантия на все виды работ.</p><span class="step__time">30 минут</span></div>
    </div>
  </div>
</section>

<section class="section" id="reviews">
  <div class="wrap">
    <div class="section__head reveal"><div class="section__tag">Отзывы</div><h2>Что говорят клиенты</h2><p class="section__desc">Смотрите актуальные отзывы на 2ГИС и Яндекс.Картах.</p></div>
    <div class="reviews">
      <div class="review reveal"><div class="review__stars">★★★★★</div><p class="review__text">Сотрудник автосервиса грамотно объяснил плюсы и минусы процедуры. Персонал приветливый, общительный. Работы выполнили в срок.</p><div class="review__author"><div class="review__avatar">А</div><div><div class="review__name">Александр</div><div class="review__car">2ГИС · Челябинск</div></div></div></div>
      <div class="review reveal"><div class="review__stars">★★★★★</div><p class="review__text">Делали рихтовку капота и ТО. Всё сделали как надо, никаких претензий. Цены нормальные.</p><div class="review__author"><div class="review__avatar">М</div><div><div class="review__name">Михаил</div><div class="review__car">Яндекс.Карты · Челябинск</div></div></div></div>
      <div class="review reveal"><div class="review__stars">★★★★★</div><p class="review__text">Красили бампер, цвет сложный. Подобрали идеально, даже под солнцем не отличить. Дали гарантию.</p><div class="review__author"><div class="review__avatar">Д</div><div><div class="review__name">Дмитрий</div><div class="review__car">2ГИС · Челябинск</div></div></div></div>
    </div>
    <div style="text-align:center;margin-top:32px" class="reveal">
      <a href="https://2gis.ru/chelyabinsk/firm/70000001114689029" target="_blank" rel="noopener" class="btn btn--ghost btn--lg">Все отзывы на 2ГИС →</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal" style="max-width:820px;margin:0 auto 32px;text-align:center"><div class="section__tag">Вопросы</div><h2>Частые вопросы</h2></div>
    <div class="faq reveal">
      <details open><summary>Сколько времени займёт ремонт после ДТП?</summary><div class="faq__body">Зависит от объёма. Локальная покраска — 1–2 дня. Ремонт крыла с покраской — 3–4 дня. Восстановление геометрии — от 5 дней. Точный срок фиксируем после дефектовки.</div></details>
      <details><summary>Даёте ли гарантию на работы?</summary><div class="faq__body">Да, мы предоставляем гарантию на все виды кузовных и малярных работ. Конкретный срок уточняйте у мастера.</div></details>
      <details><summary>Можно ли отремонтировать бампер, а не покупать новый?</summary><div class="faq__body">В большинстве случаев — да. Паяем трещины, восстанавливаем крепления, красим в цвет кузова.</div></details>
      <details><summary>Как вы подбираете цвет краски?</summary><div class="faq__body">По коду краски + учитываем выгорание. Делаем выкрас на пробнике до начала покраски.</div></details>
      <details><summary>Где вы находитесь?</summary><div class="faq__body">г. Челябинск, ул. Каслинская, 1/1. Тел: +7 (922) 632-60-30.</div></details>
    </div>
  </div>
</section>

<section class="section" id="contacts">
  <div class="wrap">
    <div class="cta reveal">
      <div class="cta__content">
        <div class="section__tag">Контакты</div>
        <h2>Приезжайте на бесплатную дефектовку</h2>
        <p>Осмотр 30–60 минут, точная смета и сроки — сразу на месте.</p>
        <a href="tel:+79226326030" class="btn btn--primary btn--lg">Позвонить сейчас</a>
      </div>
      <div class="cta__contacts">
        <a href="tel:+79226326030" class="cta__item"><div class="cta__item-icon">📞</div><div><div class="cta__item-label">Телефон</div><div class="cta__item-value">+7 (922) 632-60-30</div></div></a>
        <a href="https://2gis.ru/chelyabinsk/firm/70000001114689029" target="_blank" rel="noopener" class="cta__item"><div class="cta__item-icon">📍</div><div><div class="cta__item-label">Адрес</div><div class="cta__item-value">г. Челябинск, ул. Каслинская, 1/1</div></div></a>
        <a href="https://vk.me/geometriyakuzova" target="_blank" rel="noopener" class="cta__item"><div class="cta__item-icon">💬</div><div><div class="cta__item-label">Написать в группу</div><div class="cta__item-value">vk.me/geometriyakuzova</div></div></a>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <div class="logo"><span class="logo__mark">Г</span>ГЕОМЕТРИЯ КУЗОВА</div>
        <p class="footer__desc">Кузовной ремонт легковых автомобилей в Челябинске. Полный цикл работ.</p>
        <div style="display:flex;gap:14px;margin-top:18px">
          <a href="https://vk.ru/geometriyakuzova" target="_blank" rel="noopener" style="color:var(--metal)">VK</a>
          <a href="https://www.instagram.com/geometriya_kuzova" target="_blank" rel="noopener" style="color:var(--metal)">IG</a>
          <a href="https://2gis.ru/chelyabinsk/firm/70000001114689029" target="_blank" rel="noopener" style="color:var(--metal)">2ГИС</a>
          <a href="https://yandex.ru/maps/-/CXeXa0mg" target="_blank" rel="noopener" style="color:var(--metal)">Яндекс</a>
        </div>
      </div>
      <div>
        <h4>Услуги</h4>
        <ul>
          <li><a href="uslugi/remont-bamperov.html">Ремонт бамперов</a></li>
          <li><a href="uslugi/pokraska-elementa.html">Покраска элементов</a></li>
          <li><a href="uslugi/zhestyanye-raboty.html">Жестяные работы</a></li>
          <li><a href="uslugi/svarochnye-raboty.html">Сварочные работы</a></li>
          <li><a href="uslugi/vosstanovlenie-geometrii.html">Восстановление геометрии</a></li>
        </ul>
      </div>
      <div>
        <h4>Информация</h4>
        <ul>
          <li><a href="#process">Процесс ремонта</a></li>
          <li><a href="#reviews">Отзывы</a></li>
          <li><a href="#">Политика конфиденциальности</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 ГЕОМЕТРИЯ КУЗОВА. Все права защищены.</span>
      <span>Не является публичной офертой</span>
    </div>
  </div>
</footer>

<div class="mobile-bar">
  <a href="tel:+79226326030" class="btn btn--ghost">📞 Позвонить</a>
  <a href="#estimate" class="btn btn--primary">Оценить по фото</a>
</div>

<script src="app.js"></script>
</body>
</html>
'@
Set-Content -Path (Join-Path $root "index.html") -Value $index -Encoding UTF8

# ============================================================
# SERVICE PAGES — генерация 10 страниц
# ============================================================

$services = @(
  @{Slug="remont-bamperov"; H1="Ремонт бамперов и пластика"; Title="Ремонт бампера в Челябинске — от 1 000 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Ремонт и пайка бамперов в Челябинске. Восстановление креплений, покраска в цвет кузова. ул. Каслинская 1/1. Тел: +7 (922) 632-60-30."; Price="от 1 000 ₽"; Time="1–2 дня"; Lead="Паяем трещины, восстанавливаем крепления, красим в цвет кузова. Не всегда нужно покупать новый бампер — часто дешевле отремонтировать."},
  @{Slug="lokalnaya-pokraska"; H1="Локальная покраска элемента"; Title="Локальная покраска автомобиля в Челябинске — от 5 000 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Локальная покраска элемента в Челябинске без полной покраски. Точный подбор цвета. ул. Каслинская 1/1."; Price="от 5 000 ₽"; Time="1 день"; Lead="Устраняем небольшие дефекты без полной покраски элемента — быстро, аккуратно и без риска несовпадения оттенка."},
  @{Slug="pokraska-elementa"; H1="Покраска элемента кузова"; Title="Покраска элемента кузова в Челябинске — от 12 000 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Покраска элементов кузова автомобиля в Челябинске. Подбор краски по коду, выкрас на пробнике."; Price="от 12 000 ₽"; Time="2–3 дня"; Lead="Полное обновление внешнего вида одного или нескольких элементов кузова с подбором краски по коду и выкрасом на пробнике."},
  @{Slug="udalenie-korrozii"; H1="Удаление коррозии"; Title="Удаление ржавчины и коррозии кузова в Челябинске | ГЕОМЕТРИЯ КУЗОВА"; Desc="Удаление коррозии автомобиля в Челябинске. Остановим ржавчину, защитим кузов. ул. Каслинская 1/1."; Price="от 1 000 ₽"; Time="1–2 дня"; Lead="Останавливаем ржавчину и защищаем кузов от дальнейшего разрушения. Обработка антикоррозийными составами."},
  @{Slug="zhestyanye-raboty"; H1="Жестяные работы"; Title="Жестяные работы по кузову в Челябинске — от 3 000 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Жестяные работы: восстановление формы кузова после вмятин и деформаций. Челябинск, ул. Каслинская 1/1."; Price="от 3 000 ₽"; Time="от 1 дня"; Lead="Восстанавливаем форму кузова после вмятин и деформаций. Работаем с металлом любой толщины."},
  @{Slug="zamena-arok"; H1="Замена арок"; Title="Замена арок автомобиля в Челябинске — от 2 500 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Замена колесных арок в Челябинске. Восстановление целостности кузова."; Price="от 2 500 ₽"; Time="от 2 дней"; Lead="Вернём целостность и эстетику колесных арок. Вырезаем ржавые участки, ввариваем новые, обрабатываем антикором."},
  @{Slug="zamena-porogov"; H1="Замена порогов"; Title="Замена порогов автомобиля в Челябинске — от 4 500 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Замена порогов кузова в Челябинске. Сварка, антикоррозийная обработка. ул. Каслинская 1/1."; Price="от 4 500 ₽"; Time="от 2 дней"; Lead="Полная или частичная замена порогов с последующей обработкой антикором и покраской."},
  @{Slug="zamena-privarnyh-paneley"; H1="Замена приварных панелей"; Title="Замена приварных панелей кузова в Челябинске | ГЕОМЕТРИЯ КУЗОВА"; Desc="Замена приварных панелей автомобиля в Челябинске. Профессиональная сварка и покраска."; Price="от 5 000 ₽"; Time="от 3 дней"; Lead="Профессиональная замена приварных элементов кузова с соблюдением заводских технологий."},
  @{Slug="svarochnye-raboty"; H1="Сварочные работы"; Title="Сварочные работы по кузову в Челябинске — от 1 000 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Сварочные работы кузова автомобиля в Челябинске. Качественный ремонт любой сложности."; Price="от 1 000 ₽"; Time="от 1 дня"; Lead="Полуавтомат, аргон, точечная сварка. Выполняем любые сварочные работы по кузову автомобиля."},
  @{Slug="vosstanovlenie-geometrii"; H1="Восстановление геометрии кузова"; Title="Восстановление геометрии кузова в Челябинске — от 5 000 ₽ | ГЕОМЕТРИЯ КУЗОВА"; Desc="Восстановление геометрии кузова на стапеле в Челябинске. Вернём заводские параметры."; Price="от 5 000 ₽"; Time="от 3 дней"; Lead="На стапеле вернём вашему автомобилю заводские параметры кузова после серьёзного ДТП."}
)

foreach ($s in $services) {
  $slug = $s.Slug
  $title = $s.Title
  $desc = $s.Desc
  $h1 = $s.H1
  $price = $s.Price
  $time = $s.Time
  $lead = $s.Lead

  $page = @"
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$title</title>
<meta name="description" content="$desc">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://geometriya-kuzova.ru/uslugi/$slug.html">
<link rel="stylesheet" href="../style.css">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":"https://geometriya-kuzova.ru/"},{"@type":"ListItem","position":2,"name":"Услуги","item":"https://geometriya-kuzova.ru/#services"},{"@type":"ListItem","position":3,"name":"$h1","item":"https://geometriya-kuzova.ru/uslugi/$slug.html"}]}
</script>
</head>
<body>

<header class="header">
  <div class="wrap header__inner">
    <a href="../index.html" class="logo"><span class="logo__mark">Г</span>ГЕОМЕТРИЯ КУЗОВА</a>
    <nav class="nav">
      <a href="../index.html#services">Услуги</a>
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
      <li aria-current="page">$h1</li>
    </ol>
  </div>
</nav>

<section class="hero" style="padding:56px 0 40px">
  <div class="wrap" style="max-width:820px">
    <div class="eyebrow">Челябинск · ул. Каслинская 1/1</div>
    <h1>$h1 <span class="accent">в Челябинске</span></h1>
    <p class="hero__sub">$lead</p>
    <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:32px">
      <a href="tel:+79226326030" class="btn btn--primary btn--lg">+7 (922) 632-60-30</a>
      <a href="../index.html#estimate" class="btn btn--ghost btn--lg">Оценить по фото</a>
    </div>
    <div style="display:flex;gap:28px;flex-wrap:wrap;padding:20px 24px;background:var(--graphite-2);border:1px solid var(--line);border-radius:var(--radius)">
      <div><div style="font-size:12px;color:var(--muted);margin-bottom:4px">Стоимость</div><div style="font-size:22px;font-weight:800">$price</div></div>
      <div><div style="font-size:12px;color:var(--muted);margin-bottom:4px">Срок</div><div style="font-size:22px;font-weight:800">$time</div></div>
      <div><div style="font-size:12px;color:var(--muted);margin-bottom:4px">Адрес</div><div style="font-size:15px;font-weight:600">ул. Каслинская, 1/1</div></div>
    </div>
  </div>
</section>

<section class="section" style="border-top:0;padding:48px 0">
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

<section class="section">
  <div class="wrap" style="max-width:820px">
    <h2>Как мы работаем</h2>
    <div class="process" style="grid-template-columns:repeat(2,1fr);margin-top:32px">
      <div class="step"><h3>Заявка и фото</h3><p>Присылаете фото повреждения — получаете предварительную оценку.</p><span class="step__time">15 минут</span></div>
      <div class="step"><h3>Осмотр и смета</h3><p>Проводим дефектовку, согласовываем работы и финальную стоимость.</p><span class="step__time">30–60 минут</span></div>
      <div class="step"><h3>Работы</h3><p>Выполняем по этапам, отправляем фотоотчёт на связи.</p><span class="step__time">$time</span></div>
      <div class="step"><h3>Выдача</h3><p>Проверяете результат, подписываете акт, получаете гарантию.</p><span class="step__time">30 минут</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap" style="max-width:820px">
    <h2>Частые вопросы</h2>
    <div class="faq" style="margin-top:32px">
      <details open><summary>Сколько стоит услуга?</summary><div class="faq__body">Стоимость начинается от $price. Точная цена зависит от степени повреждения и определяется после дефектовки.</div></details>
      <details><summary>Сколько времени займёт?</summary><div class="faq__body">Ориентировочный срок — $time. Точные сроки фиксируем после осмотра автомобиля.</div></details>
      <details><summary>Даёте ли гарантию?</summary><div class="faq__body">Да, мы предоставляем гарантию на все виды кузовных и малярных работ. Конкретный срок уточняйте у мастера.</div></details>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap" style="max-width:820px">
    <div style="background:var(--graphite-2);border:1px solid var(--line);border-radius:20px;padding:44px;text-align:center">
      <h2 style="margin-bottom:16px">Запишитесь на бесплатную оценку</h2>
      <p style="color:var(--metal);margin-bottom:26px">Пришлите фото повреждения — рассчитаем стоимость и сроки.</p>
      <a href="tel:+79226326030" class="btn btn--primary btn--lg">Позвонить: +7 (922) 632-60-30</a>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="wrap">
    <div class="footer__bottom" style="padding-top:0;border-top:0">
      <span>© 2026 ГЕОМЕТРИЯ КУЗОВА. Все права защищены.</span>
      <span><a href="../index.html">Вернуться на главную</a></span>
    </div>
  </div>
</footer>

</body>
</html>
"@
  Set-Content -Path (Join-Path $uslugi "$slug.html") -Value $page -Encoding UTF8
}

# ============================================================
# README
# ============================================================
$readme = @'
# ГЕОМЕТРИЯ КУЗОВА — сайт

## Структура
- index.html — главная
- style.css — стили
- app.js — Telegram-форма, слайдер, анимации
- uslugi/ — 10 страниц услуг

## Что нужно сделать перед публикацией

1. **Яндекс.Метрика:** откройте index.html и app.js, замените XXXXXXXXX на номер счётчика.
2. **Telegram-бот:** в app.js замените YOUR_BOT_TOKEN_HERE и YOUR_CHAT_ID_HERE.
3. **Домен:** замените geometriya-kuzova.ru на реальный домен (в canonical и Schema.org).
4. **Фото:** в index.html найдите блоки .ba__before / .ba__after и замените на реальные фото.
5. **Политика конфиденциальности:** создайте страницу privacy.html.

## Как открыть локально
Двойной клик по index.html.

## Как запустить Telegram-бота
1. @BotFather → /newbot → получите TOKEN
2. Напишите боту /start, откройте:
   https://api.telegram.org/bot<TOKEN>/getUpdates
3. Найдите "chat":{"id":XXXXXXXX}
4. Вставьте TOKEN и ID в app.js
'@
Set-Content -Path (Join-Path $root "README.md") -Value $readme -Encoding UTF8

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "  Сайт 'ГЕОМЕТРИЯ КУЗОВА' создан!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Папка: $root" -ForegroundColor Yellow
Write-Host ""
Write-Host "Открыть index.html двойным кликом или выполните:" -ForegroundColor Yellow
Write-Host "  start $root\index.html" -ForegroundColor Cyan
Write-Host ""