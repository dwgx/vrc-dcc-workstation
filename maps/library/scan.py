# -*- coding: utf-8 -*-
"""Scan local.json unityvrchat_library into catalog.json. Never wipes notes.json. Does not move files."""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
from _stdio import utf8_stdio
from library.paths import usb_root

BOOTH_RE = re.compile(r"^(\d{6,8})")
SKIP_DIR = {
    "_工序", ".agent", "__pycache__", "unpack", "旧版本", "VRChat400+",
    "node_modules", ".git", "LocalBackup",
}
KIND_DIR = {
    "衣服": "clothes", "头发": "hair", "妆容": "makeup", "妆容与身体": "makeup",
    "妆造": "makeup", "插件": "plugin", "模型": "body", "面捕": "tracking",
    "饰品": "accessory", "配饰": "accessory", "道具": "prop", "音效": "sfx",
    "表情和动画": "motion", "预制件": "prefab", "Base": "body", "工具与插件": "plugin",
}
BUCKET_NAMES = set(KIND_DIR) | {
    "角色", "通用散件", "工具与插件", "模型库", "Other", "A更新", "补档",
    "模型本体", "unity散件",
}
ASSET_EXT = {".unitypackage", ".fbx", ".prefab", ".vrm", ".blend"}
PACK_EXT = {".unitypackage", ".zip", ".rar", ".7z"}


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def booth_prefix(name: str) -> str | None:
    m = BOOTH_RE.match(name)
    return m.group(1) if m else None


def kind_from_parts(parts: tuple[str, ...]) -> str:
    blob = "".join(parts)
    if "衣服" in blob:
        return "clothes"
    if "头发" in blob or "发型" in blob:
        return "hair"
    if "插件" in blob:
        return "plugin"
    if "妆容" in blob or "妆造" in blob:
        return "makeup"
    if "面捕" in blob:
        return "tracking"
    if "饰品" in blob or "配饰" in blob:
        return "accessory"
    if "音效" in blob:
        return "sfx"
    if "道具" in blob:
        return "prop"
    for p in reversed(parts):
        if p in KIND_DIR:
            return KIND_DIR[p]
    if parts and parts[0] == "工具与插件":
        return "plugin"
    return "other"


def prefer_copy(candidate: dict, current: dict) -> bool:
    """Rurune合集 wins over Airi dumps of the same Booth id."""
    def score(n: dict) -> tuple:
        col = n.get("collection") or ""
        rurune = 1 if ("Rurune" in col or "ルルネ" in col) else 0
        fusion = 1 if n.get("wear_fusion") else 0
        clothes = 1 if n.get("kind") == "clothes" else 0
        return (rurune, fusion, clothes)
    return score(candidate) > score(current)


def collection_of(rel: Path) -> str:
    parts = rel.parts
    if not parts:
        return ""
    if parts[0] == "角色" and len(parts) > 1:
        return parts[1]
    if parts[0] == "通用散件":
        return "通用散件"
    if parts[0] == "工具与插件":
        return "工具与插件"
    return parts[0]


def bodies_of(rel: Path, name: str) -> list[str]:
    blob = (str(rel) + " " + name).lower()
    out: list[str] = []

    def add(tag: str) -> None:
        if tag not in out:
            out.append(tag)

    col = collection_of(rel)
    if "Rurune" in col or "ルルネ" in col:
        add("rurune")
    if "Kaguya" in col or "辉夜" in col:
        add("kaguya_shop")
    if "Airi" in col or "爱莉" in col:
        add("airi")
    if "Shinano" in col or "しなの" in col or "信浓" in col:
        add("shinano")
    if "Plum" in col or "Lime" in col or "Chiffon" in col:
        add("plum_family")
    if "rurune" in blob or "ルルネ" in name:
        add("rurune")
    if "mizuki" in blob or "瑞希" in name:
        add("mizuki")
    if "kaguya" in blob and "fusion" not in blob:
        add("kaguya_shop")
    if "airi" in blob or "爱莉" in name:
        add("airi")
    if "shinano" in blob:
        add("shinano")
    if "しずく" in name or "shizuku" in blob:
        add("shizuku_other")
    return out


def wear_fusion(bodies: list[str]) -> bool:
    if "rurune" in bodies:
        return True
    return False


def node_id(booth: str | None, name: str) -> str:
    if booth:
        return "booth." + booth
    return "pack." + name


def label_of(name: str, booth: str | None) -> str:
    s = name
    if booth and s.startswith(booth):
        s = s[len(booth):].lstrip(" _-")
    return s or name


def is_pack_dir(name: str, filenames: list[str], parent_name: str) -> bool:
    if name in SKIP_DIR or name in BUCKET_NAMES:
        return False
    if booth_prefix(name):
        return True
    if parent_name in KIND_DIR:
        for f in filenames:
            if Path(f).suffix.lower() in ASSET_EXT or f == "item.json":
                return True
        return True
    return False


def sidecar(dirpath: Path) -> dict:
    p = dirpath / "item.json"
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def merge_notes(notes: dict, seed: dict, sidecars: dict[str, dict]) -> dict:
    """Fill missing keys only. Never delete. Never overwrite a non-empty note."""
    for nid, meta in seed.items():
        cur = notes.setdefault(nid, {})
        for k, v in meta.items():
            if k == "note":
                if not (cur.get("note") or "").strip():
                    cur["note"] = v
            elif k not in cur or cur[k] in (None, "", "never") and v:
                if k == "kaguya" and cur.get("kaguya") in {"installed", "removed"}:
                    continue
                if k not in cur:
                    cur[k] = v
                elif cur[k] in (None, ""):
                    cur[k] = v
    for nid, extra in sidecars.items():
        cur = notes.setdefault(nid, {})
        for k, v in extra.items():
            if k == "note" and (cur.get("note") or "").strip():
                continue
            if k not in cur or not cur[k]:
                cur[k] = v
    return notes


def scan(root: Path) -> tuple[list[dict], dict[str, dict]]:
    nodes: list[dict] = []
    by_booth: dict[str, dict] = {}
    seen_pack: set[str] = set()
    sidecars: dict[str, dict] = {}
    roots = [root / "角色", root / "通用散件", root / "工具与插件"]

    def emit(path: Path, booth: str | None, kind: str, rel: Path) -> None:
        nid = node_id(booth, path.name)
        bodies = bodies_of(rel, path.name)
        extra = sidecar(path) if path.is_dir() else {}
        if extra.get("bodies"):
            bodies = list(extra["bodies"])
        node = {
            "id": nid,
            "kind": extra.get("kind") or kind,
            "label": extra.get("label") or label_of(path.name, booth),
            "booth_id": booth or extra.get("booth_id") or "",
            "path": str(path),
            "rel": rel.as_posix(),
            "collection": collection_of(rel),
            "bodies": bodies,
            "wear_fusion": bool(extra.get("wear_fusion")) if "wear_fusion" in extra else wear_fusion(bodies),
            "copies": [],
        }
        if extra:
            sidecars[nid] = extra
        if booth:
            prev = by_booth.get(booth)
            if prev is None:
                by_booth[booth] = node
                return
            copy = {"rel": rel.as_posix(), "collection": node["collection"], "bodies": bodies, "path": str(path)}
            if prefer_copy(node, prev):
                copy = {"rel": prev["rel"], "collection": prev["collection"], "bodies": prev["bodies"], "path": prev["path"]}
                node["copies"] = list(prev.get("copies") or []) + [copy]
                node["id"] = prev["id"]
                by_booth[booth] = node
            else:
                prev.setdefault("copies", []).append(copy)
                if node["wear_fusion"]:
                    prev["wear_fusion"] = True
                for b in bodies:
                    if b not in prev["bodies"]:
                        prev["bodies"].append(b)
            return
        if nid in seen_pack:
            return
        seen_pack.add(nid)
        nodes.append(node)

    for base in roots:
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            p = Path(dirpath)
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIR and not d.startswith(".")]
            try:
                rel = p.relative_to(root)
            except ValueError:
                continue
            parent = p.parent.name
            if is_pack_dir(p.name, filenames, parent) and p != base:
                emit(p, booth_prefix(p.name), kind_from_parts(rel.parts), rel)
                dirnames[:] = []
                continue
            if p.name in KIND_DIR or p == base or p.name in BUCKET_NAMES:
                for f in filenames:
                    fp = p / f
                    if fp.suffix.lower() not in PACK_EXT:
                        continue
                    b = booth_prefix(f)
                    if not b:
                        continue
                    emit(fp, b, kind_from_parts(rel.parts), rel / f)
    nodes.extend(by_booth.values())
    nodes.sort(key=lambda n: (n.get("collection") or "", n.get("kind") or "", n.get("id") or ""))
    return nodes, sidecars


def write_catalog(root: Path, nodes: list[dict]) -> Path:
    catalog = {
        "avatar": "library",
        "root": str(root),
        "updated": date.today().isoformat(),
        "dump": "scan",
        "dump_note": "Folder names + Booth ids. Does not unpack unitypackages. Skips 模型库/VRChat400+.",
        "count": len(nodes),
        "nodes": nodes,
    }
    out = HERE / "catalog.json"
    out.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def main() -> int:
    utf8_stdio()
    root = usb_root()
    if not root.exists():
        print("USB library missing:", root or "(unset)", file=sys.stderr)
        print("Set local.json unityvrchat_library (or UNITYVRCHAT_LIBRARY)", file=sys.stderr)
        return 2
    nodes, sidecars = scan(root)
    write_catalog(root, nodes)
    notes_path = HERE / "notes.json"
    notes = load_json(notes_path, {})
    seed = load_json(HERE / "seed.json", {})
    notes = merge_notes(notes, seed, sidecars)
    keep = set(seed) | set(sidecars)
    for nid in list(notes):
        meta = notes[nid]
        if nid in keep:
            continue
        if (meta.get("note") or "").strip():
            continue
        if meta.get("kaguya") in {"installed", "removed"}:
            continue
        if meta.get("status") == "confirmed":
            continue
        del notes[nid]
    notes_path.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("catalog nodes:", len(nodes), " notes:", len(notes), " root:", root)
    from library.render import render
    render()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
