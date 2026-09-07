# -*- coding: utf-8 -*-
"""JOB.json chat lease. Second holder while the lease is live = refuse."""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

HOLDER_ENV = "VRC_DCC_JOB_HOLDER"
DEFAULT_TTL_SEC = 3600

_now_fn: Callable[[], datetime] | None = None


def set_now_fn(fn: Callable[[], datetime] | None) -> None:
    global _now_fn
    _now_fn = fn


def now_utc() -> datetime:
    if _now_fn is not None:
        return _now_fn()
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(text: str) -> datetime | None:
    if not text or not isinstance(text, str):
        return None
    raw = text.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def ttl_sec(policy: dict | None, override: int = 0) -> int:
    if override and override > 0:
        return override
    if policy:
        raw = policy.get("job_lease_ttl_sec")
        if type(raw) is int and raw > 0:
            return raw
    return DEFAULT_TTL_SEC


def resolve_holder(cli: str | None) -> str:
    h = (cli or "").strip() or (os.environ.get(HOLDER_ENV) or "").strip()
    return h


def lease_of(job: dict) -> dict | None:
    lease = job.get("lease")
    if not isinstance(lease, dict):
        return None
    return lease


def lease_active(job: dict, at: datetime | None = None) -> bool:
    lease = lease_of(job)
    if not lease:
        return False
    exp = parse_iso(str(lease.get("expires") or ""))
    if exp is None:
        return False
    return exp > (at or now_utc())


def acquire(
    job: dict,
    *,
    holder: str,
    slice_id: str,
    ttl: int,
    at: datetime | None = None,
) -> tuple[dict, str | None]:
    """Stamp a lease. Error string if another holder still owns it."""
    when = at or now_utc()
    incoming = (holder or "").strip()
    current = lease_of(job)
    if lease_active(job, when) and current:
        owned = str(current.get("holder") or "")
        if incoming and owned and incoming != owned:
            return job, "LEASE_HELD"
        if not incoming and owned:
            return job, "LEASE_HELD"
        incoming = incoming or owned
    if not incoming:
        return job, "NEED_HOLDER"
    keep = (
        current
        if current
        and lease_active(job, when)
        and str(current.get("holder") or "") == incoming
        else None
    )
    job["lease"] = {
        "id": str((keep or {}).get("id") or uuid.uuid4().hex[:12]),
        "holder": incoming,
        "slice": slice_id,
        "acquired": str((keep or {}).get("acquired") or iso(when)),
        "expires": iso(when + timedelta(seconds=ttl)),
        "ttl_sec": ttl,
    }
    return job, None


def require(
    job: dict,
    holder: str,
    *,
    at: datetime | None = None,
) -> str | None:
    """None if this holder may mutate. Else an error token."""
    incoming = (holder or "").strip()
    if not job.get("open_slice"):
        return "NO_LEASE_BEGIN"
    if not lease_of(job):
        return "NO_LEASE_BEGIN"
    if not lease_active(job, at):
        return "LEASE_EXPIRED"
    owned = str((lease_of(job) or {}).get("holder") or "")
    if not incoming:
        return "LEASE_HELD"
    if owned and incoming != owned:
        return "LEASE_HELD"
    return None


def require_http(
    job: dict,
    holder: str,
    *,
    at: datetime | None = None,
) -> str | None:
    """Station HTTP tools/call: live lease required (no pre-S00-c hole)."""
    if not job.get("open_slice"):
        return "NO_LEASE_BEGIN"
    if not lease_of(job):
        return "NO_LEASE_BEGIN"
    return require(job, holder, at=at)
