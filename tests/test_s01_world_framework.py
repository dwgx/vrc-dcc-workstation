# -*- coding: utf-8 -*-
"""World map handshake/gate + cross-domain allowlist. No live Editor."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
sys.path.insert(0, str(MAPS))

from allowlist import check_tool  # noqa: E402

PY = sys.executable


def test_world_allowlist() -> None:
    ok, r = check_tool("world_probe", domain="world")
    assert not ok and "not implemented" in r
    listed, r_listed = check_tool(
        "world_probe",
        {"allow_mcp_tools": ["world_probe"]},
        domain="world",
    )
    assert not listed and "not implemented" in r_listed
    dump, r_dump = check_tool("world_scene_dump", domain="world")
    assert not dump and "not implemented" in r_dump
    bad, r = check_tool("vrc_audit", domain="world")
    assert not bad and "cross-domain" in r
    bad2, r2 = check_tool("execute_code", domain="world")
    assert not bad2 and "denied" in r2
    still, r3 = check_tool("world_probe", domain="avatar")
    assert not still and "cross-domain" in r3
    print("PASS world allowlist")


def test_world_handshake_cli() -> None:
    world_id = "example-s01a-" + uuid.uuid4().hex[:8]
    dest = MAPS / "worlds" / world_id
    assert not dest.exists()
    try:
        r = subprocess.run(
            [PY, "init_world.py", world_id],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if r.returncode != 0:
            raise SystemExit("init_world: %s %s" % (r.stdout, r.stderr))
        hs = subprocess.run(
            [PY, "world_handshake.py", world_id],
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
        assert "production_route: discover_installed_editor_tools" in hs.stdout
        assert "job sku" not in hs.stdout
        hs_json = subprocess.run(
            [PY, "world_handshake.py", world_id, "--json"], cwd=MAPS,
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        payload = json.loads(hs_json.stdout)
        assert payload["implemented_world_tools"] is False
        assert payload["station_adapter_optional"] is True
        assert payload["policy_scope"] == "station_named_tool_client"
        assert (ROOT / payload["production_guide"]).is_file()
        assert "sku_quota" not in payload["job"]
        env = os.environ.copy()
        env["VRC_DCC_JOB_HOLDER"] = "world-holder"
        b = subprocess.run(
            [PY, "world_gate.py", world_id, "begin", "example.world-probe", "--ttl", "3600"],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        if b.returncode != 0:
            raise SystemExit("world begin: %s %s" % (b.stdout, b.stderr))

        def gate(*args: str, code: int = 0) -> subprocess.CompletedProcess:
            result = subprocess.run(
                [PY, "world_gate.py", world_id, *args], cwd=MAPS,
                capture_output=True, text=True, encoding="utf-8", env=env,
            )
            assert result.returncode == code, (args, result.stdout, result.stderr)
            return result

        # Two production slices in one task, with another writer still excluded.
        review_path = dest / "REVIEW.json"
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["items"].append({**review["items"][0], "id": "example.room"})
        review_path.write_text(json.dumps(review) + "\n", encoding="utf-8")
        gate("mutated")
        job_path = dest / "JOB.json"
        before = job_path.read_bytes()
        lease_id = json.loads(before)["lease"]["id"]
        competing = gate("begin", "example.room", "--holder", "other-writer", code=2)
        assert "LEASE_HELD" in competing.stdout + competing.stderr
        assert job_path.read_bytes() == before
        gate("begin", "example.room")
        job = json.loads(job_path.read_text(encoding="utf-8"))
        assert job["open_slice"] == "example.room" and job["mutation_revision"] == 1
        assert job["lease"]["id"] == lease_id and job["lease"]["slice"] == "example.room"
        assert not {"sku_quota", "sku_used", "skus", "avatar"}.intersection(job)

        # Reset is a lease release, not a way to make stale evidence fresh again.
        gate("reset")
        job = json.loads(job_path.read_text(encoding="utf-8"))
        assert job["lease"] is None and job["open_slice"] is None
        assert job["mutation_revision"] == 1 and job["mutated"] is True

        # Old overlays remain usable; inherited Avatar quotas have no World effect.
        pol = json.loads((dest / "POLICY.json").read_text(encoding="utf-8"))
        pol["sku_quota"] = 1
        (dest / "POLICY.json").write_text(json.dumps(pol) + "\n", encoding="utf-8")
        job.update(sku_quota=1, sku_used=1, skus=["legacy-avatar-only"])
        job_path.write_text(json.dumps(job) + "\n", encoding="utf-8")
        gate("begin", "example.world-probe")
        gate("mutated")
        gate("begin", "example.room")
        job = json.loads(job_path.read_text(encoding="utf-8"))
        assert job["mutation_revision"] == 2
        assert not {"sku_quota", "sku_used", "skus"}.intersection(job)
        before = job_path.read_bytes()
        gate("begin", "missing.row", code=2)
        assert job_path.read_bytes() == before

        pol["avatar"] = "nope"
        (dest / "POLICY.json").write_text(json.dumps(pol, indent=2) + "\n", encoding="utf-8")
        bad = subprocess.run(
            [PY, "world_handshake.py", world_id],
            cwd=str(MAPS),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if bad.returncode != 2:
            raise SystemExit("expected handshake 2 on avatar field, got %s" % bad.returncode)
        print("PASS world handshake cli")
    finally:
        assert dest.resolve().parent == (MAPS / "worlds").resolve()
        assert dest.name == world_id and world_id.startswith("example-s01a-")
        shutil.rmtree(dest, ignore_errors=True)
        worlds = MAPS / "worlds"
        if worlds.is_dir() and not any(worlds.iterdir()):
            worlds.rmdir()


if __name__ == "__main__":
    test_world_allowlist()
    test_world_handshake_cli()
    print("PASS test_s01_world_framework")
