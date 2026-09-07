# -*- coding: utf-8 -*-
"""Evidence fingerprints + STALE + owned plan/apply. No Unity. No HTTP."""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from lease import parse_iso, require_http, resolve_holder

SCHEMA = 1
LAYERS = (
    "STATIC_SOURCE",
    "UNITY_RESOLVED",
    "PROVIDER_PREVIEW",
    "NDMF_BUILT",
    "SDK_BUILD",
    "CLIENT_RUNTIME",
    "UPLOAD_CONFIRMED",
    "UDON_COMPILED",
    "CLIENTSIM",
    "MULTIPLAYER",
)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def fingerprint(
    *,
    layer: str,
    payload: bytes | str,
    product_id: str,
    domain: str,
    holder: str,
    lease_id: str | None = None,
    path: str = "",
    captured_at: str | None = None,
) -> dict[str, Any]:
    if layer not in LAYERS:
        raise ValueError("unknown evidence layer %r" % layer)
    raw = payload.encode("utf-8") if isinstance(payload, str) else payload
    when = captured_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema": SCHEMA,
        "layer": layer,
        "sha256": sha256_bytes(raw),
        "captured_at": when,
        "holder": (holder or "").strip(),
        "lease_id": lease_id or "",
        "product": {"domain": domain, "id": product_id},
        "path": path,
        "stale": False,
        "stale_reason": None,
    }


def is_stale(row: dict, job: dict) -> str | None:
    """Return a STALE token or None if this fingerprint may still be cited."""
    if not isinstance(row, dict):
        return "EVIDENCE_BAD"
    if row.get("stale"):
        return str(row.get("stale_reason") or "STALE")
    lease = job.get("lease") if isinstance(job.get("lease"), dict) else {}
    owned = str(lease.get("id") or "")
    got = str(row.get("lease_id") or "")
    if got and owned and got != owned:
        return "STALE_LEASE"
    cap = parse_iso(str(row.get("captured_at") or ""))
    mut_at = parse_iso(str(job.get("mutated_at") or ""))
    if job.get("mutated"):
        if mut_at and cap and cap >= mut_at and (not got or not owned or got == owned):
            return None
        return "STALE_MUTATED"
    return None


def mark_stale(row: dict, reason: str) -> dict:
    out = dict(row)
    out["stale"] = True
    out["stale_reason"] = reason
    return out


def apply_allowed(plan: dict, job: dict, holder: str) -> str | None:
    """None if this holder may apply a recorded plan. Else an error token."""
    who = resolve_holder(holder)
    planned = str((plan or {}).get("holder") or "").strip()
    if not planned:
        return "PLAN_NO_HOLDER"
    if not who or who != planned:
        return "PLAN_HOLDER"
    return require_http(job, who)
