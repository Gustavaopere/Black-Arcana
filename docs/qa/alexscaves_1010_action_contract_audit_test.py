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

    def acid_fixture(self):
        """Seal exactly one damage card without borrowing the Dreadbow roster."""
        doc = copy.deepcopy(self.doc)
        relative = "damage-types/acid.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "ACID_DAMAGE_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc

    def desolate_dagger_fixture(self):
        """Seal the two literal dagger cards with independent member evidence."""
        doc = copy.deepcopy(self.doc)
        doc["catalog_family"] = "DESOLATE_DAGGER_CONTRACTS"
        doc["cards"], doc["contract_evidence"] = {}, {}
        selected_classes = {}
        for action, relative in zip(ACTIONS, sorted(audit.DESOLATE_DAGGER)):
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

    def forsaken_fixture(self):
        """Seal the existing damage card without inventing a new magic root."""
        doc = copy.deepcopy(self.doc)
        relative = "damage-types/forsaken-sonic-boom.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "FORSAKEN_SONIC_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc

    def gumball_fixture(self):
        """Seal the two literal Shot Gum and Gumball cards with independent member evidence."""
        doc = copy.deepcopy(self.doc)
        doc["catalog_family"] = "GUMBALL_CONTRACTS"
        doc["cards"], doc["contract_evidence"] = {}, {}
        selected_classes = {}
        for action, relative in zip(ACTIONS, sorted(audit.GUMBALL)):
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


    def nuclear_fixture(self):
        """Seal the two literal Intentional Game Design and Nuke cards with independent member evidence."""
        doc = copy.deepcopy(self.doc)
        doc["catalog_family"] = "NUCLEAR_DAMAGE_CONTRACTS"
        doc["cards"], doc["contract_evidence"] = {}, {}
        selected_classes = {}
        for action, relative in zip(ACTIONS, sorted(audit.NUCLEAR)):
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


    def spirit_dinosaur_fixture(self):
        """Seal one literal damage contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "damage-types/spirit-dinosaur.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "SPIRIT_DINOSAUR_DAMAGE_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc

    def heavy_slam_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/heavy-slam.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "HEAVY_SLAM_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc

    def herd_phalanx_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/herd-phalanx.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "HERD_PHALANX_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc

    def impending_stab_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/impending-stab.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "IMPENDING_STAB_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def lasting_morale_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/lasting-morale.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "LASTING_MORALE_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def multiple_mint_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/multiple-mint.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def relentless_darkness_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/relentless-darkness.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def sated_blade_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/sated-blade.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "SATED_BLADE_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def seapairing_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/seapairing.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "SEAPAIRING_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def shaded_respite_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/shaded-respite.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "SHADED_RESPITE_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def sharp_cane_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/sharp-cane.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "SHARP_CANE_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
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

    def test_acid_literal_roster_and_single_class_synthetic_audit(self):
        doc = self.acid_fixture()
        self.assertEqual({"damage-types/acid.md"}, set(audit.ACID))
        audit.validate_structure(doc, profile="acid")
        audit.validate_cards(doc, self.root, profile="acid")
        result = self.inspect(doc, profile="acid")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("ACID_DAMAGE_CONTRACT", result["catalog_family"])
        self.assertEqual(1, result["cards_checked"])
        self.assertEqual(1, result["classes_checked"])
        self.assertEqual(1, result["methods_checked"])
        self.assertEqual(8, result["semantic_magic_roots"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])

    def test_acid_is_isolated_from_all_previous_profiles_without_global_mutation(self):
        snapshots = tuple(copy.deepcopy(value) for value in
                          (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE, audit.ACID_SCOPE))
        documents = {"actions": self.doc, "effects": self.effects_fixture(),
                     "dreadbow": self.dreadbow_fixture(), "acid": self.acid_fixture()}
        for profile, manifest in documents.items():
            for other in documents:
                if profile == other:
                    continue
                with self.subTest(profile=profile, selected=other), self.assertRaises(ValueError):
                    audit.validate_structure(manifest, profile=other)
                with self.subTest(profile=profile, cards=other), self.assertRaises(ValueError):
                    audit.validate_cards(manifest, self.root, profile=other)
        self.inspect(documents["acid"], profile="acid")
        for profile in ("dreadbow", "effects", "actions"):
            self.inspect(documents[profile], profile=profile)
        self.assertEqual(snapshots,
                         (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE, audit.ACID_SCOPE))

    def test_acid_missing_extra_and_cross_family_alias_cards_rejected(self):
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/extra.md", "equipment/dreadbow.md",
                                "effects/bubbled.md", ACTIONS[0]):
                doc = self.acid_fixture()
                value = doc[key].pop("damage-types/acid.md")
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="acid")
            doc = self.acid_fixture()
            doc[key]["damage-types/extra.md"] = doc[key]["damage-types/acid.md"]
            with self.subTest(key=key, mode="extra"), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="acid")

    def test_acid_scope_and_evidence_family_tampering_rejected(self):
        for key, value in (("catalog_family", "DREADBOW_AND_DARK_ARROW"),
                           ("catalog_family", None), ("semantic_magic_roots", 1),
                           ("provider_universe_closed", True), ("mutating_hook", "VERIFIED"),
                           ("physical_qa", "PASS"), ("artifact_size_bytes", True)):
            doc = self.acid_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="acid")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.acid_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="acid")

    def test_acid_still_requires_one_class_with_an_instruction_anchor(self):
        for mode in ("no_class", "no_anchored_class"):
            doc = self.acid_fixture()
            if mode == "no_class":
                doc["classes"].clear()
                doc["contract_evidence"]["damage-types/acid.md"]["classes"].clear()
            else:
                next(iter(doc["classes"].values()))["methods"] = []
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="acid")

    def test_acid_profile_rejects_stale_card_or_symlink_escape(self):
        doc = self.acid_fixture()
        card = self.root / "damage-types/acid.md"
        original = card.read_bytes()
        card.write_bytes(original + b"stale acid contract")
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="acid")
        outside = Path(self.temp.name) / "outside-acid.md"
        outside.write_bytes(original)
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="acid")

    def test_acid_profile_rechecks_card_after_its_single_bytecode_inspection(self):
        doc = self.acid_fixture()
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            card = self.root / "damage-types/acid.md"
            card.write_bytes(card.read_bytes() + b"changed during acid audit")
            changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="acid",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_cli_accepts_explicit_acid_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "acid"]
        with mock.patch.object(audit, "load_manifest", return_value=self.acid_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("acid", inspect.call_args.kwargs["profile"])

    def test_desolate_dagger_literal_roster_and_two_class_synthetic_audit(self):
        doc = self.desolate_dagger_fixture()
        self.assertEqual({"equipment/desolate-dagger.md", "damage-types/desolate-dagger.md"},
                         set(audit.DESOLATE_DAGGER))
        audit.validate_structure(doc, profile="desolate_dagger")
        audit.validate_cards(doc, self.root, profile="desolate_dagger")
        result = self.inspect(doc, profile="desolate_dagger")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("DESOLATE_DAGGER_CONTRACTS", result["catalog_family"])
        self.assertEqual(2, result["cards_checked"])
        self.assertEqual(2, result["classes_checked"])
        self.assertEqual(2, result["methods_checked"])
        self.assertEqual(8, result["semantic_magic_roots"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])

    def test_desolate_dagger_is_isolated_from_four_previous_profiles(self):
        globals_ = (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE,
                    audit.ACID_SCOPE, audit.DESOLATE_DAGGER_SCOPE)
        snapshots = tuple(copy.deepcopy(value) for value in globals_)
        documents = {"actions": self.doc, "effects": self.effects_fixture(),
                     "dreadbow": self.dreadbow_fixture(), "acid": self.acid_fixture(),
                     "desolate_dagger": self.desolate_dagger_fixture()}
        for profile, manifest in documents.items():
            for other in documents:
                if profile == other:
                    continue
                with self.subTest(profile=profile, selected=other), self.assertRaises(ValueError):
                    audit.validate_structure(manifest, profile=other)
                with self.subTest(profile=profile, cards=other), self.assertRaises(ValueError):
                    audit.validate_cards(manifest, self.root, profile=other)
        for profile in ("desolate_dagger", "acid", "dreadbow", "effects", "actions"):
            self.inspect(documents[profile], profile=profile)
        self.assertEqual(snapshots, globals_)

    def test_desolate_dagger_missing_extra_and_cross_family_alias_cards_rejected(self):
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "equipment/extra.md", "equipment/dreadbow.md",
                                "damage-types/acid.md", "effects/bubbled.md", ACTIONS[0]):
                doc = self.desolate_dagger_fixture()
                value = doc[key].pop("equipment/desolate-dagger.md")
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="desolate_dagger")
            doc = self.desolate_dagger_fixture()
            doc[key]["equipment/extra.md"] = doc[key]["equipment/desolate-dagger.md"]
            with self.subTest(key=key, mode="extra"), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="desolate_dagger")

    def test_desolate_dagger_scope_and_evidence_family_tampering_rejected(self):
        for key, value in (("catalog_family", "ACID_DAMAGE_CONTRACT"), ("catalog_family", None),
                           ("semantic_magic_roots", 2), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True)):
            doc = self.desolate_dagger_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="desolate_dagger")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.desolate_dagger_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="desolate_dagger")

    def test_desolate_dagger_keeps_two_class_and_anchored_class_minima(self):
        for mode in ("missing_class", "anchorless_class"):
            doc = self.desolate_dagger_fixture()
            path = next(iter(doc["classes"]))
            if mode == "missing_class":
                doc["classes"].pop(path)
                replacement = next(iter(doc["classes"]))
                for record in doc["contract_evidence"].values():
                    record["classes"] = [replacement if item == path else item for item in record["classes"]]
            else:
                doc["classes"][path]["methods"] = []
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="desolate_dagger")

    def test_desolate_dagger_rejects_stale_card_and_symlink_escape(self):
        doc = self.desolate_dagger_fixture()
        card = self.root / "equipment/desolate-dagger.md"
        original = card.read_bytes()
        card.write_bytes(original + b"stale dagger card")
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="desolate_dagger")
        outside = Path(self.temp.name) / "outside-dagger.md"
        outside.write_bytes(original)
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="desolate_dagger")

    def test_desolate_dagger_rechecks_card_after_bytecode_inspection(self):
        doc = self.desolate_dagger_fixture()
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            if not changed:
                card = self.root / "damage-types/desolate-dagger.md"
                card.write_bytes(card.read_bytes() + b"changed during dagger audit")
                changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="desolate_dagger",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_cli_accepts_explicit_desolate_dagger_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "desolate_dagger"]
        with mock.patch.object(audit, "load_manifest", return_value=self.desolate_dagger_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("desolate_dagger", inspect.call_args.kwargs["profile"])

    def test_forsaken_single_card_audit_keeps_static_and_runtime_boundaries(self):
        doc = self.forsaken_fixture()
        self.assertEqual({"damage-types/forsaken-sonic-boom.md"}, set(audit.FORSAKEN))
        audit.validate_structure(doc, profile="forsaken")
        audit.validate_cards(doc, self.root, profile="forsaken")
        result = self.inspect(doc, profile="forsaken")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("FORSAKEN_SONIC_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1, 1), tuple(result[k] for k in
                         ("cards_checked", "classes_checked", "methods_checked", "instruction_anchors_checked")))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual(8, result["semantic_magic_roots"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])

    def test_forsaken_isolated_from_five_prior_families_without_global_mutation(self):
        globals_ = (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE,
                    audit.ACID_SCOPE, audit.DESOLATE_DAGGER_SCOPE, audit.FORSAKEN_SCOPE)
        snapshots = tuple(copy.deepcopy(value) for value in globals_)
        documents = {"actions": self.doc, "effects": self.effects_fixture(),
                     "dreadbow": self.dreadbow_fixture(), "acid": self.acid_fixture(),
                     "desolate_dagger": self.desolate_dagger_fixture(), "forsaken": self.forsaken_fixture()}
        for profile, doc in documents.items():
            for other in documents:
                if profile == other:
                    continue
                with self.subTest(profile=profile, selected=other), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile=other)
                with self.subTest(profile=profile, cards=other), self.assertRaises(ValueError):
                    audit.validate_cards(doc, self.root, profile=other)
        for profile in ("forsaken", "desolate_dagger", "acid", "dreadbow", "effects", "actions"):
            self.inspect(documents[profile], profile=profile)
        self.assertEqual(snapshots, globals_)

    def test_forsaken_rejects_missing_extra_or_aliased_card_and_evidence_rosters(self):
        relative = "damage-types/forsaken-sonic-boom.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/acid.md", "equipment/dreadbow.md",
                                "damage-types/forsaken-sonic-boom.md/../alias.md", ACTIONS[0]):
                doc = self.forsaken_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="forsaken")
            doc = self.forsaken_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, mode="extra"), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="forsaken")

    def test_forsaken_rejects_identity_runtime_and_evidence_family_inflation(self):
        mutations = (("catalog_family", "DESOLATE_DAGGER_CONTRACTS"), ("catalog_family", None),
                     ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                     ("artifact_sha1", "a" * 40), ("artifact_sha256", "b" * 64),
                     ("artifact_size_bytes", True), ("version", "1.1.1"),
                     ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                     ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"))
        for key, value in mutations:
            doc = self.forsaken_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="forsaken")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.forsaken_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="forsaken")

    def test_forsaken_rejects_stale_card_and_matching_hash_symlink_escape(self):
        doc = self.forsaken_fixture()
        card = self.root / "damage-types/forsaken-sonic-boom.md"
        original = card.read_bytes()
        card.write_bytes(original + b"stale Forsaken contract")
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="forsaken")
        outside = Path(self.temp.name) / "outside-forsaken.md"
        outside.write_bytes(original)
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="forsaken")

    def test_forsaken_rechecks_card_after_bytecode_inspection(self):
        doc = self.forsaken_fixture()
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            card = self.root / "damage-types/forsaken-sonic-boom.md"
            card.write_bytes(card.read_bytes() + b"changed during Forsaken audit")
            changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="forsaken",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_forsaken_still_requires_anchored_and_referenced_member_evidence(self):
        for mode in ("no_class", "no_anchored_class", "duplicate_class", "orphan_resource", "too_many_anchors"):
            doc = self.forsaken_fixture()
            path = next(iter(doc["classes"]))
            record = doc["contract_evidence"]["damage-types/forsaken-sonic-boom.md"]
            if mode == "no_class":
                doc["classes"].clear()
                record["classes"].clear()
            elif mode == "no_anchored_class":
                doc["classes"][path]["methods"] = []
            elif mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "orphan_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            else:
                doc["classes"][path]["methods"][0]["anchors"] = [
                    {"offset": i, "opcode": "nop", "operand": "", "symbol": ""} for i in range(257)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="forsaken")

    def test_forsaken_verifies_actual_artifact_resources_and_instruction_values(self):
        doc = self.forsaken_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="forsaken")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["opcode"] = "iconst_2"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="forsaken")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="forsaken")

    def test_cli_accepts_explicit_forsaken_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "forsaken"]
        with mock.patch.object(audit, "load_manifest", return_value=self.forsaken_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("forsaken", inspect.call_args.kwargs["profile"])

    def test_gumball_literal_roster_and_two_class_synthetic_audit(self):
        doc = self.gumball_fixture()
        self.assertEqual({"equipment/shot-gum.md", "damage-types/gumball.md"},
                         set(audit.GUMBALL))
        audit.validate_structure(doc, profile="gumball")
        audit.validate_cards(doc, self.root, profile="gumball")
        result = self.inspect(doc, profile="gumball")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("GUMBALL_CONTRACTS", result["catalog_family"])
        self.assertEqual(2, result["cards_checked"])
        self.assertEqual(2, result["classes_checked"])
        self.assertEqual(2, result["methods_checked"])
        self.assertEqual(8, result["semantic_magic_roots"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])

    def test_gumball_is_isolated_from_six_previous_profiles(self):
        globals_ = (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE,
                    audit.ACID_SCOPE, audit.DESOLATE_DAGGER_SCOPE, audit.FORSAKEN_SCOPE, audit.GUMBALL_SCOPE)
        snapshots = tuple(copy.deepcopy(value) for value in globals_)
        documents = {"actions": self.doc, "effects": self.effects_fixture(),
                     "dreadbow": self.dreadbow_fixture(), "acid": self.acid_fixture(),
                     "desolate_dagger": self.desolate_dagger_fixture(),
                     "forsaken": self.forsaken_fixture(), "gumball": self.gumball_fixture()}
        for profile, manifest in documents.items():
            for other in documents:
                if profile == other:
                    continue
                with self.subTest(profile=profile, selected=other), self.assertRaises(ValueError):
                    audit.validate_structure(manifest, profile=other)
                with self.subTest(profile=profile, cards=other), self.assertRaises(ValueError):
                    audit.validate_cards(manifest, self.root, profile=other)
        for profile in ("gumball", "forsaken", "desolate_dagger", "acid", "dreadbow", "effects", "actions"):
            self.inspect(documents[profile], profile=profile)
        self.assertEqual(snapshots, globals_)

    def test_gumball_missing_extra_and_cross_family_alias_cards_rejected(self):
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "equipment/extra.md", "equipment/dreadbow.md",
                                "damage-types/acid.md", "damage-types/forsaken-sonic-boom.md",
                                "equipment/desolate-dagger.md", "effects/bubbled.md", ACTIONS[0]):
                doc = self.gumball_fixture()
                value = doc[key].pop("equipment/shot-gum.md")
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="gumball")
            doc = self.gumball_fixture()
            doc[key]["equipment/extra.md"] = doc[key]["equipment/shot-gum.md"]
            with self.subTest(key=key, mode="extra"), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="gumball")

    def test_gumball_scope_and_evidence_family_tampering_rejected(self):
        for key, value in (("catalog_family", "ACID_DAMAGE_CONTRACT"), ("catalog_family", None),
                           ("semantic_magic_roots", 2), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1")):
            doc = self.gumball_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="gumball")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.gumball_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="gumball")

    def test_gumball_keeps_two_class_and_anchored_class_minima(self):
        for mode in ("missing_class", "anchorless_class"):
            doc = self.gumball_fixture()
            path = next(iter(doc["classes"]))
            if mode == "missing_class":
                doc["classes"].pop(path)
                replacement = next(iter(doc["classes"]))
                for record in doc["contract_evidence"].values():
                    record["classes"] = [replacement if item == path else item for item in record["classes"]]
            else:
                doc["classes"][path]["methods"] = []
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="gumball")

    def test_gumball_rejects_stale_card_and_symlink_escape(self):
        doc = self.gumball_fixture()
        card = self.root / "equipment/shot-gum.md"
        original = card.read_bytes()
        card.write_bytes(original + b"stale gumball card")
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="gumball")
        outside = Path(self.temp.name) / "outside-gumball.md"
        outside.write_bytes(original)
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="gumball")

    def test_gumball_rechecks_card_after_bytecode_inspection(self):
        doc = self.gumball_fixture()
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            if not changed:
                card = self.root / "damage-types/gumball.md"
                card.write_bytes(card.read_bytes() + b"changed during gumball audit")
                changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="gumball",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_cli_accepts_explicit_gumball_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "gumball"]
        with mock.patch.object(audit, "load_manifest", return_value=self.gumball_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("gumball", inspect.call_args.kwargs["profile"])

    def test_gumball_verifies_actual_artifact_resources_and_instruction_values(self):
        doc = self.gumball_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="gumball")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["opcode"] = "iconst_2"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="gumball")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="gumball")

    def test_nuclear_literal_roster_and_two_class_synthetic_audit(self):
        doc = self.nuclear_fixture()
        self.assertEqual({"damage-types/intentional-game-design.md", "damage-types/nuke.md"},
                         set(audit.NUCLEAR))
        audit.validate_structure(doc, profile="nuclear")
        audit.validate_cards(doc, self.root, profile="nuclear")
        result = self.inspect(doc, profile="nuclear")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("NUCLEAR_DAMAGE_CONTRACTS", result["catalog_family"])
        self.assertEqual(2, result["cards_checked"])
        self.assertEqual(2, result["classes_checked"])
        self.assertEqual(2, result["methods_checked"])
        self.assertEqual(8, result["semantic_magic_roots"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])

    def test_nuclear_is_isolated_from_seven_previous_profiles(self):
        globals_ = (audit.SCOPE, audit.EFFECT_SCOPE, audit.DREADBOW_SCOPE,
                    audit.ACID_SCOPE, audit.DESOLATE_DAGGER_SCOPE, audit.FORSAKEN_SCOPE, audit.GUMBALL_SCOPE, audit.NUCLEAR_SCOPE)
        snapshots = tuple(copy.deepcopy(value) for value in globals_)
        documents = {"actions": self.doc, "effects": self.effects_fixture(),
                     "dreadbow": self.dreadbow_fixture(), "acid": self.acid_fixture(),
                     "desolate_dagger": self.desolate_dagger_fixture(),
                     "forsaken": self.forsaken_fixture(), "gumball": self.gumball_fixture(),
                     "nuclear": self.nuclear_fixture()}
        for profile, manifest in documents.items():
            for other in documents:
                if profile == other:
                    continue
                with self.subTest(profile=profile, selected=other), self.assertRaises(ValueError):
                    audit.validate_structure(manifest, profile=other)
                with self.subTest(profile=profile, cards=other), self.assertRaises(ValueError):
                    audit.validate_cards(manifest, self.root, profile=other)
        for profile in ("nuclear", "gumball", "forsaken", "desolate_dagger", "acid", "dreadbow", "effects", "actions"):
            self.inspect(documents[profile], profile=profile)
        self.assertEqual(snapshots, globals_)

    def test_nuclear_missing_extra_and_cross_family_alias_cards_rejected(self):
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "equipment/extra.md", "equipment/dreadbow.md",
                                "damage-types/acid.md", "damage-types/forsaken-sonic-boom.md",
                                "equipment/desolate-dagger.md", "effects/bubbled.md", ACTIONS[0]):
                doc = self.nuclear_fixture()
                value = doc[key].pop("damage-types/intentional-game-design.md")
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="nuclear")
            doc = self.nuclear_fixture()
            doc[key]["equipment/extra.md"] = doc[key]["damage-types/intentional-game-design.md"]
            with self.subTest(key=key, mode="extra"), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="nuclear")

    def test_nuclear_scope_and_evidence_family_tampering_rejected(self):
        for key, value in (("catalog_family", "ACID_DAMAGE_CONTRACT"), ("catalog_family", None),
                           ("semantic_magic_roots", 2), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1")):
            doc = self.nuclear_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="nuclear")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.nuclear_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="nuclear")

    def test_nuclear_keeps_two_class_and_anchored_class_minima(self):
        for mode in ("missing_class", "anchorless_class"):
            doc = self.nuclear_fixture()
            path = next(iter(doc["classes"]))
            if mode == "missing_class":
                doc["classes"].pop(path)
                replacement = next(iter(doc["classes"]))
                for record in doc["contract_evidence"].values():
                    record["classes"] = [replacement if item == path else item for item in record["classes"]]
            else:
                doc["classes"][path]["methods"] = []
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="nuclear")

    def test_nuclear_rejects_stale_card_and_symlink_escape(self):
        doc = self.nuclear_fixture()
        card = self.root / "damage-types/intentional-game-design.md"
        original = card.read_bytes()
        card.write_bytes(original + b"stale nuclear card")
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="nuclear")
        outside = Path(self.temp.name) / "outside-nuclear.md"
        outside.write_bytes(original)
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.inspect(doc, profile="nuclear")

    def test_nuclear_rechecks_card_after_bytecode_inspection(self):
        doc = self.nuclear_fixture()
        changed = False
        def completed(command, **kwargs):
            nonlocal changed
            if not changed:
                card = self.root / "damage-types/nuke.md"
                card.write_bytes(card.read_bytes() + b"changed during nuclear audit")
                changed = True
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaises(ValueError):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="nuclear",
                            expected_identity=self.expected_identity)
        self.assertTrue(changed)

    def test_cli_accepts_explicit_nuclear_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "nuclear"]
        with mock.patch.object(audit, "load_manifest", return_value=self.nuclear_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("nuclear", inspect.call_args.kwargs["profile"])

    def test_nuclear_verifies_actual_artifact_resources_and_instruction_values(self):
        doc = self.nuclear_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="nuclear")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["opcode"] = "iconst_2"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="nuclear")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="nuclear")

    def test_spirit_dinosaur_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.spirit_dinosaur_fixture()
        self.assertEqual({"damage-types/spirit-dinosaur.md"}, set(audit.SPIRIT_DINOSAUR))
        audit.validate_structure(doc, profile="spirit_dinosaur")
        audit.validate_cards(doc, self.root, profile="spirit_dinosaur")
        result = self.inspect(doc, profile="spirit_dinosaur")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("SPIRIT_DINOSAUR_DAMAGE_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_spirit_dinosaur_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear")}
        snapshots = copy.deepcopy(previous)
        doc = self.spirit_dinosaur_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="spirit_dinosaur")
        self.inspect(doc, profile="spirit_dinosaur")
        self.assertEqual(snapshots, previous)

    def test_spirit_dinosaur_rejects_missing_extra_and_aliased_roster(self):
        relative = "damage-types/spirit-dinosaur.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md", ACTIONS[0]):
                doc = self.spirit_dinosaur_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="spirit_dinosaur")
            doc = self.spirit_dinosaur_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="spirit_dinosaur")

    def test_spirit_dinosaur_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "NUCLEAR_DAMAGE_CONTRACTS"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1")):
            doc = self.spirit_dinosaur_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="spirit_dinosaur")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.spirit_dinosaur_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="spirit_dinosaur")

    def test_spirit_dinosaur_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.spirit_dinosaur_fixture()
        relative = "damage-types/spirit-dinosaur.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="spirit_dinosaur")
        doc = self.spirit_dinosaur_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-spirit.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="spirit_dinosaur")

    def test_spirit_dinosaur_rechecks_card_after_bytecode_inspection(self):
        doc = self.spirit_dinosaur_fixture()
        def completed(command, **kwargs):
            card = self.root / "damage-types/spirit-dinosaur.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="spirit_dinosaur",
                            expected_identity=self.expected_identity)

    def test_spirit_dinosaur_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.spirit_dinosaur_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="spirit_dinosaur")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="spirit_dinosaur")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="spirit_dinosaur")

    def test_spirit_dinosaur_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_anchors"):
            doc = self.spirit_dinosaur_fixture()
            path = next(iter(doc["classes"]))
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                doc["classes"][path]["methods"] = []
            else:
                anchor = doc["classes"][path]["methods"][0]["anchors"][0]
                doc["classes"][path]["methods"][0]["anchors"] = [
                    {**anchor, "offset": offset} for offset in range(257)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="spirit_dinosaur")

    def test_cli_accepts_explicit_spirit_dinosaur_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "manifest.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "spirit_dinosaur"]
        with mock.patch.object(audit, "load_manifest", return_value=self.spirit_dinosaur_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("spirit_dinosaur", inspect.call_args.kwargs["profile"])

    def test_heavy_slam_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.heavy_slam_fixture()
        self.assertEqual({"enchantments/heavy-slam.md"}, set(audit.HEAVY_SLAM))
        audit.validate_structure(doc, profile="heavy_slam")
        audit.validate_cards(doc, self.root, profile="heavy_slam")
        result = self.inspect(doc, profile="heavy_slam")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("HEAVY_SLAM_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_heavy_slam_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur")}
        snapshots = copy.deepcopy(previous)
        doc = self.heavy_slam_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="heavy_slam")
        self.inspect(doc, profile="heavy_slam")
        self.assertEqual(snapshots, previous)

    def test_heavy_slam_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/heavy-slam.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/heavy_slam.md", "enchantments/triple-strike.md",
                                "enchantments/../enchantments/heavy-slam.md", ACTIONS[0]):
                doc = self.heavy_slam_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="heavy_slam")
            doc = self.heavy_slam_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="heavy_slam")

    def test_heavy_slam_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "SPIRIT_DINOSAUR_DAMAGE_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1")):
            doc = self.heavy_slam_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="heavy_slam")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.heavy_slam_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="heavy_slam")

    def test_heavy_slam_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.heavy_slam_fixture()
        relative = "enchantments/heavy-slam.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="heavy_slam")
        doc = self.heavy_slam_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-heavy-slam.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="heavy_slam")

    def test_heavy_slam_rechecks_card_after_bytecode_inspection(self):
        doc = self.heavy_slam_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/heavy-slam.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="heavy_slam",
                            expected_identity=self.expected_identity)

    def test_heavy_slam_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.heavy_slam_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="heavy_slam")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="heavy_slam")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="heavy_slam")

    def test_heavy_slam_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/heavy-slam.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_resource", "duplicate_method", "boolean_offset"):
            doc = self.heavy_slam_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="heavy_slam")

    def test_heavy_slam_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.heavy_slam_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="heavy_slam")

    def test_cli_accepts_explicit_heavy_slam_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-HEAVY-SLAM-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "heavy_slam"]
        with mock.patch.object(audit, "load_manifest", return_value=self.heavy_slam_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("heavy_slam", inspect.call_args.kwargs["profile"])

    def test_herd_phalanx_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.herd_phalanx_fixture()
        self.assertEqual({"enchantments/herd-phalanx.md"}, set(audit.HERD_PHALANX))
        audit.validate_structure(doc, profile="herd_phalanx")
        audit.validate_cards(doc, self.root, profile="herd_phalanx")
        result = self.inspect(doc, profile="herd_phalanx")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("HERD_PHALANX_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_herd_phalanx_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam")}
        snapshots = copy.deepcopy(previous)
        doc = self.herd_phalanx_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="herd_phalanx")
        self.inspect(doc, profile="herd_phalanx")
        self.assertEqual(snapshots, previous)

    def test_herd_phalanx_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/herd-phalanx.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/herd_phalanx.md", "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/../enchantments/herd-phalanx.md", ACTIONS[0]):
                doc = self.herd_phalanx_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="herd_phalanx")
            doc = self.herd_phalanx_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="herd_phalanx")

    def test_herd_phalanx_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1")):
            doc = self.herd_phalanx_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="herd_phalanx")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.herd_phalanx_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="herd_phalanx")

    def test_herd_phalanx_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.herd_phalanx_fixture()
        relative = "enchantments/herd-phalanx.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="herd_phalanx")
        doc = self.herd_phalanx_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-herd-phalanx.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="herd_phalanx")

    def test_herd_phalanx_rechecks_card_after_bytecode_inspection(self):
        doc = self.herd_phalanx_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/herd-phalanx.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="herd_phalanx",
                            expected_identity=self.expected_identity)

    def test_herd_phalanx_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.herd_phalanx_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="herd_phalanx")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="herd_phalanx")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="herd_phalanx")

    def test_herd_phalanx_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/herd-phalanx.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.herd_phalanx_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="herd_phalanx")

    def test_herd_phalanx_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.herd_phalanx_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="herd_phalanx")

    def test_cli_accepts_explicit_herd_phalanx_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-HERD-PHALANX-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "herd_phalanx"]
        with mock.patch.object(audit, "load_manifest", return_value=self.herd_phalanx_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("herd_phalanx", inspect.call_args.kwargs["profile"])

    def test_impending_stab_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.impending_stab_fixture()
        self.assertEqual({"enchantments/impending-stab.md"}, set(audit.IMPENDING_STAB))
        audit.validate_structure(doc, profile="impending_stab")
        audit.validate_cards(doc, self.root, profile="impending_stab")
        result = self.inspect(doc, profile="impending_stab")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("IMPENDING_STAB_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_impending_stab_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx")}
        snapshots = copy.deepcopy(previous)
        doc = self.impending_stab_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="impending_stab")
        self.inspect(doc, profile="impending_stab")
        self.assertEqual(snapshots, previous)

    def test_impending_stab_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/impending-stab.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/impending_stab.md", "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/impending-stab.md", ACTIONS[0]):
                doc = self.impending_stab_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="impending_stab")
            doc = self.impending_stab_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="impending_stab")

    def test_impending_stab_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1")):
            doc = self.impending_stab_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="impending_stab")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.impending_stab_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="impending_stab")

    def test_impending_stab_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.impending_stab_fixture()
        relative = "enchantments/impending-stab.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="impending_stab")
        doc = self.impending_stab_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-impending-stab.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="impending_stab")

    def test_impending_stab_rechecks_card_after_bytecode_inspection(self):
        doc = self.impending_stab_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/impending-stab.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="impending_stab",
                            expected_identity=self.expected_identity)

    def test_impending_stab_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.impending_stab_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="impending_stab")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="impending_stab")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="impending_stab")

    def test_impending_stab_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/impending-stab.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.impending_stab_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="impending_stab")

    def test_impending_stab_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.impending_stab_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="impending_stab")

    def test_cli_accepts_explicit_impending_stab_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-IMPENDING-STAB-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "impending_stab"]
        with mock.patch.object(audit, "load_manifest", return_value=self.impending_stab_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("impending_stab", inspect.call_args.kwargs["profile"])


    def test_lasting_morale_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.lasting_morale_fixture()
        self.assertEqual({"enchantments/lasting-morale.md"}, set(audit.LASTING_MORALE))
        audit.validate_structure(doc, profile="lasting_morale")
        audit.validate_cards(doc, self.root, profile="lasting_morale")
        result = self.inspect(doc, profile="lasting_morale")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("LASTING_MORALE_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_lasting_morale_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab")}
        snapshots = copy.deepcopy(previous)
        doc = self.lasting_morale_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="lasting_morale")
        self.inspect(doc, profile="lasting_morale")
        self.assertEqual(snapshots, previous)

    def test_lasting_morale_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/lasting-morale.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/lasting_morale.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/lasting-morale.md", ACTIONS[0]):
                doc = self.lasting_morale_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="lasting_morale")
            doc = self.lasting_morale_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="lasting_morale")

    def test_lasting_morale_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.lasting_morale_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="lasting_morale")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.lasting_morale_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="lasting_morale")

    def test_lasting_morale_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.lasting_morale_fixture()
        relative = "enchantments/lasting-morale.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="lasting_morale")
        doc = self.lasting_morale_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-lasting-morale.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="lasting_morale")

    def test_lasting_morale_rechecks_card_after_bytecode_inspection(self):
        doc = self.lasting_morale_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/lasting-morale.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="lasting_morale",
                            expected_identity=self.expected_identity)

    def test_lasting_morale_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.lasting_morale_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="lasting_morale")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="lasting_morale")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="lasting_morale")

    def test_lasting_morale_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.lasting_morale_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="lasting_morale")

    def test_lasting_morale_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.lasting_morale_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="lasting_morale",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_lasting_morale_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/lasting-morale.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.lasting_morale_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="lasting_morale")

    def test_lasting_morale_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.lasting_morale_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="lasting_morale")

    def test_cli_accepts_explicit_lasting_morale_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-LASTING-MORALE-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "lasting_morale"]
        with mock.patch.object(audit, "load_manifest", return_value=self.lasting_morale_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("lasting_morale", inspect.call_args.kwargs["profile"])


    def test_multiple_mint_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.multiple_mint_fixture()
        self.assertEqual({"enchantments/multiple-mint.md"}, set(audit.MULTIPLE_MINT))
        audit.validate_structure(doc, profile="multiple_mint")
        audit.validate_cards(doc, self.root, profile="multiple_mint")
        result = self.inspect(doc, profile="multiple_mint")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("MULTIPLE_MINT_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_multiple_mint_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale")}
        snapshots = copy.deepcopy(previous)
        doc = self.multiple_mint_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="multiple_mint")
        self.inspect(doc, profile="multiple_mint")
        self.assertEqual(snapshots, previous)

    def test_multiple_mint_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/multiple-mint.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/multiple_mint.md", "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/multiple-mint.md", ACTIONS[0]):
                doc = self.multiple_mint_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="multiple_mint")
            doc = self.multiple_mint_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="multiple_mint")

    def test_multiple_mint_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.multiple_mint_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="multiple_mint")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.multiple_mint_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="multiple_mint")

    def test_multiple_mint_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.multiple_mint_fixture()
        relative = "enchantments/multiple-mint.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="multiple_mint")
        doc = self.multiple_mint_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-multiple-mint.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="multiple_mint")

    def test_multiple_mint_rechecks_card_after_bytecode_inspection(self):
        doc = self.multiple_mint_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/multiple-mint.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="multiple_mint",
                            expected_identity=self.expected_identity)

    def test_multiple_mint_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.multiple_mint_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="multiple_mint")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="multiple_mint")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="multiple_mint")

    def test_multiple_mint_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.multiple_mint_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="multiple_mint")

    def test_multiple_mint_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.multiple_mint_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="multiple_mint",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_multiple_mint_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/multiple-mint.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.multiple_mint_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="multiple_mint")

    def test_multiple_mint_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.multiple_mint_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="multiple_mint")

    def test_cli_accepts_explicit_multiple_mint_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "multiple_mint"]
        with mock.patch.object(audit, "load_manifest", return_value=self.multiple_mint_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("multiple_mint", inspect.call_args.kwargs["profile"])


    def test_relentless_darkness_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.relentless_darkness_fixture()
        self.assertEqual({"enchantments/relentless-darkness.md"}, set(audit.RELENTLESS_DARKNESS))
        audit.validate_structure(doc, profile="relentless_darkness")
        audit.validate_cards(doc, self.root, profile="relentless_darkness")
        result = self.inspect(doc, profile="relentless_darkness")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_relentless_darkness_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint")}
        snapshots = copy.deepcopy(previous)
        doc = self.relentless_darkness_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="relentless_darkness")
        self.inspect(doc, profile="relentless_darkness")
        self.assertEqual(snapshots, previous)

    def test_relentless_darkness_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/relentless-darkness.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/relentless_darkness.md", "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/relentless-darkness.md", ACTIONS[0]):
                doc = self.relentless_darkness_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="relentless_darkness")
            doc = self.relentless_darkness_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="relentless_darkness")

    def test_relentless_darkness_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.relentless_darkness_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="relentless_darkness")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.relentless_darkness_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="relentless_darkness")

    def test_relentless_darkness_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.relentless_darkness_fixture()
        relative = "enchantments/relentless-darkness.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="relentless_darkness")
        doc = self.relentless_darkness_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-relentless-darkness.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="relentless_darkness")

    def test_relentless_darkness_rechecks_card_after_bytecode_inspection(self):
        doc = self.relentless_darkness_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/relentless-darkness.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="relentless_darkness",
                            expected_identity=self.expected_identity)

    def test_relentless_darkness_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.relentless_darkness_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="relentless_darkness")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="relentless_darkness")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="relentless_darkness")

    def test_relentless_darkness_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.relentless_darkness_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="relentless_darkness")

    def test_relentless_darkness_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.relentless_darkness_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="relentless_darkness",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_relentless_darkness_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/relentless-darkness.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.relentless_darkness_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="relentless_darkness")

    def test_relentless_darkness_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.relentless_darkness_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="relentless_darkness")

    def test_cli_accepts_explicit_relentless_darkness_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "relentless_darkness"]
        with mock.patch.object(audit, "load_manifest", return_value=self.relentless_darkness_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("relentless_darkness", inspect.call_args.kwargs["profile"])


    def test_sated_blade_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.sated_blade_fixture()
        self.assertEqual({"enchantments/sated-blade.md"}, set(audit.SATED_BLADE))
        audit.validate_structure(doc, profile="sated_blade")
        audit.validate_cards(doc, self.root, profile="sated_blade")
        result = self.inspect(doc, profile="sated_blade")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("SATED_BLADE_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_sated_blade_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness")}
        snapshots = copy.deepcopy(previous)
        doc = self.sated_blade_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="sated_blade")
        self.inspect(doc, profile="sated_blade")
        self.assertEqual(snapshots, previous)

    def test_sated_blade_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/sated-blade.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/sated_blade.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/sated-blade.md", ACTIONS[0]):
                doc = self.sated_blade_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="sated_blade")
            doc = self.sated_blade_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sated_blade")

    def test_sated_blade_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.sated_blade_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sated_blade")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.sated_blade_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sated_blade")

    def test_sated_blade_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.sated_blade_fixture()
        relative = "enchantments/sated-blade.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="sated_blade")
        doc = self.sated_blade_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-sated-blade.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="sated_blade")

    def test_sated_blade_rechecks_card_after_bytecode_inspection(self):
        doc = self.sated_blade_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/sated-blade.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="sated_blade",
                            expected_identity=self.expected_identity)

    def test_sated_blade_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.sated_blade_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="sated_blade")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="sated_blade")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="sated_blade")

    def test_sated_blade_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.sated_blade_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="sated_blade")

    def test_sated_blade_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.sated_blade_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="sated_blade",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_sated_blade_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/sated-blade.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.sated_blade_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sated_blade")

    def test_sated_blade_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.sated_blade_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sated_blade")

    def test_cli_accepts_explicit_sated_blade_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-SATED-BLADE-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "sated_blade"]
        with mock.patch.object(audit, "load_manifest", return_value=self.sated_blade_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("sated_blade", inspect.call_args.kwargs["profile"])


    def test_seapairing_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.seapairing_fixture()
        self.assertEqual({"enchantments/seapairing.md"}, set(audit.SEAPAIRING))
        audit.validate_structure(doc, profile="seapairing")
        audit.validate_cards(doc, self.root, profile="seapairing")
        result = self.inspect(doc, profile="seapairing")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("SEAPAIRING_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_seapairing_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade")}
        snapshots = copy.deepcopy(previous)
        doc = self.seapairing_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="seapairing")
        self.inspect(doc, profile="seapairing")
        self.assertEqual(snapshots, previous)

    def test_seapairing_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/seapairing.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/sea-pairing.md", "enchantments/sated-blade.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/seapairing.md", ACTIONS[0]):
                doc = self.seapairing_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="seapairing")
            doc = self.seapairing_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="seapairing")

    def test_seapairing_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.seapairing_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="seapairing")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.seapairing_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="seapairing")

    def test_seapairing_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.seapairing_fixture()
        relative = "enchantments/seapairing.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="seapairing")
        doc = self.seapairing_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-seapairing.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="seapairing")

    def test_seapairing_rechecks_card_after_bytecode_inspection(self):
        doc = self.seapairing_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/seapairing.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="seapairing",
                            expected_identity=self.expected_identity)

    def test_seapairing_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.seapairing_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="seapairing")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="seapairing")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="seapairing")

    def test_seapairing_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.seapairing_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="seapairing")

    def test_seapairing_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.seapairing_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="seapairing",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_seapairing_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/seapairing.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.seapairing_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="seapairing")

    def test_seapairing_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.seapairing_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="seapairing")

    def test_cli_accepts_explicit_seapairing_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-SEAPAIRING-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "seapairing"]
        with mock.patch.object(audit, "load_manifest", return_value=self.seapairing_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("seapairing", inspect.call_args.kwargs["profile"])


    def test_shaded_respite_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.shaded_respite_fixture()
        self.assertEqual({"enchantments/shaded-respite.md"}, set(audit.SHADED_RESPITE))
        audit.validate_structure(doc, profile="shaded_respite")
        audit.validate_cards(doc, self.root, profile="shaded_respite")
        result = self.inspect(doc, profile="shaded_respite")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("SHADED_RESPITE_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_shaded_respite_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade", "seapairing")}
        snapshots = copy.deepcopy(previous)
        doc = self.shaded_respite_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture(), self.seapairing_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="shaded_respite")
        self.inspect(doc, profile="shaded_respite")
        self.assertEqual(snapshots, previous)

    def test_shaded_respite_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/shaded-respite.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/shaded_respite.md", "enchantments/sated-blade.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/shaded-respite.md", ACTIONS[0]):
                doc = self.shaded_respite_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="shaded_respite")
            doc = self.shaded_respite_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="shaded_respite")

    def test_shaded_respite_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.shaded_respite_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="shaded_respite")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.shaded_respite_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="shaded_respite")

    def test_shaded_respite_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.shaded_respite_fixture()
        relative = "enchantments/shaded-respite.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="shaded_respite")
        doc = self.shaded_respite_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-shaded_respite.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="shaded_respite")

    def test_shaded_respite_rechecks_card_after_bytecode_inspection(self):
        doc = self.shaded_respite_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/shaded-respite.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="shaded_respite",
                            expected_identity=self.expected_identity)

    def test_shaded_respite_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.shaded_respite_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="shaded_respite")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="shaded_respite")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="shaded_respite")

    def test_shaded_respite_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.shaded_respite_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="shaded_respite")

    def test_shaded_respite_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.shaded_respite_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="shaded_respite",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_shaded_respite_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/shaded-respite.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.shaded_respite_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="shaded_respite")

    def test_shaded_respite_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.shaded_respite_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="shaded_respite")

    def test_cli_accepts_explicit_shaded_respite_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-SHADED-RESPITE-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "shaded_respite"]
        with mock.patch.object(audit, "load_manifest", return_value=self.shaded_respite_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("shaded_respite", inspect.call_args.kwargs["profile"])


    def test_sharp_cane_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.sharp_cane_fixture()
        self.assertEqual({"enchantments/sharp-cane.md"}, set(audit.SHARP_CANE))
        audit.validate_structure(doc, profile="sharp_cane")
        audit.validate_cards(doc, self.root, profile="sharp_cane")
        result = self.inspect(doc, profile="sharp_cane")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("SHARP_CANE_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_sharp_cane_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade", "seapairing", "shaded_respite")}
        snapshots = copy.deepcopy(previous)
        doc = self.sharp_cane_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture(), self.seapairing_fixture(), self.shaded_respite_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="sharp_cane")
        self.inspect(doc, profile="sharp_cane")
        self.assertEqual(snapshots, previous)

    def test_sharp_cane_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/sharp-cane.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/sharp_cane.md", "enchantments/sated-blade.md",
                                "enchantments/seapairing.md", "enchantments/shaded-respite.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/sharp-cane.md", ACTIONS[0]):
                doc = self.sharp_cane_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="sharp_cane")
            doc = self.sharp_cane_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sharp_cane")

    def test_sharp_cane_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SEAPAIRING_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHADED_RESPITE_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.sharp_cane_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sharp_cane")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.sharp_cane_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sharp_cane")

    def test_sharp_cane_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.sharp_cane_fixture()
        relative = "enchantments/sharp-cane.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="sharp_cane")
        doc = self.sharp_cane_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-sharp_cane.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="sharp_cane")

    def test_sharp_cane_rechecks_card_after_bytecode_inspection(self):
        doc = self.sharp_cane_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/sharp-cane.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="sharp_cane",
                            expected_identity=self.expected_identity)

    def test_sharp_cane_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.sharp_cane_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="sharp_cane")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="sharp_cane")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="sharp_cane")

    def test_sharp_cane_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.sharp_cane_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="sharp_cane")

    def test_sharp_cane_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.sharp_cane_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="sharp_cane",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_sharp_cane_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/sharp-cane.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.sharp_cane_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sharp_cane")

    def test_sharp_cane_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.sharp_cane_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="sharp_cane")

    def test_cli_accepts_explicit_sharp_cane_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-SHARP-CANE-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "sharp_cane"]
        with mock.patch.object(audit, "load_manifest", return_value=self.sharp_cane_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("sharp_cane", inspect.call_args.kwargs["profile"])


    def triple_splash_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/triple-splash.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "TRIPLE_SPLASH_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def test_triple_splash_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.triple_splash_fixture()
        self.assertEqual({"enchantments/triple-splash.md"}, set(audit.TRIPLE_SPLASH))
        audit.validate_structure(doc, profile="triple_splash")
        audit.validate_cards(doc, self.root, profile="triple_splash")
        result = self.inspect(doc, profile="triple_splash")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("TRIPLE_SPLASH_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_triple_splash_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade", "seapairing", "shaded_respite", "sharp_cane")}
        snapshots = copy.deepcopy(previous)
        doc = self.triple_splash_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture(), self.seapairing_fixture(), self.shaded_respite_fixture(), self.sharp_cane_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="triple_splash")
        self.inspect(doc, profile="triple_splash")
        self.assertEqual(snapshots, previous)

    def test_triple_splash_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/triple-splash.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/triple_splash.md", "enchantments/sated-blade.md",
                                "enchantments/seapairing.md", "enchantments/shaded-respite.md",
                                "enchantments/sharp-cane.md", "enchantments/soak-seeking.md",
                                "enchantments/sightless.md", "enchantments/triple-split.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/triple-splash.md", ACTIONS[0]):
                doc = self.triple_splash_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="triple_splash")
            doc = self.triple_splash_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_splash")

    def test_triple_splash_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SEAPAIRING_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHADED_RESPITE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHARP_CANE_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.triple_splash_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_splash")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.triple_splash_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_splash")

    def test_triple_splash_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.triple_splash_fixture()
        relative = "enchantments/triple-splash.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="triple_splash")
        doc = self.triple_splash_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-triple_splash.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="triple_splash")

    def test_triple_splash_rechecks_card_after_bytecode_inspection(self):
        doc = self.triple_splash_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/triple-splash.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="triple_splash",
                            expected_identity=self.expected_identity)

    def test_triple_splash_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.triple_splash_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="triple_splash")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="triple_splash")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="triple_splash")

    def test_triple_splash_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.triple_splash_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="triple_splash")

    def test_triple_splash_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.triple_splash_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="triple_splash",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_triple_splash_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/triple-splash.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.triple_splash_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_splash")

    def test_triple_splash_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.triple_splash_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_splash")

    def test_cli_accepts_explicit_triple_splash_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-SHARP-CANE-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "triple_splash"]
        with mock.patch.object(audit, "load_manifest", return_value=self.triple_splash_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("triple_splash", inspect.call_args.kwargs["profile"])


    def triple_split_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/triple-split.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "TRIPLE_SPLIT_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def test_triple_split_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.triple_split_fixture()
        self.assertEqual({"enchantments/triple-split.md"}, set(audit.TRIPLE_SPLIT))
        audit.validate_structure(doc, profile="triple_split")
        audit.validate_cards(doc, self.root, profile="triple_split")
        result = self.inspect(doc, profile="triple_split")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("TRIPLE_SPLIT_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_triple_split_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade", "seapairing", "shaded_respite", "sharp_cane", "triple_splash")}
        snapshots = copy.deepcopy(previous)
        doc = self.triple_split_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture(), self.seapairing_fixture(), self.shaded_respite_fixture(), self.sharp_cane_fixture(),
                    self.triple_splash_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="triple_split")
        self.inspect(doc, profile="triple_split")
        self.assertEqual(snapshots, previous)

    def test_triple_split_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/triple-split.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/triple_split.md", "enchantments/sated-blade.md",
                                "enchantments/seapairing.md", "enchantments/shaded-respite.md",
                                "enchantments/sharp-cane.md", "enchantments/soak-seeking.md",
                                "enchantments/sightless.md", "enchantments/triple-splash.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/triple-split.md", ACTIONS[0]):
                doc = self.triple_split_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="triple_split")
            doc = self.triple_split_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_split")

    def test_triple_split_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SEAPAIRING_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHADED_RESPITE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHARP_CANE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TRIPLE_SPLASH_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.triple_split_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_split")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.triple_split_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_split")

    def test_triple_split_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.triple_split_fixture()
        relative = "enchantments/triple-split.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="triple_split")
        doc = self.triple_split_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-triple_split.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="triple_split")

    def test_triple_split_rechecks_card_after_bytecode_inspection(self):
        doc = self.triple_split_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/triple-split.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="triple_split",
                            expected_identity=self.expected_identity)

    def test_triple_split_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.triple_split_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="triple_split")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="triple_split")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="triple_split")

    def test_triple_split_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.triple_split_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="triple_split")

    def test_triple_split_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.triple_split_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="triple_split",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_triple_split_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/triple-split.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.triple_split_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_split")

    def test_triple_split_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.triple_split_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="triple_split")

    def test_cli_accepts_explicit_triple_split_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "triple_split"]
        with mock.patch.object(audit, "load_manifest", return_value=self.triple_split_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("triple_split", inspect.call_args.kwargs["profile"])


    def tsunami_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/tsunami.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "TSUNAMI_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def test_tsunami_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.tsunami_fixture()
        self.assertEqual({"enchantments/tsunami.md"}, set(audit.TSUNAMI))
        audit.validate_structure(doc, profile="tsunami")
        audit.validate_cards(doc, self.root, profile="tsunami")
        result = self.inspect(doc, profile="tsunami")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("TSUNAMI_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_tsunami_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade", "seapairing", "shaded_respite", "sharp_cane", "triple_splash", "triple_split")}
        snapshots = copy.deepcopy(previous)
        doc = self.tsunami_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture(), self.seapairing_fixture(), self.shaded_respite_fixture(), self.sharp_cane_fixture(),
                    self.triple_splash_fixture(), self.triple_split_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="tsunami")
        self.inspect(doc, profile="tsunami")
        self.assertEqual(snapshots, previous)

    def test_tsunami_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/tsunami.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/Tsunami.md", "enchantments/triple-split.md", "enchantments/sated-blade.md",
                                "enchantments/seapairing.md", "enchantments/shaded-respite.md",
                                "enchantments/sharp-cane.md", "enchantments/soak-seeking.md",
                                "enchantments/sightless.md", "enchantments/triple-splash.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/tsunami.md", ACTIONS[0]):
                doc = self.tsunami_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="tsunami")
            doc = self.tsunami_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="tsunami")

    def test_tsunami_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SEAPAIRING_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHADED_RESPITE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHARP_CANE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TRIPLE_SPLASH_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TRIPLE_SPLIT_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.tsunami_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="tsunami")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.tsunami_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="tsunami")

    def test_tsunami_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.tsunami_fixture()
        relative = "enchantments/tsunami.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="tsunami")
        doc = self.tsunami_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-tsunami.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="tsunami")

    def test_tsunami_rechecks_card_after_bytecode_inspection(self):
        doc = self.tsunami_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/tsunami.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="tsunami",
                            expected_identity=self.expected_identity)

    def test_tsunami_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.tsunami_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="tsunami")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="tsunami")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="tsunami")

    def test_tsunami_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.tsunami_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="tsunami")

    def test_tsunami_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.tsunami_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="tsunami",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_tsunami_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/tsunami.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.tsunami_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="tsunami")

    def test_tsunami_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.tsunami_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="tsunami")

    def test_cli_accepts_explicit_tsunami_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-TSUNAMI-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "tsunami"]
        with mock.patch.object(audit, "load_manifest", return_value=self.tsunami_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("tsunami", inspect.call_args.kwargs["profile"])


    def arrow_inducting_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/arrow-inducting.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "ARROW_INDUCTING_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def test_arrow_inducting_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.arrow_inducting_fixture()
        self.assertEqual({"enchantments/arrow-inducting.md"}, set(audit.ARROW_INDUCTING))
        audit.validate_structure(doc, profile="arrow_inducting")
        audit.validate_cards(doc, self.root, profile="arrow_inducting")
        result = self.inspect(doc, profile="arrow_inducting")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("ARROW_INDUCTING_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_arrow_inducting_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade", "seapairing", "shaded_respite", "sharp_cane", "triple_splash", "triple_split", "tsunami")}
        snapshots = copy.deepcopy(previous)
        doc = self.arrow_inducting_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture(), self.seapairing_fixture(), self.shaded_respite_fixture(), self.sharp_cane_fixture(),
                    self.triple_splash_fixture(), self.triple_split_fixture(), self.tsunami_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="arrow_inducting")
        self.inspect(doc, profile="arrow_inducting")
        self.assertEqual(snapshots, previous)

    def test_arrow_inducting_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/arrow-inducting.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/Arrow-Inducting.md", "enchantments/tsunami.md", "enchantments/arrow_inducting.md", "enchantments/triple-split.md", "enchantments/sated-blade.md",
                                "enchantments/seapairing.md", "enchantments/shaded-respite.md",
                                "enchantments/sharp-cane.md", "enchantments/soak-seeking.md",
                                "enchantments/sightless.md", "enchantments/triple-splash.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/arrow-inducting.md", ACTIONS[0]):
                doc = self.arrow_inducting_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="arrow_inducting")
            doc = self.arrow_inducting_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="arrow_inducting")

    def test_arrow_inducting_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SEAPAIRING_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHADED_RESPITE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHARP_CANE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TRIPLE_SPLASH_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TRIPLE_SPLIT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TSUNAMI_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.arrow_inducting_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="arrow_inducting")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.arrow_inducting_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="arrow_inducting")

    def test_arrow_inducting_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.arrow_inducting_fixture()
        relative = "enchantments/arrow-inducting.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="arrow_inducting")
        doc = self.arrow_inducting_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-arrow_inducting.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="arrow_inducting")

    def test_arrow_inducting_rechecks_card_after_bytecode_inspection(self):
        doc = self.arrow_inducting_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/arrow-inducting.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="arrow_inducting",
                            expected_identity=self.expected_identity)

    def test_arrow_inducting_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.arrow_inducting_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="arrow_inducting")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="arrow_inducting")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="arrow_inducting")

    def test_arrow_inducting_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.arrow_inducting_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="arrow_inducting")

    def test_arrow_inducting_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.arrow_inducting_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="arrow_inducting",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_arrow_inducting_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/arrow-inducting.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.arrow_inducting_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="arrow_inducting")

    def test_arrow_inducting_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.arrow_inducting_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="arrow_inducting")

    def test_cli_accepts_explicit_arrow_inducting_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-ARROW-INDUCTING-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "arrow_inducting"]
        with mock.patch.object(audit, "load_manifest", return_value=self.arrow_inducting_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("arrow_inducting", inspect.call_args.kwargs["profile"])


    def astral_transferring_fixture(self):
        """Seal one literal enchantment contract while reusing synthetic artifact members."""
        doc = copy.deepcopy(self.doc)
        relative = "enchantments/astral-transferring.md"
        card = self.root / relative
        card.parent.mkdir(exist_ok=True)
        card.write_bytes((self.root / ACTIONS[0]).read_bytes())
        record = doc.pop("action_evidence")[ACTIONS[0]]
        doc["catalog_family"] = "ASTRAL_TRANSFERRING_ENCHANTMENT_CONTRACT"
        doc["cards"] = {relative: sha256(card.read_bytes())}
        doc["contract_evidence"] = {relative: record}
        doc["classes"] = {path: doc["classes"][path] for path in record["classes"]}
        return doc


    def test_astral_transferring_literal_roster_and_single_card_synthetic_audit(self):
        doc = self.astral_transferring_fixture()
        self.assertEqual({"enchantments/astral-transferring.md"}, set(audit.ASTRAL_TRANSFERRING))
        audit.validate_structure(doc, profile="astral_transferring")
        audit.validate_cards(doc, self.root, profile="astral_transferring")
        result = self.inspect(doc, profile="astral_transferring")
        self.assertEqual("PASS", result["status"])
        self.assertEqual("ASTRAL_TRANSFERRING_ENCHANTMENT_CONTRACT", result["catalog_family"])
        self.assertEqual((1, 1, 1), (result["cards_checked"], result["classes_checked"], result["methods_checked"]))
        self.assertEqual((1, 1), (result["resources_checked"], result["instruction_anchors_checked"]))
        self.assertEqual("STATIC_TECHNICAL_CATALOG_ONLY", result["claim_scope"])
        self.assertEqual("SHA_EXACT_BINARY_BEHAVIOR", result["evidence_grade"])
        self.assertEqual("NOT_VERIFIED", result["mutating_hook"])
        self.assertEqual("NOT_TESTED", result["physical_qa"])
        self.assertFalse(result["provider_universe_closed"])
        self.assertEqual(8, result["semantic_magic_roots"])

    def test_astral_transferring_remains_isolated_from_all_previous_profiles(self):
        previous = {name: audit.profile_spec(name) for name in (
            "actions", "effects", "dreadbow", "acid", "desolate_dagger",
            "forsaken", "gumball", "radiation", "nuclear", "spirit_dinosaur", "heavy_slam", "herd_phalanx", "impending_stab", "lasting_morale", "multiple_mint", "relentless_darkness", "sated_blade", "seapairing", "shaded_respite", "sharp_cane", "triple_splash", "triple_split", "tsunami", "arrow_inducting")}
        snapshots = copy.deepcopy(previous)
        doc = self.astral_transferring_fixture()
        for name in previous:
            with self.subTest(selected=name), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile=name)
            with self.subTest(cards=name), self.assertRaises(ValueError):
                audit.validate_cards(doc, self.root, profile=name)
        fixtures = (self.doc, self.effects_fixture(), self.dreadbow_fixture(), self.acid_fixture(),
                    self.desolate_dagger_fixture(), self.forsaken_fixture(), self.gumball_fixture(),
                    self.nuclear_fixture(), self.spirit_dinosaur_fixture(), self.heavy_slam_fixture(),
                    self.herd_phalanx_fixture(), self.impending_stab_fixture(), self.lasting_morale_fixture(),
                    self.multiple_mint_fixture(), self.relentless_darkness_fixture(), self.sated_blade_fixture(), self.seapairing_fixture(), self.shaded_respite_fixture(), self.sharp_cane_fixture(),
                    self.triple_splash_fixture(), self.triple_split_fixture(), self.tsunami_fixture(), self.arrow_inducting_fixture())
        for manifest in fixtures:
            with self.subTest(family=manifest.get("catalog_family")), self.assertRaises(ValueError):
                audit.validate_structure(manifest, profile="astral_transferring")
        self.inspect(doc, profile="astral_transferring")
        self.assertEqual(snapshots, previous)

    def test_astral_transferring_rejects_missing_extra_and_aliased_roster(self):
        relative = "enchantments/astral-transferring.md"
        for key in ("cards", "contract_evidence"):
            for replacement in (None, "damage-types/nuke.md", "damage-types/radiation.md",
                                "damage-types/acid.md", "damage-types/tremorzilla-beam.md",
                                "effects/irradiated.md", "equipment/extinction-spear.md",
                                "enchantments/Astral-Transferring.md", "enchantments/tsunami.md", "enchantments/astral_transferring.md", "enchantments/triple-split.md", "enchantments/sated-blade.md",
                                "enchantments/seapairing.md", "enchantments/shaded-respite.md",
                                "enchantments/sharp-cane.md", "enchantments/soak-seeking.md",
                                "enchantments/sightless.md", "enchantments/triple-splash.md",
                                "enchantments/second-wave.md", "enchantments/relentless-darkness.md",
                                "enchantments/multiple-mint.md",
                                "enchantments/lasting-morale.md",
                                "enchantments/peppermint-punting.md", "enchantments/spell-lasting.md",
                                "enchantments/seekcandy.md", "enchantments/impending-stab.md",
                                "enchantments/heavy-slam.md", "enchantments/triple-strike.md",
                                "enchantments/herd-phalanx.md", "enchantments/humungous-hex.md",
                                "enchantments/../enchantments/astral-transferring.md", ACTIONS[0]):
                doc = self.astral_transferring_fixture()
                value = doc[key].pop(relative)
                if replacement is not None:
                    doc[key][replacement] = value
                with self.subTest(key=key, replacement=replacement), self.assertRaises(ValueError):
                    audit.validate_structure(doc, profile="astral_transferring")
            doc = self.astral_transferring_fixture()
            doc[key]["damage-types/extra.md"] = doc[key][relative]
            with self.subTest(key=key, extra=True), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="astral_transferring")

    def test_astral_transferring_rejects_scope_and_evidence_promotion(self):
        for key, value in (("catalog_family", "HEAVY_SLAM_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "HERD_PHALANX_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "IMPENDING_STAB_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "LASTING_MORALE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "MULTIPLE_MINT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "RELENTLESS_DARKNESS_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SATED_BLADE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SEAPAIRING_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHADED_RESPITE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "SHARP_CANE_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TRIPLE_SPLASH_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TRIPLE_SPLIT_ENCHANTMENT_CONTRACT"),
                           ("catalog_family", "TSUNAMI_ENCHANTMENT_CONTRACT"), ("catalog_family", None),
                           ("claim_scope", "COMPLETE_PERK_READY"), ("evidence_grade", "SOURCE_ONLY"),
                           ("semantic_magic_roots", 9), ("provider_universe_closed", True),
                           ("mutating_hook", "VERIFIED"), ("physical_qa", "PASS"),
                           ("artifact_size_bytes", True), ("artifact_sha1", "a" * 40),
                           ("artifact_sha256", "b" * 64), ("version", "1.1.1"),
                           ("runtime_verified", True), ("perk_certification", "CERTIFIED"),
                           ("complete_control_flow", "RECONSTRUCTED"), ("schema_version", True)):
            doc = self.astral_transferring_fixture()
            if value is None:
                doc.pop(key)
            else:
                doc[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="astral_transferring")
        for alias in ("action_evidence", "effect_evidence"):
            doc = self.astral_transferring_fixture()
            doc[alias] = doc.pop("contract_evidence")
            with self.subTest(alias=alias), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="astral_transferring")

    def test_astral_transferring_rejects_forged_card_seal_and_symlink_escape(self):
        doc = self.astral_transferring_fixture()
        relative = "enchantments/astral-transferring.md"
        doc["cards"][relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale card seal"):
            self.inspect(doc, profile="astral_transferring")
        doc = self.astral_transferring_fixture()
        card = self.root / relative
        outside = Path(self.temp.name) / "outside-astral_transferring.md"
        outside.write_bytes(card.read_bytes())
        card.unlink()
        card.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "escapes provider root"):
            self.inspect(doc, profile="astral_transferring")

    def test_astral_transferring_rechecks_card_after_bytecode_inspection(self):
        doc = self.astral_transferring_fixture()
        def completed(command, **kwargs):
            card = self.root / "enchantments/astral-transferring.md"
            card.write_bytes(card.read_bytes() + b"changed during audit")
            return subprocess.CompletedProcess(command, 0, stdout=JAVAP.replace(OWNER, command[-1]), stderr="")
        with mock.patch.object(audit.subprocess, "run", side_effect=completed):
            with self.assertRaisesRegex(ValueError, "stale card seal"):
                audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="astral_transferring",
                            expected_identity=self.expected_identity)

    def test_astral_transferring_verifies_artifact_resources_and_anchor_operands(self):
        doc = self.astral_transferring_fixture()
        with self.assertRaisesRegex(ValueError, "artifact identity mismatch"):
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="astral_transferring")
        drifted = copy.deepcopy(doc)
        path = next(iter(drifted["classes"]))
        drifted["classes"][path]["methods"][0]["anchors"][0]["operand"] = "unobserved operand"
        with self.assertRaisesRegex(ValueError, "instruction anchor mismatch"):
            self.inspect(drifted, profile="astral_transferring")
        self.members[self.resource] += b"resource drift"
        self.write_jar()
        with self.assertRaisesRegex(ValueError, "resource hash mismatch"):
            self.inspect(doc, profile="astral_transferring")

    def test_astral_transferring_rejects_class_hash_abi_and_all_anchor_drift(self):
        for mode in ("class_hash", "descriptor", "offset", "opcode", "operand", "symbol"):
            doc = self.astral_transferring_fixture()
            entry = next(iter(doc["classes"].values()))
            method = entry["methods"][0]
            if mode == "class_hash":
                entry["sha256"] = "0" * 64
            elif mode == "descriptor":
                method["descriptor"] = "(J)I"
            else:
                method["anchors"][0][mode] = {
                    "offset": 99, "opcode": "iconst_0", "operand": "2", "symbol": "wrong"}[mode]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.inspect(doc, profile="astral_transferring")

    def test_astral_transferring_uses_read_only_javap_with_existing_time_budget(self):
        doc = self.astral_transferring_fixture()
        path = next(iter(doc["classes"]))
        owner = path.removesuffix(".class").replace("/", ".")
        completed = subprocess.CompletedProcess([], 0, stdout=JAVAP.replace(OWNER, owner), stderr="")
        with mock.patch.object(audit.subprocess, "run", return_value=completed) as run:
            audit.audit(self.jar, doc, self.root, "synthetic-javap", profile="astral_transferring",
                        expected_identity=self.expected_identity)
        run.assert_called_once_with(
            ["synthetic-javap", "-p", "-c", "-s", "-classpath", str(self.jar), owner],
            capture_output=True, text=True, check=False, timeout=60)

    def test_astral_transferring_rejects_invalid_and_unreferenced_evidence(self):
        relative = "enchantments/astral-transferring.md"
        for mode in ("duplicate_class", "unknown_class", "unknown_resource", "unsafe_resource",
                     "unreferenced_class", "unreferenced_resource", "duplicate_resource",
                     "duplicate_method", "boolean_offset"):
            doc = self.astral_transferring_fixture()
            record = doc["contract_evidence"][relative]
            methods = next(iter(doc["classes"].values()))["methods"]
            if mode == "duplicate_class":
                record["classes"] *= 2
            elif mode == "unknown_class":
                record["classes"] = ["com/github/alexmodguy/alexscaves/Missing.class"]
            elif mode == "unknown_resource":
                record["resources"] = ["data/alexscaves/missing.json"]
            elif mode == "unsafe_resource":
                resource = "data/alexscaves/../unsafe.json"
                doc["resources"] = {resource: "a" * 64}
                record["resources"] = [resource]
            elif mode == "unreferenced_class":
                doc["classes"]["com/github/alexmodguy/alexscaves/Orphan.class"] = {
                    "sha256": "a" * 64, "methods": []}
            elif mode == "duplicate_resource":
                record["resources"] *= 2
            elif mode == "unreferenced_resource":
                doc["resources"]["data/alexscaves/orphan.json"] = "a" * 64
            elif mode == "duplicate_method":
                methods.append(copy.deepcopy(methods[0]))
            else:
                methods[0]["anchors"][0]["offset"] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="astral_transferring")

    def test_astral_transferring_keeps_existing_anchor_and_class_budgets(self):
        for mode in ("missing_class", "anchorless", "too_many_classes", "too_many_resources",
                     "too_many_methods", "too_many_anchors", "too_many_total_anchors"):
            doc = self.astral_transferring_fixture()
            path = next(iter(doc["classes"]))
            entry = doc["classes"][path]
            if mode == "missing_class":
                doc["classes"].clear()
            elif mode == "anchorless":
                entry["methods"] = []
            elif mode == "too_many_classes":
                doc["classes"] = {path.removesuffix(".class") + str(index) + ".class": entry
                                  for index in range(129)}
            elif mode == "too_many_resources":
                doc["resources"] = {"data/alexscaves/synthetic" + str(index) + ".json": "a" * 64
                                    for index in range(257)}
            elif mode == "too_many_methods":
                entry["methods"] = [{**entry["methods"][0], "name": "value" + str(index)}
                                    for index in range(129)]
            else:
                method = entry["methods"][0]
                anchor = method["anchors"][0]
                if mode == "too_many_anchors":
                    method["anchors"] = [{**anchor, "offset": offset} for offset in range(257)]
                else:
                    entry["methods"] = [{**method, "name": "value" + str(index), "anchors": [
                        {**anchor, "offset": offset} for offset in range(256)]} for index in range(33)]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                audit.validate_structure(doc, profile="astral_transferring")

    def test_cli_accepts_explicit_astral_transferring_profile(self):
        arguments = ["--jar", str(self.jar), "--manifest", str(self.root / "EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json"),
                     "--provider-root", str(self.root), "--javap", "synthetic-javap",
                     "--profile", "astral_transferring"]
        with mock.patch.object(audit, "load_manifest", return_value=self.astral_transferring_fixture()), \
                mock.patch.object(audit, "audit", return_value={"status": "PASS"}) as inspect, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, audit.main(arguments))
            self.assertEqual("astral_transferring", inspect.call_args.kwargs["profile"])


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



class BonkingProfileTests(unittest.TestCase):
    """Bonking extends the dispatcher without changing historical profile policy."""
    @classmethod
    def setUpClass(cls):
        cls.provider = Path(__file__).resolve().parents[2] / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
        cls.manifest = audit.load_manifest(cls.provider / 'EXACT-BONKING-CONTRACT-1.0.10.json')

    def reject(self, edit):
        document = copy.deepcopy(self.manifest)
        edit(document)
        with self.assertRaises(audit.AuditError):
            audit.validate_structure(document, profile='bonking')

    def test_bonking_is_one_explicit_static_family(self):
        self.assertEqual(audit.profile_spec('bonking'),
                         (audit.BONKING_SCOPE, frozenset({'enchantments/bonking.md'}), 'contract_evidence'))
        audit.validate_structure(self.manifest, profile='bonking')
        self.assertEqual(audit.profile_spec('actions'), (audit.SCOPE, audit.ACTIONS, 'action_evidence'))

    def test_old_profiles_reject_bonking_native_metadata(self):
        for profile in ('actions', 'effects', 'radiation', 'astral_transferring'):
            with self.subTest(profile=profile), self.assertRaises(audit.AuditError):
                audit.validate_structure(self.manifest, profile=profile)

    def test_native_metadata_is_required_and_closed(self):
        self.reject(lambda d: d.pop('native_metadata'))
        self.reject(lambda d: d['native_metadata'].update(unsealed_claim=True))
        self.reject(lambda d: d['native_metadata'].pop('interface'))

    def test_interface_is_separate_from_executable_anchor_policy(self):
        self.assertNotIn(audit.BONKING_INTERFACE, self.manifest['classes'])
        self.assertEqual(self.manifest['native_metadata']['interface']['path'], audit.BONKING_INTERFACE)
        def abstract_anchor(d):
            method = next(iter(d['classes'].values()))['methods'][0]
            method['anchors'] = []
        self.reject(abstract_anchor)

    def test_full_body_anchor_deletion_and_stale_fingerprint_fail(self):
        self.reject(lambda d: d['classes'][audit.BONKING_PREFIX + 'server/event/CommonEvents.class']['methods'][0]['anchors'].pop())
        self.reject(lambda d: d['native_metadata']['method_coverage'][0].update(parsed_method_sha256='0' * 64))

    def test_full_body_branch_metadata_cannot_omit_a_target(self):
        def remove(d):
            record = next(r for r in d['native_metadata']['method_coverage'] if r['name'] == 'livingDie')
            record['branch_edges'].pop()
        self.reject(remove)

    def test_partial_registries_cannot_be_relabelled_complete(self):
        def relabel(d):
            record = next(r for r in d['native_metadata']['method_coverage'] if r['name'] == '<clinit>')
            record['coverage'] = 'FULL_BODY'
        self.reject(relabel)

    def test_partial_registry_window_cannot_move(self):
        def move(d):
            selected = next(m for m in d['classes'][audit.BONKING_PREFIX + 'server/enchantment/ACEnchantmentRegistry.class']['methods'] if m['name'] == '<clinit>')
            selected['anchors'][0]['offset'] = 131
        self.reject(move)

    def test_coverage_cannot_duplicate_or_replace_a_method(self):
        def duplicate(d):
            d['native_metadata']['method_coverage'][1] = copy.deepcopy(d['native_metadata']['method_coverage'][0])
        self.reject(duplicate)
        def replace(d):
            d['native_metadata']['method_coverage'][0]['name'] = 'unsealed_method'
        self.reject(replace)

    def test_existing_256_instruction_budget_still_applies_to_bonking(self):
        def exceed(d):
            method = next(iter(d['classes'].values()))['methods'][0]
            method['anchors'] = [dict(offset=i, opcode='nop', operand='', symbol='') for i in range(257)]
        self.reject(exceed)

    def test_declaration_reader_preserves_abstract_abi_and_annotation_arguments(self):
        def u2(n): return n.to_bytes(2, 'big')
        def utf8(s):
            value = s.encode()
            return b'\x01' + u2(len(value)) + value
        # Minimal synthetic Java 21 interface: no executable Code attribute.
        constants = [utf8('test/Accessor'), b'\x07' + u2(1), utf8('java/lang/Object'),
                     b'\x07' + u2(3), utf8('bridge'), utf8('()V'),
                     utf8('RuntimeVisibleAnnotations'), utf8('Ltest/Marker;')]
        annotation = u2(1) + u2(8) + u2(0)
        member = u2(0x0401) + u2(5) + u2(6) + u2(1) + u2(7) + len(annotation).to_bytes(4, 'big') + annotation
        raw = b'\xca\xfe\xba\xbe\x00\x00\x00A' + u2(9) + b''.join(constants)
        raw += u2(0x0601) + u2(2) + u2(4) + u2(0) + u2(0) + u2(1) + member + u2(0)
        declaration = audit.class_metadata(raw)
        self.assertEqual(declaration['name'], 'test/Accessor')
        method = declaration['methods'][0]
        self.assertEqual((method['name'], method['descriptor']), ('bridge', '()V'))
        self.assertEqual(method['annotations'], [dict(visibility='RuntimeVisibleAnnotations', type='Ltest/Marker;', values={})])
        self.assertNotIn('exception_handlers', method)
        for broken in (raw[:-1], raw + b'bad', raw[:6] + b'\x00=' + raw[8:]):
            with self.subTest(broken=broken[-5:]), self.assertRaises(audit.AuditError):
                audit.class_metadata(broken)

    def test_current_card_seal_rejects_modified_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = 'enchantments/bonking.md'
            (root / 'enchantments').mkdir()
            (root / relative).write_bytes((self.provider / relative).read_bytes() + b'changed\n')
            with self.assertRaises(audit.AuditError):
                audit.validate_cards(self.manifest, root, profile='bonking')


if __name__ == "__main__":
    unittest.main()
