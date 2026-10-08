#!/usr/bin/env python3
"""Regression tests for read-only physical provider fingerprinting."""
from __future__ import annotations

import importlib.util
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
        self.assertIn("Somake Spells", manifest)
        self.assertEqual("somakespells-1.0.9-1.21.1.jar", manifest["Somake Spells"])

    def test_fake_valid_jar_can_be_fingerprinted_without_registry_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            mods = Path(tmp) / "mods"
            mods.mkdir()
            names = collector.load_manifest()
            filename = names["Somake Spells"]
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
            observed = next(x for x in report["entries"] if x["provider"] == "Somake Spells")
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
