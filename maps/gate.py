# -*- coding: utf-8 -*-
"""Slice gate: review board + JOB.json sku quota + chat lease. Does not write Unity.

  python gate.py <avatar>
  python gate.py <avatar> --json
  python gate.py <avatar> job
  python gate.py <avatar> begin <review-id>
  python gate.py <avatar> consume-sku <booth-id>
  python gate.py <avatar> mutated
  python gate.py <avatar> reset

begin requires an existing REVIEW.json row id. Handshake first: python handshake.py <avatar>.
Set VRC_DCC_JOB_HOLDER (or --holder) so a second chat cannot mutate while the lease is live.

Exit 2 on lint fail, quota, second-product, or LEASE_HELD / LEASE_EXPIRED.
Home may run this. It does not call Unity HTTP (unlike audit.py).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from _stdio import utf8_stdio
from lease import acquire, require, resolve_holder, ttl_sec
from review import load_review, lint_data, open_items

HERE = Path(__file__).resolve().parent
JOB_DEFAULT = {
    "schema": 1,
    "sku_quota": 1,
    "sku_used": 0,
    "skus": [],
    "open_slice": None,
    "mutated": False,
    "lease": None,
}


def job_path(name: str) -> Path:
    return HERE / name / "JOB.json"


def load_job(name: str) -> dict:
    path = job_path(name)
    if not path.is_file():
        data = dict(JOB_DEFAULT)
        data["avatar"] = name
        return data
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("JOB.json must be an object")
    return data


def save_job(name: str, data: dict) -> None:
    data["avatar"] = name
    data["updated"] = date.today().isoformat()
    path = job_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def refuse(msg: str, extra: dict | None = None) -> int:
    payload = {"ok": False, "error": msg}
    if extra:
        payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
    print("error:", msg, file=sys.stderr)
    return 2


def cmd_status(name: str, as_json: bool) -> int:
    data = load_review(name)
    errs = lint_data(data)
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 2
    nxt = open_items(data)
    job = load_job(name)
    lease = job.get("lease") if isinstance(job.get("lease"), dict) else {}
    payload = {
        "ok": True,
        "avatar": data.get("avatar", name),
        "job": {
            "sku_quota": int(job.get("sku_quota") or 1),
            "sku_used": int(job.get("sku_used") or 0),
            "skus": job.get("skus") or [],
            "open_slice": job.get("open_slice"),
            "mutated": bool(job.get("mutated")),
            "lease_holder": lease.get("holder"),
            "lease_expires": lease.get("expires"),
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
        "unity": "named vrc_* tools in unity/vrc-dcc-tools; do not invent execute_code",
        "home": "do not python maps/audit.py mutate from home cwd",
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print("ok gate", name, "open", len(nxt), "lessons", payload["lessons"])
    j = payload["job"]
    print(
        "job sku %d/%d slice=%s mutated=%s lease=%s until %s"
        % (
            j["sku_used"],
            j["sku_quota"],
            j["open_slice"] or "-",
            j["mutated"],
            j.get("lease_holder") or "-",
            j.get("lease_expires") or "-",
        )
    )
    for it in nxt[:8]:
        print("%s\t%s\t%s\t%s" % (it["status"], it["gate"], it["id"], it.get("title") or ""))
    if len(nxt) > 8:
        print("…", len(nxt) - 8, "more; use --json")
    return 0


def cmd_job(name: str) -> int:
    print(json.dumps(load_job(name), ensure_ascii=False, indent=2))
    return 0


def review_ids(name: str) -> set[str]:
    data = load_review(name)
    return {str(it.get("id")) for it in (data.get("items") or []) if it.get("id")}


def _policy_dict(name: str) -> dict:
    policy_file = HERE / name / "POLICY.json"
    if not policy_file.is_file():
        return {}
    try:
        pol = json.loads(policy_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return pol if isinstance(pol, dict) else {}


def cmd_begin(name: str, slice_id: str, holder: str = "", ttl_override: int = 0) -> int:
    if not slice_id:
        return refuse("begin needs a REVIEW row id")
    ids = review_ids(name)
    if slice_id not in ids:
        return refuse(
            "begin id is not a REVIEW row; python maps/handshake.py %s" % name,
            {"wanted": slice_id},
        )
    job = load_job(name)
    pol = _policy_dict(name)
    if pol.get("sku_quota"):
        try:
            job["sku_quota"] = int(pol["sku_quota"])
        except (TypeError, ValueError):
            pass
    open_id = job.get("open_slice")
    if open_id and open_id != slice_id:
        return refuse(
            "second product this chat; python maps/gate.py %s reset or new Unity chat" % name,
            {"open_slice": open_id, "wanted": slice_id},
        )
    if job.get("mutated") and open_id and open_id != slice_id:
        return refuse("already mutated another slice this chat")
    who = resolve_holder(holder)
    job, err = acquire(
        job,
        holder=who,
        slice_id=slice_id,
        ttl=ttl_sec(pol, ttl_override),
    )
    if err:
        extra = {"error": err, "lease": job.get("lease")}
        return refuse(err, extra)
    job["open_slice"] = slice_id
    save_job(name, job)
    lease = job.get("lease") or {}
    print(
        json.dumps(
            {
                "ok": True,
                "open_slice": slice_id,
                "lease": lease,
                "holder_env": "VRC_DCC_JOB_HOLDER",
            },
            ensure_ascii=False,
        )
    )
    return 0


def cmd_consume_sku(name: str, sku: str, holder: str = "") -> int:
    if not sku:
        return refuse("consume-sku needs a Booth id or pack name")
    job = load_job(name)
    if not job.get("open_slice"):
        return refuse(
            "consume-sku needs begin first; python maps/gate.py %s begin <review-id>" % name
        )
    held = require(job, resolve_holder(holder))
    if held:
        return refuse(held, {"lease": job.get("lease")})
    used = int(job.get("sku_used") or 0)
    quota = int(job.get("sku_quota") or 1)
    if used >= quota:
        return refuse(
            "sku_quota exhausted; Owner looks in Edit, then new chat or gate.py reset",
            {"sku_used": used, "sku_quota": quota, "skus": job.get("skus") or []},
        )
    skus = list(job.get("skus") or [])
    skus.append(sku)
    job["skus"] = skus
    job["sku_used"] = used + 1
    save_job(name, job)
    print(
        json.dumps(
            {"ok": True, "sku": sku, "sku_used": job["sku_used"], "sku_quota": quota},
            ensure_ascii=False,
        )
    )
    return 0


def cmd_mutated(name: str, holder: str = "") -> int:
    job = load_job(name)
    if not job.get("open_slice"):
        return refuse(
            "mutated needs begin first; python maps/gate.py %s begin <review-id>" % name
        )
    held = require(job, resolve_holder(holder))
    if held:
        return refuse(held, {"lease": job.get("lease")})
    job["mutated"] = True
    save_job(name, job)
    print(json.dumps({"ok": True, "mutated": True, "open_slice": job.get("open_slice")}, ensure_ascii=False))
    return 0


def cmd_reset(name: str) -> int:
    job = load_job(name)
    quota = int(job.get("sku_quota") or 1)
    fresh = dict(JOB_DEFAULT)
    fresh["avatar"] = name
    fresh["sku_quota"] = quota
    fresh["note"] = job.get("note") or ""
    fresh["lease"] = None
    save_job(name, fresh)
    print(json.dumps({"ok": True, "reset": True, "sku_quota": quota}, ensure_ascii=False))
    return 0


def main() -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="Review + JOB gate (no Unity write)")
    ap.add_argument("avatar")
    ap.add_argument(
        "cmd",
        nargs="?",
        default="status",
        choices=("status", "job", "begin", "consume-sku", "mutated", "reset"),
    )
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--holder", default="", help="chat lease holder (or env VRC_DCC_JOB_HOLDER)")
    ap.add_argument("--ttl", type=int, default=0, help="lease ttl seconds for begin")
    args = ap.parse_args()
    name = args.avatar.strip().lower()
    if args.cmd == "status":
        return cmd_status(name, args.as_json)
    if args.cmd == "job":
        return cmd_job(name)
    if args.cmd == "begin":
        return cmd_begin(name, args.arg.strip(), holder=args.holder, ttl_override=args.ttl)
    if args.cmd == "consume-sku":
        return cmd_consume_sku(name, args.arg.strip(), holder=args.holder)
    if args.cmd == "mutated":
        return cmd_mutated(name, holder=args.holder)
    return cmd_reset(name)


if __name__ == "__main__":
    raise SystemExit(main())
