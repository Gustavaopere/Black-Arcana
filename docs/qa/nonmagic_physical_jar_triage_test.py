#!/usr/bin/env python3
"""Regression tests for exact physical non-Magic archive-name triage."""
from __future__ import annotations

import importlib.util
import hashlib
from unittest import mock
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "docs/qa/nonmagic_physical_jar_triage.py"
spec = importlib.util.spec_from_file_location("nonmagic_physical_jar_triage", TARGET)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class NonMagicPhysicalJarTriageTest(unittest.TestCase):
    def test_manifest_excludes_loader_and_97_magic_rows(self):
        rows = module.manifest_entries()
        self.assertEqual(489, len(rows))
        self.assertEqual(489, len(set(r["filename"] for r in rows)))
        self.assertTrue(all(r["filename"].endswith(".jar") for r in rows))
        self.assertTrue(all(r["physical_number"] != 1 for r in rows))
        self.assertEqual(
            {"LEXICAL_NAME": 46, "RPG_GEAR_MOBS_DIMENSIONS": 96, "OTHER": 347},
            {group: sum(r["triage_group"] == group for r in rows)
             for group in ("LEXICAL_NAME", "RPG_GEAR_MOBS_DIMENSIONS", "OTHER")},
        )

    def test_zip_member_name_hints_do_not_copy_payload(self):
        with tempfile.TemporaryDirectory() as td:
            mods = Path(td)
            with zipfile.ZipFile(mods / "provider.jar", "w") as jar:
                jar.writestr("data/example/spells/light.json", "secret-unique-test-body")
                jar.writestr("example/SummonAbility.class", b"fake-class-body")
                jar.writestr("assets/example/lang/en_us.json", '{"secret": true}')
                jar.writestr("../spell/escape.txt", "unsafe-path")
            report = module.scan(mods, [{
                "physical_number": 121, "name": "Test Provider",
                "filename": "provider.jar", "triage_group": "RPG_GEAR_MOBS_DIMENSIONS",
            }])
            item = report["rows"][0]
            self.assertEqual("FINGERPRINTED", item["status"])
            self.assertEqual(2, item["lexical_hint_member_count"])
            self.assertEqual(4, item["archive_member_count"])
            self.assertEqual(40, len(item["sha1"]))
            self.assertEqual(64, len(item["sha256"]))
            self.assertNotIn("secret-unique-test-body", json.dumps(report))
            self.assertNotIn("fake-class-body", json.dumps(report))
            self.assertNotIn("../spell/escape.txt", json.dumps(report))
            self.assertEqual(
                "ZIP_MEMBER_NAME_HINTS_AND_SHA_NOT_REGISTRY_OR_RUNTIME_PROOF",
                report["evidence"],
            )

    def test_zero_lexical_hits_do_not_become_no_magic_assertion(self):
        with tempfile.TemporaryDirectory() as td:
            mods = Path(td)
            with zipfile.ZipFile(mods / "plain.jar", "w") as jar:
                jar.writestr("data/demo/recipes/iron.json", "{}")
            item = module.scan(mods, [{
                "physical_number": 31, "name": "Plain",
                "filename": "plain.jar", "triage_group": "OTHER",
            }])["rows"][0]
            self.assertEqual("FINGERPRINTED", item["status"])
            self.assertEqual(0, item["lexical_hint_member_count"])
            self.assertNotIn("magic_absent", item)

    def test_missing_and_invalid_jars_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            mods = Path(td)
            (mods / "broken.jar").write_bytes(b"not an archive")
            report = module.scan(mods, [
                {"physical_number": 1, "name": "Broken",
                 "filename": "broken.jar", "triage_group": "OTHER"},
                {"physical_number": 2, "name": "Missing",
                 "filename": "missing.jar", "triage_group": "OTHER"},
            ])
            self.assertEqual(
                {"INVALID_ZIP_JAR": 1, "MISSING": 1},
                report["statuses"],
            )

    def test_symlink_to_external_jar_is_never_read(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mods = root / "mods"
            mods.mkdir()
            outside = root / "outside.jar"
            with zipfile.ZipFile(outside, "w") as jar:
                jar.writestr("data/demo/spells/secret.json", "SENSITIVE")
            (mods / "provider.jar").symlink_to(outside)
            item = module.scan(mods, [
                {"physical_number": 121, "name": "Provider",
                 "filename": "provider.jar", "triage_group": "OTHER"},
            ])["rows"][0]
            self.assertEqual("UNSAFE_SYMLINK", item["status"])
            self.assertNotIn("sha1", item)
            self.assertNotIn("lexical_hint_examples", item)

    def test_nonmagic_manifest_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            manifest = module.MANIFEST
            obj = json.loads(manifest.read_text(encoding="utf-8"))
            obj["rows"][0]["filename"] = "../escape.jar"
            tmp = Path(td) / "invalid.json"
            tmp.write_text(json.dumps(obj), encoding="utf-8")
            with self.assertRaises(ValueError):
                module.manifest_entries(tmp)

    def test_replaced_jar_path_cannot_mix_zip_hints_and_other_jar_hash(self):
        with tempfile.TemporaryDirectory() as td:
            mods = Path(td)
            original = mods / "provider.jar"
            replacement = mods / "replacement.jar"
            with zipfile.ZipFile(original, "w") as jar:
                jar.writestr("data/example/spells/one.json", "{}")
            with zipfile.ZipFile(replacement, "w") as jar:
                jar.writestr("data/example/recipes/iron.json", "{}")
            replacement_sha = hashlib.sha256(replacement.read_bytes()).hexdigest()
            real_zip = zipfile.ZipFile

            class SwapAfterZipRead:
                def __init__(self, source):
                    self.handle = real_zip(source)

                def __enter__(self):
                    return self.handle

                def __exit__(self, exc_type, exc, tb):
                    self.handle.close()
                    replacement.replace(original)

            with mock.patch.object(module.zipfile, "ZipFile", side_effect=SwapAfterZipRead):
                report = module.scan(mods, [{
                    "physical_number": 272, "name": "Provider",
                    "filename": "provider.jar", "triage_group": "OTHER",
                }])
            item = report["rows"][0]
            self.assertEqual("CHANGED_DURING_SCAN", item["status"])
            self.assertEqual({"CHANGED_DURING_SCAN": 1}, report["statuses"])
            self.assertNotIn("sha256", item)
            self.assertNotIn("sha1", item)
            self.assertNotIn("lexical_hint_member_count", item)
            self.assertNotIn("lexical_hint_examples", item)
            self.assertNotIn(replacement_sha, json.dumps(report))

    def test_in_place_mutation_cannot_claim_fingerprinted_hints(self):
        with tempfile.TemporaryDirectory() as td:
            mods = Path(td)
            target = mods / "provider.jar"
            updated = mods / "updated.jar"
            with zipfile.ZipFile(target, "w") as jar:
                jar.writestr("data/example/spells/one.json", "{}")
            with zipfile.ZipFile(updated, "w") as jar:
                jar.writestr("data/example/recipes/changed.json", '{"different":true}')
            changed_bytes = updated.read_bytes()
            real_zip = zipfile.ZipFile

            class RewriteOnClose:
                def __init__(self, source):
                    self.handle = real_zip(source)

                def __enter__(self):
                    return self.handle

                def __exit__(self, exc_type, exc, tb):
                    self.handle.close()
                    target.write_bytes(changed_bytes)

            with mock.patch.object(module.zipfile, "ZipFile", side_effect=RewriteOnClose):
                result = module.scan(mods, [{
                    "physical_number": 272, "name": "Provider",
                    "filename": "provider.jar", "triage_group": "OTHER",
                }])["rows"][0]
            self.assertEqual("CHANGED_DURING_SCAN", result["status"])
            self.assertNotIn("sha1", result)
            self.assertNotIn("sha256", result)
            self.assertNotIn("lexical_hint_member_count", result)

    def test_max_member_count_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            mods = Path(td)
            with zipfile.ZipFile(mods / "provider.jar", "w") as jar:
                jar.writestr("spells/x.json", "{}")
                jar.writestr("spell/y.json", "{}")
            previous = module.MAX_ARCHIVE_MEMBERS
            try:
                module.MAX_ARCHIVE_MEMBERS = 1
                item = module.scan(mods, [
                    {"physical_number": 121, "name": "Provider",
                     "filename": "provider.jar", "triage_group": "OTHER"},
                ])["rows"][0]
                self.assertEqual("TOO_MANY_MEMBERS", item["status"])
                self.assertNotIn("sha1", item)
                self.assertNotIn("lexical_hint_examples", item)
            finally:
                module.MAX_ARCHIVE_MEMBERS = previous


if __name__ == "__main__":
    unittest.main()
