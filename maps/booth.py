# -*- coding: utf-8 -*-
"""One public Booth item page. No shop crawl, no paid download."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from _stdio import utf8_stdio

HERE = Path(__file__).resolve().parent
ITEM_RE = re.compile(r"booth\.pm/(?:[a-z]{2}/)?items/(\d+)", re.I)
OG_RE = re.compile(
    r'<meta[^>]+(?:property|name)=["\']og:(title|description|url|image)["\'][^>]+content=["\']([^"\']*)["\']',
    re.I,
)
OG_RE_REV = re.compile(
    r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\']og:(title|description|url|image)["\']',
    re.I,
)
TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.I)
PRICE_RE = re.compile(r'"price"\s*:\s*"?(\d+)"?')
SHOP_RE = re.compile(r"booth\.pm/([^/\"']+)/items/", re.I)
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def search_recipe(terms: list[str]) -> str:
    q = " ".join(terms).strip()
    return 'site:booth.pm {0} VRChat'.format(q)


def item_id(url: str) -> str | None:
    m = ITEM_RE.search(url)
    return m.group(1) if m else None


def fetch(url: str, timeout: int) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        ctype = resp.headers.get("Content-Type", "")
        enc = "utf-8"
        if "charset=" in ctype.lower():
            enc = ctype.split("charset=", 1)[1].split(";")[0].strip() or "utf-8"
        return raw.decode(enc, errors="replace")


def parse(html: str, url: str) -> dict:
    og: dict[str, str] = {}
    for m in OG_RE.finditer(html):
        og[m.group(1).lower()] = m.group(2)
    for m in OG_RE_REV.finditer(html):
        og.setdefault(m.group(2).lower(), m.group(1))
    title = og.get("title")
    if not title:
        tm = TITLE_RE.search(html)
        title = tm.group(1).strip() if tm else ""
    price = None
    pm = PRICE_RE.search(html)
    if pm:
        price = pm.group(1)
    iid = item_id(url) or item_id(og.get("url") or "")
    shop = None
    sm = SHOP_RE.search(og.get("url") or url)
    if sm:
        shop = sm.group(1)
        if shop in {"ja", "en", "ko", "zh-cn", "zh-tw"}:
            shop = None
    return {
        "item_id": iid,
        "url": og.get("url") or url,
        "title": title,
        "description": (og.get("description") or "")[:400],
        "image": og.get("image") or "",
        "price": price,
        "shop": shop,
        "source": "booth.pm/items/{0}".format(iid) if iid else url,
        "status": "observed",
        "body_fit": "Shop size charts are not this mesh until Edit confirms. Fusion / retarget bodies need a live dump, not the SKU name.",
    }


def main() -> int:
    utf8_stdio()
    p = argparse.ArgumentParser(description="Booth: search recipe or one item fetch")
    p.add_argument("target", nargs="*", help="item URL, or words with --search")
    p.add_argument("--search", action="store_true", help="Print the WebSearch query; do not hit Google")
    p.add_argument("--timeout", type=int, default=20)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    if args.search:
        if not args.target:
            print("usage: booth.py --search Fallen Servant Airi", file=sys.stderr)
            return 2
        recipe = search_recipe(args.target)
        print("WebSearch (one):", recipe)
        print("Then: python booth.py https://booth.pm/ja/items/<id>")
        print("Do not buy. Do not download paid files. Shop charts are not a live mesh.")
        return 0
    if not args.target:
        print("usage: booth.py <https://booth.pm/.../items/N>   or  booth.py --search <words>", file=sys.stderr)
        return 2
    url = args.target[0].strip()
    if not item_id(url) and not url.startswith("http"):
        print("not a Booth item URL. Try: python booth.py --search", url, file=sys.stderr)
        return 2
    if not url.startswith("http"):
        url = "https://" + url
    try:
        html = fetch(url, args.timeout)
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        print("fetch failed:", e, file=sys.stderr)
        print("Next: parent WebFetch that URL once. Do not invent a listing.", file=sys.stderr)
        return 1
    info = parse(html, url)
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print("id:", info["item_id"])
        print("title:", info["title"])
        print("url:", info["url"])
        if info["price"]:
            print("price:", info["price"])
        print("source:", info["source"])
        print("status: observed")
        print(info["body_fit"])
        print("notes.json: set source to", info["source"], "until Owner keeps the mesh in Edit.")
    return 0 if info.get("title") else 1


if __name__ == "__main__":
    raise SystemExit(main())
