# -*- coding: utf-8 -*-
"""Windows consoles are often cp1252. Index text is UTF-8."""
from __future__ import annotations

import sys


def utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
