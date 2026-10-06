#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скачивание всех уникальных фотографий из каталога v2.
Сохраняет в <site>/img/works/. Также формирует _vk_photos_index_v2.json.
"""
import json
import os
import time
import urllib.request
import io
import sys

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
ROOT = os.path.dirname(os.path.abspath(__file__))          # .../tools
SITE_DIR = os.path.dirname(ROOT)                            # корень репозитория = сайт
IMG_DIR = os.path.join(SITE_DIR, "img", "works")
CATALOG_PATH = os.path.join(ROOT, "_vk_catalog_v2.json")
INDEX_PATH = os.path.join(ROOT, "_vk_photos_index_v2.json")

def fetch_bytes(url: str, referer: str = "https://m.vk.com/geometriyakuzova", retries: int = 4) -> bytes:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Referer": referer,
                "Accept": "image/webp,image/*,*/*;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}: {last}")

def main():
    catalog = json.load(open(CATALOG_PATH, encoding="utf-8"))
    os.makedirs(IMG_DIR, exist_ok=True)

    unique = {}
    order = []
    for it in catalog["items"]:
        for p in it["photos"]:
            pid = p["id"]
            if pid not in unique:
                unique[pid] = p
                order.append(pid)

    print(f"unique photos: {len(order)}", file=sys.stderr)

    index = {}
    if os.path.exists(INDEX_PATH):
        try:
            index = json.load(open(INDEX_PATH, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            index = {}

    downloaded = 0
    failed = []
    for i, pid in enumerate(order):
        p = unique[pid]
        big_url = p["big"].split("|")[0]
        fname = pid.replace("-", "_") + ".jpg"
        local = os.path.join(IMG_DIR, fname)
        if os.path.exists(local) and os.path.getsize(local) > 1024:
            index[pid] = {"id": pid, "local": os.path.relpath(local, SITE_DIR).replace("\\", "/")}
            continue
        try:
            data = fetch_bytes(big_url)
            with open(local, "wb") as f:
                f.write(data)
            index[pid] = {"id": pid, "local": os.path.relpath(local, SITE_DIR).replace("\\", "/")}
            downloaded += 1
            if downloaded % 25 == 0:
                print(f"  ... {downloaded}/{len(order)}", file=sys.stderr)
            time.sleep(0.3)
        except Exception as e:  # noqa: BLE001
            failed.append((pid, str(e)))
            print(f"  FAIL {pid}", file=sys.stderr)

    # привязка постов
    post_of_photo = {}
    for it in catalog["items"]:
        for p in it["photos"]:
            if p["id"] not in post_of_photo:
                post_of_photo[p["id"]] = it

    for pid in index:
        entry = index[pid]
        fp = post_of_photo.get(pid)
        entry["post_id"] = fp["post_id"] if fp else None
        entry["text"] = fp["text"][:400] if fp else ""
        entry["post_photos"] = len(fp["photos"]) if fp else 0

    json.dump(index, open(INDEX_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK: unique={len(order)} downloaded={downloaded} failed={len(failed)} index={len(index)}")

if __name__ == "__main__":
    main()