# -*- coding: utf-8 -*-
"""Merge catalog.json + notes.json -> LIBRARY.md. Do not hand-edit LIBRARY.md."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
from _stdio import utf8_stdio
from library.paths import usb_root


def load() -> tuple[dict, dict]:
    catalog = json.loads((HERE / "catalog.json").read_text(encoding="utf-8"))
    notes = json.loads((HERE / "notes.json").read_text(encoding="utf-8")) if (HERE / "notes.json").exists() else {}
    return catalog, notes


def kaguya_of(note: dict | None) -> str:
    if not note or "kaguya" not in note:
        return "unset"
    val = note.get("kaguya")
    if val in (None, ""):
        return "unset"
    return str(val)


def render() -> Path:
    catalog, notes = load()
    by_id = {n["id"]: n for n in catalog.get("nodes", [])}
    lines: list[str] = []
    shelf = str(usb_root() or catalog.get("root") or "(unset)")
    lines.append("# USB library")
    lines.append("")
    lines.append("Generated. Structure: `scan.py`. Remarks: `notes.json` (never wipe). Agents and humans Read **this file**.")
    lines.append("")
    lines.append("- root: `{0}`  updated: `{1}`  packs: `{2}`".format(
        catalog.get("root") or shelf, catalog.get("updated"), catalog.get("count")))
    lines.append("- " + (catalog.get("dump_note") or ""))
    lines.append("- live avatar index (on-body): `maps/<avatar>/MAP.md`")
    lines.append("")
    lines.append("## How to use")
    lines.append("")
    lines.append("```")
    lines.append("python maps/query.py library 毛衣")
    lines.append("python maps/query.py library --fusion")
    lines.append("python maps/library/scan.py")
    lines.append("```")
    lines.append("")
    lines.append("Find on the USB **before** Booth. `wear_fusion` means a fusion prefab exists in the listing heuristic, not that Edit already fit. Do not unpack unitypackages on the shelf unless the owner asked. Do not Ultra. Do not split the shelf by body.")
    lines.append("")

    def row(nid: str, node: dict, meta: dict) -> None:
        booth = node.get("booth_id") or ""
        src = ("booth.pm/items/" + booth) if booth else (meta.get("source") or "")
        lines.append("- **`{0}`** {1}".format(nid, node.get("label")))
        lines.append("  - path: `{0}`".format(node.get("rel") or node.get("path")))
        bodies = ",".join(node.get("bodies") or []) or "?"
        lines.append("  - bodies: `{0}`  wear_fusion: `{1}`  legacy_kaguya_key: `{2}`".format(
            bodies, node.get("wear_fusion"), kaguya_of(meta)))
        if meta.get("map_id"):
            lines.append("  - map: `{0}`".format(meta["map_id"]))
        if meta.get("note"):
            lines.append("  - " + meta["note"].replace("\n", " "))
        if src:
            lines.append("  - source: " + src)
        lines.append("")

    lines.append("## Legacy overlay key `kaguya` = installed (not a generic on-body API)")
    lines.append("")
    any_on = False
    for nid, meta in notes.items():
        if meta.get("kaguya") != "installed":
            continue
        any_on = True
        row(nid, by_id.get(nid, {"id": nid, "label": nid}), meta)
    if not any_on:
        lines.append("(none in notes)")
        lines.append("")

    lines.append("## Removed / do not reinstall")
    lines.append("")
    any_rm = False
    for nid, meta in notes.items():
        if meta.get("kaguya") != "removed":
            continue
        any_rm = True
        row(nid, by_id.get(nid, {"id": nid, "label": nid}), meta)
    if not any_rm:
        lines.append("(none)")
        lines.append("")

    lines.append("## Listed fusion clothes not on this body (candidates)")
    lines.append("")
    cands = []
    for node in catalog.get("nodes", []):
        if node.get("kind") != "clothes":
            continue
        if not node.get("wear_fusion"):
            continue
        meta = notes.get(node["id"], {})
        if kaguya_of(meta) != "never":
            continue
        cands.append((node, meta))
    if not cands:
        lines.append("(none — scan USB or empty catalog)")
        lines.append("")
    else:
        for node, meta in cands[:40]:
            row(node["id"], node, meta)
        if len(cands) > 40:
            lines.append("- … `{0}` more. `query.py library --fusion`".format(len(cands) - 40))
            lines.append("")

    lines.append("## Unmatched bases (do not Merge)")
    lines.append("")
    lines.append("Clothes for a different body stay off this avatar until the owner keeps a mesh in Edit. Query by collection if you need those packs later.")
    lines.append("")

    lines.append("## How to refresh")
    lines.append("")
    lines.append("1. USB path in `local.json` `unityvrchat_library` reachable.")
    lines.append("2. `python maps/library/scan.py` (rebuilds catalog, keeps notes).")
    lines.append("3. New lock: patch overlay notes.json key `kaguya` only for that historical profile + `map_id`.")
    lines.append("4. Optional sidecar on a pack folder: `item.json` (bodies, booth_id, note). Scan fills empty keys only.")
    lines.append("5. New zip: drop in `unityvrchat_stage`, read `INGEST.md`, owner confirms bucket, then scan.")
    lines.append("")

    out = HERE / "LIBRARY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", out)
    return out


def main() -> int:
    utf8_stdio()
    if not (HERE / "catalog.json").exists():
        print("no catalog.json — run scan.py first", file=sys.stderr)
        return 2
    render()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
