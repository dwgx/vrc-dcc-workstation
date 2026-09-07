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
from policy import validate_policy  # noqa: E402
from unity_mcp_call import _message_for_id, _unwrap, call_tool  # noqa: E402

PY = sys.executable
DEAD_MCP = "http://127.0.0.1:1/mcp"


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
    bad_cs, _ = check_tool("execute_csharp")
    assert not bad_cs
    bad_case, _ = check_tool("Execute_Code")
    assert not bad_case
    bad2, r2 = check_tool("world_scene_dump")
    assert not bad2 and "cross-domain" in r2
    bad3, r3 = check_tool("manage_scene")
    assert not bad3 and "vrc_" in r3
    bad4, _ = check_tool("vrc_upload_avatar")
    assert not bad4
    unpublished, _ = check_tool("vrc_unpublished_menu")
    assert unpublished
    exec_pref, _ = check_tool("vrc_execute_code")
    assert not exec_pref
    pol = {"disable_mcp_tools": ["vrc_audit"]}
    bad5, r5 = check_tool("vrc_audit", pol)
    assert not bad5 and "disable_mcp_tools" in r5
    pol2 = {"allow_mcp_tools": ["vrc_pose_bounds"]}
    ok2, _ = check_tool("vrc_pose_bounds", pol2)
    assert ok2
    bad6, _ = check_tool("vrc_audit", pol2)
    assert not bad6
    wide, wr = check_tool("manage_scene", {"allow_mcp_tools": ["manage_scene"]})
    assert not wide
    assert "vrc_" in wr or "denied" in wr or "not a named" in wr
    print("PASS allowlist")


def test_lease_holders() -> None:
    frozen = datetime(2026, 9, 7, 0, 0, tzinfo=timezone.utc)
    set_now_fn(lambda: frozen)
    try:
        empty, need = acquire({"lease": None}, holder="", slice_id="example.sdk-build", ttl=60)
        assert need == "NEED_HOLDER" and empty.get("lease") is None
        job: dict = {"open_slice": None, "lease": None}
        job, err = acquire(job, holder="chat-a", slice_id="example.sdk-build", ttl=60)
        assert err is None
        job["open_slice"] = "example.sdk-build"
        assert require(job, "chat-a") is None
        assert require(job, "chat-b") == "LEASE_HELD"
        assert require(job, "") == "LEASE_HELD"
        assert require({"open_slice": "example.sdk-build", "lease": None}, "chat-a") == "NO_LEASE_BEGIN"
        set_now_fn(lambda: frozen + timedelta(seconds=120))
        assert require(job, "chat-a") == "LEASE_EXPIRED"
        expired_empty, need2 = acquire(job, holder="", slice_id="example.sdk-build", ttl=60)
        assert need2 == "NEED_HOLDER"
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
        none = _gate(
            "example-s00c",
            "begin",
            "example.sdk-build",
            "--ttl",
            "3600",
            env={"VRC_DCC_JOB_HOLDER": ""},
        )
        if none.returncode != 2 or "NEED_HOLDER" not in (none.stderr or ""):
            raise SystemExit("begin without holder: %s" % none.stderr)
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
        steal = _gate("example-s00c", "reset", env=env_b)
        if steal.returncode != 2 or "LEASE_HELD" not in (steal.stderr or ""):
            raise SystemExit("reset other holder: %s" % steal.stderr)
        rst = _gate("example-s00c", "reset", env=env_a)
        if rst.returncode != 0:
            raise SystemExit("reset: %s" % rst.stderr)
        b2 = _gate("example-s00c", "begin", "example.sdk-build", env=env_b)
        if b2.returncode != 0:
            raise SystemExit("begin after reset: %s" % b2.stderr)
        forced = _gate("example-s00c", "reset", "--force", env=env_a)
        if forced.returncode != 0:
            raise SystemExit("reset --force: %s" % forced.stderr)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    print("PASS gate lease cli")


def test_concurrent_begin() -> None:
    dest = _seed("example-s00c-race")
    try:
        procs: list[subprocess.Popen[str]] = []
        for holder in ("race-a", "race-b"):
            env = os.environ.copy()
            env["VRC_DCC_JOB_HOLDER"] = holder
            procs.append(
                subprocess.Popen(
                    [PY, "gate.py", "example-s00c-race", "begin", "example.sdk-build", "--ttl", "3600"],
                    cwd=str(MAPS),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    env=env,
                )
            )
        codes = [p.wait() for p in procs]
        ok_n = sum(1 for c in codes if c == 0)
        held_n = sum(1 for c in codes if c == 2)
        logs = [(p.returncode, (p.stderr.read() if p.stderr else "")) for p in procs]
        if ok_n != 1 or held_n != 1:
            raise SystemExit("concurrent begin expected one ok one LEASE_HELD, got %s %s" % (codes, logs))
        job = json.loads((dest / "JOB.json").read_text(encoding="utf-8"))
        holder = str((job.get("lease") or {}).get("holder") or "")
        if holder not in ("race-a", "race-b"):
            raise SystemExit("unexpected lease holder %r" % holder)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    print("PASS concurrent begin")


def test_rpc_id_and_null_error() -> None:
    got = _message_for_id([{"id": "2", "result": {"ok": True}}], 2)
    assert got["result"]["ok"] is True
    last = _message_for_id(
        [
            {"method": "notifications/progress"},
            {"id": 2, "result": {"n": 1}},
            {"id": 2, "result": {"n": 2}},
        ],
        2,
    )
    assert last["result"]["n"] == 2
    out = _unwrap({"id": 2, "error": None, "result": {"ok": True}})
    assert out["result"]["ok"] is True
    print("PASS rpc id")


def test_fake_mcp_notify_and_errors() -> None:
    good = FakeMCP("notify_then_result")
    good.start()
    try:
        out = call_tool("vrc_audit", {}, timeout=5, url=good.url, skip_lease=True)
        assert out.get("result", {}).get("content")
    finally:
        good.stop()

    err = FakeMCP("rpc_error")
    err.start()
    try:
        try:
            call_tool("vrc_audit", {}, timeout=5, url=err.url, skip_lease=True)
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
            call_tool("vrc_audit", {}, timeout=5, url=ie.url, skip_lease=True)
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
            call_tool("vrc_audit", {}, timeout=5, url=note.url, skip_lease=True)
            raise SystemExit("notify_only should raise")
        except RuntimeError as ex:
            if "notify-before-result" not in str(ex):
                raise SystemExit("expected notify-before-result: %s" % ex)
    finally:
        note.stop()

    hang = FakeMCP("hang")
    hang.start()
    try:
        raised: BaseException | None = None
        try:
            call_tool("vrc_audit", {}, timeout=1, url=hang.url, skip_lease=True)
        except Exception as ex:
            raised = ex
        else:
            raise SystemExit("hang should not return a tool result")
        methods = [c.get("method") for c in hang.calls]
        if "initialize" not in methods:
            raise SystemExit("hang never reached FakeMCP initialize: %s / %s" % (methods, raised))
        if "tools/call" not in methods:
            raise SystemExit("hang never reached tools/call: %s / %s" % (methods, raised))
        text = str(raised).lower()
        if isinstance(raised, RuntimeError) and (
            "refused" in text or "lease" in text or "avatar" in text
        ):
            raise SystemExit("hang failed closed before FakeMCP hang: %s" % raised)
    finally:
        hang.stop()

    try:
        call_tool("execute_code", {}, timeout=1, url=DEAD_MCP)
        raise SystemExit("execute_code must refuse before HTTP")
    except RuntimeError as ex:
        if "refused" not in str(ex):
            raise SystemExit("expected refuse: %s" % ex)

    try:
        call_tool("vrc_audit", {}, timeout=1, url=DEAD_MCP)
        raise SystemExit("library call_tool must require JOB lease")
    except RuntimeError as ex:
        if "avatar" not in str(ex).lower() and "lease" not in str(ex).lower() and "NO_LEASE" not in str(ex):
            raise SystemExit("expected lease gate: %s" % ex)
    print("PASS fake mcp")


def test_cli_lease_before_http() -> None:
    dest = _seed("example-s00c-http")
    try:
        args = dest / "empty.json"
        args.write_text("{}\n", encoding="utf-8")
        isolated = os.environ.copy()
        isolated["VRC_DCC_MCP_URL"] = DEAD_MCP
        bare = subprocess.run(
            [PY, "unity_mcp_call.py", "vrc_audit", str(args)],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=isolated,
        )
        if bare.returncode != 2 or "--avatar" not in (bare.stderr or ""):
            raise SystemExit("CLI without --avatar: %s" % bare.stderr)
        nobegin = subprocess.run(
            [PY, "unity_mcp_call.py", "vrc_audit", str(args), "--avatar", "example-s00c-http"],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=isolated,
        )
        if nobegin.returncode != 2 or "NO_LEASE_BEGIN" not in (nobegin.stderr or ""):
            raise SystemExit("CLI without begin: %s" % nobegin.stderr)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    print("PASS cli lease before http")


def test_policy_allow_list_vrc_only() -> None:
    dest = _seed("example-s00c-pol")
    try:
        data = json.loads((dest / "POLICY.json").read_text(encoding="utf-8"))
        data["allow_mcp_tools"] = ["manage_scene"]
        errs = validate_policy("example-s00c-pol", data)
        if not any("vrc_" in e for e in errs):
            raise SystemExit("expected vrc_* allow_mcp_tools error, got %s" % errs)
        (dest / "POLICY.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        hs = subprocess.run(
            [PY, "handshake.py", "example-s00c-pol"],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if hs.returncode != 2:
            raise SystemExit("handshake should refuse generic allow_mcp_tools, got %s" % hs.returncode)
    finally:
        shutil.rmtree(dest, ignore_errors=True)
    print("PASS policy allow list")


if __name__ == "__main__":
    test_allowlist()
    test_lease_holders()
    test_gate_lease_cli()
    test_concurrent_begin()
    test_rpc_id_and_null_error()
    test_fake_mcp_notify_and_errors()
    test_cli_lease_before_http()
    test_policy_allow_list_vrc_only()
    print("PASS test_s00c_lease_allowlist")
