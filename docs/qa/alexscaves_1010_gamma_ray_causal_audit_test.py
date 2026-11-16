#!/usr/bin/env python3
"""Fail-closed native Gamma Ray audit and optional physical publisher CLI tests.

Set AC_GAMMA_JAR and AC_GAMMA_JAVAP for the physical tests; CI supplies both.
The tests execute no Minecraft world, provider hook or packet handler.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import alexscaves_1010_gamma_ray_causal_audit as audit

SEAL = audit.PROVIDER / "EXACT-GAMMA-RAY-CAUSAL-1.0.10.json"
SCRIPT = Path(audit.__file__).resolve()


class NativeGammaAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"), object_pairs_hook=audit.unique_pairs)
        cls.tick = {"instructions": [{key: row[key] for key in ("offset", "opcode", "operand", "symbol")}
                                    for row in cls.seal["pivots"] if row["owner"] == audit.CLASS and row["name"] == "onUseTick"]}

    def test_scope_and_composed_whole_method_boundaries(self):
        self.assertEqual(self.seal["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(self.seal["safety"], audit.SAFETY)
        self.assertEqual(self.seal["prior_seal_sha256"], audit.PRIOR_SEALS)
        methods = self.seal["census"]["method_census"]
        tick = next(m for m in methods if m["name"] == "onUseTick")
        self.assertEqual((tick["instructions"], tick["direct_branches"]), (523, 57))
        self.assertEqual(tick["body_sha256"], audit.PARENT_HASHES["onUseTick"])
        self.assertEqual(len(methods), 12)
        self.assertEqual(self.seal["census"]["declared_methods"], audit.DECLARED_COUNTS)

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            json.loads('{"max_level":1,"max_level":2}', object_pairs_hook=audit.unique_pairs)

    def test_causal_pivots_and_boolean_slot_are_closed(self):
        audit.check_pivots(self.tick, audit.TICK_PIVOTS)
        self.assertEqual(audit.gamma_slot(self.tick)["reads"], [367, 402, 922, 1029, 1138])
        for offset, key, replacement in ((338, "opcode", "iflt"), (1016, "operand", "1051"),
                                         (1034, "opcode", "fconst_1"), (1088, "operand", "1111"),
                                         (1111, "operand", "400"), (1122, "opcode", "ifne")):
            changed = copy.deepcopy(self.tick)
            next(row for row in changed["instructions"] if row["offset"] == offset)[key] = replacement
            with self.subTest(offset=offset), self.assertRaisesRegex(ValueError, "pivot drift"):
                audit.check_pivots(changed, audit.TICK_PIVOTS)
        duplicate = copy.deepcopy(self.tick)
        duplicate["instructions"].append(copy.deepcopy(duplicate["instructions"][0]))
        with self.assertRaisesRegex(ValueError, "offsets"):
            audit.check_pivots(duplicate, audit.TICK_PIVOTS)

    def test_slot_alias_and_second_lookup_are_rejected(self):
        for row in ({"offset": 1200, "opcode": "istore", "operand": "18", "symbol": ""},
                    {"offset": 1200, "opcode": "iinc", "operand": "18, 1", "symbol": ""},
                    {"offset": 1200, "opcode": "iload", "operand": "18", "symbol": ""}):
            changed = copy.deepcopy(self.tick)
            changed["instructions"].append(row)
            with self.subTest(opcode=row["opcode"]), self.assertRaisesRegex(ValueError, "local18"):
                audit.gamma_slot(changed)
        changed = copy.deepcopy(self.tick)
        lookup = copy.deepcopy(next(r for r in changed["instructions"] if r["offset"] == 332))
        lookup["offset"] = 1200
        changed["instructions"].append(lookup)
        with self.assertRaisesRegex(ValueError, "lookup population"):
            audit.gamma_slot(changed)

    def test_full_body_and_branch_census_reject_changes_away_from_pivots(self):
        source = "  public void fixture();\n    descriptor: ()V\n    Code:\n       0: iconst_0\n       1: ifeq 5\n       4: return\n       5: return\n"
        method = audit.parse_methods(source)[0]
        digest = audit.digest_method(method)
        audit.verify_method(method, source, digest, 4, 1)
        altered = copy.deepcopy(method)
        altered["instructions"][0]["opcode"] = "iconst_1"
        with self.assertRaisesRegex(ValueError, "whole native method"):
            audit.verify_method(altered, source, digest, 4, 1)
        with self.assertRaisesRegex(ValueError, "instruction census"):
            audit.verify_method(method, source, digest, 3, 1)
        with self.assertRaisesRegex(ValueError, "branch census"):
            audit.verify_method(method, source, digest, 4, 0)
        altered = copy.deepcopy(method)
        altered["instructions"][1]["operand"] = "3"
        with self.assertRaisesRegex(ValueError, "branch target"):
            audit.verify_method(altered, source, audit.digest_method(altered), 4, 1)

    def test_seal_rejects_resource_pivot_method_branch_and_scope_mutations(self):
        mutations = [
            lambda s: s["resource_json"].update(max_level=2),
            lambda s: s["x_ray_resource_json"].update(exclusive_set=[]),
            lambda s: s["class_sha256"].update({audit.CLASS: "0" * 64}),
            lambda s: s["artifact"].update(sha256="0" * 64),
            lambda s: s["census"]["method_census"][0].update(body_sha256="0" * 64),
            lambda s: s["census"]["method_census"][0].update(direct_branches=56),
            lambda s: s["pivots"][0].update(opcode="nop"),
            lambda s: s["safety"].update(mutating_hook="VERIFIED"),
            lambda s: s.update(claim_scope="GAMEPLAY_CERTIFIED"),
        ]
        audit.verify_seal(self.seal, self.seal)
        for n, mutate in enumerate(mutations):
            changed = copy.deepcopy(self.seal)
            mutate(changed)
            with self.subTest(mutation=n), self.assertRaises(ValueError):
                audit.verify_seal(self.seal, changed)

    def test_unsealed_or_truncated_resource_roster_rejected(self):
        with self.assertRaisesRegex(ValueError, "resource roster"):
            audit.verify_resources({audit.RES: b"{}"})
        with self.assertRaisesRegex(ValueError, "resource fingerprint"):
            audit.verify_resources({path: b"{}" for path in audit.RESOURCE_HASHES})

    def test_all_token_owners_have_bounded_native_or_visual_disposition(self):
        visual = self.seal["visual_consumers"]
        self.assertEqual(visual["scope"], "SELECTED_NATIVE_CLIENT_VISUAL_CONSUMERS_ONLY")
        self.assertEqual(visual["class_sha256"], audit.VISUAL_CLASS_HASHES)
        self.assertEqual(set(self.seal["compiled_token_owners"]), {audit.CLASS, audit.CLASS_REG} | set(visual["class_sha256"]))
        self.assertEqual([m["instructions"] for m in visual["method_census"]], [1771, 209])
        self.assertEqual(visual["limits"]["complete_rendering_cfg"], "NOT_RECONSTRUCTED")
        self.assertEqual(visual["limits"]["actual_pixels_and_delivery"], "NOT_TESTED")
        for owner, offset, key, replacement in (
            (audit.ITEM_RENDERER, 1989, "symbol", "Field RAYGUN_TEXTURE:Lnet/minecraft/resources/ResourceLocation;"),
            (audit.ITEM_RENDERER, 1974, "opcode", "iflt"),
            (audit.RAY_RENDERER, 178, "operand", "12"),
            (audit.RAY_RENDERER, 300, "operand", "308"),
        ):
            method = {"instructions": [{k: row[k] for k in ("offset", "opcode", "operand", "symbol")} for row in visual["pivots"] if row["owner"] == owner]}
            audit.check_visual_pivots(owner, method)
            next(row for row in method["instructions"] if row["offset"] == offset)[key] = replacement
            with self.subTest(owner=owner, offset=offset), self.assertRaisesRegex(ValueError, "pivot drift"):
                audit.check_visual_pivots(owner, method)

    def test_server_cadence_is_not_charge_warmup(self):
        self.assertEqual([n for n in range(16) if (n - 15) % 3 == 0], [0, 3, 6, 9, 12, 15])
        self.assertIn("no extra elapsed>=15", self.seal["static_contract"]["server_damage_gate"])
        self.assertIn("Tremorzilla ||", self.seal["static_contract"]["status_gate"])
        self.assertEqual(self.seal["resource_json"], audit.EXACT_GAMMA)
        self.assertNotIn("exclusive_set", self.seal["resource_json"])


class PublisherGammaCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        jar, javap = os.environ.get("AC_GAMMA_JAR"), os.environ.get("AC_GAMMA_JAVAP")
        if not jar or not javap:
            raise unittest.SkipTest("set AC_GAMMA_JAR and AC_GAMMA_JAVAP to run physical publisher CLI tests")
        cls.jar, cls.javap = Path(jar), javap
        if not cls.jar.is_file() or not Path(javap).is_file():
            raise AssertionError("configured physical JAR/javap does not exist")
        cls.expected = SEAL.read_bytes()

    def run_cli(self, output, *, jar=None, seal=SEAL, javap=None):
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        return subprocess.run([sys.executable, str(SCRIPT), "--jar", str(jar or self.jar), "--javap", str(javap or self.javap), "--seal", str(seal), "--output", str(output)], capture_output=True, text=True, timeout=120, env=env)

    def test_publisher_cli_is_exact_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "evidence.json"
            for _ in range(2):
                result = self.run_cli(output)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(output.read_bytes(), self.expected)

    def test_real_cli_refuses_artifact_and_scope_mutations_without_output_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output, wrong = tmp / "evidence.json", tmp / "wrong.jar"
            output.write_text("preserve failed-run output\n")
            wrong.write_bytes(b"wrong publisher artifact")
            result = self.run_cli(output, jar=wrong)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("fingerprint drift", result.stderr)
            changed = json.loads(self.expected)
            changed["safety"]["mutating_hook"] = "VERIFIED"
            seal = tmp / "unsafe.json"
            seal.write_text(audit.canonical(changed))
            result = self.run_cli(output, seal=seal)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe Gamma seal", result.stderr)
            self.assertEqual(output.read_text(), "preserve failed-run output\n")

    def test_real_cli_refuses_causal_seal_and_native_transcript_mutations(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output, seal = tmp / "evidence.json", tmp / "changed.json"
            changed = json.loads(self.expected)
            next(row for row in changed["pivots"] if row["owner"] == audit.CLASS and row["offset"] == 1034)["opcode"] = "fconst_1"
            seal.write_text(audit.canonical(changed))
            result = self.run_cli(output, seal=seal)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("exact native causal seal drift", result.stderr)
            self.assertFalse(output.exists())
            # The JAR stays SHA-exact; a successful external javap process lies
            # about a native damage constant. Whole-method verification fails.
            wrapper = tmp / "javap-mutated"
            wrapper.write_text("#!" + sys.executable + "\nimport subprocess,sys\nr=subprocess.run(" + repr([self.javap]) + "+sys.argv[1:],capture_output=True,text=True)\nsys.stdout.write(r.stdout.replace('1034: fconst_2','1034: fconst_1'))\nsys.stderr.write(r.stderr)\nsys.exit(r.returncode)\n")
            wrapper.chmod(0o755)
            result = self.run_cli(output, javap=wrapper)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("method identity mismatch", result.stderr)
            self.assertFalse(output.exists())

    def test_physical_resources_and_duplicate_seal_keys_fail_closed(self):
        with zipfile.ZipFile(self.jar) as arc:
            raw = {path: arc.read(path) for path in audit.RESOURCE_HASHES}
        audit.verify_resources(raw)
        changed = dict(raw)
        changed[audit.RES] = changed[audit.RES].replace(b'"max_level": 1', b'"max_level": 2')
        self.assertNotEqual(changed[audit.RES], raw[audit.RES])
        with self.assertRaisesRegex(ValueError, "resource fingerprint"):
            audit.verify_resources(changed)
        with tempfile.TemporaryDirectory() as tmp:
            output, duplicate = Path(tmp) / "report.json", Path(tmp) / "duplicate.json"
            duplicate.write_text('{"claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY","claim_scope":"GAMEPLAY"}')
            result = self.run_cli(output, seal=duplicate)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate JSON key", result.stderr)
            self.assertFalse(output.exists())

    def test_real_cli_refuses_client_texture_selection_transcript_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            output, wrapper = Path(tmp) / "evidence.json", Path(tmp) / "javap-visual-mutated"
            # Successful javap output changes only the Gamma texture consumer;
            # artifact, server methods, resources and Gamma slot stay exact.
            wrapper.write_text("#!" + sys.executable + "\nimport subprocess,sys\nr=subprocess.run(" + repr([self.javap]) + "+sys.argv[1:],capture_output=True,text=True)\nsys.stdout.write(r.stdout.replace('Field RAYGUN_BLUE_TEXTURE:', 'Field RAYGUN_TEXTURE:'))\nsys.stderr.write(r.stderr)\nsys.exit(r.returncode)\n")
            wrapper.chmod(0o755)
            result = self.run_cli(output, javap=wrapper)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Gamma visual method identity drift", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
