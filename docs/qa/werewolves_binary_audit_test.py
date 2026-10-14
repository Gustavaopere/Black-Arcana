#!/usr/bin/env python3
"""Synthetic Java 21 bytecode regression; never real Werewolves gameplay evidence."""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

P = Path(__file__).resolve().with_name("werewolves_binary_audit.py")
spec = importlib.util.spec_from_file_location("werewolves_audit", P)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
TEST_PAIRS = (("human_form", "HUMAN_FORM"),
              ("beast_form", "BEAST_FORM"),
              ("leap", "LEAP"))


class WerewolvesExactRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        src, compiled = root / "src", root / "classes"
        compiled.mkdir()
        code = {
            "net/neoforged/neoforge/registries/DeferredHolder.java":
                "package net.neoforged.neoforge.registries; public class DeferredHolder {}",
            "net/neoforged/neoforge/registries/DeferredRegister.java":
                "package net.neoforged.neoforge.registries;"
                "import java.util.function.Supplier; public class DeferredRegister {"
                "public static DeferredRegister create(){return new DeferredRegister();}"
                "public DeferredHolder register(String id, Supplier<?> factory){return new DeferredHolder();}"
                "}",
            "de/teamlapen/werewolves/core/ModActions.java":
                "package de.teamlapen.werewolves.core;"
                "import net.neoforged.neoforge.registries.*;"
                "public class ModActions {"
                "public static final DeferredRegister ACTIONS=DeferredRegister.create();"
                "public static final DeferredHolder HUMAN_FORM=ACTIONS.register(\"human_form\",Object::new);"
                "public static final DeferredHolder BEAST_FORM=ACTIONS.register(\"beast_form\",Object::new);"
                "public static final DeferredHolder LEAP=ACTIONS.register(\"leap\",Object::new);"
                "}",
        }
        paths = []
        for name, src_code in code.items():
            out = src / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(src_code, encoding="utf-8")
            paths.append(str(out))
        subprocess.run(["javac","-d",str(compiled),*paths],
                       capture_output=True,text=True,check=True,timeout=35)
        cls.jar = root / mod.FILENAME
        with zipfile.ZipFile(cls.jar,"w") as z:
            z.writestr("META-INF/neoforge.mods.toml",'[[mods]]\nmodId="werewolves"\n')
            for p in compiled.rglob("*.class"):
                z.write(p,p.relative_to(compiled).as_posix())
        cls.sha1 = hashlib.sha1(cls.jar.read_bytes()).hexdigest()
        r = subprocess.run(["javap","-c","-p","-classpath",str(cls.jar),mod.CLASS],
                           capture_output=True,text=True,check=True,timeout=30)
        cls.disassembly=r.stdout

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_three_real_compiled_static_pairs(self):
        pairs, fields = mod.parse(self.disassembly)
        self.assertEqual(list(TEST_PAIRS), pairs)
        self.assertEqual({f for _,f in TEST_PAIRS}, set(fields))
        result = mod.reconcile(self.disassembly, TEST_PAIRS)
        self.assertEqual("PASS", result["result"])
        self.assertEqual(3, result["registered_observed"])

    def test_missing_id_rejected(self):
        bad = self.disassembly.replace("String beast_form", "String unexpected")
        result = mod.reconcile(bad, TEST_PAIRS)
        self.assertEqual("UNPROVEN_OR_MISMATCH", result["result"])
        self.assertIn("beast_form:BEAST_FORM", result["deviations"]["missing"])

    def test_missing_field_rejected(self):
        bad = self.disassembly.replace("Field LEAP:", "Field WRONG:")
        result = mod.reconcile(bad, TEST_PAIRS)
        self.assertNotEqual("PASS", result["result"])

    def test_wrong_invocation_kind_fails_closed(self):
        bad = self.disassembly.replace("invokevirtual", "invokestatic")
        self.assertEqual(0, mod.reconcile(bad, TEST_PAIRS)["registered_observed"])

    def test_excluded_action_not_automatically_normal_reachable(self):
        info = mod.reconcile(self.disassembly, TEST_PAIRS)
        self.assertFalse(info["semantic_reachability_verified_by_binary"])
        self.assertEqual(["leap"], info["excluded_from_semantic_count_source_classification"])

    def test_wrong_real_publisher_hash_rejected(self):
        with self.assertRaisesRegex(mod.AuditError,"SHA-1 mismatch"):
            mod.audit(self.jar, expected=TEST_PAIRS)

    def test_synthetic_fixture_hash_is_not_gameplay_pass(self):
        report = mod.audit(self.jar, expected=TEST_PAIRS, expected_sha1=self.sha1)
        self.assertEqual("PASS",report["result"])
        self.assertIn("action grants, cooldowns, server authority, config and Survival",report["not_proven"])

    def test_same_file_name_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            alias=Path(tmp)/"wrong.jar"
            alias.write_bytes(self.jar.read_bytes())
            with self.assertRaises(mod.AuditError):
                mod.audit(alias,expected=TEST_PAIRS,expected_sha1=self.sha1)

    def test_malformed_zip_is_not_success(self):
        original = self.jar.read_bytes()
        try:
            self.jar.write_bytes(b"not a valid JAR")
            with self.assertRaises(mod.AuditError):
                mod.audit(self.jar,expected_sha1=hashlib.sha1(b"not a valid JAR").hexdigest(),expected=TEST_PAIRS)
        finally:
            self.jar.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
