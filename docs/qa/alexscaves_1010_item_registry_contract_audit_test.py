#!/usr/bin/env python3
"""Semantic negative controls and immutable exact-binary registry reproduction."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from alexscaves_1010_item_registry_contract_audit import (
    AuditError, BRIDGE, CLAIMS, ENTRY, IDS, NATIVE_PIN, PROVIDER, SEAL, TARGET,
    canonical, cp_index, digest, load_seal, method_at, resolve_bindings,
    validate_bridge_pipeline, validate_contract,
)

SCRIPT = Path(__file__).with_name("alexscaves_1010_item_registry_contract_audit.py")
ORIGINAL_PROBE = Path(__file__).with_name("alexscaves_1010_item_registry_probe.py")
ORIGINAL_WORKFLOW = SCRIPT.parents[2] / ".github/workflows/alexscaves-1010-item-registry-probe.yml"


class RegistryContractNegativeControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seal = load_seal(SEAL)

    def rejected(self, change):
        altered = copy.deepcopy(self.seal)
        change(altered)
        with self.assertRaises(AuditError):
            validate_contract(altered)

    def test_complete_scope_is_internally_closed(self):
        validate_contract(self.seal)
        native = self.seal["native"]
        self.assertEqual(digest(canonical(native).encode()), NATIVE_PIN)
        self.assertEqual(len(native["bindings"]), 188)
        self.assertEqual(len(native["spawn_egg_registrations"]), 43)
        self.assertEqual(len(native["support_field_initializers"]), 12)
        self.assertLess(SEAL.stat().st_size, 2_000_000)
        self.assertEqual(native["counts"]["literal_registration_requests"], 231)

    def test_binding_without_write_is_rejected(self):
        self.rejected(lambda d: d["native"]["bindings"].pop())

    def test_duplicate_binding_is_rejected(self):
        self.rejected(lambda d: d["native"]["bindings"].append(copy.deepcopy(d["native"]["bindings"][0])))

    def test_field_cannot_be_mapped_to_another_literal(self):
        self.rejected(lambda d: d["native"]["bindings"][0].update(path="other_item"))

    def test_factory_cannot_be_swapped_between_fields(self):
        def change(d):
            bindings = d["native"]["bindings"]
            bindings[0]["factory"], bindings[1]["factory"] = bindings[1]["factory"], bindings[0]["factory"]
        self.rejected(change)

    def test_causal_stack_rejects_missing_initializer_producer(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        body = method_at(target, "<clinit>")["instructions"]
        offset = self.seal["native"]["bindings"][0]["factory_site_offset"]
        body[:] = [row for row in body if row["offset"] != offset]
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_causal_stack_rejects_duplicate_field_write(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        body = method_at(target, "<clinit>")["instructions"]
        offset = self.seal["native"]["bindings"][0]["write_offset"]
        index = next(i for i, row in enumerate(body) if row["offset"] == offset)
        body.insert(index, {"offset": offset - 1, "opcode": "dup", "operand": "", "symbol": ""})
        body.insert(index + 2, copy.deepcopy(body[index + 1]))
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_wrong_namespace_is_rejected_by_causal_semantics(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        namespace = next(row for row in method_at(target, "<clinit>")["instructions"] if row["offset"] == 295)
        target["constants"][str(cp_index(namespace["operand"]))]["value"] = "minecraft"
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_field_names_cannot_be_used_to_infer_ids(self):
        bindings = self.seal["native"]["bindings"]
        # Retain actual CP literals even when future declarations do not match a
        # field-name spelling. This seal pins the current exact associations.
        self.assertTrue(all(b["resource_location"] == "alexscaves:" + b["path"] for b in bindings))
        self.rejected(lambda d: d["native"]["bindings"][0].update(resource_location="minecraft:acid_bucket"))

    def test_wrong_factory_owner_is_rejected_by_bootstrap_semantics(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        index = self.seal["native"]["bindings"][0]["bootstrap_index"]
        target["bootstrap_methods"][index]["arguments"][1]["reference"][1] = "example/OtherRegistry"
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_duplicate_factory_is_rejected_by_bijection(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        first, second = self.seal["native"]["bindings"][:2]
        target["bootstrap_methods"][first["bootstrap_index"]] = copy.deepcopy(
            target["bootstrap_methods"][second["bootstrap_index"]])
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_wrong_factory_reference_kind_is_rejected(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        index = self.seal["native"]["bindings"][0]["bootstrap_index"]
        target["bootstrap_methods"][index]["arguments"][1]["reference_kind"] = 8
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_argument_reordering_is_rejected_by_stack_semantics(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        body = method_at(target, "<clinit>")["instructions"]
        binding = self.seal["native"]["bindings"][0]
        literal = next(i for i, row in enumerate(body) if row["offset"] == binding["literal_offset"])
        dynamic = next(i for i, row in enumerate(body) if row["offset"] == binding["factory_site_offset"])
        body[literal], body[dynamic] = body[dynamic], body[literal]
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_unknown_opcode_does_not_receive_lexical_window_credit(self):
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        method_at(target, "<clinit>")["instructions"][0]["opcode"] = "goto"
        with self.assertRaises(AuditError):
            resolve_bindings(target)

    def test_spawn_egg_ids_use_observed_prefix_recipe(self):
        eggs = self.seal["native"]["spawn_egg_registrations"]
        self.assertEqual(eggs[0]["resource_location"], "alexscaves:spawn_egg_teletor")
        self.assertTrue(all(e["path"] == "spawn_egg_" + e["base_name"] for e in eggs))
        target = copy.deepcopy(self.seal["native"]["classes"][TARGET])
        target["bootstrap_methods"][0]["arguments"] = ["\u0001_spawn_egg"]
        with self.assertRaises(AuditError):
            resolve_bindings(target)
        self.rejected(lambda d: d["native"]["spawn_egg_registrations"].pop())

    def test_bridge_wrapper_dispatch_cannot_be_substituted(self):
        classes = copy.deepcopy(self.seal["native"]["classes"])
        classes[BRIDGE]["bootstrap_methods"][0]["arguments"][1]["reference"][2][1] = "raw"
        with self.assertRaises(AuditError):
            validate_bridge_pipeline(classes)

    def test_bridge_registration_order_is_not_interchangeable(self):
        classes = copy.deepcopy(self.seal["native"]["classes"])
        body = method_at(classes[BRIDGE], "register")["instructions"]
        body[10], body[12] = body[12], body[10]
        with self.assertRaises(AuditError):
            validate_bridge_pipeline(classes)

    def test_event_bus_handoff_must_use_native_raw_delegate(self):
        classes = copy.deepcopy(self.seal["native"]["classes"])
        method_at(classes[ENTRY], "<init>")["instructions"][:] = [row for row in
            method_at(classes[ENTRY], "<init>")["instructions"] if row["offset"] != 264]
        # Whole-body validation rejects truncation before handoff indexing.
        self.rejected(lambda d: d["native"]["classes"].update({ENTRY: classes[ENTRY]}))

    def test_deferred_setup_dispatch_cannot_be_promoted_to_immediate(self):
        self.rejected(lambda d: method_at(d["native"]["classes"][ENTRY], "commonSetup")
                      ["instructions"][4].update(opcode="invokestatic"))

    def test_threadlocal_exception_cleanup_and_rethrow_are_required(self):
        classes = copy.deepcopy(self.seal["native"]["classes"])
        method_at(classes[IDS], "constructing")["declaration"]["exception_handlers"].pop()
        with self.assertRaises(AuditError):
            validate_bridge_pipeline(classes)
        self.rejected(lambda d: method_at(d["native"]["classes"][IDS], "constructing")
                      ["instructions"][-1].update(opcode="areturn"))

    def test_helper_bodies_cannot_be_replaced_by_metadata_hashes(self):
        self.rejected(lambda d: method_at(d["native"]["classes"][TARGET], "setup").pop("instructions"))

    def test_factory_hashes_do_not_certify_item_behavior(self):
        item_factory = next(m for m in self.seal["native"]["classes"][TARGET]["methods"]
                            if m["declaration"]["descriptor"] == "()Lnet/minecraft/world/item/Item;"
                            and m["declaration"]["name"].startswith("lambda$static$"))
        self.assertNotIn("instructions", item_factory)
        self.rejected(lambda d: d["boundaries"].update(factory_item_behavior="CERTIFIED"))
        self.rejected(lambda d: d["boundaries"].update(projectile_entity_lifecycle="CERTIFIED"))

    def test_nested_projectile_callback_branches_and_operands_are_pinned(self):
        self.rejected(lambda d: method_at(d["native"]["classes"][TARGET + "$4"], "getProjectile")
                      ["instructions"][-2].update(opcode="pop"))
        self.rejected(lambda d: method_at(d["native"]["classes"][TARGET + "$7"], "execute")
                      ["instructions"][0].update(opcode="aconst_null"))

    def test_nuclear_callback_cost_and_acceptance_handling_cannot_change(self):
        def change_cost(d):
            body = method_at(d["native"]["classes"][TARGET + "$7"], "execute")["instructions"]
            next(row for row in body if row["offset"] == 115)["opcode"] = "iconst_0"
        self.rejected(change_cost)
        def change_acceptance(d):
            body = method_at(d["native"]["classes"][TARGET + "$7"], "execute")["instructions"]
            next(row for row in body if row["offset"] == 69)["opcode"] = "ifeq"
        self.rejected(change_acceptance)

    def test_typed_census_and_pending_caller_boundary_are_pinned(self):
        self.rejected(lambda d: d["native"]["typed_census"].pop(TARGET))
        self.rejected(lambda d: d["native"]["counts"].update(pending_method_references=1))
        self.rejected(lambda d: d["boundaries"].update(threadlocal_key_consumption="VERIFIED"))

    def test_claims_fail_closed_for_runtime_mutation_hook_qa_perks_and_universe(self):
        for key, value in {"runtime_dispatch": "VERIFIED", "mutating_hook": "VERIFIED",
                           "physical_qa": "TESTED", "perk_certification": "CERTIFIED",
                           "mutation": "MUTATION", "provider_universe_closed": True,
                           "semantic_magic_roots_delta": 231}.items():
            with self.subTest(key=key):
                self.rejected(lambda d, k=key, v=value: d["claims"].update({k: v}))
        self.assertEqual(self.seal["claims"], CLAIMS)

    def test_duplicate_json_keys_are_rejected_by_loader(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "duplicate.json"
            path.write_text('{"claims":{},"claims":{}}')
            with self.assertRaises(AuditError):
                load_seal(path)


@unittest.skipUnless((os.environ.get("AC_ITEM_REGISTRY_JAR") and os.environ.get("AC_ITEM_REGISTRY_JAVAP"))
                     or os.environ.get("CI"), "local exact publisher/JDK21 paths; mandatory in contract CI")
class RegistryExactBinaryReproduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (os.environ.get("AC_ITEM_REGISTRY_JAR") and os.environ.get("AC_ITEM_REGISTRY_JAVAP")):
            raise AssertionError("CI requires AC_ITEM_REGISTRY_JAR and AC_ITEM_REGISTRY_JAVAP")

    def cli(self, jar, output, seal=SEAL):
        return subprocess.run([sys.executable, str(SCRIPT), "--jar", str(jar), "--javap",
            os.environ["AC_ITEM_REGISTRY_JAVAP"], "--seal", str(seal), "--output", str(output)],
            text=True, capture_output=True, timeout=240)

    def test_two_real_cli_runs_preserve_all_inputs_and_reproduce_seal(self):
        jar = Path(os.environ["AC_ITEM_REGISTRY_JAR"])
        paths = [jar, Path(os.environ["AC_ITEM_REGISTRY_JAVAP"]), SEAL, SCRIPT,
                 ORIGINAL_PROBE, ORIGINAL_WORKFLOW]
        before = {path: digest(path.read_bytes()) for path in paths}
        with tempfile.TemporaryDirectory() as raw:
            first, second = (Path(raw) / name for name in ("first.json", "second.json"))
            for output in (first, second):
                proc = self.cli(jar, output)
                self.assertEqual(proc.returncode, 0, proc.stderr[-5000:])
                self.assertIn("NO_MUTATION", proc.stdout)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first.read_bytes(), SEAL.read_bytes())
            self.assertEqual(json.loads(first.read_text()), load_seal(SEAL))
            # Existing paths cannot be overwritten even when otherwise valid.
            proc = self.cli(jar, first)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(first.read_bytes(), SEAL.read_bytes())
        self.assertEqual(before, {path: digest(path.read_bytes()) for path in paths})

    def test_wrong_artifact_is_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as raw:
            jar, output = Path(raw) / "wrong.jar", Path(raw) / "out.json"
            jar.write_bytes(b"not the pinned publisher artifact")
            before = jar.read_bytes()
            proc = self.cli(jar, output)
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(jar.read_bytes(), before)

    def test_tampered_scope_seal_is_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as raw:
            seal, output = Path(raw) / "bad-seal.json", Path(raw) / "out.json"
            altered = load_seal(SEAL)
            altered["claims"]["runtime_dispatch"] = "VERIFIED"
            seal.write_text(canonical(altered))
            before = seal.read_bytes()
            proc = self.cli(Path(os.environ["AC_ITEM_REGISTRY_JAR"]), output, seal)
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(seal.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
