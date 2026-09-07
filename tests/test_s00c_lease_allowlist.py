# -*- coding: utf-8 -*-
"""S00-c: tool allowlist, JOB lease, fake MCP notify/error/timeout."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
sys.path.insert(0, str(MAPS))
sys.path.insert(0, str(ROOT / "tests"))

from allowlist import check_tool  # noqa: E402
from fake_mcp import FakeMCP  # noqa: E402
from lease import acquire, require, set_now_fn  # noqa: E402
from unity_mcp_call import call_tool  # noqa: E402

PY = sys.executable


def _seed(aid: str) -> Path:
    dest = MAPS / aid
    if dest.exists():
        shutil.rmtree(dest)
    r = subprocess.run([PY, "init_avatar.py", aid], cwd=str(MAPS), capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("init_avatar failed: %s %s" % (r.stdout, r.stderr))
    return dest


def _gate(aid: str, *args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    e = os.environ.copy()
    if env:
        e.update(env)
    return subprocess.run(
        [PY, "gate.py", aid, *args],
        cwd=str(MAPS),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=e,
    )


def test_allowlist() -> None:
    ok, _ = check_tool("vrc_audit")
    assert ok
    bad, reason = check_tool("execute_code")
    assert not bad and "denied" in reason
    bad2, r2 = check_tool("world_scene_dump")
    assert not bad2 and "cross-domain" in r2
    bad3, r3 = check_tool("manage_scene")
    assert not bad3 and "vrc_" in r3
    bad4, _ = check_tool("vrc_upload_avatar")
    assert not bad4
    pol = {"disable_mcp_tools": ["vrc_audit"]}
    bad5, r5 = check_tool("vrc_audit", pol)
    assert not bad5 and "disable_mcp_tools" in r5
    pol2 = {"allow_mcp_tools": ["vrc_pose_bounds"]}
    ok2, _ = check_tool("vrc_pose_bounds", pol2)
    assert ok2
    bad6, _ = check_tool("vrc_audit", pol2)
    assert not bad6
    print("PASS allowlist")


def test_lease_holders() -> None:
    frozen = datetime(2026, 9, 7, 0, 0, tzinfo=timezone.utc)
    set_now_fn(lambda: frozen)
    try:
        job: dict = {"open_slice": None, "lease": None}
        job, err = acquire(job, holder="chat-a", slice_id="example.sdk-build", ttl=60)
        assert err is None
        job["open_slice"] = "example.sdk-build"
        assert require(job, "chat-a") is None
        assert require(job, "chat-b") == "LEASE_HELD"
        assert require(job, "") == "LEASE_HELD"
        set_now_fn(lambda: frozen + timedelta(seconds=120))
        assert require(job, "chat-a") == "LEASE_EXPIRED"
        job2, err2 = acquire(job, holder="chat-b", slice_id="example.sdk-build", ttl=60)
        assert err2 is None
        assert job2["lease"]["holder"] == "chat-b"
    finally:
        set_now_fn(None)
    print("PASS lease holders")


def test_gate_lease_cli() -> None:
    dest = _seed("example-s00c")
    try:
        env_a = {"VRC_DCC_JOB_HOLDER": "holder-a"}
        env_b = {"VRC_DCC_JOB_HOLDER": "holder-b"}
        a = _gate("example-s00c", "begin", "example.sdk-build", "--ttl", "3600", env=env_a)
        if a.returncode != 0:
            raise SystemExit("begin A: %s %s" % (a.stdout, a.stderr))
        b = _gate("example-s00c", "begin", "example.sdk-build", env=env_b)
        if b.returncode != 2 or "LEASE_HELD" not in (b.stderr or ""):
            raise SystemExit("expected LEASE_HELD, got %s %s" % (b.returncode, b.stderr))
        m = _gate("example-s00c", "mutated", env=env_b)
        if m.returncode != 2 or "LEASE_HELD" not in (m.stderr or ""):
            raise SystemExit("mutated other holder: %s" % m.stderr)
        okm = _gate("example-s00c", "mutated", env=env_a)
        if okm.returncode != 0:
            raise SystemExit("mutated owner: %s" % okm.stderr)
        rst = _gate("example-s00c", "reset", env=env_a)
        if rst.returncode != 0:
            raise SystemExit("reset: %s" % rst.stderr)
        b2 = _gate("example-s00c", "begin", "example.sdk-build", env=env_b)
        if b2.returncode != 0:
            raise SystemExit("begin after reset: %s" % b2.stderr)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    print("PASS gate lease cli")


def test_fake_mcp_notify_and_errors() -> None:
    good = FakeMCP("notify_then_result")
    good.start()
    try:
        out = call_tool("vrc_audit", {}, timeout=5, url=good.url)
        assert out.get("result", {}).get("content")
    finally:
        good.stop()

    err = FakeMCP("rpc_error")
    err.start()
    try:
        try:
            call_tool("vrc_audit", {}, timeout=5, url=err.url)
            raise SystemExit("rpc_error should raise")
        except RuntimeError as ex:
            if "jsonrpc error" not in str(ex):
                raise SystemExit("expected jsonrpc error: %s" % ex)
    finally:
        err.stop()

    ie = FakeMCP("is_error")
    ie.start()
    try:
        try:
            call_tool("vrc_audit", {}, timeout=5, url=ie.url)
            raise SystemExit("isError should raise")
        except RuntimeError as ex:
            if "isError" not in str(ex):
                raise SystemExit("expected isError: %s" % ex)
    finally:
        ie.stop()

    note = FakeMCP("notify_only")
    note.start()
    try:
        try:
            call_tool("vrc_audit", {}, timeout=5, url=note.url)
            raise SystemExit("notify_only should raise")
        except RuntimeError as ex:
            if "notify-before-result" not in str(ex):
                raise SystemExit("expected notify-before-result: %s" % ex)
    finally:
        note.stop()

    hang = FakeMCP("hang")
    hang.start()
    try:
        try:
            call_tool("vrc_audit", {}, timeout=1, url=hang.url)
        except Exception:
            pass
        else:
            raise SystemExit("hang should not return a tool result")
    finally:
        hang.stop()

    try:
        call_tool("execute_code", {}, timeout=1, url="http://127.0.0.1:1/mcp")
        raise SystemExit("execute_code must refuse before HTTP")
    except RuntimeError as ex:
        if "refused" not in str(ex):
            raise SystemExit("expected refuse: %s" % ex)
    print("PASS fake mcp")


if __name__ == "__main__":
    test_allowlist()
    test_lease_holders()
    test_gate_lease_cli()
    test_fake_mcp_notify_and_errors()
    print("PASS test_s00c_lease_allowlist")
