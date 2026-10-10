#!/usr/bin/env python3
"""Focused synthetic-JAR tests for the physical #272 metadata-only probe."""
import importlib.util
import hashlib
from unittest import mock
import json
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

TARGET = Path(__file__).with_name("nonmagic_272_metadata_probe.py")
spec = importlib.util.spec_from_file_location("nonmagic_272_metadata_probe", TARGET)
probe = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(probe)

MOD_ID = "factory_construction_registry_probe"
VALID_TOML = (
    'modLoader="javafml"\nloaderVersion="[4,)"\nlicense="MIT"\n'
    '[[mods]]\nmodId="factory_construction_registry_probe"\nversion="0.1.0"\n'
)


class MetadataProbeTest(unittest.TestCase):
    def _jar(self, root: Path, content=VALID_TOML,
             metadata_name="META-INF/neoforge.mods.toml") -> Path:
        dest = root / "factory_construction_registry_probe-0.1.0.jar"
        with zipfile.ZipFile(dest, "w") as z:
            z.writestr(metadata_name, content)
            z.writestr("data/example/spells/forbidden.json", '{"secret":"NOT COPIED"}')
        return dest

    def test_matching_binary_metadata_proves_only_mod_id_not_spells(self):
        with tempfile.TemporaryDirectory() as td:
            result = probe.inspect_272_metadata(self._jar(Path(td)), MOD_ID)
        self.assertEqual("MATCHED_EMBEDDED_MOD_ID", result["status"])
        self.assertEqual([MOD_ID], result["embedded_mod_ids"])
        self.assertEqual(64, len(result["sha256"]))
        self.assertFalse(result["registry_entries_verified"])
        self.assertFalse(result["survival_acquisition_verified"])
        self.assertIsNone(result["spell_count"])
        self.assertNotIn("NOT COPIED", json.dumps(result))
        self.assertNotIn("forbidden.json", json.dumps(result))

    def test_version_literal_match_does_not_prove_registry(self):
        with tempfile.TemporaryDirectory() as td:
            record = probe.inspect_272_metadata(self._jar(Path(td)), MOD_ID, "0.1.0")
        self.assertEqual("MATCHED_EMBEDDED_MOD_ID", record["status"])
        self.assertEqual("MATCHED_SOURCE_LITERAL", record["version_evidence"])
        self.assertEqual("0.1.0", record["embedded_version"])
        self.assertFalse(record["registry_entries_verified"])

    def test_version_mismatch_is_not_promoted_from_mod_id_match(self):
        with tempfile.TemporaryDirectory() as td:
            jar = self._jar(Path(td), VALID_TOML.replace('version="0.1.0"', 'version="9.9.9"'))
            record = probe.inspect_272_metadata(jar, MOD_ID, "0.1.0")
        self.assertEqual("MATCHED_EMBEDDED_MOD_ID", record["status"])
        self.assertEqual("MISMATCHED_SOURCE_LITERAL", record["version_evidence"])
        self.assertEqual("9.9.9", record["embedded_version"])
        self.assertFalse(record["registry_entries_verified"])

    def test_template_version_remains_unresolved(self):
        with tempfile.TemporaryDirectory() as td:
            jar = self._jar(Path(td), VALID_TOML.replace('version="0.1.0"', 'version="${file.jarVersion}"'))
            record = probe.inspect_272_metadata(jar, MOD_ID, "0.1.0")
        self.assertEqual("UNRESOLVED_TEMPLATE", record["version_evidence"])
        self.assertEqual("${file.jarVersion}", record["embedded_version"])

    def test_version_gate_selects_matching_mod_id_in_multi_mod_metadata(self):
        other = '[[mods]]\nmodId="other_mod"\nversion="9.9.9"\n'
        with tempfile.TemporaryDirectory() as td:
            record = probe.inspect_272_metadata(self._jar(Path(td), VALID_TOML + other), MOD_ID, "0.1.0")
        self.assertEqual("MATCHED_SOURCE_LITERAL", record["version_evidence"])
        self.assertEqual("0.1.0", record["embedded_version"])

    def test_version_from_pinned_probe_instance_is_checked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "mods").mkdir()
            self._jar(root / "mods", VALID_TOML.replace('version="0.1.0"', 'version="9.9.9"'))
            manifest = root / "manifest.json"
            provenance = root / "provenance.json"
            manifest.write_text(json.dumps({"source_commit": probe.SOURCE_COMMIT, "rows": [{
                "physical_number": 272, "name": "Factory Construction Registry Probe",
                "filename": "factory_construction_registry_probe-0.1.0.jar",
                "version": "0.1.0", "triage_group": "OTHER",
            }]}), encoding="utf-8")
            provenance.write_text(json.dumps({
                "snapshot": {"commit": probe.SOURCE_COMMIT},
                "physical_number": 272,
                "observed_from_pinned_sibling": {
                    "jar_filename": "factory_construction_registry_probe-0.1.0.jar",
                    "version": "0.1.0", "declared_mod_id": MOD_ID,
                    "dossier_available": False,
                },
            }), encoding="utf-8")
            record = probe.probe_instance(root, manifest, provenance)
        self.assertEqual("MISMATCHED_SOURCE_LITERAL", record["version_evidence"])
        self.assertEqual("0.1.0", record["expected_version"])

    def test_missing_and_non_zip_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            missing = root / "notfound.jar"
            self.assertEqual("MISSING_JAR",
                             probe.inspect_272_metadata(missing, MOD_ID)["status"])
            bad = root / "broken.jar"
            bad.write_bytes(b"badjar")
            self.assertEqual("INVALID_JAR",
                             probe.inspect_272_metadata(bad, MOD_ID)["status"])

    def test_mismatch_not_misclassified_as_match(self):
        with tempfile.TemporaryDirectory() as td:
            data = VALID_TOML.replace(MOD_ID, "some_other_mod")
            result = probe.inspect_272_metadata(self._jar(Path(td), data), MOD_ID)
        self.assertEqual("MOD_ID_MISMATCH", result["status"])
        self.assertEqual(["some_other_mod"], result["embedded_mod_ids"])
        self.assertFalse(result["registry_entries_verified"])

    def test_missing_and_oversized_metadata_are_blocking(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            no_metadata = self._jar(root, metadata_name="data/not-metadata.toml")
            self.assertEqual(
                "MISSING_NEOFORGE_METADATA",
                probe.inspect_272_metadata(no_metadata, MOD_ID)["status"],
            )
            oversized = self._jar(root, VALID_TOML + ("# filler\n" * 9000))
            self.assertEqual(
                "METADATA_OVERSIZED",
                probe.inspect_272_metadata(oversized, MOD_ID)["status"],
            )

    def test_malformed_and_duplicate_metadata_are_blocking(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            malformed = self._jar(root, '[[mods]\nmodId="broken"')
            self.assertEqual(
                "INVALID_NEOFORGE_METADATA",
                probe.inspect_272_metadata(malformed, MOD_ID)["status"],
            )
            jar = root / "factory_construction_registry_probe-0.1.0.jar"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                with zipfile.ZipFile(jar, "w") as z:
                    z.writestr("META-INF/neoforge.mods.toml", VALID_TOML)
                    z.writestr("META-INF/neoforge.mods.toml", VALID_TOML)
            self.assertEqual(
                "AMBIGUOUS_NEOFORGE_METADATA",
                probe.inspect_272_metadata(jar, MOD_ID)["status"],
            )

    def test_pinned_provenance_selects_only_manifest_272_filename(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "mods").mkdir()
            jar = self._jar(root / "mods")
            manifest = root / "manifest.json"
            provenance = root / "provenance.json"
            source = {"source_commit": probe.SOURCE_COMMIT, "rows": [{
                "physical_number": 272, "name": "Factory Construction Registry Probe",
                "filename": jar.name, "version": "0.1.0", "triage_group": "OTHER",
            }]}
            evidence = {
                "snapshot": {"commit": probe.SOURCE_COMMIT},
                "physical_number": 272,
                "observed_from_pinned_sibling": {
                    "jar_filename": jar.name, "version": "0.1.0",
                    "declared_mod_id": MOD_ID, "dossier_available": False,
                },
            }
            manifest.write_text(json.dumps(source), encoding="utf-8")
            provenance.write_text(json.dumps(evidence), encoding="utf-8")
            result = probe.probe_instance(root, manifest, provenance)
            self.assertEqual("MATCHED_EMBEDDED_MOD_ID", result["status"])
            self.assertEqual(272, result["physical_number"])
            self.assertEqual(jar.name, result["filename"])
            source["source_commit"] = "unverified-sha"
            manifest.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "provenance mismatch"):
                probe.probe_instance(root, manifest, provenance)

    def test_replaced_path_does_not_mix_metadata_and_sha256(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jar = self._jar(root)
            original_hash = hashlib.sha256(jar.read_bytes()).hexdigest()
            replacement = root / "replacement.jar"
            with zipfile.ZipFile(replacement, "w") as z:
                z.writestr(
                    "META-INF/neoforge.mods.toml",
                    VALID_TOML.replace(MOD_ID, "other_mod"),
                )
            replacement_hash = hashlib.sha256(replacement.read_bytes()).hexdigest()
            self.assertNotEqual(original_hash, replacement_hash)
            real_zip = zipfile.ZipFile

            class SwappingZip:
                def __init__(self, source):
                    self.handle = real_zip(source)

                def __enter__(self):
                    return self.handle

                def __exit__(self, exc_type, exc, tb):
                    self.handle.close()
                    replacement.replace(jar)

            with mock.patch.object(probe.zipfile, "ZipFile", side_effect=SwappingZip):
                result = probe.inspect_272_metadata(jar, MOD_ID)
            self.assertEqual("CHANGED_DURING_SCAN", result["status"])
            self.assertNotIn("sha256", result)
            self.assertNotIn("embedded_mod_ids", result)

    def test_symlink_never_scanned(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jar = self._jar(root)
            link = root / "shortcut.jar"
            link.symlink_to(jar)
            self.assertEqual(
                "UNSAFE_SYMLINK",
                probe.inspect_272_metadata(link, MOD_ID)["status"],
            )


if __name__ == "__main__":
    unittest.main()
