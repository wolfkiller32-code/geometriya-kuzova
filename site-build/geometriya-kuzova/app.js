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
const MAX_PHOTOS = 5;             // Telegram принимает до 10, но 5 достаточно

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
  const fileInput = form.querySelector('#photo');
  const files = fileInput ? Array.from(fileInput.files).slice(0, MAX_PHOTOS) : [];

  const message = '🔔 Новая заявка с сайта\n━━━━━━━━━━━━━━━━\n👤 Имя: ' + name +
                  '\n📞 Телефон: ' + phone + '\n🛠 Услуга: ' + service +
                  (files.length ? '\n📷 Фото: ' + files.length : '');

  const api = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN;

  try {
    // 1. Текстовое сообщение
    const response = await fetch(api + '/sendMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text: message })
    });
    if (!response.ok) throw new Error('message failed');

    // 2. Фотографии повреждений (если приложены) — обычная отправка файлов
    for (let i = 0; i < files.length; i++) {
      const fd = new FormData();
      fd.append('chat_id', TELEGRAM_CHAT_ID);
      fd.append('caption', (i === 0 ? (name + ', ' + phone + ' — фото повреждений') : ('Фото ' + (i + 1))));
      fd.append('photo', files[i]);
      try {
        const pr = await fetch(api + '/sendPhoto', { method: 'POST', body: fd });
        if (!pr.ok) throw new Error('photo failed');
      } catch (photoErr) {
        // фото не ушло — не ломаем заявку, текст уже доставлен
        console.warn('Фото не отправлено:', photoErr);
        break;
      }
    }

    btn.textContent = 'Заявка отправлена ✓';
    btn.style.background = '#2BA84A';
    if (typeof ym === 'function') ym(YM_COUNTER_ID, 'reachGoal', 'lead_form_submit');
    form.reset();
    setTimeout(() => { btn.textContent = originalText; btn.style.background=''; btn.disabled=false; }, 4000);
  } catch (e) {
    btn.textContent = 'Ошибка. Позвоните: +7 (922) 632-60-30';
    btn.style.background = '#E53E3E';
    btn.disabled = false;
    setTimeout(() => { btn.textContent = originalText; btn.style.background=''; }, 5000);
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

// ================== ГАЛЕРЕЯ РАБОТ: ФИЛЬТР ==================
const filterBtns = document.querySelectorAll('.works-filter button');
const workItems = document.querySelectorAll('.work');
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const f = btn.dataset.filter;
    filterBtns.forEach(b => b.classList.toggle('is-active', b === btn));
    workItems.forEach(item => {
      const cats = (item.dataset.cat || '').split(' ');
      const show = (f === 'all') || cats.indexOf(f) !== -1;
      item.classList.toggle('is-hidden', !show);
    });
  });
});

// ================== ГАЛЕРЕЯ РАБОТ: ЛАЙТБОКС ==================
(function () {
  const box = document.getElementById('lightbox');
  if (!box) return;
  const img = document.getElementById('lightboxImg');
  const title = document.getElementById('lightboxTitle');
  const desc = document.getElementById('lightboxDesc');
  const link = document.getElementById('lightboxLink');
  const closeBtn = document.getElementById('lightboxClose');
  const lastFocus = { el: null };

  function open(item) {
    lastFocus.el = document.activeElement;
    img.src = item.dataset.full || item.querySelector('img').src;
    img.alt = item.querySelector('img').alt || '';
    title.textContent = item.dataset.title || '';
    desc.textContent = item.dataset.desc || '';
    if (item.dataset.link) { link.href = item.dataset.link; link.style.display = ''; }
    else { link.style.display = 'none'; }
    box.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }
  function close() {
    box.classList.remove('is-open');
    document.body.style.overflow = '';
    if (lastFocus.el) lastFocus.el.focus();
  }

  workItems.forEach(item => {
    item.setAttribute('tabindex', '0');
    item.setAttribute('role', 'button');
    item.addEventListener('click', () => open(item));
    item.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(item); }
    });
  });
  closeBtn.addEventListener('click', close);
  box.addEventListener('click', e => { if (e.target === box || e.target === img) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && box.classList.contains('is-open')) close(); });
})();

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

// ================== КНОПКА «НАВЕРХ» ==================
(function () {
  const btn = document.getElementById('toTop');
  if (!btn) return;
  btn.addEventListener('click', e => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();

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
