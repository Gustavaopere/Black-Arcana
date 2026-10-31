#!/usr/bin/env python3
"""Deterministic positive/negative tests for the bounded Gumball evidence seal."""
import unittest
import json
from pathlib import Path

from alexscaves_1010_gumball_split_enchant_probe import (
    CLASSES, GumballStateProbeError, key_anchor, projection
)
from alexscaves_1010_gumball_state_probe import strict_pairs

CHAIN = [
    (188, "iconst_4"), (190, "getstatic"), (193, "invokestatic"),
    (196, "iconst_2"), (197, "imul"), (198, "iadd"), (199, "istore"),
]


def ins(offset, opcode="getstatic", symbol=""):
    return {"offset": offset, "opcode": opcode, "operand": "", "symbol": symbol}


def sample():
    classes = []
    for path, name, descriptor, anchors in CLASSES:
        filename = path.rsplit("/", 1)[-1]
        branch_offsets = {144, 161, 178, 205, 156}
        const_offsets = {151, 168, 185, 188, 196, 155}
        symbols = [ins(a) for a in anchors if a not in branch_offsets | const_offsets]
        windows = ([{"at": 198, "instructions": [ins(o, op) for o, op in CHAIN]}]
                   if filename == "ShotGumItem.class" else [])
        classes.append({
            "class_path": path, "class_sha256": "a" * 64,
            "selected_method": {
                "name": name, "descriptor": descriptor,
                "parsed_method_sha256": "b" * 64,
                "instruction_count": 200,
                "symbols": symbols,
                "branches": [ins(a,"ifeq") for a in anchors if a in branch_offsets],
                "constants": [ins(a,"iconst_2") for a in anchors if a in const_offsets],
                "selected_windows": windows,
            },
        })
    return {"schema_version":1,"scope":"SYNTHETIC","artifact":{},"classes":classes}


class GumballSplitEnchantmentTest(unittest.TestCase):
    def test_compact_anchor_has_exact_fields(self):
        self.assertEqual(key_anchor(ins(1)), ins(1))

    def test_snapshot_requires_all_selected_anchors(self):
        data=sample()
        result=projection(data)
        self.assertEqual(len(result["classes"]), 3)
        shot=result["classes"][1]
        self.assertEqual([x["opcode"] for x in shot["arithmetic_chain"]],
                         [o for _,o in CHAIN])

    def test_arithmetic_drift_fails_closed(self):
        data=sample()
        data["classes"][1]["selected_method"]["selected_windows"][0]["instructions"][4]["opcode"]="iadd"
        with self.assertRaisesRegex(GumballStateProbeError,"bounce formula changed"):
            projection(data)

    def test_missing_critical_offset_fails_closed(self):
        data=sample()
        data["classes"][0]["selected_method"]["symbols"]=[]
        data["classes"][0]["selected_method"]["branches"]=[]
        data["classes"][0]["selected_method"]["constants"]=[]
        with self.assertRaisesRegex(GumballStateProbeError,"missing sealed offset"):
            projection(data)



class SealedPublisherSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = (Path(__file__).resolve().parents[2] /
                "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json")
        cls.snapshot = json.loads(path.read_text(encoding="utf8"),
                                  object_pairs_hook=strict_pairs)

    def test_three_exact_classes_with_pinned_owners(self):
        entries = self.snapshot["classes"]
        self.assertEqual(len(entries), 3)
        self.assertEqual([i["class_path"].split("/")[-1] for i in entries],
                         ["GumballEntity.class", "ShotGumItem.class", "ACCompat.class"])
        self.assertEqual(entries[2]["class_sha256"],
                         "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b")
        self.assertEqual(entries[2]["instruction_count"], 4)
        self.assertEqual(entries[2]["essential_anchors"][0]["symbol"],
                         "Method net/minecraft/world/entity/EntityType.create:(Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/entity/Entity;")

    def test_enchantment_arithmetic_and_split_reference_ledger(self):
        entries = self.snapshot["classes"]
        self.assertEqual(len(entries[0]["essential_anchors"]), 13)
        self.assertEqual(len(entries[1]["essential_anchors"]), 25)
        self.assertEqual(len(entries[2]["essential_anchors"]), 1)
        self.assertEqual([x["opcode"] for x in entries[1]["arithmetic_chain"]],
                         [op for _, op in CHAIN])
        self.assertEqual([x["offset"] for x in entries[1]["arithmetic_chain"]],
                         [at for at, _ in CHAIN])
        self.assertEqual(entries[0]["name"], "onHitEntity")
        self.assertTrue(any("ACCompat.createEntity" in x["symbol"]
                            for x in entries[0]["essential_anchors"]))
        self.assertFalse(any("setOwner:" in x["symbol"]
                             for x in entries[0]["essential_anchors"]))

    def test_duplicate_snapshot_keys_fail_closed(self):
        with self.assertRaisesRegex(GumballStateProbeError,"duplicate snapshot key"):
            json.loads('{"schema_version":1,"schema_version":2}',
                       object_pairs_hook=strict_pairs)

if __name__ == "__main__":
    unittest.main()
