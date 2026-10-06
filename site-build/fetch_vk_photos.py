#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборщик фотографий из группы ВК «ГЕОМЕТРИЯ КУЗОВА» (vk.com/geometriyakuzova, id 113402547).
v2: корректно разделяем посты по границам data-post-id; собираем только СВОИ фото поста.
"""
import html as html_mod
import json
import os
import re
import sys
import time
import urllib.request

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
GROUP = "geometriyakuzova"
BASE = f"https://m.vk.com/{GROUP}"
ROOT = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(ROOT, "_vk_catalog_v2.json")

def fetch(url: str, retries: int = 5) -> str:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.5",
                "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            if "charset=" in ctype:
                return data.decode(ctype.split("charset=")[-1].strip(), errors="replace")
            return data.decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"fetch failed: {url}: {last}")

def pos_boundaries(text: str) -> list:
    """Список (start, end) для каждого поста: границы — открывающий div.wall_item."""
    markers = list(re.finditer(r'<div class="wall_item[^"]*"[^>]*data-post-id="(-?\d+_\d+)"', text))
    bounds = []
    for i, m in enumerate(markers):
        start = m.start()
        end = markers[i + 1].start() if i + 1 < len(markers) else text.find('<div class="show_more_wrap"', start)
        if end == -1:
            end = len(text)
        bounds.append((start, end, m.group(1)))
    return bounds

def parse_post(text: str) -> dict:
    post_id = None
    m = re.search(r'data-post-id="(-?\d+_\d+)"', text)
    if m:
        post_id = m.group(1)

    # текст
    tm = re.search(r'<div class="pi_text"[^>]*data-testid="post_description"[^>]*>(.*?)</div>\s*<div class="pi_medias[ >]', text, re.S)
    post_text = ""
    if tm:
        raw = tm.group(1)
        raw = re.sub(r"<br\s*/?>", "\n", raw)
        raw = re.sub(r"<[^>]+>", "", raw)
        post_text = html_mod.unescape(raw).strip()

    # свои фото: находим href="/photo<id>" в сочетании с data-src_big (учитывая переносы строк)
    photos = []
    for m in re.finditer(r'href="/photo(-?\d+_\d+)"[^>]*class="thumb_link\s*"[^>]*>(.*?)</a>', text, re.S):
        pid = m.group(1)
        inner = m.group(2)
        sbig = re.search(r'data-src_big="([^"]+)"', inner, re.S)
        if not sbig:
            # часть сайтов даёт data-id и data-src_big раздельно
            sbig = re.search(r'data-id="[^"]*"[^>]*data-src_big="([^"]+)"', inner, re.S)
        big = html_mod.unescape(sbig.group(1)) if sbig else ""
        if not pid.startswith("-"):
            pid = "-" + pid
        photos.append({"id": pid, "big": big})

    # видео-обложки (постеры), если есть длительность
    videos = []
    vm = re.finditer(r'<a\s+href="/video(-?\d+_\d+)"[^>]*aria-label="([^"]*?длительностью [^"]*?)"[^>]*class="thumb_link\s*"[^>]*>\s*<span class="mt_label mt_dur">([^<]*)</span><div[^>]*background-image: url\(([^)]+)\);', text)
    for v in vm:
        videos.append({"id": "-" + v.group(1) if not v.group(1).startswith("-") else v.group(1),
                       "label": v.group(2), "dur": v.group(3), "thumb": html_mod.unescape(v.group(4).strip("'\""))})

    return {"post_id": post_id, "text": post_text, "photos": photos, "videos": videos}

def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    offset = 0
    all_items = []
    seen = set()
    pages = 0
    while offset is not None and pages < 80:
        url = f"{BASE}?offset={offset}&own=1" if offset else BASE
        print(f"page offset={offset}", file=sys.stderr)
        page = fetch(url)
        bounds = pos_boundaries(page)
        fresh = 0
        for start, end, post_id in bounds:
            if post_id in seen:
                continue
            seen.add(post_id)
            item = parse_post(page[start:end])
            all_items.append(item)
            fresh += 1
        pages += 1
        if fresh == 0:
            break
        nxts = [int(x) for x in re.findall(r'href="/geometriyakuzova\?offset=(\d+)(?:&own=1)?"', page)]
        if not nxts:
            break
        nxt = max(nxts)  # "дальше" — максимальный offset
        if nxt <= offset:
            break
        offset = nxt
        if len(all_items) >= limit:
            break
        time.sleep(1.5)

    catalog = {"group": GROUP, "group_id": 113402547, "items": all_items}
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=1)
    n_photos = sum(len(it["photos"]) for it in all_items)
    n_videos = sum(len(it["videos"]) for it in all_items)
    print(f"OK: {len(all_items)} постов, фото={n_photos}, видео={n_videos}")

if __name__ == "__main__":
    main()