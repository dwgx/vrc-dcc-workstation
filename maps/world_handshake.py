# -*- coding: utf-8 -*-
"""World product handshake. No Unity write. Named world_* are proposed.

  python world_handshake.py <world-id>
  python world_handshake.py <world-id> --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _stdio import utf8_stdio
from product import WORLD, product_dir
from review import lint_data, load_review_folder, open_items
from world_policy import validate_world_policy

HANDSHAKE = "1.1-world"
PROPOSED = ["world_probe", "world_scene_dump", "world_udon_inventory"]


def cmd_handshake(name: str, as_json: bool) -> int:
    dest = product_dir(name, WORLD)
    if not dest.is_dir():
        print(
            "error: no maps/worlds/%s/ — python maps/init_world.py %s" % (name, name),
            file=sys.stderr,
        )
        return 2
    policy_file = dest / "POLICY.json"
    if not policy_file.is_file():
        print("error: missing %s" % policy_file, file=sys.stderr)
        return 2
    policy = json.loads(policy_file.read_text(encoding="utf-8"))
    errs = validate_world_policy(name, policy)
    if errs:
        print("error:", "; ".join(errs), file=sys.stderr)
        return 2
    try:
        data = load_review_folder(dest)
    except SystemExit as ex:
        print("error:", ex, file=sys.stderr)
        return 2
    lint = lint_data(data)
    if lint:
        for e in lint:
            print(e, file=sys.stderr)
        return 2
    job_path = dest / "JOB.json"
    job = json.loads(job_path.read_text(encoding="utf-8")) if job_path.is_file() else {}
    nxt = open_items(data)
    payload = {
        "ok": True,
        "handshake": HANDSHAKE,
        "world": name,
        "kind": "world-product",
        "domain": WORLD,
        "policy": str(policy_file.as_posix()),
        "proposed_tools": PROPOSED,
        "implemented_world_tools": False,
        "production_route": "discover_installed_editor_tools",
        "production_guide": "docs/WORLD_PRODUCTION.md",
        "station_adapter_optional": True,
        "policy_scope": "station_named_tool_client",
        "disable_mcp_tools": policy.get("disable_mcp_tools") or [],
        "job": {
            "open_slice": job.get("open_slice"),
            "mutated": bool(job.get("mutated")),
            "mutation_revision": int(job.get("mutation_revision") or 0),
            "lease": job.get("lease") if isinstance(job.get("lease"), dict) else None,
        },
        "open": [
            {
                "id": it.get("id"),
                "status": it.get("status"),
                "gate": it.get("gate"),
                "title": it.get("title"),
            }
            for it in nxt
        ],
        "unity": (
            "Installed project tools can support World production now. Discover their actual schemas "
            "and verify the selected Editor/project. Proposed station world_* are not implemented; "
            "their roadmap does not block native MCP, CLI, SDK or project-owned Editor builders. "
            "Keep Avatar and World SDKs in their respective projects."
        ),
        "next": "Follow docs/WORLD_PRODUCTION.md in the authorized World project",
        "station_ledger_next": "python maps/world_gate.py %s begin <review-id> (optional ledger)" % name,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print("handshake", HANDSHAKE)
    print("world:", name)
    print("kind: world-product")
    print("proposed_tools:", " ".join(PROPOSED))
    print("implemented_world_tools: false")
    print("production_route:", payload["production_route"])
    print("production_guide:", payload["production_guide"])
    print("policy_scope:", payload["policy_scope"])
    print("disable_mcp_tools:", " ".join(payload["disable_mcp_tools"]) if payload["disable_mcp_tools"] else "-")
    j = payload["job"]
    lease = j.get("lease") or {}
    print(
        "job slice=%s mutated=%s revision=%d lease=%s"
        % (j["open_slice"] or "-", j["mutated"], j["mutation_revision"], lease.get("holder") or "-")
    )
    print("open:", len(nxt))
    print("unity:", payload["unity"])
    print("next:", payload["next"])
    print("station_ledger_next:", payload["station_ledger_next"])
    return 0


def main() -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Per-world handshake (no Unity write)")
    ap.add_argument("world")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()
    return cmd_handshake(args.world.strip().lower(), args.as_json)


if __name__ == "__main__":
    raise SystemExit(main())
