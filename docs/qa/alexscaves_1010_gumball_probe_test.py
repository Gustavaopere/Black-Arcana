#!/usr/bin/env python3
"""Synthetic regressions for SHA-exact Gumball snapshot sealing, without a JAR."""
import copy
import json
import unittest
from pathlib import Path

from alexscaves_1010_gumball_probe import (
    GumballEvidenceError, snapshot_view, strict_pairs
)

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GUMBALL-IMPACT-1.0.10.json"


def minimal_evidence(snapshot):
    selected = []
    for method in snapshot["selected_methods"]:
        entry = dict(method)
        entry["symbolic_references"] = list(snapshot["selected_anchors"].get(method["name"], []))
        entry["branches"] = []
        entry["constants"] = []
        selected.append(entry)
    return {
        "scope": snapshot["scope"],
        "artifact": snapshot["artifact"],
        "class_path": snapshot["class_path"],
        "class_sha256": snapshot["class_sha256"],
        "declared_methods": [{} for _ in range(snapshot["declared_method_count"])],
        "selected_methods": selected,
    }


class GumballSnapshotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads(SNAPSHOT.read_text(encoding="utf8"), object_pairs_hook=strict_pairs)

    def test_selected_anchor_projection_is_stable(self):
        self.assertEqual(snapshot_view(minimal_evidence(self.snapshot)), self.snapshot)
        self.assertEqual(len(self.snapshot["selected_methods"]), 17)
        self.assertEqual(self.snapshot["declared_method_count"], 28)

    def test_important_call_sites_are_pinned(self):
        anchors = self.snapshot["selected_anchors"]
        def at(name, offset):
            return next(a for a in anchors[name] if a["offset"] == offset)
        self.assertIn("causeGumballDamage", at("onHitEntity", 86)["symbol"])
        self.assertIn("Entity.hurt", at("onHitEntity", 139)["symbol"])
        self.assertIn("addFreshEntity", at("onHitEntity", 335)["symbol"])
        self.assertIn("Level.explode", at("tick", 242)["symbol"])
        self.assertIn("ownedBy", at("onHit", 77)["symbol"])
        self.assertIn("getEntitiesOfClass", at("bounceFromDirection", 101)["symbol"])
        self.assertIn("putInt", at("addAdditionalSaveData", 13)["symbol"])
        self.assertIn("ACCompat.getInt", at("readAdditionalSaveData", 10)["symbol"])

    def test_missing_targeting_anchor_fails_closed(self):
        sample = minimal_evidence(self.snapshot)
        target = next(m for m in sample["selected_methods"] if m["name"] == "bounceFromDirection")
        target["symbolic_references"] = [
            a for a in target["symbolic_references"] if a["offset"] != 101
        ]
        with self.assertRaisesRegex(GumballEvidenceError, "missing or ambiguous bytecode anchor"):
            snapshot_view(sample)

    def test_changed_method_digest_is_not_equal(self):
        sample = minimal_evidence(self.snapshot)
        sample["selected_methods"][0]["parsed_method_sha256"] = "0" * 64
        self.assertNotEqual(snapshot_view(sample), self.snapshot)

    def test_duplicated_method_identity_fails_closed(self):
        sample = minimal_evidence(self.snapshot)
        sample["selected_methods"].append(copy.deepcopy(sample["selected_methods"][0]))
        with self.assertRaisesRegex(GumballEvidenceError, "duplicated method identity"):
            snapshot_view(sample)

    def test_duplicate_json_key_fails_closed(self):
        with self.assertRaisesRegex(GumballEvidenceError, "duplicate snapshot field"):
            json.loads('{"same":1,"same":2}', object_pairs_hook=strict_pairs)


if __name__ == "__main__":
    unittest.main()
