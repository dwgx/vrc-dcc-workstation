# -*- coding: utf-8 -*-
"""Unique-candidate picker (Python twin of VrcDccIdentity). No Unity."""
from __future__ import annotations

from typing import Sequence

OK = "ok"
NOT_APPLICABLE = "not_applicable"
AMBIGUOUS = "ambiguous"
MISSING_PATH = "missing_policy_path"
BAD_POLICY = "bad_policy"


def pick_unique(*, explicit: str | None, candidates: Sequence[str], cap: int = 8) -> dict:
    """Zero → not_applicable. Two+ → ambiguous. Never return the first of many."""
    cand = [c for c in candidates if c]
    if explicit is not None:
        wanted = explicit.strip()
        if not wanted:
            return {"status": BAD_POLICY, "path": None, "candidates": [], "wanted": explicit}
        hits = [c for c in cand if c == wanted]
        if not hits:
            return {
                "status": MISSING_PATH,
                "path": None,
                "candidates": cand[:cap],
                "wanted": wanted,
            }
        if len(hits) > 1:
            return {"status": AMBIGUOUS, "path": None, "candidates": hits[:cap], "wanted": wanted}
        return {"status": OK, "path": hits[0], "candidates": hits, "wanted": wanted}
    if not cand:
        return {"status": NOT_APPLICABLE, "path": None, "candidates": []}
    if len(cand) > 1:
        return {"status": AMBIGUOUS, "path": None, "candidates": cand[:cap]}
    return {"status": OK, "path": cand[0], "candidates": list(cand)}
