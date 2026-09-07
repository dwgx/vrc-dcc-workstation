# -*- coding: utf-8 -*-
"""World shelf entries keep their namespace when Booth ids overlap avatars."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
sys.path.insert(0, str(MAPS))

from library.scan import migrate_legacy_world_notes, scan  # noqa: E402


BOOTH = "1234567"


def make_pack(root: Path, rel: str) -> None:
    pack = root / rel
    pack.mkdir(parents=True)
    (pack / "package.unitypackage").write_bytes(b"fixture")


class WorldShelfTests(unittest.TestCase):
    def test_cross_domain_booth_ids_and_same_domain_copies(self) -> None:
        with TemporaryDirectory(prefix="vrc-dcc-world-shelf-") as temp:
            shelf = Path(temp)
            avatar_a = f"角色/Airi/{BOOTH}_legacy-avatar"
            avatar_rurune = f"角色/Rurune/{BOOTH}_rurune-avatar"
            world_map = f"世界/地图/{BOOTH}_world-map"
            world_kit = f"世界/建筑家具/{BOOTH}_world-kit"
            for rel in (avatar_a, avatar_rurune, world_map, world_kit):
                make_pack(shelf, rel)

            nodes, sidecars = scan(shelf)

        self.assertEqual(sidecars, {})
        matching = [node for node in nodes if node["booth_id"] == BOOTH]
        self.assertEqual(len(matching), 2, matching)
        by_id = {node["id"]: node for node in matching}

        # Existing avatar consumers keep their historical id and same-domain
        # copies still collapse to one preferred node.
        avatar = by_id["booth." + BOOTH]
        self.assertEqual(avatar["collection"], "Rurune")
        self.assertEqual(avatar["rel"], avatar_rurune)
        self.assertEqual(
            {avatar["rel"], *(copy["rel"] for copy in avatar["copies"])},
            {avatar_a, avatar_rurune},
        )

        # World entries use a separate stable id, while their own duplicate
        # directories still follow the same copies contract.
        world = by_id["world.booth." + BOOTH]
        self.assertEqual(
            {world["rel"], *(copy["rel"] for copy in world["copies"])},
            {world_map, world_kit},
        )
        self.assertEqual(world["booth_id"], avatar["booth_id"])

    def test_world_pack_namespace_keeps_same_name_as_avatar_pack(self) -> None:
        with TemporaryDirectory(prefix="vrc-dcc-world-pack-") as temp:
            shelf = Path(temp)
            avatar_rel = "角色/衣服/shared-pack"
            world_rel = "世界/地图/shared-pack"
            make_pack(shelf, avatar_rel)
            make_pack(shelf, world_rel)

            nodes, _ = scan(shelf)

        by_rel = {node["rel"]: node for node in nodes}
        self.assertEqual(by_rel[avatar_rel]["id"], "pack.shared-pack")
        self.assertEqual(by_rel[world_rel]["id"], "world.pack.shared-pack")
        self.assertEqual(len({by_rel[avatar_rel]["id"], by_rel[world_rel]["id"]}), 2)

    def test_legacy_world_note_moves_only_when_catalog_is_unambiguous(self) -> None:
        old_id = "booth." + BOOTH
        new_id = "world.booth." + BOOTH
        old_catalog = {
            "nodes": [{
                "id": old_id,
                "booth_id": BOOTH,
                "kind": "world-map",
                "collection": "世界/地图",
                "rel": "世界/地图/1234567_world-map",
            }]
        }
        notes = {old_id: {"note": "keep this World note", "status": "observed"}}
        migrated = migrate_legacy_world_notes(
            notes,
            old_catalog,
            [{"id": new_id, "booth_id": BOOTH, "collection": "世界/地图"}],
        )
        self.assertNotIn(old_id, migrated)
        self.assertEqual(migrated[new_id]["note"], "keep this World note")

        pack_old_id = "pack.old-world-kit"
        pack_new_id = "world.pack.old-world-kit"
        pack_notes = {pack_old_id: {"note": "keep old pack note"}}
        pack_catalog = {
            "nodes": [{
                "id": pack_old_id,
                "kind": "world-kit",
                "collection": "世界/建筑家具",
                "rel": "世界/建筑家具/old-world-kit",
            }]
        }
        migrate_legacy_world_notes(
            pack_notes,
            pack_catalog,
            [{"id": pack_new_id, "collection": "世界/建筑家具"}],
        )
        self.assertEqual(pack_notes, {pack_new_id: {"note": "keep old pack note"}})

        existing_new = {
            old_id: {"note": "old value"},
            new_id: {"note": "new value", "status": "confirmed"},
        }
        migrate_legacy_world_notes(
            existing_new,
            old_catalog,
            [{"id": new_id, "booth_id": BOOTH, "collection": "世界/地图"}],
        )
        self.assertEqual(existing_new[new_id], {"note": "new value", "status": "confirmed"})

        ambiguous_notes = {old_id: {"note": "do not guess"}}
        ambiguous_catalog = {
            "nodes": [{
                **old_catalog["nodes"][0],
                "copies": [{
                    "rel": "角色/Rurune/1234567_avatar",
                    "collection": "Rurune",
                }],
            }, {
                "id": old_id,
                "booth_id": BOOTH,
                "kind": "clothes",
                "collection": "Rurune",
                "rel": "角色/Rurune/1234567_avatar",
            }]
        }
        migrate_legacy_world_notes(
            ambiguous_notes,
            ambiguous_catalog,
            [{"id": new_id, "booth_id": BOOTH, "collection": "世界/地图"}],
        )
        self.assertEqual(ambiguous_notes, {old_id: {"note": "do not guess"}})


if __name__ == "__main__":
    unittest.main()
