# -*- coding: utf-8 -*-
"""Propose buckets for files in local.json unityvrchat_stage. Does not move anything."""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
from _stdio import utf8_stdio
from library.paths import stage_root

BOOTH_RE = re.compile(r"(\d{6,8})")


def guess(name: str) -> str:
    m = BOOTH_RE.search(name)
    booth = m.group(1) if m else ""
    hint = "booth %s — " % booth if booth else ""
    return hint + "Owner names the collection folder (do not invent a top-level bucket)"


def main() -> int:
    utf8_stdio()
    print("INGEST propose only. Owner confirms, then a human/agent moves. Then scan.py.")
    stage = stage_root()
    print("stage:", stage if str(stage) else "(unset — local.json unityvrchat_stage)")
    if not stage or not stage.exists():
        print("stage folder missing — set local.json unityvrchat_stage and drop zips there. Do not dump on the USB root.")
        return 2
    items = [p for p in stage.iterdir() if p.name not in {".gitkeep"}]
    if not items:
        print("stage empty.")
        return 0
    for p in sorted(items, key=lambda x: x.name.lower()):
        m = BOOTH_RE.search(p.name)
        booth = m.group(1) if m else "(no booth id in name)"
        print("-", p.name)
        print("  booth:", booth)
        print("  propose:", guess(p.name))
        if m:
            print("  listing: https://booth.pm/ja/items/" + m.group(1))
    print("Do not split the shelf by body. Do not Ultra. Do not unpack unitypackage on the USB root.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
