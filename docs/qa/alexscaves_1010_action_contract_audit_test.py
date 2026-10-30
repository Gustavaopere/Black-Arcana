#!/usr/bin/env python3
"""Synthetic fail-closed tests; no publisher bytecode or artifact fixture is shipped."""
import copy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile

import alexscaves_1010_action_contract_audit as audit


ACTIONS = (
    "actions/sea-staff-water-bolt.md", "actions/sugar-staff-peppermint-cast.md",
    "actions/sugar-staff-hex-cast.md", "actions/magic-conch-summon-deep-ones.md",
    "actions/totem-possession-remote-control.md", "actions/occult-gem-beholder-observation.md",
    "actions/cloak-darkness-incarnate.md", "actions/conversion-crucible-biome-conversion.md",
)
OWNER = "com.github.alexmodguy.alexscaves.server.item.Synthetic"
JAVAP = """Compiled from "Synthetic.java"
public class com.github.alexmodguy.alexscaves.server.item.Synthetic {
  public com.github.alexmodguy.alexscaves.server.item.Synthetic();
    descriptor: ()V
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return
  public int value();
    descriptor: ()I
    Code:
       0: iconst_1
       1: ireturn
  public int value(int);
    descriptor: (I)I
    Code:
       0: iload_1
       1: tableswitch   { // 0 to 1
                     0: 24
                     1: 26
               default: 28
          }
      24: iconst_0
      25: ireturn
      26: iconst_1
      27: ireturn
      28: iconst_m1
      29: ireturn
  private static void lambda$value$0();
    descriptor: ()V
    Code:
       0: return
  static {};
    descriptor: ()V
    Code:
       0: return
}
"""


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


class ContractAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "provider"
        self.root.mkdir()
        self.jar = Path(self.temp.name) / "synthetic.jar"
        self.resource = "data/alexscaves/synthetic.json"
        self.members = {self.resource: b'{"synthetic":true}\n'}
        self.doc = {
            "schema_version": 1, "version": "1.0.10",
            "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
            "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
            "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
            "provider_universe_closed": False, "semantic_magic_roots": 8,
            "artifact_sha1": "6960b299a39a039ac8a5eb9b07be4ad0e3e0a570",
            "artifact_sha256": "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c",
            "artifact_size_bytes": 75279314,
            "adjacent_source": {
                "repository": "Codx-org/AlexsCavesContinued",
                "revision": "523308608422ab8e31974befa7111ecdf495dd37",
                "declared_version": "1.1.1",
                "role": "CORROBORATION_ONLY_NOT_INSTALLED_PARAMETERS",
            },
            "cards": {}, "action_evidence": {}, "classes": {},
            "resources": {self.resource: sha256(self.members[self.resource])},
        }
        for index, action in enumerate(ACTIONS):
            card = self.root / action
            card.parent.mkdir(exist_ok=True)
            card.write_text("# Synthetic contract " + str(index) + "\n", encoding="utf8")
            self.doc["cards"][action] = sha256(card.read_bytes())
            path = OWNER.replace(".", "/") + str(index) + ".class"
            blob = b"\xca\xfe\xba\xbe\x00\x00\x00\x41" + bytes([index])
            self.members[path] = blob
            self.doc["classes"][path] = {"sha256": sha256(blob), "methods": [{
                "name": "value", "descriptor": "()I",
                "anchors": [{"offset": 0, "opcode": "iconst_1", "operand": "", "symbol": ""}],
            }]}
            self.doc["action_evidence"][action] = {"classes": [path], "resources": [self.resource]}
        self.write_jar()

    def write_jar(self, extras=()):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.jar, "w") as archive:
                for path, blob in [*self.members.items(), *extras]:
                    archive.writestr(path, blob)

    def expected_identity(self):
        blob = self.jar.read_bytes()
        return {"sha1": hashlib.sha1(blob).hexdigest(), "sha256": sha256(blob), "size_bytes": len(blob)}

    def inspect(self, doc=None, output=JAVAP, *, profile="actions"):
        def completed(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, stdout=output.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            return audit.audit(self.jar, doc or self.doc, self.root, "synthetic-javap",
                               expected_identity=self.expected_identity, profile=profile)

    def effects_fixture(self):
        """Keep artifact fixtures shared, but seal a separate literal card roster."""
        doc = copy.deepcopy(self.doc)
        doc["catalog_family"] = "MOB_EFFECTS"
        doc["effect_evidence"] = {}
        doc["cards"] = {}
        for action, effect in zip(ACTIONS, sorted(audit.EFFECTS)):
            card = self.root / effect
            card.parent.mkdir(exist_ok=True)
            card.write_bytes((self.root / action).read_bytes())
            doc["cards"][effect] = sha256(card.read_bytes())
            doc["effect_evidence"][effect] = doc["action_evidence"][action]
        del doc["action_evidence"]
        return doc

    def dreadbow_fixture(self):
        """A two-card family needs only two anchored classes, independently sealed."""
        doc = copy.deepcopy(self.doc)
        doc["catalog_family"] = "DREADBOW_AND_DARK_ARROW"
        doc["contract_evidence"] = {}
        doc["cards"] = {}
        selected_classes = {}
        for action, relative in zip(ACTIONS, sorted(audit.DREADBOW)):
            card = self.root / relative
            card.parent.mkdir(exist_ok=True)
            card.write_bytes((self.root / action).read_bytes())
            doc["cards"][relative] = sha256(card.read_bytes())
            record = doc["action_evidence"][action]
            doc["contract_evidence"][relative] = record
            selected_classes.update({path: doc["classes"][path] for path in record["classes"]})
        doc["classes"] = selected_classes
        del doc["action_evidence"]
        return doc

    def test_parser_preserves_overloads_constructor_static_lambda_and_switch(self):
        parsed = audit.parse_javap(JAVAP, OWNER)
        self.assertEqual({("<init>", "()V"), ("<clinit>", "()V"), ("value", "()I"),
                          ("value", "(I)I"), ("lambda$value$0", "()V")}, set(parsed))
        self.assertEqual(("iconst_1", "", ""), parsed[("value", "()I")][0])
        self.assertEqual("tableswitch", parsed[("value", "(I)I")][1][0])
        self.assertEqual({0, 1, 24, 25, 26, 27, 28, 29}, set(parsed[("value", "(I)I")]))
        self.assertEqual("invokespecial", parsed[("<init>", "()V")][1][0])
        self.assertIn('java/lang/Object."<init>":()V', parsed[("<init>", "()V")][1][2])

    def test_parser_rejects_duplicate_offset_or_method_descriptor(self):
        for text in (JAVAP.replace("       1: ireturn", "       0: ireturn", 1),
                     JAVAP.replace("    descriptor: (I)I", "    descriptor: ()I", 1)):
            with self.subTest(text=text[-100:]), self.assertRaises(ValueError):
                audit.parse_javap(text, OWNER)

    def test_parser_binds_typed_generic_declarations_to_exact_owner(self):
        original = "public class " + OWNER + " {"
        declarations = (
            "public class " + OWNER + " {",
            "public abstract class " + OWNER + "<T extends java.lang.Object> implements java.lang.Runnable {",
            "public interface " + OWNER + "<T extends java.lang.Object> {",
            "public enum " + OWNER + " {",
            "public record " + OWNER + "(java.lang.String name) {",
        )
        for declaration in declarations:
            with self.subTest(declaration=declaration):
                parsed = audit.parse_javap(JAVAP.replace(original, declaration), OWNER)
                self.assertIn(("value", "()I"), parsed)
        for wrong in (OWNER + "Extra", "com.example.WrongOwner"):
            with self.subTest(wrong=wrong), self.assertRaises(ValueError):
                audit.parse_javap(JAVAP.replace(original, "public class " + wrong + " {"), OWNER)

    def test_valid_structure_and_cards(self):
        audit.validate_structure(self.doc)
        audit.validate_cards(self.doc, self.root)

    def test_effects_profile_validates_separate_literal_roster(self):
        doc = self.effects_fixture()
        audit.validate_structure(doc, profile="effects")
        audit.validate_cards(doc, self.root, profile="effects")
        self.assertEqual(8, len(doc["cards"]))
        self.assertEqual({"effects/irradiated.md", "effects/magnetizing.md", "effects/rage.md",
                          "effects/stunned.md", "effects/bubbled.md", "effects/deepsight.md",
                          "effects/darkness-incarnate.md", "effects/sugar-rush.md"}, set(doc["cards"]))

    def test_profiles_reject_cross_family_manifests_and_unknown_profile(self):
        doc = self.effects_fixture()
        for manifest, profile in ((doc, "actions"), (self.doc, "effects"), (doc, "all")):
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile=profile)
        with self.assertRaises(ValueError):
            audit.validate_cards(doc, self.root)
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="actions")
        # Selection does not mutate action globals or weaken subsequent defaults.
        audit.validate_structure(self.doc)
        self.assertNotIn("catalog_family", audit.SCOPE)

    def test_effects_missing_extra_or_action_alias_card_rejected(self):
        for key in ("cards", "effect_evidence"):
            for mode in ("missing", "extra", "action_alias"):
                doc = self.effects_fixture()
                victim = "effects/irradiated.md"
                value = doc[key].pop(victim)
                if mode == "extra":
                    doc[key][victim] = value
                    doc[key]["effects/extra.md"] = value
                elif mode == "action_alias":
                    doc[key][ACTIONS[0]] = value
                with self.subTest(key=key, mode=mode), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="effects")

    def test_effects_profile_rejects_missing_wrong_or_inflated_scope(self):
        for key, value in (("catalog_family", "ACTIONS"), ("catalog_family", None),
                           ("semantic_magic_roots", 16), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS")):
            doc = self.effects_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="effects")

    def test_effects_synthetic_audit_preserves_root_count_and_runtime_limits(self):
        result = self.inspect(self.effects_fixture(), profile="effects")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("MOB_EFFECTS", result["catalog_family"])
        self.assertEqual(8, result["semantic_magic_roots"])
        self.assertEqual(8, result["cards_checked"])
        self.assertEqual(8, result["classes_checked"])
        self.assertEqual(8, result["methods_checked"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertNotIn("catalog_family", self.inspect())

    def test_effects_profile_checks_card_seals_and_symlink_containment(self):
        doc = self.effects_fixture()
        card = self.root / "effects/irradiated.md"
        original = card.read_bytes()
        card.write_bytes(original + b"drift")
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="effects")
        outside = Path(self.temp.name) / "outside-effect.md"
        outside.write_bytes(original)
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="effects")

    def test_effects_profile_rechecks_card_seals_after_javap(self):
        doc = self.effects_fixture()
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            if not changed:
                card = self.root / "effects/irradiated.md"
                card.write_bytes(card.read_bytes() + b"changed during effects audit")
                changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="effects",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_cli_selects_explicit_effects_profile_and_keeps_action_default(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap"]
        for profile in ("actions", "effects"):
            argv = arguments + (["--profile", "effects"] if profile == "effects" else [])
            doc = self.effects_fixture() if profile == "effects" else self.doc
            with self.subTest(profile=profile), mock.patch.object(audit, "load_manifest", return_value=doc), \
                    mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, audit.main(argv))
                self.assertEqual(profile, inspect.call_args.kwargs["profile"])

    def test_dreadbow_literal_roster_and_two_class_synthetic_audit(self):
        doc = self.dreadbow_fixture()
        self.assertEqual({"equipment/dreadbow.md", "damage-types/dark-arrow.md"}, set(audit.DREADBOW))
        audit.validate_structure(doc, profile="dreadbow")
        audit.validate_cards(doc, self.root, profile="dreadbow")
        result = self.inspect(doc, profile="dreadbow")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("DREADBOW_AND_DARK_ARROW", result["catalog_family"])
        self.assertEqual(2, result["cards_checked"])
        self.assertEqual(2, result["classes_checked"])
        self.assertEqual(2, result["methods_checked"])
        self.assertEqual(8, result["semantic_magic_roots"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])

    def test_all_three_profiles_are_isolated_without_global_state_mutation(self):
        snapshots = tuple(copy.deepcopy(value) for value in
                          (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE))
        documents = {"actions": self.doc, "effects": self.effects_fixture(),
                     "dreadbow": self.dreadbow_fixture()}
        for profile, manifest in documents.items():
            for other in documents:
                if profile == other:
                    continue
                with self.subTest(profile=profile, selected=other), self.assertRaises(ValueError):
                    audit.validate_structure(manifest, profile=other)
                with self.subTest(profile=profile, cards=other), self.assertRaises(ValueError):
                    audit.validate_cards(manifest, self.root, profile=other)
        self.inspect(documents["dreadbow"], profile="dreadbow")
        self.inspect(documents["effects"], profile="effects")
        self.inspect()
        self.assertEqual(snapshots, (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE))

    def test_dreadbow_missing_extra_or_aliased_roster_rejected(self):
        for key in ("cards", "contract_evidence"):
            for mode in ("missing", "extra", "action_alias", "effect_alias"):
                doc = self.dreadbow_fixture()
                value = doc[key].pop("equipment/dreadbow.md")
                if mode == "extra":
                    doc[key]["equipment/dreadbow.md"] = value
                    doc[key]["equipment/extra.md"] = value
                elif mode == "action_alias":
                    doc[key][ACTIONS[0]] = value
                elif mode == "effect_alias":
                    doc[key]["effects/bubbled.md"] = value
                with self.subTest(key=key, mode=mode), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="dreadbow")

    def test_dreadbow_scope_and_evidence_family_tampering_rejected(self):
        for key, value in (("catalog_family", "MOB_EFFECTS"), ("catalog_family", None),
                           ("semantic_magic_roots", 2), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True)):
            doc = self.dreadbow_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="dreadbow")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.dreadbow_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="dreadbow")

    def test_dreadbow_card_count_does_not_weaken_other_profiles_class_minimum(self):
        for profile, manifest, evidence_key in (
                ("actions", self.doc, "action_evidence"),
                ("effects", self.effects_fixture(), "effect_evidence"),
                ("dreadbow", self.dreadbow_fixture(), "contract_evidence")):
            for mode in ("class_count", "anchored_class_count"):
                doc = copy.deepcopy(manifest)
                path = next(iter(doc["classes"]))
                if mode == "class_count":
                    doc["classes"].pop(path)
                    replacement = next(iter(doc["classes"]))
                    for record in doc[evidence_key].values():
                        record["classes"] = [replacement if item == path else item
                                             for item in record["classes"]]
                else:
                    doc["classes"][path]["methods"] = []
                with self.subTest(profile=profile, mode=mode), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile=profile)

    def test_dreadbow_profile_rechecks_card_seal_after_bytecode_inspection(self):
        doc = self.dreadbow_fixture()
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            if not changed:
                card = self.root / "damage-types/dark-arrow.md"
                card.write_bytes(card.read_bytes() + b"changed during dreadbow audit")
                changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="dreadbow",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_cli_accepts_explicit_dreadbow_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "dreadbow"]
        doc = self.dreadbow_fixture()
        with mock.patch.object(audit, "load_manifest", return_value=doc), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("dreadbow", inspect.call_args.kwargs["profile"])

    def test_missing_extra_action_and_card_evidence_mismatch_rejected(self):
        variants = []
        for key in ("cards", "action_evidence"):
            doc = copy.deepcopy(self.doc); doc[key].pop(ACTIONS[0]); variants.append(doc)
            doc = copy.deepcopy(self.doc); doc[key]["actions/extra.md"] = next(iter(doc[key].values())); variants.append(doc)
        for doc in variants:
            with self.subTest(keys=list(doc["cards"])), self.assertRaises(ValueError):
                audit.validate_structure(doc)

    def test_scope_source_identity_and_boolean_type_tampering_rejected(self):
        mutations = [("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                     ("provider_universe_closed", True), ("semantic_magic_roots", True),
                     ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                     ("version", "1.1.1"), ("schema_version", True), ("runtime_verified", True),
                     ("artifact_sha1", "a" * 40), ("artifact_sha256", "b" * 64),
                     ("artifact_size_bytes", True)]
        for key, value in mutations:
            doc = copy.deepcopy(self.doc); doc[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): audit.validate_structure(doc)
        for key, value in (("declared_version", "1.0.10"), ("role", "INSTALLED_PARAMETERS"),
                           ("revision", "main"), ("repository", "other/repo")):
            doc = copy.deepcopy(self.doc); doc["adjacent_source"][key] = value
            with self.subTest(source=key), self.assertRaises(ValueError): audit.validate_structure(doc)

    def test_duplicate_json_keys_rejected(self):
        path = Path(self.temp.name) / "duplicate.json"
        path.write_text('{"version":"1.0.10","version":"1.0.10"}', encoding="utf8")
        with self.assertRaises(ValueError): audit.load_manifest(path)

    def test_duplicate_unsafe_unreferenced_or_anchorless_paths_rejected(self):
        for mode in ("duplicate", "unsafe", "unreferenced", "anchorless", "missing_resource"):
            doc = copy.deepcopy(self.doc)
            if mode == "duplicate": doc["action_evidence"][ACTIONS[0]]["classes"] *= 2
            if mode == "unsafe": doc["resources"]["data/alexscaves/../bad.json"] = "a" * 64
            if mode == "unreferenced": doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            if mode == "anchorless": doc["classes"][next(iter(doc["classes"]))]["methods"] = []
            if mode == "missing_resource": doc["resources"].clear()
            with self.subTest(mode=mode), self.assertRaises(ValueError): audit.validate_structure(doc)

    def test_duplicate_method_or_anchor_and_boolean_offset_rejected(self):
        for mode in ("method", "anchor", "boolean_offset"):
            doc = copy.deepcopy(self.doc)
            methods = doc["classes"][next(iter(doc["classes"]))]["methods"]
            if mode == "method": methods.append(copy.deepcopy(methods[0]))
            elif mode == "anchor": methods[0]["anchors"] *= 2
            else: methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError): audit.validate_structure(doc)

    def test_support_class_may_be_hash_only_when_action_has_anchored_class(self):
        path = OWNER.replace(".", "/") + "Support.class"
        self.members[path] = b"\xca\xfe\xba\xbe\x00\x00\x00\x41"
        self.doc["classes"][path] = {"sha256": sha256(self.members[path]), "methods": []}
        self.doc["action_evidence"][ACTIONS[0]]["classes"].append(path)
        self.write_jar()
        self.assertEqual(9, self.inspect()["classes_checked"])

    def test_stale_card_or_symlink_escape_rejected(self):
        card = self.root / ACTIONS[0]
        card.write_text("stale doc", encoding="utf8")
        with self.assertRaises(ValueError): audit.validate_cards(self.doc, self.root)
        outside = Path(self.temp.name) / "outside.md"
        outside.write_bytes(card.read_bytes()); self.doc["cards"][ACTIONS[0]] = sha256(outside.read_bytes())
        card.unlink(); card.symlink_to(outside)
        with self.assertRaises(ValueError): audit.validate_cards(self.doc, self.root)

    def test_valid_synthetic_archive_and_read_only_javap_arguments(self):
        def completed(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed) as run:
            result = audit.audit(self.jar, self.doc, self.root, "synthetic-javap",
                                 expected_identity=self.expected_identity)
        self.assertIsInstance(result, dict)
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertNotIn("Compiled from", json.dumps(result))
        self.assertGreaterEqual(run.call_count, 8)
        for call in run.call_args_list:
            self.assertIsInstance(call.args[0], list)
            self.assertFalse(call.kwargs.get("shell", False))

    def test_default_validator_rejects_other_artifact_even_when_self_consistent(self):
        with self.assertRaises(ValueError): audit.audit(self.jar, self.doc, self.root, "unused")

    def test_duplicate_zip_member_rejected(self):
        self.write_jar([(self.resource, self.members[self.resource])])
        with self.assertRaises(ValueError): self.inspect()

    def test_javap_failure_is_not_a_successful_audit(self):
        failed = subprocess.CompletedProcess([], 1, stdout=JAVAP, stderr="synthetic failure")
        with mock.patch.object(audit.subprocess, "run", return_value=failed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, self.doc, self.root, "synthetic-javap",
                            expected_identity=self.expected_identity)

    def test_wrong_javap_owner_for_each_selected_class_rejected(self):
        for victim_path in self.doc["classes"]:
            victim = victim_path.removesuffix(".class").replace("/", ".")
            def completed(command, **kwargs):
                owner = "com.example.WrongOwner" if command[-1] == victim else command[-1]
                return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
            with self.subTest(owner=victim), mock.patch.object(audit.subprocess, "run", side_effect=completed) as run:
                with self.assertRaises(ValueError):
                    audit.audit(self.jar, self.doc, self.root, "synthetic-javap",
                                expected_identity=self.expected_identity)
                self.assertTrue(any(call.args[0][-1] == victim for call in run.call_args_list))

    def test_archive_mutation_during_javap_rejected_with_identity_sampled_once(self):
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            if not changed:
                self.jar.write_bytes(self.jar.read_bytes() + b"synthetic mutation during javap")
                changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        expected = mock.Mock(side_effect=self.expected_identity)
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, self.doc, self.root, "synthetic-javap", expected_identity=expected)
        self.assertTrue(changed)
        self.assertEqual(1, expected.call_count)

    def test_card_mutation_during_first_javap_rejected(self):
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            if not changed:
                card = self.root / ACTIONS[0]
                card.write_bytes(card.read_bytes() + b"modified during javap\n")
                changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, self.doc, self.root, "synthetic-javap",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_hash_and_classfile_version_or_magic_rejected(self):
        path = next(iter(self.doc["classes"]))
        for blob in (b"changed", b"\xca\xfe\xba\xbe\x00\x00\x00\x3d", b"BAD!\x00\x00\x00\x41"):
            with self.subTest(blob=blob):
                self.members[path] = blob; self.write_jar()
                with self.assertRaises(ValueError): self.inspect()
                doc = copy.deepcopy(self.doc); doc["classes"][path]["sha256"] = sha256(blob)
                with self.assertRaises(ValueError): self.inspect(doc)

    def test_resource_hash_and_method_abi_or_anchor_drift_rejected(self):
        for mode in ("resource", "class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = copy.deepcopy(self.doc)
            method = doc["classes"][next(iter(doc["classes"]))]["methods"][0]
            if mode == "resource": doc["resources"][self.resource] = "0" * 64
            elif mode == "class_hash": doc["classes"][next(iter(doc["classes"]))]["sha256"] = "0" * 64
            elif mode == "descriptor": method["descriptor"] = "(J)I"
            else: method["anchors"][0][mode] = {"offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError): self.inspect(doc)


if __name__ == "__main__":
    unittest.main()
