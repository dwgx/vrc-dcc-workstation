# -*- coding: utf-8 -*-
"""Resolve the USB shelf root. Index files stay in this clone."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATION = HERE.parent.parent


def _local() -> dict:
    loc = STATION / "local.json"
    if loc.is_file():
        try:
            data = json.loads(loc.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}
    return {}


def usb_root() -> Path:
    data = _local()
    raw = (data.get("unityvrchat_library") or os.environ.get("UNITYVRCHAT_LIBRARY") or "").strip()
    return Path(raw) if raw else Path()


def stage_root() -> Path:
    data = _local()
    raw = (data.get("unityvrchat_stage") or os.environ.get("UNITYVRCHAT_STAGE") or "").strip()
    return Path(raw) if raw else Path()


def python_exe() -> str:
    data = _local()
    raw = (data.get("python_exe") or "").strip()
    if raw and Path(raw).exists():
        return raw
    return sys.executable
