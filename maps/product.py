# -*- coding: utf-8 -*-
"""Avatar vs world map folders. No Unity. No default product."""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
AVATAR = "avatar"
WORLD = "world"
DOMAINS = (AVATAR, WORLD)


def normalize_domain(raw: str | None) -> str:
    d = (raw or AVATAR).strip().lower()
    if d in ("worlds", "udon"):
        d = WORLD
    if d not in DOMAINS:
        raise SystemExit("domain must be avatar or world (got %r)" % raw)
    return d


def product_dir(name: str, domain: str = AVATAR) -> Path:
    nid = (name or "").strip().lower()
    if not nid:
        raise SystemExit("product id is empty")
    if normalize_domain(domain) == WORLD:
        return HERE / "worlds" / nid
    return HERE / nid
