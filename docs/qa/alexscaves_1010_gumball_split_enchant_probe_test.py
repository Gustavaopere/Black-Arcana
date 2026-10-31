#!/usr/bin/env python3
"""Deterministic positive/negative tests for the bounded Gumball evidence seal."""
import unittest

from alexscaves_1010_gumball_split_enchant_probe import (
    CLASSES, GumballStateProbeError, key_anchor, projection
)

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
        symbols = [ins(a) for a in anchors]
        windows = []
        if filename == "ShotGumItem.class":
            symbols = [i for i in symbols if i["offset"] not in {144, 151, 161, 168, 178, 185, 188, 196, 205}]
            # Projection is tested against the merged refs+constants+branches
            # without requiring a live publisher artifact for synthetic cases.
            windows = [{"at": 198, "instructions": [ins(o, op) for o, op in CHAIN]}]
        classes.append({
            "class_path": path, "class_sha256": "a" * 64,
            "selected_method": {
                "name": name, "descriptor": descriptor,
                "parsed_method_sha256": "b" * 64,
                "instruction_count": 200,
                "symbols": symbols,
                "branches": [ins(a,"ifeq") for a in anchors if a in {144,161,178,205,156}],
                "constants": [ins(a,"iconst_2") for a in anchors if a in {151,168,185,188,196,155}],
                "selected_windows": windows,
            },
        })
    return {"schema_version":1,"scope":"SYNTHETIC","artifact":{},"classes":classes}


class GumballSplitEnchantmentTest(unittest.TestCase):
    def test_compact_anchor_has_exact_fields(self):
        self.assertEqual(key_anchor(ins(1)), ins(1))

    def test_snapshot_requires_all_selected_anchors(self):
        data=sample()
        # Avoid duplicates when an offset moves into a more precise class.
        for entry in data["classes"]:
            method=entry["selected_method"]
            already=set()
            for kind in ("symbols","branches","constants"):
                method[kind]=[i for i in method[kind] if i["offset"] not in already
                              and not already.add(i["offset"])]
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


if __name__ == "__main__":
    unittest.main()
