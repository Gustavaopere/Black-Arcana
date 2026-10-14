#!/usr/bin/env python3
"""Synthetic Java 21 fixtures for static 24-item/25-ability binary audit."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "reliquified_irons_027_audit", HERE / "reliquified_irons_binary_audit.py"
)
assert spec and spec.loader
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
EXPECTED_FIXTURE = (
    ("alpha", "ItemAlpha", ("alpha_spell",)),
    ("beta", "ItemBeta", ("beta_cast", "beta_burst")),
    ("none", "ItemNone", ()),
)


class BinaryRelicAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        base = Path(cls.tmp.name)
        cls.jar = base / audit.EXPECTED_JAR
        root = base / "src"
        classes = base / "classes"
        classes.mkdir()
        sources = {
            "net/neoforged/neoforge/registries/DeferredHolder.java":
                "package net.neoforged.neoforge.registries; public class DeferredHolder {}",
            "net/neoforged/neoforge/registries/DeferredRegister.java":
                "package net.neoforged.neoforge.registries; "
                "import java.util.function.Supplier; public class DeferredRegister {"
                "public static DeferredRegister create(){return new DeferredRegister();}"
                "public DeferredHolder register(String id, Supplier<?> source){return new DeferredHolder();}"
                "}",
            "it/hurts/sskirillss/relics/api/relics/abilities/AbilityTemplate.java":
                "package it.hurts.sskirillss.relics.api.relics.abilities;"
                "public class AbilityTemplate {"
                "public static AbilityTemplate builder(String id){return new AbilityTemplate();}"
                "}",
            "it/hurts/shatterbyte/reliquified_irons_spells_and_spellbooks/init/RISASItems.java":
                "package it.hurts.shatterbyte.reliquified_irons_spells_and_spellbooks.init;"
                "import net.neoforged.neoforge.registries.*;"
                "import it.hurts.shatterbyte.reliquified_irons_spells_and_spellbooks.items.*;"
                "public class RISASItems {"
                "public static final DeferredRegister ITEMS=DeferredRegister.create();"
                "public static final DeferredHolder ALPHA=ITEMS.register(\"alpha\",ItemAlpha::new);"
                "public static final DeferredHolder BETA=ITEMS.register(\"beta\",ItemBeta::new);"
                "public static final DeferredHolder NONE=ITEMS.register(\"none\",ItemNone::new);"
                "}",
            "it/hurts/shatterbyte/reliquified_irons_spells_and_spellbooks/items/ItemAlpha.java":
                "package it.hurts.shatterbyte.reliquified_irons_spells_and_spellbooks.items;"
                "import it.hurts.sskirillss.relics.api.relics.abilities.AbilityTemplate;"
                "public class ItemAlpha { public void constructDefaultRelicTemplate(){"
                "AbilityTemplate.builder(\"alpha_spell\"); }}",
            "it/hurts/shatterbyte/reliquified_irons_spells_and_spellbooks/items/ItemBeta.java":
                "package it.hurts.shatterbyte.reliquified_irons_spells_and_spellbooks.items;"
                "import it.hurts.sskirillss.relics.api.relics.abilities.AbilityTemplate;"
                "public class ItemBeta { public void constructDefaultRelicTemplate(){"
                "AbilityTemplate.builder(\"beta_cast\");AbilityTemplate.builder(\"beta_burst\"); }}",
            "it/hurts/shatterbyte/reliquified_irons_spells_and_spellbooks/items/ItemNone.java":
                "package it.hurts.shatterbyte.reliquified_irons_spells_and_spellbooks.items;"
                "public class ItemNone {public void constructDefaultRelicTemplate(){}}",
        }
        paths = []
        for name, source in sources.items():
            file = root / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(source, encoding="utf-8")
            paths.append(str(file))
        subprocess.run(["javac", "-d", str(classes), *paths],
                       check=True, capture_output=True, text=True, timeout=35)
        with zipfile.ZipFile(cls.jar, "w") as z:
            z.writestr("META-INF/neoforge.mods.toml", '[[mods]]\nmodId="reliquified_irons_spells_and_spellbooks"\n')
            for p in classes.rglob("*.class"):
                z.write(p, p.relative_to(classes).as_posix())
        cls.sha = hashlib.sha1(cls.jar.read_bytes()).hexdigest()
        cls.outputs = {}
        for name in (audit.REGISTRY_CLASS, *(f"{audit.ITEM_PACKAGE}.{c}" for _, c, _ in EXPECTED_FIXTURE)):
            run = subprocess.run(["javap", "-c", "-p", "-classpath", str(cls.jar), name],
                                 capture_output=True, text=True, check=True, timeout=25)
            cls.outputs["registry" if name == audit.REGISTRY_CLASS else name.rsplit(".", 1)[1]] = run.stdout

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_compiled_registration_and_primary_template_counts(self):
        report = audit.verify(self.outputs, EXPECTED_FIXTURE)
        self.assertEqual("PASS", report["status"])
        self.assertEqual((3, 3), (report["items_observed"], report["abilities_observed"]))
        self.assertEqual(2, report["ability_bearing_classes_observed"])

    def test_wrong_expected_ability_fails_closed(self):
        wrong = (EXPECTED_FIXTURE[0], ("beta", "ItemBeta", ("beta_cast", "made_up")), EXPECTED_FIXTURE[2])
        report = audit.verify(self.outputs, wrong)
        self.assertEqual("UNPROVEN_OR_MISMATCH", report["status"])
        self.assertIn("beta_ability_mismatch", report["deviations"])

    def test_missing_item_registration_fails_closed(self):
        changed = dict(self.outputs)
        changed["registry"] = changed["registry"].replace("String alpha", "String corrupted")
        report = audit.verify(changed, EXPECTED_FIXTURE)
        self.assertEqual("UNPROVEN_OR_MISMATCH", report["status"])
        self.assertGreater(len(report["deviations"]["missing_item_pairs"]), 0)

    def test_shadow_item_without_template_remains_not_a_root(self):
        actual = audit.ability_roots(self.outputs["ItemNone"])
        self.assertEqual([], actual)

    def test_bare_string_constant_is_not_accepted_as_ability(self):
        fake = self.outputs["ItemNone"] + "\n  900: ldc #20 // String bogus_ability\n"
        self.assertEqual([], audit.ability_roots(fake))

    def test_mismatched_publisher_hash_rejected(self):
        with self.assertRaisesRegex(audit.AuditError, "SHA-1 mismatch"):
            audit.audit(self.jar, expected=EXPECTED_FIXTURE)

    def test_matching_fixture_hash_is_not_minecraft_gameplay(self):
        report = audit.audit(self.jar, expected_sha1=self.sha, expected=EXPECTED_FIXTURE)
        self.assertEqual("PASS", report["result"])
        self.assertIn("real client/dedicated server and item acquisition", report["not_proven"])
        self.assertEqual(3, report["registry"]["items_observed"])

    def test_corrupted_zip_rejected(self):
        original = self.jar.read_bytes()
        try:
            self.jar.write_bytes(b"not a jar")
            with self.assertRaises(zipfile.BadZipFile):
                audit.audit(self.jar, expected_sha1=hashlib.sha1(b"not a jar").hexdigest(),
                            expected=EXPECTED_FIXTURE)
        finally:
            self.jar.write_bytes(original)

    def test_duplicate_spec_fails(self):
        with self.assertRaises(audit.AuditError):
            audit.verify(self.outputs, (EXPECTED_FIXTURE[0], EXPECTED_FIXTURE[0]))

    def test_missing_class_never_promotes(self):
        altered = dict(self.outputs)
        del altered["ItemBeta"]
        self.assertNotEqual("PASS", audit.verify(altered, EXPECTED_FIXTURE)["status"])


if __name__ == "__main__":
    unittest.main()
