# -*- coding: utf-8 -*-
"""Merge a Unity dump into maps/<avatar>/graph.json. Never wipes notes.json."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from _stdio import utf8_stdio

HERE = Path(__file__).resolve().parent

# Vendor plugin object names only. Outfit/menu names are per-body:
# maps/<avatar>/dump-map.json (overlay). Unmapped dump rows stay unresolved.
DEFAULT_DUMP_NAME_TO_ID = {
    "ABT": "plugin.abt",
    "VRSuya_Suyasuya": "plugin.suyasuya",
    "SPS": "plugin.sps",
    "SPS_DLC": "plugin.sps_dlc",
    "Penetration Contact System": "plugin.pcs",
}


def dump_name_to_id(avatar: str) -> dict[str, str]:
    merged = dict(DEFAULT_DUMP_NAME_TO_ID)
    extra = HERE / avatar / "dump-map.json"
    if extra.is_file():
        data = json.loads(extra.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for k, v in data.items():
                merged[str(k)] = str(v)
    return merged


def parse_tsv(text: str) -> list[tuple[str, str, str | None]]:
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue
        parts = line.split("\t")
        name = parts[0].strip()
        hier = parts[1].strip() if len(parts) > 1 else ""
        extra = parts[2].strip() if len(parts) > 2 else None
        rows.append((name, hier, extra))
    return rows


def merge_json_nodes(graph: dict, incoming: dict) -> tuple[int, int]:
    by_id = {n["id"]: n for n in graph["nodes"]}
    added = updated = 0
    for node in incoming.get("nodes", []):
        nid = node.get("id")
        if not nid:
            continue
        if nid in by_id:
            keep = by_id[nid]
            for k, v in node.items():
                if k == "id":
                    continue
                if v not in (None, ""):
                    keep[k] = v
            updated += 1
        else:
            graph["nodes"].append(node)
            by_id[nid] = node
            added += 1
    if incoming.get("edges"):
        seen = {(e.get("from"), e.get("to"), e.get("rel")) for e in graph.get("edges", [])}
        graph.setdefault("edges", [])
        for e in incoming["edges"]:
            key = (e.get("from"), e.get("to"), e.get("rel"))
            if key not in seen:
                graph["edges"].append(e)
                seen.add(key)
    for k in ("avatar", "scene", "dump", "dump_note"):
        if incoming.get(k):
            graph[k] = incoming[k]
    return added, updated


def merge_tsv(graph: dict, rows: list[tuple[str, str, str | None]], mark_missing: bool, notes: dict, name_to_id: dict[str, str]) -> tuple[int, list[str], list[str]]:
    by_id = {n["id"]: n for n in graph["nodes"]}
    seen_ids: set[str] = set()
    updated = 0
    unresolved: list[str] = []
    for name, hier, extra in rows:
        nid = name_to_id.get(name)
        if not nid:
            unresolved.append(name)
            continue
        seen_ids.add(nid)
        node = by_id.get(nid)
        if not node:
            unresolved.append(name)
            continue
        if hier:
            node["hierarchy"] = hier
            updated += 1
        if extra and extra.startswith("active="):
            node["active"] = extra.split("=", 1)[1]
    missing: list[str] = []
    if mark_missing:
        today = date.today().isoformat()
        for name, nid in name_to_id.items():
            if nid in seen_ids:
                continue
            missing.append(nid)
            meta = notes.setdefault(nid, {"status": "observed", "note": "", "source": "unity-dump"})
            flag = "gone from dump " + today
            if flag not in (meta.get("note") or ""):
                prev = (meta.get("note") or "").strip()
                meta["note"] = (prev + " | " if prev else "") + flag
                meta["status"] = "observed"
    return updated, missing, unresolved


def render(avatar: str) -> None:
    custom = HERE / avatar / "render.py"
    if custom.is_file():
        import runpy
        runpy.run_path(str(custom), run_name="__main__")
        return
    from render_map import render as render_map
    render_map(HERE / avatar)


def main() -> int:
    utf8_stdio()
    p = argparse.ArgumentParser(description="Refresh maps/<avatar> from a dump; keep notes.json. No default product.")
    p.add_argument("avatar", help="maps/<avatar> folder. Required.")
    p.add_argument("--from-dump", dest="dump", help="TSV from unity-dump.txt, or a graph JSON")
    p.add_argument("--mark-missing", action="store_true", help="Flag mapped dump names not in this dump")
    p.add_argument("--render-only", action="store_true")
    args = p.parse_args()
    root = HERE / args.avatar
    gpath = root / "graph.json"
    npath = root / "notes.json"
    if not gpath.exists():
        print("no index:", root, file=sys.stderr)
        return 2
    if args.render_only:
        render(args.avatar)
        return 0
    if not args.dump:
        print("pass --from-dump FILE or --render-only", file=sys.stderr)
        return 2
    src = Path(args.dump)
    text = src.read_text(encoding="utf-8-sig")
    graph = json.loads(gpath.read_text(encoding="utf-8"))
    notes = json.loads(npath.read_text(encoding="utf-8")) if npath.exists() else {}
    stripped = text.lstrip()
    if stripped.startswith("{"):
        incoming = json.loads(text)
        added, updated = merge_json_nodes(graph, incoming)
        print("json merge  added:", added, " updated:", updated)
        missing: list[str] = []
    else:
        rows = parse_tsv(text)
        name_map = dump_name_to_id(args.avatar)
        updated, missing, unresolved = merge_tsv(graph, rows, args.mark_missing, notes, name_map)
        print("tsv merge  hierarchy updates:", updated, " rows:", len(rows))
        if unresolved:
            print("unresolved dump names (not merged, not deleted):", ", ".join(unresolved))
        graph["dump"] = "unity-dump"
        graph["dump_note"] = "Merged from " + src.name
    graph["updated"] = date.today().isoformat()
    gpath.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.mark_missing:
        npath.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if missing:
            print("marked missing:", ", ".join(missing))
    render(args.avatar)
    print("kept notes.json  ids:", len(notes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
