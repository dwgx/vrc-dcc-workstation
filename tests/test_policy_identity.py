# -*- coding: utf-8 -*-
"""S00-b: POLICY schema + unique identity picker. python tests/test_policy_identity.py"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
sys.path.insert(0, str(MAPS))

from identity import AMBIGUOUS, BAD_POLICY, MISSING_PATH, NOT_APPLICABLE, OK, pick_unique  # noqa: E402
from policy import validate_policy  # noqa: E402

PY = sys.executable


def _seed(aid: str) -> Path:
    dest = MAPS / aid
    if dest.exists():
        shutil.rmtree(dest)
    r = subprocess.run([PY, "init_avatar.py", aid], cwd=str(MAPS), capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("init_avatar failed: %s %s" % (r.stdout, r.stderr))
    return dest


def _handshake(aid: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, "handshake.py", aid],
        cwd=str(MAPS),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_picker() -> None:
    z = pick_unique(explicit=None, candidates=[])
    assert z["status"] == NOT_APPLICABLE and z["path"] is None
    one = pick_unique(explicit=None, candidates=["Root/Body"])
    assert one["status"] == OK and one["path"] == "Root/Body"
    two = pick_unique(explicit=None, candidates=["A/Body", "B/Body"])
    assert two["status"] == AMBIGUOUS and two["path"] is None
    miss = pick_unique(explicit="Body_b", candidates=["Root/Other"])
    assert miss["status"] == MISSING_PATH
    hit = pick_unique(explicit="Root/Body", candidates=["Root/Body", "Root/Hair"])
    assert hit["status"] == OK and hit["path"] == "Root/Body"
    bad = pick_unique(explicit="  ", candidates=["Root/Body"])
    assert bad["status"] == BAD_POLICY
    print("PASS picker")


def test_policy_ok_and_mismatch() -> None:
    dest = _seed("example-s00b")
    try:
        data = json.loads((dest / "POLICY.json").read_text(encoding="utf-8"))
        assert validate_policy("example-s00b", data) == []
        hs = _handshake("example-s00b")
        if hs.returncode != 0:
            raise SystemExit("handshake seed should pass: %s %s" % (hs.stdout, hs.stderr))
        data["avatar"] = "other-body"
        (dest / "POLICY.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        bad = _handshake("example-s00b")
        if bad.returncode != 2:
            raise SystemExit("expected handshake exit 2 on avatar mismatch, got %s" % bad.returncode)
        if "must equal maps folder" not in (bad.stderr or ""):
            raise SystemExit("expected mismatch text: %s" % bad.stderr)
        print("PASS policy mismatch")
    finally:
        shutil.rmtree(dest, ignore_errors=True)


def test_policy_placeholder_and_schema() -> None:
    dest = _seed("example-s00b-ph")
    try:
        data = json.loads((dest / "POLICY.json").read_text(encoding="utf-8"))
        data["unity_root_name"] = "AVATAR_ID"
        (dest / "POLICY.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        hs = _handshake("example-s00b-ph")
        if hs.returncode != 2:
            raise SystemExit("placeholder root should fail handshake")
        data["unity_root_name"] = "example-s00b-ph"
        data["schema"] = 99
        (dest / "POLICY.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        hs2 = _handshake("example-s00b-ph")
        if hs2.returncode != 2:
            raise SystemExit("bad schema should fail handshake")
        print("PASS placeholder and schema")
    finally:
        shutil.rmtree(dest, ignore_errors=True)


def test_policy_duplicate_tools_and_empty_path() -> None:
    dest = _seed("example-s00b-dup")
    try:
        data = json.loads((dest / "POLICY.json").read_text(encoding="utf-8"))
        data["disable_mcp_tools"] = ["execute_code", "execute_code"]
        (dest / "POLICY.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        hs = _handshake("example-s00b-dup")
        if hs.returncode != 2:
            raise SystemExit("duplicate disable_mcp_tools should fail")
        data["disable_mcp_tools"] = ["execute_code"]
        data["nipple_smr_path"] = ""
        (dest / "POLICY.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        hs2 = _handshake("example-s00b-dup")
        if hs2.returncode != 2:
            raise SystemExit("empty nipple_smr_path should fail")
        print("PASS duplicate tools and empty path")
    finally:
        shutil.rmtree(dest, ignore_errors=True)


if __name__ == "__main__":
    test_picker()
    test_policy_ok_and_mismatch()
    test_policy_placeholder_and_schema()
    test_policy_duplicate_tools_and_empty_path()
    print("PASS test_policy_identity")
