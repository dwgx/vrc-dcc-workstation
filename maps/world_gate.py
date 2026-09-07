# -*- coding: utf-8 -*-
"""World JOB lease. No Unity. No live world_* HTTP.

  python world_gate.py <world-id>
  python world_gate.py <world-id> job
  python world_gate.py <world-id> begin <review-id>
  python world_gate.py <world-id> mutated
  python world_gate.py <world-id> reset

Same lease tokens as gate.py. Named world_* dumps are S01-c (not this file).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from _stdio import utf8_stdio
from gate import JOB_DEFAULT, lock_folder, refuse
from lease import acquire, iso, lease_active, now_utc, require_http, resolve_holder, ttl_sec
from product import WORLD, product_dir
from review import lint_data, load_review_folder
from world_policy import validate_world_policy


def wdir(name: str) -> Path:
    return product_dir(name, WORLD)


def load_job(name: str) -> dict:
    path = wdir(name) / "JOB.json"
    if not path.is_file():
        data = dict(JOB_DEFAULT)
        data["domain"] = WORLD
        data["world"] = name
        return data
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("JOB.json must be an object")
    return data


def save_job(name: str, data: dict) -> None:
    data["domain"] = WORLD
    data["world"] = name
    data.pop("avatar", None)
    data["updated"] = date.today().isoformat()
    path = wdir(name) / "JOB.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _policy(name: str) -> dict:
    path = wdir(name) / "POLICY.json"
    if not path.is_file():
        return {}
    try:
        pol = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return pol if isinstance(pol, dict) else {}


def cmd_begin(name: str, slice_id: str, holder: str = "", ttl_override: int = 0) -> int:
    dest = wdir(name)
    if not dest.is_dir():
        return refuse("no maps/worlds/%s/ — python maps/init_world.py %s" % (name, name))
    pol = _policy(name)
    verrs = validate_world_policy(name, pol) if pol else ["missing POLICY.json"]
    if verrs:
        return refuse("; ".join(verrs))
    try:
        review = load_review_folder(dest)
    except SystemExit as ex:
        return refuse(str(ex))
    lint = lint_data(review)
    if lint:
        return refuse("; ".join(lint))
    ids = {str(it.get("id")) for it in (review.get("items") or []) if it.get("id")}
    if not slice_id:
        return refuse("begin needs a REVIEW row id")
    if slice_id not in ids:
        return refuse("begin id is not a REVIEW row; python maps/world_handshake.py %s" % name)
    with lock_folder(dest):
        job = load_job(name)
        if pol.get("sku_quota"):
            try:
                job["sku_quota"] = int(pol["sku_quota"])
            except (TypeError, ValueError):
                pass
        open_id = job.get("open_slice")
        if open_id and open_id != slice_id:
            return refuse(
                "second product this chat; python maps/world_gate.py %s reset" % name,
                {"open_slice": open_id, "wanted": slice_id},
            )
        who = resolve_holder(holder)
        job, err = acquire(job, holder=who, slice_id=slice_id, ttl=ttl_sec(pol, ttl_override))
        if err:
            return refuse(err, {"error": err, "lease": job.get("lease")})
        job["open_slice"] = slice_id
        save_job(name, job)
        lease = job.get("lease") or {}
    print(
        json.dumps(
            {
                "ok": True,
                "domain": WORLD,
                "open_slice": slice_id,
                "lease": lease,
                "world_tools": "proposed",
            },
            ensure_ascii=False,
        )
    )
    return 0


def cmd_mutated(name: str, holder: str = "") -> int:
    dest = wdir(name)
    with lock_folder(dest):
        job = load_job(name)
        if not job.get("open_slice"):
            return refuse("mutated needs begin first")
        held = require_http(job, resolve_holder(holder))
        if held:
            return refuse(held, {"lease": job.get("lease")})
        job["mutated"] = True
        job["mutated_at"] = iso(now_utc())
        save_job(name, job)
        payload = {"ok": True, "mutated": True, "open_slice": job.get("open_slice")}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def cmd_reset(name: str, holder: str = "", force: bool = False) -> int:
    dest = wdir(name)
    with lock_folder(dest):
        job = load_job(name)
        if lease_active(job) and not force:
            held = require_http(job, resolve_holder(holder))
            if held:
                return refuse(held, {"lease": job.get("lease")})
        quota = int(job.get("sku_quota") or 1)
        fresh = dict(JOB_DEFAULT)
        fresh["domain"] = WORLD
        fresh["world"] = name
        fresh["sku_quota"] = quota
        fresh["note"] = job.get("note") or ""
        save_job(name, fresh)
        payload = {"ok": True, "reset": True, "domain": WORLD}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def cmd_job(name: str) -> int:
    print(json.dumps(load_job(name), ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(description="World JOB gate (no Unity, no world_* HTTP)")
    ap.add_argument("world")
    ap.add_argument("cmd", nargs="?", default="job", choices=("job", "begin", "mutated", "reset"))
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--holder", default="")
    ap.add_argument("--ttl", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    name = args.world.strip().lower()
    if args.cmd == "job":
        return cmd_job(name)
    if args.cmd == "begin":
        return cmd_begin(name, args.arg.strip(), holder=args.holder, ttl_override=args.ttl)
    if args.cmd == "mutated":
        return cmd_mutated(name, holder=args.holder)
    return cmd_reset(name, holder=args.holder, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
