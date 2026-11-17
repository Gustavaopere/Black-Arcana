#!/usr/bin/env python3
"""Fail-closed X-Ray native proof and optional real publisher CLI regressions.

Set AC_XRAY_JAR and AC_XRAY_JAVAP for physical artifact tests; CI supplies both.
No test executes a Minecraft world, provider mutation or packet handler.
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

import alexscaves_1010_xray_causal_audit as audit

SEAL = audit.PROVIDER / "EXACT-XRAY-CAUSAL-1.0.10.json"
SCRIPT = Path(audit.__file__).resolve()


class NativeXrayAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = json.loads(SEAL.read_text(encoding="utf8"), object_pairs_hook=audit.unique_pairs)
        rows = {row["offset"]: {key: row[key] for key in ("offset", "opcode", "operand", "symbol")}
                for row in cls.seal["pivots"] if row["owner"] == audit.CLASS}
        for accesses in cls.seal["local_slot_accesses"].values():
            rows.update({row["offset"]: {key: row[key] for key in ("offset", "opcode", "operand", "symbol")} for row in accesses})
        cls.tick = {"instructions": [rows[offset] for offset in sorted(rows)]}

    def test_scope_inherited_native_and_network_boundaries(self):
        self.assertEqual(self.seal["claim_scope"], "STATIC_TECHNICAL_CATALOG_ONLY")
        self.assertEqual(self.seal["safety"], audit.SAFETY)
        self.assertEqual(self.seal["prior_seal_sha256"], audit.PRIOR_SEALS)
        self.assertEqual(self.seal["composed_gamma_report_sha256"], audit.GAMMA_REPORT_SHA256)
        self.assertEqual(self.seal["composed_energy_report_sha256"], audit.ENERGY_REPORT_SHA256)
        inherited = self.seal["inherited_native_contract"]
        self.assertEqual((inherited["native_method_count"], inherited["onUseTick_instructions"], inherited["onUseTick_direct_branches"], inherited["visual_method_count"]), (12, 523, 57, 2))
        self.assertEqual(inherited["network_authorization"], "NOT_VERIFIED")
        self.assertEqual(inherited["codec_and_packet_delivery"], "NOT_VERIFIED")
        self.assertEqual(inherited["projectile_predicate_bootstrap"]["xray_additional_invokedynamic_offset"], 635)
        self.assertEqual(inherited["projectile_predicate_bootstrap"]["implementation"], "REF_invokeVirtual net/minecraft/world/entity/Entity.canBeHitByProjectile:()Z")

    def test_duplicate_json_keys_and_malformed_seal_scope_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            json.loads('{"max_level":1,"max_level":2}', object_pairs_hook=audit.unique_pairs)
        for changed in ([], {}, {"claim_scope": "GAMEPLAY_CERTIFIED", "safety": audit.SAFETY}):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "unsafe X-Ray seal"):
                audit.verify_seal(self.seal, changed)

    def test_individual_pivots_fail_closed_for_branch_endpoint_trace_and_aabb(self):
        audit.check_pivots(self.tick, audit.TICK_PIVOTS)
        for offset, key, replacement in (
            (50, "opcode", "iflt"), (105, "operand", "19"), (115, "operand", "10"),
            (578, "operand", "7"), (586, "opcode", "fconst_0"), (600, "opcode", "ifgt"),
            (606, "opcode", "fconst_0"), (633, "operand", "21"), (635, "symbol", "InvokeDynamic #1:test:"),
            (640, "symbol", "Method ProjectileUtil.getHitResultOnViewVector:"),
            (647, "opcode", "ifnonnull"), (654, "operand", "657"), (659, "opcode", "fconst_2"),
            (666, "operand", "669"), (689, "operand", "24"), (711, "opcode", "ifeq"),
            (724, "opcode", "ifne"), (754, "symbol", "Method EntityHitResult.getLocation:"),
            (766, "operand", "13"), (897, "symbol", "double -2.0d"), (911, "opcode", "dconst_0"),
        ):
            changed = copy.deepcopy(self.tick)
            next(row for row in changed["instructions"] if row["offset"] == offset)[key] = replacement
            with self.subTest(offset=offset), self.assertRaisesRegex(ValueError, "pivot drift"):
                audit.check_pivots(changed, audit.TICK_PIVOTS)
        changed = copy.deepcopy(self.tick)
        changed["instructions"].append(changed["instructions"][0])
        with self.assertRaisesRegex(ValueError, "offsets"):
            audit.check_pivots(changed, audit.TICK_PIVOTS)

    def test_full_slot_population_aliases_rewrites_and_lookup_rejected(self):
        self.assertEqual(audit.local_slots(self.tick), self.seal["local_slot_accesses"])
        self.assertEqual(self.seal["xray_boolean_slot"]["writes"], [58])
        self.assertEqual(self.seal["xray_boolean_slot"]["reads"], [105, 122, 569])
        for slot, opcode in ((9, "istore"), (9, "iinc"), (9, "iload"), (8, "fstore"), (14, "astore"), (23, "fload")):
            changed = copy.deepcopy(self.tick)
            changed["instructions"].append({"offset": 1200, "opcode": opcode, "operand": str(slot) + (", 1" if opcode == "iinc" else ""), "symbol": ""})
            with self.subTest(slot=slot, opcode=opcode), self.assertRaisesRegex(ValueError, "local" + str(slot)):
                audit.local_slots(changed)
        changed = copy.deepcopy(self.tick)
        changed["instructions"].append({"offset": 1200, "opcode": "getstatic", "operand": "#270", "symbol": "Field ACEnchantmentRegistry.X_RAY:Lnet/minecraft/resources/ResourceKey;"})
        with self.assertRaisesRegex(ValueError, "lookup population"):
            audit.local_slots(changed)

    def test_slot23_float_lifetime_is_distinct_from_later_reuse(self):
        slot = self.seal["loop_slot23"]
        self.assertEqual((slot["initial"], slot["step"], slot["guard"]), (1.0, 1.0, "local23<local8"))
        self.assertEqual(slot["writes"], [587, 661])
        self.assertEqual(slot["reads"], [595, 657])
        self.assertEqual(slot["later_reuse"], {"block_position_store": 689, "impact_position_store": 834, "status_amplifier_store": 932})
        self.assertEqual(self.seal["range_slot"]["formula"], "25.0F*warmup_progress(local7)")
        self.assertEqual(self.seal["endpoint_slots"]["initial_selection"], "XRay?local12:local11.pick_location")

    def test_registry_mapping_and_complete_initializer_are_bounded(self):
        methods = self.seal["census"]["method_census"]
        self.assertEqual([(m["name"], m["instructions"], m["direct_branches"]) for m in methods], [("onUseTick", 523, 57), ("key", 6, 0), ("<clinit>", 182, 0)])
        self.assertEqual(methods[2]["body_sha256"], audit.CLINIT_SHA256)
        source = "  static {};\n    descriptor: ()V\n    Code:\n       0: return\n"
        clinit = audit.registry_clinit(source)
        self.assertEqual(clinit["instructions"][0]["opcode"], "return")
        for changed in ("", source + source):
            with self.assertRaisesRegex(ValueError, "initializer"):
                audit.registry_clinit(changed)
        for name, expected in (("key", audit.KEY_PIVOTS), ("<clinit>", audit.REGISTRY_PIVOTS)):
            method = {"instructions": [{k: row[k] for k in ("offset", "opcode", "operand", "symbol")} for row in self.seal["pivots"] if row["name"] == name]}
            audit.check_pivots(method, expected)
            method["instructions"][0]["symbol"] = "drift"
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "pivot drift"):
                audit.check_pivots(method, expected)

    def test_whole_body_and_direct_branch_targets_reject_away_from_pivot_drift(self):
        source = "  public void fixture();\n    descriptor: ()V\n    Code:\n       0: iconst_0\n       1: ifeq 5\n       4: return\n       5: return\n"
        method = audit.parse_methods(source)[0]
        audit.gamma.verify_method(method, source, audit.digest_method(method), 4, 1)
        changed = copy.deepcopy(method)
        changed["instructions"][0]["opcode"] = "iconst_1"
        with self.assertRaisesRegex(ValueError, "whole native method"):
            audit.gamma.verify_method(changed, source, audit.digest_method(method), 4, 1)
        with self.assertRaisesRegex(ValueError, "instruction census"):
            audit.gamma.verify_method(method, source, audit.digest_method(method), 3, 1)
        with self.assertRaisesRegex(ValueError, "branch census"):
            audit.gamma.verify_method(method, source, audit.digest_method(method), 4, 0)
        changed["instructions"][1]["operand"] = "3"
        with self.assertRaisesRegex(ValueError, "branch target"):
            audit.gamma.verify_method(changed, source, audit.digest_method(changed), 4, 1)

    def test_publisher_metadata_token_owner_roster_and_no_xray_bonus(self):
        self.assertEqual(self.seal["resource_json"], audit.EXACT_X_RAY)
        self.assertEqual(self.seal["gamma_ray_resource_json"], audit.EXACT_GAMMA)
        self.assertEqual(self.seal["supported_item_tag"], {"values": ["alexscaves:raygun"]})
        self.assertEqual(self.seal["compiled_token_owners"], audit.TOKEN_OWNERS)
        contract = self.seal["static_contract"]
        self.assertIn("first nonnull", contract["scan_break"])
        self.assertIn("remains unchanged", contract["scan_no_hit"])
        self.assertIn("only X-Ray false", contract["block_sturdy"])
        self.assertIn("no damage/status boolean read or separate bonus", contract["native_pipeline_reference"])
        self.assertEqual(contract["native_damage_status"]["gamma_false"], 1.5)
        self.assertEqual(contract["native_damage_status"]["gamma_true"], 2.0)
        self.assertEqual(contract["native_damage_status"]["effect_duration_ticks"], 800)
        self.assertEqual(contract["native_damage_status"]["gamma_false_amplifier"], 0)
        self.assertEqual(contract["native_damage_status"]["gamma_true_amplifier"], 4)

    def test_roster_resource_and_source_fingerprints_reject_changes(self):
        with self.assertRaisesRegex(ValueError, "resource roster"):
            audit.verify_resources({audit.RES: b"{}"})
        with self.assertRaisesRegex(ValueError, "resource fingerprint"):
            audit.verify_resources({name: b"{}" for name in audit.RESOURCE_HASHES})
        census = self.seal["publisher_enchantment_census"]
        self.assertEqual(census["count"], 51)
        self.assertEqual(census["resource_sha256"], audit.PUBLISHER_ENCHANTMENT_HASHES)
        self.assertEqual(census["ids"], sorted(Path(p).stem for p in audit.PUBLISHER_ENCHANTMENT_HASHES))
        self.assertTrue(census["inventory_ids_match"])
        self.assertEqual(self.seal["source_helper_sha256"], {"docs/qa/" + name: audit.digest((SCRIPT.parent / name).read_bytes()) for name in audit.SOURCE_HELPERS})

    def test_seal_rejects_safety_body_branch_slot_range_and_roster_mutations(self):
        mutations = [
            lambda s: s["resource_json"].update(max_level=2),
            lambda s: s["resource_json"].update(exclusive_set=[]),
            lambda s: s["census"]["method_census"][0].update(direct_branches=56),
            lambda s: s["census"]["method_census"][2].update(body_sha256="0" * 64),
            lambda s: s["pivots"][0].update(opcode="nop"),
            lambda s: s["xray_boolean_slot"].update(reads=[105, 122]),
            lambda s: s["range_slot"].update(formula="50*progress"),
            lambda s: s["loop_slot23"].update(step=2),
            lambda s: s["publisher_enchantment_census"].update(count=52),
            lambda s: s["source_helper_sha256"].update({"docs/qa/" + audit.SOURCE_HELPERS[0]: "0" * 64}),
            lambda s: s["safety"].update(wall_penetration="VERIFIED"),
            lambda s: s["safety"].update(mutating_hook="VERIFIED"),
            lambda s: s.update(claim_scope="GAMEPLAY_CERTIFIED"),
        ]
        audit.verify_seal(self.seal, self.seal)
        for n, mutate in enumerate(mutations):
            changed = copy.deepcopy(self.seal)
            mutate(changed)
            with self.subTest(mutation=n), self.assertRaises(ValueError):
                audit.verify_seal(self.seal, changed)


class PublisherXrayCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        jar, javap = os.environ.get("AC_XRAY_JAR"), os.environ.get("AC_XRAY_JAVAP")
        if not jar or not javap:
            raise unittest.SkipTest("set AC_XRAY_JAR and AC_XRAY_JAVAP to run physical publisher CLI tests")
        cls.jar, cls.javap = Path(jar), javap
        if not cls.jar.is_file() or not Path(javap).is_file():
            raise AssertionError("configured physical publisher JAR/javap does not exist")
        cls.expected = SEAL.read_bytes()

    def run_cli(self, output, *, jar=None, seal=SEAL, javap=None):
        return subprocess.run([sys.executable, str(SCRIPT), "--jar", str(jar or self.jar), "--javap", str(javap or self.javap), "--seal", str(seal), "--output", str(output)], capture_output=True, text=True, timeout=180, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    def test_publisher_cli_is_exact_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "evidence.json"
            for _ in range(2):
                result = self.run_cli(output)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(output.read_bytes(), self.expected)

    def test_real_cli_refuses_wrong_artifact_unsafe_scope_and_duplicate_keys_without_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output, wrong, seal = tmp / "evidence.json", tmp / "wrong.jar", tmp / "changed.json"
            output.write_text("preserve failed-run output\n")
            wrong.write_bytes(b"wrong publisher artifact")
            result = self.run_cli(output, jar=wrong)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("fingerprint drift", result.stderr)
            changed = json.loads(self.expected)
            changed["safety"]["mutating_hook"] = "VERIFIED"
            seal.write_text(audit.canonical(changed))
            result = self.run_cli(output, seal=seal)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe X-Ray seal", result.stderr)
            seal.write_text('{"claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY","claim_scope":"GAMEPLAY"}')
            result = self.run_cli(output, seal=seal)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate JSON key", result.stderr)
            self.assertEqual(output.read_text(), "preserve failed-run output\n")

    def test_real_cli_refuses_causal_seal_mutation_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output, seal = Path(tmp) / "evidence.json", Path(tmp) / "changed.json"
            changed = json.loads(self.expected)
            next(row for row in changed["pivots"] if row["owner"] == audit.CLASS and row["offset"] == 647)["opcode"] = "ifnonnull"
            seal.write_text(audit.canonical(changed))
            result = self.run_cli(output, seal=seal)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("exact native causal seal drift", result.stderr)
            self.assertFalse(output.exists())

    def test_real_cli_refuses_successful_javap_lies_about_loop_and_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for old, new, error in (("647: ifnull", "647: ifnonnull", "method identity mismatch"), ("String x_ray", "String altered_x_ray", "whole native method fingerprint drift")):
                output, wrapper = tmp / "evidence.json", tmp / "javap-mutated"
                wrapper.write_text("#!" + sys.executable + "\nimport subprocess,sys\nr=subprocess.run(" + repr([self.javap]) + "+sys.argv[1:],capture_output=True,text=True)\nsys.stdout.write(r.stdout.replace(" + repr(old) + "," + repr(new) + "))\nsys.stderr.write(r.stderr)\nsys.exit(r.returncode)\n")
                wrapper.chmod(0o755)
                result = self.run_cli(output, javap=wrapper)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(error, result.stderr)
                self.assertFalse(output.exists())

    def test_physical_publisher_resources_roster_and_inventory_changes_fail_closed(self):
        with zipfile.ZipFile(self.jar) as arc:
            raw = {path: arc.read(path) for path in audit.RESOURCE_HASHES}
            enchants = {path: arc.read(path) for path in audit.PUBLISHER_ENCHANTMENT_HASHES}
        audit.verify_resources(raw)
        changed = dict(raw)
        changed[audit.RES] = changed[audit.RES].replace(b'"max_level": 1', b'"max_level": 2')
        self.assertNotEqual(changed[audit.RES], raw[audit.RES])
        with self.assertRaisesRegex(ValueError, "resource fingerprint"):
            audit.verify_resources(changed)
        inventory = json.loads((audit.PROVIDER / "INTEGRATION-SCOPE-INVENTORY-1.0.10.json").read_text())
        audit.publisher_enchantment_census(enchants, inventory)
        changed = dict(enchants)
        changed.pop(audit.RES)
        with self.assertRaisesRegex(ValueError, "population drift"):
            audit.publisher_enchantment_census(changed, inventory)
        changed = dict(enchants)
        changed[audit.RES] += b" "
        with self.assertRaisesRegex(ValueError, "hash drift"):
            audit.publisher_enchantment_census(changed, inventory)
        changed = copy.deepcopy(inventory)
        changed["remaining_family_inventory"]["enchantment_ids"].remove("x_ray")
        with self.assertRaisesRegex(ValueError, "IDs/inventory drift"):
            audit.publisher_enchantment_census(enchants, changed)


if __name__ == "__main__":
    unittest.main()
