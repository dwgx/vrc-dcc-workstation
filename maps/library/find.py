# -*- coding: utf-8 -*-
"""Search maps/library/catalog.json + notes.json. No network."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
from _stdio import utf8_stdio


def blob(node: dict, note: dict | None) -> str:
    parts = [
        node.get("id", ""), node.get("kind", ""), node.get("label", ""),
        node.get("path", "") or "", node.get("rel", "") or "",
        node.get("collection", ""), node.get("booth_id", ""),
        " ".join(node.get("bodies") or []),
        "fusion" if node.get("wear_fusion") else "",
    ]
    if note:
        parts += [note.get("status", ""), note.get("kaguya", ""), note.get("note", ""),
                  note.get("source", ""), note.get("map_id", "")]
    return " ".join(str(p) for p in parts).lower()


def legacy_kaguya_display(note: dict | None) -> str:
    """Overlay notes.json key 'kaguya' is one historical profile. Missing is unset, not never."""
    if not note or "kaguya" not in note:
        return "unset"
    val = note.get("kaguya")
    if val in (None, ""):
        return "unset"
    return str(val)


def run(terms: list[str], *, confirmed: bool = False, observed: bool = False,
        node_id: str | None = None, as_json: bool = False,
        fusion: bool = False, legacy_kaguya: str | None = None,
        kind: str | None = None) -> int:
    cat_path = HERE / "catalog.json"
    if not cat_path.exists():
        print("no catalog.json — run maps/library/scan.py", file=sys.stderr)
        return 2
    catalog = json.loads(cat_path.read_text(encoding="utf-8"))
    notes = json.loads((HERE / "notes.json").read_text(encoding="utf-8")) if (HERE / "notes.json").exists() else {}
    hits = []
    for node in catalog.get("nodes", []):
        nid = node["id"]
        note = notes.get(nid)
        if node_id and nid != node_id and node.get("booth_id") != node_id.removeprefix("booth."):
            continue
        st = (note or {}).get("status", "")
        if confirmed and st != "confirmed":
            continue
        if observed and st != "observed":
            continue
        if fusion and not node.get("wear_fusion"):
            continue
        if legacy_kaguya:
            if not note or "kaguya" not in note:
                continue
            if note.get("kaguya") != legacy_kaguya:
                continue
        if kind and node.get("kind") != kind:
            continue
        if terms:
            b = blob(node, note)
            if not all(t.lower() in b for t in terms):
                continue
        hits.append((node, note))
    terms_l = [t.lower() for t in terms]

    def rank(pair: tuple[dict, dict | None]) -> tuple:
        node, note = pair
        bid = node["id"].lower()
        lab = (node.get("label") or "").lower()
        kg = (note or {}).get("kaguya") if note and "kaguya" in (note or {}) else None
        rec = 0 if (node.get("wear_fusion") and kg == "never") else 1
        if terms_l and all(t in bid or t in str(node.get("booth_id", "")) for t in terms_l):
            return (0, rec, bid)
        if terms_l and all(t in lab for t in terms_l):
            return (1, rec, bid)
        return (2, rec, bid)

    hits.sort(key=rank)
    if not hits:
        if as_json:
            print("[]")
        else:
            print("0 hits. Next: Read LIBRARY.md, then one Booth search (maps/AGENT.md).")
        return 1
    if as_json:
        out = []
        for node, note in hits:
            row = dict(node)
            row["legacy_kaguya_key"] = legacy_kaguya_display(note)
            if note:
                row["note"] = dict(note)
            out.append(row)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    for node, note in hits:
        print("id:", node["id"])
        print("  kind:", node.get("kind"), " label:", node.get("label"))
        print("  collection:", node.get("collection"))
        if node.get("booth_id"):
            print("  booth:", node["booth_id"], " https://booth.pm/ja/items/" + node["booth_id"])
        print("  path:", node.get("path"))
        print("  bodies:", ",".join(node.get("bodies") or []) or "?",
              " wear_fusion:", node.get("wear_fusion"))
        copies = node.get("copies") or []
        if copies:
            print("  copies:", len(copies), "(same Booth id in other 合集 — use the path above for this body)")
        print("  legacy_kaguya_key:", legacy_kaguya_display(note), " status:", (note or {}).get("status") or "(none)")
        if note and note.get("map_id"):
            print("  map_id:", note["map_id"])
        if note and note.get("note"):
            print("  note:", note["note"])
        print()
    print("hits:", len(hits), "  map:", HERE / "LIBRARY.md")
    return 0


def main() -> int:
    utf8_stdio()
    if any(a == "--on-body" or a.startswith("--on-body=") for a in sys.argv[1:]):
        print(
            "--on-body is not a generic on-this-avatar API. "
            "Use python maps/query.py <avatar> for the named body. "
            "Overlay-only filter: --kaguya reads notes.json key 'kaguya' for one historical profile.",
            file=sys.stderr,
        )
        return 2
    p = argparse.ArgumentParser(description="Query the USB shelf catalog")
    p.add_argument("terms", nargs="*", help="AND match on id/label/path/note")
    p.add_argument("--confirmed", action="store_true")
    p.add_argument("--observed", action="store_true")
    p.add_argument("--id", dest="node_id")
    p.add_argument("--json", action="store_true")
    p.add_argument("--fusion", action="store_true", help="wear_fusion (listed for a fusion body)")
    p.add_argument(
        "--kaguya",
        dest="legacy_kaguya",
        choices=["installed", "removed", "never"],
        help="Overlay-only. Filter notes.json key 'kaguya' (one historical profile). "
             "Missing key does not match. Not a generic on-body API.",
    )
    p.add_argument("--kind", help="clothes|hair|plugin|...")
    args = p.parse_args()
    return run(
        args.terms,
        confirmed=args.confirmed,
        observed=args.observed,
        node_id=args.node_id,
        as_json=args.json,
        fusion=args.fusion,
        legacy_kaguya=args.legacy_kaguya,
        kind=args.kind,
    )


if __name__ == "__main__":
    raise SystemExit(main())
