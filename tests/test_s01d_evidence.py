# -*- coding: utf-8 -*-
"""S01-d: fingerprints, STALE, owned plan/apply. No Unity."""
from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "maps"))

from evidence import apply_allowed, fingerprint, is_stale  # noqa: E402
from lease import acquire, iso  # noqa: E402
import gate  # noqa: E402


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
    job["mutation_revision"] = 1
    washed = fingerprint(
        layer="STATIC_SOURCE",
        payload="Packages/manifest.json\n",
        product_id="example-s01a",
        domain="world",
        holder="chat-a",
        lease_id=str(job["lease"]["id"]),
        captured_at=iso(frozen + timedelta(minutes=6)),
    )
    assert is_stale(washed, job) == "STALE_MUTATED"
    recaptured = fingerprint(
        layer="STATIC_SOURCE",
        payload="Packages/manifest.json\n",
        product_id="example-s01a",
        domain="world",
        holder="chat-a",
        lease_id=str(job["lease"]["id"]),
        captured_at=iso(frozen + timedelta(minutes=6)),
        mutation_revision=1,
    )
    assert is_stale(recaptured, job) is None
    assert is_stale(recaptured, {"mutation_revision": 0}) == "STALE_MUTATED"
    print("PASS fingerprint stale")


def test_reset_preserves_stale_evidence() -> None:
    with tempfile.TemporaryDirectory(prefix="vrc-evidence-") as tmp:
        name = "example-reset"
        with patch.object(gate, "HERE", Path(tmp)):
            job = {"mutation_revision": 2, "mutated": True, "mutated_at": "2026-09-07T12:05:00Z"}
            gate.save_job(name, job)
            older = fingerprint(
                layer="STATIC_SOURCE", payload="old scene", product_id=name,
                domain="avatar", holder="example-holder", mutation_revision=1,
            )
            assert is_stale(older, job) == "STALE_MUTATED"
            assert gate.cmd_reset(name) == 0
            reset = gate.load_job(name)
            assert reset["mutation_revision"] == 2 and reset["mutated"] is True
            assert reset["mutated_at"] == job["mutated_at"]
            assert reset["open_slice"] is None and reset["lease"] is None
            assert is_stale(older, reset) == "STALE_MUTATED"
    print("PASS reset preserves stale evidence")


def test_owned_plan() -> None:
    frozen = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)
    job, err = acquire({"open_slice": None, "lease": None}, holder="chat-a", slice_id="example.world-probe", ttl=3600, at=frozen)
    assert err is None
    job["open_slice"] = "example.world-probe"
    plan = {"holder": "chat-a", "slice": "example.world-probe", "intent": "read-only probe"}
    # The lease was issued at frozen, so validation must use that same clock.
    # Otherwise this fixture expires one hour after its literal date forever.
    with patch("lease.now_utc", return_value=frozen + timedelta(minutes=1)):
        assert apply_allowed(plan, job, "chat-a") is None
        assert apply_allowed(plan, job, "chat-b") == "PLAN_HOLDER"
        assert apply_allowed({"holder": ""}, job, "chat-a") == "PLAN_NO_HOLDER"
    with patch("lease.now_utc", return_value=frozen + timedelta(hours=1)):
        assert apply_allowed(plan, job, "chat-a") == "LEASE_EXPIRED"
    print("PASS owned plan")


if __name__ == "__main__":
    test_fingerprint_and_stale()
    test_reset_preserves_stale_evidence()
    test_owned_plan()
    print("PASS test_s01d_evidence")
