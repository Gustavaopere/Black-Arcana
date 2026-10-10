#!/usr/bin/env python3
"""Regression tests for read-only physical provider fingerprinting."""
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
COLLECTOR = ROOT / "docs/qa/physical_provider_fingerprint_collector.py"
spec = importlib.util.spec_from_file_location("physical_provider_fingerprints", COLLECTOR)
collector = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(collector)


class PhysicalProviderFingerprintTest(unittest.TestCase):
    def test_manifest_tracks_all_69_unique_physical_jars(self):
        manifest = collector.load_manifest()
        self.assertEqual(69, len(manifest))
        self.assertEqual(69, len(set(manifest.values())))
        self.assertIn("Ars Nouveau", manifest)
        self.assertEqual("ars_nouveau-1.21.1-5.13.1.jar", manifest["Ars Nouveau"])

    def test_fake_valid_jar_can_be_fingerprinted_without_registry_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            mods = Path(tmp) / "mods"
            mods.mkdir()
            names = collector.load_manifest()
            filename = names["Ars Nouveau"]
            with zipfile.ZipFile(mods / filename, "w") as archive:
                archive.writestr("META-INF/MANIFEST.MF", "Fixture, not a real mod")
            report = collector.fingerprint_instance(mods, names)
            self.assertEqual(69, report["expected"])
            self.assertEqual(1, report["counts"]["FINGERPRINTED"])
            self.assertEqual(68, report["counts"]["MISSING"])
            self.assertEqual(
                "READ_ONLY_JAR_FINGERPRINT_NOT_REGISTRY_PROOF",
                report["evidence_class"],
            )
            observed = next(x for x in report["entries"] if x["provider"] == "Ars Nouveau")
            self.assertEqual(40, len(observed["sha1"]))
            self.assertEqual(64, len(observed["sha256"]))
            self.assertEqual("FINGERPRINTED", observed["status"])
            self.assertNotIn("Fixture, not a real mod", json.dumps(report))

    def test_invalid_jar_is_not_fingerprinted(self):
        with tempfile.TemporaryDirectory() as tmp:
            mods = Path(tmp)
            (mods / "some-provider.jar").write_bytes(b"not a zip")
            report = collector.fingerprint_instance(mods, {"test": "some-provider.jar"})
            self.assertEqual(1, report["counts"]["INVALID_JAR"])
            self.assertNotIn("sha1", report["entries"][0])

    def test_wrong_filename_is_not_treated_as_correct_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            mods = Path(tmp)
            with zipfile.ZipFile(mods / "somakespells-1.0.8.jar", "w") as jar:
                jar.writestr("fixture.txt", "test")
            report = collector.fingerprint_instance(
                mods, {"Somake Spells": "somakespells-1.0.9-1.21.1.jar"}
            )
            self.assertEqual(1, report["counts"]["MISSING"])

    def test_symlinked_provider_jar_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            mods = Path(tmp) / "mods"
            mods.mkdir()
            outside = Path(tmp) / "outside.jar"
            with zipfile.ZipFile(outside, "w") as jar:
                jar.writestr("x", "x")
            (mods / "some-provider.jar").symlink_to(outside)
            report = collector.fingerprint_instance(mods, {"provider": "some-provider.jar"})
            self.assertEqual(1, report["counts"]["UNSAFE"])

    def test_replaced_path_never_mixes_old_jar_validation_with_new_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            mods = Path(tmp)
            filename = "ars_nouveau-1.21.1-5.13.1.jar"
            current = mods / filename
            replacement = mods / "replacement.jar"
            with zipfile.ZipFile(current, "w") as jar:
                jar.writestr("data/example/spells/alpha.json", "{}")
            with zipfile.ZipFile(replacement, "w") as jar:
                jar.writestr("data/example/recipes/new.json", '{"changed":true}')
            wrong_sha = hashlib.sha256(replacement.read_bytes()).hexdigest()
            original_sha1 = hashlib.sha1

            def replace_before_fingerprinting():
                replacement.replace(current)
                return original_sha1()

            with mock.patch.object(
                collector.hashlib, "sha1", side_effect=replace_before_fingerprinting
            ):
                report = collector.fingerprint_instance(
                    mods, {"Ars Nouveau": filename}
                )
            item = report["entries"][0]
            self.assertEqual("CHANGED_DURING_SCAN", item["status"])
            self.assertEqual(1, report["counts"]["CHANGED_DURING_SCAN"])
            self.assertNotIn("sha1", item)
            self.assertNotIn("sha256", item)
            self.assertNotIn(wrong_sha, json.dumps(report))

    def test_in_place_change_during_hash_must_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            mods = Path(tmp)
            filename = "ars_nouveau-1.21.1-5.13.1.jar"
            current = mods / filename
            with zipfile.ZipFile(current, "w") as jar:
                jar.writestr("data/example/spells/alpha.json", "{}")
            replacement = mods / "replacement.jar"
            with zipfile.ZipFile(replacement, "w") as jar:
                jar.writestr("data/example/recipes/different.json", '{"x":true}')
            new_bytes = replacement.read_bytes()
            original_sha1 = hashlib.sha1

            def rewrite_before_fingerprinting():
                current.write_bytes(new_bytes)
                return original_sha1()

            with mock.patch.object(
                collector.hashlib, "sha1", side_effect=rewrite_before_fingerprinting
            ):
                report = collector.fingerprint_instance(
                    mods, {"Ars Nouveau": filename}
                )
            item = report["entries"][0]
            self.assertEqual("CHANGED_DURING_SCAN", item["status"])
            self.assertEqual(1, report["counts"]["CHANGED_DURING_SCAN"])
            self.assertNotIn("sha1", item)
            self.assertNotIn("sha256", item)

    def test_directory_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside"
            outside.mkdir()
            link = Path(tmp) / "mods"
            link.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                collector.fingerprint_instance(link, {})


if __name__ == "__main__":
    unittest.main()
