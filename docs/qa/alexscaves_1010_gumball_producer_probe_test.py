#!/usr/bin/env python3
"""Synthetic bounds for the SHA-exact Gumball producer reference probe."""
import unittest
import json
from pathlib import Path
from alexscaves_1010_gumball_producer_probe import (
    MAX_HITS_PER_METHOD, ProducerProbeError, method_row, REF_PATTERN, snapshot_view, strict_pairs
)


def fake_method(symbols):
    return {
        "header": "public void fire()",
        "descriptor": "()V",
        "instructions": [
            {"offset": 3 * i, "opcode": "invokestatic", "operand": "#1", "symbol": symbol}
            for i, symbol in enumerate(symbols)
        ],
    }


class ProducerProbeTest(unittest.TestCase):
    def test_exact_gumball_reference_names(self):
        self.assertTrue(REF_PATTERN.search(
            "Method com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.<init>:()V"))
        self.assertTrue(REF_PATTERN.search(
            "Field com/github/alexmodguy/alexscaves/server/entity/ACEntityRegistry.GUMBALL:Ljava/util/function/Supplier;"))
        self.assertFalse(REF_PATTERN.search("Method java/lang/Math.random:()D"))

    def test_misses_unrelated_method(self):
        self.assertIsNone(method_row(fake_method(["Method java/lang/Math.random:()D"])))

    def test_selected_window_remains_bounded(self):
        m = fake_method([
            "Method java/lang/Math.random:()D",
            "Method com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.setDamage:(F)V",
            "Method java/lang/Math.random:()D",
        ])
        row = method_row(m)
        self.assertEqual(row["name"], "fire")
        self.assertEqual(len(row["reference_windows"]), 1)
        self.assertEqual(row["reference_windows"][0]["at"], 3)
        self.assertEqual(row["effective_parameter_flow"], "NOT_PROVEN")

    def test_excessive_callsites_fail_closed(self):
        m = fake_method(["Method GumballEntity.setDamage:(F)V"] * (MAX_HITS_PER_METHOD + 1))
        with self.assertRaisesRegex(ProducerProbeError, "selected callsite count exceeded"):
            method_row(m)

    def test_excessive_method_body_fails_closed(self):
        m = fake_method(["Method java/lang/Math.random:()D"] * 3200 +
                        ["Method GumballEntity.<init>:()V"])
        with self.assertRaisesRegex(ProducerProbeError, "unsafe selected method instruction population"):
            method_row(m)


    def test_exact_producer_snapshot_and_missing_anchor(self):
        root = Path(__file__).resolve().parents[2]
        path = root / "wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GUMBALL-PRODUCERS-1.0.10.json"
        recorded = json.loads(path.read_text(encoding="utf8"), object_pairs_hook=strict_pairs)
        sample = {
            k: recorded[k] for k in (
                "schema_version", "scope", "artifact", "projectile_class",
                "candidate_class_count", "selected_class_count", "selected_method_count",
                "registry_support", "no_selected_symbols"
            )
        }
        sample["selected_classes"] = []
        for cls in recorded["selected_classes"]:
            selected = []
            for m in cls["methods"]:
                row = {k: m[k] for k in ("name", "descriptor", "instruction_count", "parsed_method_sha256")}
                row["reference_windows"] = [{"at": a["offset"], "reference": a} for a in m["anchors"]]
                selected.append(row)
            sample["selected_classes"].append({
                "class_path": cls["class_path"],
                "class_sha256": cls["class_sha256"],
                "methods": selected,
            })
        self.assertEqual(snapshot_view(sample), recorded)
        shotgum = next(x for x in sample["selected_classes"] if x["class_path"].endswith("ShotGumItem.class"))
        shotgum["methods"][0]["reference_windows"] = [
            x for x in shotgum["methods"][0]["reference_windows"] if x["at"] != 495
        ]
        with self.assertRaisesRegex(ProducerProbeError, "missing/duplicate producer anchor"):
            snapshot_view(sample)

    def test_duplicate_json_key_fails_closed(self):
        with self.assertRaisesRegex(ProducerProbeError, "duplicate snapshot key"):
            json.loads('{"x":1,"x":2}', object_pairs_hook=strict_pairs)


if __name__ == "__main__":
    unittest.main()
