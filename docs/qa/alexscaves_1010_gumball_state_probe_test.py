#!/usr/bin/env python3
"""Fail-closed bounded Gumball state-probe synthetic regressions."""
import unittest
import json
from pathlib import Path
from alexscaves_1010_gumball_state_probe import (
    GumballStateProbeError, classify, name_of, summarize, snapshot_view, strict_pairs
)


def fake(name, instructions):
    return {
        "header": "public void " + name + "()",
        "descriptor": "()V",
        "instructions": instructions,
    }


def inst(offset, opcode, symbol="", operand=""):
    return {"offset": offset, "opcode": opcode, "symbol": symbol,
            "operand": operand}


class GumballStateProbeTests(unittest.TestCase):
    def test_method_name_preserves_overloads(self):
        m = fake("onHitEntity", [inst(0, "return")])
        self.assertEqual(name_of(m), "onHitEntity")
        self.assertEqual(m["descriptor"], "()V")

    def test_correct_anchor_types_and_windows(self):
        m = fake("shootGumball", [
            inst(0, "aload_0"),
            inst(1, "getfield", "Field value:F", "#1"),
            inst(4, "iconst_2"),
            inst(5, "ifeq", "", "12"),
            inst(8, "invokevirtual", "Method setDamage:(F)V", "#3"),
            inst(11, "return"),
        ])
        r = summarize(m, [4, 8])
        self.assertEqual([v["offset"] for v in r["numeric_constants"]], [4])
        self.assertEqual([v["offset"] for v in r["branches"]], [5])
        self.assertEqual([v["offset"] for v in r["symbolic_references"]], [1, 8])
        self.assertEqual([v["at"] for v in r["selected_windows"]], [4, 8])
        self.assertEqual(r["runtime_reachability"], "NOT_PROVEN")

    def test_missing_exact_offset_is_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError, "missing fixed"):
            summarize(fake("tick", [inst(0, "return")]), [42])

    def test_duplicate_instruction_offsets_are_rejected(self):
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate bytecode"):
            summarize(fake("tick", [inst(1, "aload_0"), inst(1, "return")]), [])

    def test_maximum_window_budget_is_enforced(self):
        with self.assertRaisesRegex(GumballStateProbeError, "too many evidence windows"):
            summarize(fake("tick", [inst(0, "return")]), [0]*31)

    def test_classification_does_not_report_all_bytecode(self):
        self.assertIsNone(classify(inst(0, "aload_0")))
        self.assertEqual(classify(inst(0, "invokestatic")), "symbols")
        self.assertEqual(classify(inst(0, "ifne")), "branches")



class GumballSealedSnapshotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2]
        path = root / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GUMBALL-STATE-1.0.10.json"
        cls.snapshot = json.loads(path.read_text(encoding="utf8"),
                                  object_pairs_hook=strict_pairs)

    def build_sample(self):
        sample = {
            "schema_version": 1,
            "scope": self.snapshot["scope"],
            "artifact": self.snapshot["artifact"],
            "selected_method_count": self.snapshot["selected_method_count"],
            "selected_classes": [],
        }
        for cls in self.snapshot["classes"]:
            methods = []
            for m in cls["methods"]:
                matches = [a for a in cls["critical_anchors"]
                           if a["name"] == m["name"] and a["descriptor"] == m["descriptor"]]
                if len(matches) > 1:
                    raise AssertionError("duplicate critical method")
                methods.append({
                    **m,
                    "symbolic_references": matches[0]["anchors"] if matches else [],
                    "numeric_constants": [],
                    "branches": [],
                })
            sample["selected_classes"].append({
                "class_path": cls["class_path"],
                "class_sha256": cls["class_sha256"],
                "declared_methods": [{} for _ in range(cls["declared_method_count"])],
                "selected_methods": methods,
            })
        return sample

    def test_snapshot_projection_and_scope(self):
        self.assertEqual(snapshot_view(self.build_sample()), self.snapshot)
        self.assertEqual(self.snapshot["selected_method_count"], 52)
        self.assertEqual(sum(len(c["methods"]) for c in self.snapshot["classes"]), 52)
        self.assertEqual(sum(len(a["anchors"]) for c in self.snapshot["classes"]
                             for a in c["critical_anchors"]), 105)

    def test_missing_critical_targeting_anchor_fails_closed(self):
        sample = self.build_sample()
        shot = next(c for c in sample["selected_classes"] if c["class_path"].endswith("/ShotGumItem.class"))
        inv = next(m for m in shot["selected_methods"] if m["name"] == "acInventoryTick")
        inv["symbolic_references"] = [a for a in inv["symbolic_references"] if a["offset"] != 434]
        with self.assertRaisesRegex(GumballStateProbeError, "missing/duplicate sealed anchor"):
            snapshot_view(sample)

    def test_altered_method_digest_does_not_match(self):
        sample = self.build_sample()
        sample["selected_classes"][0]["selected_methods"][0]["parsed_method_sha256"] = "0" * 64
        self.assertNotEqual(snapshot_view(sample), self.snapshot)

    def test_duplicate_snapshot_json_key_fails_closed(self):
        with self.assertRaisesRegex(GumballStateProbeError, "duplicate snapshot key"):
            json.loads('{"x":1,"x":2}', object_pairs_hook=strict_pairs)


if __name__ == "__main__":
    unittest.main()
