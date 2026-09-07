# -*- coding: utf-8 -*-
"""S01-d: fingerprints, STALE, owned plan/apply. No Unity."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "maps"))

from evidence import apply_allowed, fingerprint, is_stale  # noqa: E402
from lease import acquire, iso  # noqa: E402


def test_fingerprint_and_stale() -> None:
    frozen = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)
    job, err = acquire({"lease": None}, holder="chat-a", slice_id="example.world-probe", ttl=3600, at=frozen)
    assert err is None
    job["open_slice"] = "example.world-probe"
    fp = fingerprint(
        layer="STATIC_SOURCE",
        payload="Packages/manifest.json\n",
        product_id="example-s01a",
        domain="world",
        holder="chat-a",
        lease_id=str(job["lease"]["id"]),
        path="Packages/manifest.json",
        captured_at=iso(frozen),
    )
    assert fp["sha256"]
    assert is_stale(fp, job) is None
    job["mutated"] = True
    job["mutated_at"] = iso(frozen + timedelta(minutes=5))
    assert is_stale(fp, job) == "STALE_MUTATED"
    later = fingerprint(
        layer="STATIC_SOURCE",
        payload="Packages/manifest.json\n",
        product_id="example-s01a",
        domain="world",
        holder="chat-a",
        lease_id=str(job["lease"]["id"]),
        captured_at=iso(frozen + timedelta(minutes=6)),
    )
    assert is_stale(later, job) is None
    other, _ = acquire(dict(job), holder="chat-b", slice_id="example.world-probe", ttl=3600, at=frozen + timedelta(hours=2))
    assert is_stale(later, other) == "STALE_LEASE"
    print("PASS fingerprint stale")


def test_owned_plan() -> None:
    frozen = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)
    job, err = acquire({"open_slice": None, "lease": None}, holder="chat-a", slice_id="example.world-probe", ttl=3600, at=frozen)
    assert err is None
    job["open_slice"] = "example.world-probe"
    plan = {"holder": "chat-a", "slice": "example.world-probe", "intent": "read-only probe"}
    assert apply_allowed(plan, job, "chat-a") is None
    assert apply_allowed(plan, job, "chat-b") == "PLAN_HOLDER"
    assert apply_allowed({"holder": ""}, job, "chat-a") == "PLAN_NO_HOLDER"
    print("PASS owned plan")


if __name__ == "__main__":
    test_fingerprint_and_stale()
    test_owned_plan()
    print("PASS test_s01d_evidence")
