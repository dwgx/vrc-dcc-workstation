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

HANDSHAKE = "1.0-world"
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
        "disable_mcp_tools": policy.get("disable_mcp_tools") or [],
        "job": {
            "sku_quota": int(policy.get("sku_quota") or job.get("sku_quota") or 1),
            "sku_used": int(job.get("sku_used") or 0),
            "open_slice": job.get("open_slice"),
            "mutated": bool(job.get("mutated")),
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
            "world_* are proposed, not on com.vrc-dcc.tools. Do not invent execute_code. "
            "Do not POST 8080 from station. Do not install Avatar SDK into a Worlds project."
        ),
        "next": "python maps/world_gate.py %s begin <review-id> (lease only; no live dump)" % name,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print("handshake", HANDSHAKE)
    print("world:", name)
    print("kind: world-product")
    print("proposed_tools:", " ".join(PROPOSED))
    print("implemented_world_tools: false")
    print("disable_mcp_tools:", " ".join(payload["disable_mcp_tools"]) if payload["disable_mcp_tools"] else "-")
    j = payload["job"]
    lease = j.get("lease") or {}
    print(
        "job sku %d/%d slice=%s mutated=%s lease=%s"
        % (j["sku_used"], j["sku_quota"], j["open_slice"] or "-", j["mutated"], lease.get("holder") or "-")
    )
    print("open:", len(nxt))
    print("unity:", payload["unity"])
    print("next:", payload["next"])
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
