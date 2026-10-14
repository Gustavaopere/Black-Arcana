#!/usr/bin/env python3
"""JDK21 synthetic fixtures for Hazen registry parser. Never actual-gameplay QA."""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("hazen_binary", HERE / "hazen_14014_binary_audit.py")
assert SPEC and SPEC.loader
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)
FIXTURE = [
    ("endraconic_meteor", "EndraconicMeteorSpell"),
    ("soul_flame_bolt", "SoulflameBoltSpell"),
    ("golden_shower", "GoldenShowerSpell"),
]
PREFIX = "net.hazen.hazennstuff.Spells"
GETTER = "net.minecraft.resources.ResourceLocation"
INTERFACE = "io.redspace.ironsspellbooks.api.spells.AbstractSpell"


class HazenBinaryParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.root = root
        sources = {}
        sources["net/minecraft/resources/ResourceLocation.java"] = (
            "package net.minecraft.resources; public class ResourceLocation {"
            " public static ResourceLocation fromNamespaceAndPath(String namespace,String path)"
            "{return new ResourceLocation();}}"
        )
        sources["io/redspace/ironsspellbooks/api/spells/AbstractSpell.java"] = (
            "package io.redspace.ironsspellbooks.api.spells;"
            " public abstract class AbstractSpell {"
            " public abstract net.minecraft.resources.ResourceLocation getSpellResource();}"
        )
        reg = [
            "package net.hazen.hazennstuff.Spells;",
            "import java.util.function.Supplier;",
            "import io.redspace.ironsspellbooks.api.spells.AbstractSpell;",
            "public class HnSSpellRegistries {",
            " public static Supplier<AbstractSpell> registerSpell(AbstractSpell spell) {return () -> spell;}",
        ]
        for id, klass in FIXTURE:
            reg.append(f" public static final Supplier<AbstractSpell> {id.upper()} = "
                       f"registerSpell(new Schools.Test.{klass}());")
            sources[f"net/hazen/hazennstuff/Spells/Schools/Test/{klass}.java"] = (
                "package net.hazen.hazennstuff.Spells.Schools.Test;"
                "import io.redspace.ironsspellbooks.api.spells.AbstractSpell;"
                "import net.minecraft.resources.ResourceLocation;"
                f"public class {klass} extends AbstractSpell" + "{"
                "private final ResourceLocation spellId = "
                f'ResourceLocation.fromNamespaceAndPath("hazennstuff","{id}");'
                "public ResourceLocation getSpellResource(){return spellId;}"
                "}"
            )
        reg.append("}")
        sources["net/hazen/hazennstuff/Spells/HnSSpellRegistries.java"] = "\n".join(reg)
        src_paths = []
        for path, code in sources.items():
            location = root / "src" / path
            location.parent.mkdir(parents=True, exist_ok=True)
            location.write_text(code, encoding="utf-8")
            src_paths.append(str(location))
        out = root / "classes"
        out.mkdir()
        subprocess.run(["javac", "-d", str(out), *src_paths],
                       check=True, text=True, capture_output=True, timeout=35)
        cls.disassembled = {}
        for key, classname in [
            ("registry", PREFIX + ".HnSSpellRegistries"),
            *((klass, PREFIX + ".Schools.Test." + klass) for _, klass in FIXTURE),
        ]:
            result = subprocess.run(["javap", "-c", "-p", "-classpath", str(out), classname],
                                    check=True, capture_output=True, text=True, timeout=25)
            cls.disassembled[key] = result.stdout

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_compiled_registry_and_exact_class_id_pairs(self):
        result = m.reconcile(FIXTURE, self.disassembled["registry"], self.disassembled)
        self.assertEqual("PASS", result["status"], result)
        self.assertEqual(3, result["compiled_registration_pairs"])
        self.assertEqual(3, result["exact_spell_id_class_match_count"])

    def test_missing_registration_fail_closed(self):
        changed = dict(self.disassembled)
        changed["registry"] = changed["registry"].replace(
            "Field GOLDEN_SHOWER:", "Field WRONG_FIELD:"
        )
        result = m.reconcile(FIXTURE, changed["registry"], changed)
        self.assertEqual("UNPROVEN_OR_MISMATCH", result["status"])

    def test_catalog_id_not_equal_constructor_id_fails(self):
        false_catalog = [("other_name", "EndraconicMeteorSpell"), *FIXTURE[1:]]
        result = m.reconcile(false_catalog, self.disassembled["registry"], self.disassembled)
        self.assertIn("other_name", result["deviations"]["missing_or_mismatched_class_spell_ids"])

    def test_missing_class_does_not_count_as_binary_proof(self):
        changed = dict(self.disassembled)
        del changed["SoulflameBoltSpell"]
        result = m.reconcile(FIXTURE, changed["registry"], changed)
        self.assertEqual("UNPROVEN_OR_MISMATCH", result["status"])

    def test_extra_registry_registration_rejected(self):
        result = m.reconcile(FIXTURE[:2], self.disassembled["registry"], self.disassembled)
        self.assertEqual("UNPROVEN_OR_MISMATCH", result["status"])

    def test_full_catalog_reader_requires_38_unique_entries(self):
        section = "# Inventory\n\n" + "".join(
            f"| {i} | Ender | `hazennstuff:spell_{i}` | Spell | `SpellClass{i}` | RARE | 5 | host |\n"
            for i in range(38)
        )
        self.assertEqual(38, len(m.inventory_pairs(section)))
        with self.assertRaises(m.AuditError):
            m.inventory_pairs(section.replace("spell_37", "spell_36"))
        with self.assertRaises(m.AuditError):
            m.inventory_pairs(section.replace("SpellClass37", "SpellClass36"))

    def test_old_publisher_hash_not_a_fixture_proof(self):
        bogus = self.root / m.EXPECTED_FILENAME
        bogus.write_bytes(b"dummy jar bytes")
        with self.assertRaisesRegex(m.AuditError, "SHA-1 mismatch"):
            m.audit(bogus, "")

    def test_no_static_initializer_is_blocked(self):
        with self.assertRaises(m.AuditError):
            m.static_spell_pairs("public class HnSSpellRegistries {}")

    def test_false_getter_or_factory_breaks_class_identity(self):
        spell = self.disassembled["GoldenShowerSpell"]
        self.assertTrue(m.class_identity(spell, "GoldenShowerSpell", "golden_shower"))
        self.assertFalse(m.class_identity(spell.replace("getfield", "getstatic"),
                                         "GoldenShowerSpell", "golden_shower"))
        self.assertFalse(m.class_identity(spell.replace("fromNamespaceAndPath", "parseOther"),
                                         "GoldenShowerSpell", "golden_shower"))


if __name__ == "__main__":
    unittest.main()
