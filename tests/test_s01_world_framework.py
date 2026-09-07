# -*- coding: utf-8 -*-
"""World map handshake/gate + cross-domain allowlist. No live Editor."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
sys.path.insert(0, str(MAPS))

from allowlist import check_tool  # noqa: E402

PY = sys.executable


def test_world_allowlist() -> None:
    ok, _ = check_tool("world_probe", domain="world")
    assert ok
    bad, r = check_tool("vrc_audit", domain="world")
    assert not bad and "cross-domain" in r
    bad2, r2 = check_tool("execute_code", domain="world")
    assert not bad2 and "denied" in r2
    still, r3 = check_tool("world_probe", domain="avatar")
    assert not still and "cross-domain" in r3
    print("PASS world allowlist")


def test_world_handshake_cli() -> None:
    dest = MAPS / "worlds" / "example-s01a"
    if dest.exists():
        shutil.rmtree(dest)
    try:
        r = subprocess.run(
            [PY, "init_world.py", "example-s01a"],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if r.returncode != 0:
            raise SystemExit("init_world: %s %s" % (r.stdout, r.stderr))
        hs = subprocess.run(
            [PY, "world_handshake.py", "example-s01a"],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if hs.returncode != 0:
            raise SystemExit("world_handshake: %s %s" % (hs.stdout, hs.stderr))
        if "kind: world-product" not in (hs.stdout or ""):
            raise SystemExit("expected world-product: %s" % hs.stdout)
        if "implemented_world_tools: false" not in (hs.stdout or ""):
            raise SystemExit("expected proposed-only: %s" % hs.stdout)
        env = os.environ.copy()
        env["VRC_DCC_JOB_HOLDER"] = "world-holder"
        b = subprocess.run(
            [PY, "world_gate.py", "example-s01a", "begin", "example.world-probe", "--ttl", "3600"],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        if b.returncode != 0:
            raise SystemExit("world begin: %s %s" % (b.stdout, b.stderr))
        pol = json.loads((dest / "POLICY.json").read_text(encoding="utf-8"))
        pol["avatar"] = "nope"
        (dest / "POLICY.json").write_text(json.dumps(pol, indent=2) + "\n", encoding="utf-8")
        bad = subprocess.run(
            [PY, "world_handshake.py", "example-s01a"],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if bad.returncode != 2:
            raise SystemExit("expected handshake 2 on avatar field, got %s" % bad.returncode)
        print("PASS world handshake cli")
    finally:
        shutil.rmtree(dest, ignore_errors=True)
        worlds = MAPS / "worlds"
        if worlds.is_dir() and not any(worlds.iterdir()):
            worlds.rmdir()


if __name__ == "__main__":
    test_world_allowlist()
    test_world_handshake_cli()
    print("PASS test_s01_world_framework")
