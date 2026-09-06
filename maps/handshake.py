# -*- coding: utf-8 -*-
"""One-shot product handshake (session-probe analog for one avatar map).

  python handshake.py <avatar>
  python handshake.py <avatar> --json

No Unity write. Exit 2 on missing map, missing POLICY, or REVIEW lint fail.
Tracked output is English. Chat with the Owner stays in their locale.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _stdio import utf8_stdio
from gate import load_job
from policy import validate_policy
from review import lint_data, load_review, open_items

HERE = Path(__file__).resolve().parent
HANDSHAKE = "1.0"


def policy_path(name: str) -> Path:
    return HERE / name / "POLICY.json"


def load_policy(name: str) -> dict:
    path = policy_path(name)
    if not path.is_file():
        raise SystemExit("missing %s (copy maps/templates/POLICY.json)" % path)
    data = json.loads(path.read_text(encoding="utf-8"))
    errs = validate_policy(name, data)
    if errs:
        raise SystemExit("; ".join(errs))
    return data


def cmd_handshake(name: str, as_json: bool) -> int:
    dest = HERE / name
    if not dest.is_dir():
        print("error: no maps/%s/ — python maps/init_avatar.py %s" % (name, name), file=sys.stderr)
        return 2
    try:
        policy = load_policy(name)
    except SystemExit as ex:
        print("error:", ex, file=sys.stderr)
        return 2
    data = load_review(name)
    errs = lint_data(data)
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 2
    job = load_job(name)
    quota = int(policy.get("sku_quota") or job.get("sku_quota") or 1)
    nxt = open_items(data)
    payload = {
        "ok": True,
        "handshake": HANDSHAKE,
        "avatar": name,
        "kind": "dcc-product",
        "policy": str(policy_path(name).as_posix()),
        "unity_root_name": policy.get("unity_root_name") or name,
        "body_token": policy.get("body_token") or "",
        "require_prefab_path": bool(policy.get("require_prefab_path", True)),
        "nipple_smr_path": (policy.get("nipple_smr_path") or "").strip(),
        "gogo_root_path": (policy.get("gogo_root_path") or "").strip(),
        "disable_mcp_tools": policy.get("disable_mcp_tools") or [],
        "job": {
            "sku_quota": quota,
            "sku_used": int(job.get("sku_used") or 0),
            "open_slice": job.get("open_slice"),
            "mutated": bool(job.get("mutated")),
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
        "lessons": len(data.get("lessons") or []),
        "files": {
            "state": str((dest / "STATE.md").as_posix()) if (dest / "STATE.md").is_file() else None,
            "map": str((dest / "MAP.md").as_posix()) if (dest / "MAP.md").is_file() else None,
            "conflicts": str((dest / "conflicts.json").as_posix()) if (dest / "conflicts.json").is_file() else None,
            "review": str((dest / "REVIEW.json").as_posix()),
        },
        "unity": "named vrc_* only if THIS chat has unityMCP and the Editor is this avatar. If Unity MCP is off or another product is open: station-only, do not POST 8080, do not Start CoplayDev on the foreign Editor",
        "tongue": "chat in owner locale (zh-CN/ja/en/ko); tracked files English; public git optional",
        "next": "python maps/gate.py %s begin <review-id> then one vrc_* IFF unityMCP is in this chat; else station hygiene / paste" % name,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print("handshake", HANDSHAKE)
    print("avatar:", name)
    print("kind: dcc-product")
    print("policy:", payload["policy"])
    print("unity_root_name:", payload["unity_root_name"])
    print("body_token:", payload["body_token"] or "-")
    print("require_prefab_path:", str(payload["require_prefab_path"]).lower())
    print("nipple_smr_path:", payload["nipple_smr_path"] or "-")
    print("gogo_root_path:", payload["gogo_root_path"] or "-")
    tools = payload["disable_mcp_tools"]
    print("disable_mcp_tools:", " ".join(tools) if tools else "-")
    j = payload["job"]
    print(
        "job sku %d/%d slice=%s mutated=%s"
        % (j["sku_used"], j["sku_quota"], j["open_slice"] or "-", j["mutated"])
    )
    print("open:", len(nxt), "lessons:", payload["lessons"])
    for it in nxt[:8]:
        print("%s\t%s\t%s\t%s" % (it["status"], it["gate"], it["id"], it.get("title") or ""))
    if len(nxt) > 8:
        print("…", len(nxt) - 8, "more; use --json")
    files = payload["files"]
    print("state:", files["state"] or "-")
    print("map:", files["map"] or "-")
    print("unity:", payload["unity"])
    print("tongue:", payload["tongue"])
    print("next:", payload["next"])
    return 0


def main() -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Per-avatar handshake (no Unity write)")
    ap.add_argument("avatar")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()
    return cmd_handshake(args.avatar.strip().lower(), args.as_json)


if __name__ == "__main__":
    raise SystemExit(main())
