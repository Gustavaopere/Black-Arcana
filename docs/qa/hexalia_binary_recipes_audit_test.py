#!/usr/bin/env python3
"""Synthetic ZIP fixture regressions only; not evidence of Hexalia gameplay."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "hexalia_recipe_audit", HERE / "hexalia_binary_recipes_audit.py"
)
assert spec and spec.loader
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def fixtures():
    recipes = {}
    for name in audit.NATURE:
        content = {
            "type": audit.TYPE_NATURE,
            "center": {"item": "minecraft:amethyst_shard"},
            "offerings": [{"item": "minecraft:coal"}],
        }
        if name in audit.SOUL:
            content["requires_soul"] = True
            content["result"] = {
                "type": "entity", "entity": audit.SOUL[name], "count": 1,
            }
        else:
            content["output"] = "hexalia:placeholder"
        recipes[f"data/hexalia/recipe/{name}.json"] = json.dumps(content).encode()
    for name in audit.CELESTIAL:
        recipes[f"data/hexalia/recipe/{name}.json"] = json.dumps({
            "type": audit.TYPE_CELESTIAL,
            "input": {"item": "minecraft:amethyst_shard"},
            "output": "hexalia:placeholder",
        }).encode()
    return recipes


class HexaliaExactRecipeCollectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.jar = Path(self.temp.name) / audit.EXPECTED_JAR
        self.recipes = fixtures()
        self.write_zip()

    def write_zip(self, mod_id="hexalia"):
        with zipfile.ZipFile(self.jar, "w") as jar:
            jar.writestr(
                "META-INF/neoforge.mods.toml",
                f'[[mods]]\nmodId="{mod_id}"\nversion="1.3.7"\n',
            )
            for filename, payload in self.recipes.items():
                jar.writestr(filename, payload)

    def report(self):
        return audit.examine_json_docs(self.recipes)

    def test_synthetic_23_plus_6_with_two_soul_summons(self):
        result = self.report()
        self.assertEqual("PASS", result["status"])
        self.assertEqual(23, result["natures_ritual_observed"])
        self.assertEqual(6, result["celestial_infusion_observed"])
        self.assertEqual(29, result["unique_magic_recipe_ids"])
        self.assertEqual(sorted(audit.SOUL), result["summon_recipe_ids"])

    def test_synthetic_zip_is_not_physical_sha(self):
        with self.assertRaisesRegex(audit.EvidenceError, "physical SHA-1 mismatch"):
            audit.audit_jar(self.jar)

    def test_override_digest_fixture_is_not_runtime_proof(self):
        checksum = hashlib.sha1(self.jar.read_bytes()).hexdigest()
        result = audit.audit_jar(self.jar, expected_sha1=checksum)
        self.assertEqual("PASS", result["result"])
        self.assertIn("recipes loaded by NeoForge or retained after datapack reload", result["not_proven"])

    def test_missing_ritual_fails(self):
        del self.recipes["data/hexalia/recipe/heartseed_from_ritual_table.json"]
        result = self.report()
        self.assertEqual("UNPROVEN_OR_MISMATCH", result["status"])
        self.assertEqual(["heartseed_from_ritual_table"], result["deviations"]["missing_natures_ritual"])

    def test_unexpected_celestial_recipe_fails(self):
        self.recipes["data/hexalia/recipe/new_unknown.json"] = json.dumps({
            "type": audit.TYPE_CELESTIAL, "input": {"item": "minecraft:stone"},
            "output": "hexalia:unverified",
        }).encode()
        self.assertEqual("UNPROVEN_OR_MISMATCH", self.report()["status"])

    def test_wrong_soul_entity_or_flag_fails(self):
        path = "data/hexalia/recipe/summon_cacofey.json"
        obj = json.loads(self.recipes[path])
        obj["result"]["entity"] = "minecraft:zombie"
        self.recipes[path] = json.dumps(obj).encode()
        self.assertEqual("UNPROVEN_OR_MISMATCH", self.report()["status"])
        obj["result"]["entity"] = "hexalia:cacofey"
        obj["requires_soul"] = False
        self.recipes[path] = json.dumps(obj).encode()
        self.assertEqual("UNPROVEN_OR_MISMATCH", self.report()["status"])

    def test_missing_soul_summon_ritual_output_fails(self):
        path = "data/hexalia/recipe/summon_silk_moth.json"
        obj = json.loads(self.recipes[path])
        obj.pop("result")
        self.recipes[path] = json.dumps(obj).encode()
        self.assertEqual("UNPROVEN_OR_MISMATCH", self.report()["status"])

    def test_duplicate_json_property_rejected(self):
        path = "data/hexalia/recipe/fire_node_from_ritual_table.json"
        self.recipes[path] = b'{"type":"hexalia:natures_ritual","type":"minecraft:crafting_shaped"}'
        with self.assertRaisesRegex(audit.EvidenceError, "duplicate JSON property"):
            self.report()

    def test_bad_provider_mod_id_rejected(self):
        self.write_zip(mod_id="not_hexalia")
        with self.assertRaisesRegex(audit.EvidenceError, "mod ID"):
            audit.audit_jar(
                self.jar, expected_sha1=hashlib.sha1(self.jar.read_bytes()).hexdigest()
            )

    def test_zip_duplicate_recipe_entries_rejected(self):
        with zipfile.ZipFile(self.jar, "a") as z:
            with self.assertWarns(UserWarning):
                z.writestr("data/hexalia/recipe/fire_node_from_ritual_table.json", b"{}")
        with self.assertRaisesRegex(audit.EvidenceError, "duplicate entries"):
            audit.audit_jar(
                self.jar, expected_sha1=hashlib.sha1(self.jar.read_bytes()).hexdigest()
            )

    def test_wrong_jar_name_and_symlink_rejected(self):
        other = Path(self.temp.name) / "fake.jar"
        other.write_bytes(self.jar.read_bytes())
        with self.assertRaises(audit.EvidenceError):
            audit.audit_jar(other, expected_sha1=hashlib.sha1(other.read_bytes()).hexdigest())
        self.jar.unlink()
        self.jar.symlink_to(other)
        with self.assertRaises(audit.EvidenceError):
            audit.audit_jar(self.jar, expected_sha1=hashlib.sha1(other.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
