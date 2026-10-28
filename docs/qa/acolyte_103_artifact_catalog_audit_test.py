#!/usr/bin/env python3
"""Adversarial ZIP/manifest tests without redistributing a publisher artifact."""
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import warnings
import zipfile
import acolyte_103_artifact_catalog_audit as audit


class ArtifactCatalogTests(unittest.TestCase):
    def fixture(self, members=None):
        if members is None:
            members = [("example/", b""), ("empty/", b""),
                       ("example/Actor.class", b"\xca\xfe\xba\xbe\x00\x00\x00\x41"),
                       ("data.json", b"{}")]
        stream = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(stream, "w") as archive:
                for path, body in members:
                    archive.writestr(path, body)
        blob = stream.getvalue()
        identity = (hashlib.sha1(blob).hexdigest(), hashlib.sha256(blob).hexdigest(), len(blob))
        card = "✅-acolyte/systems/fixture.md"
        files = [{"path": path, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                  "catalog_refs": ["SYSTEM:fixture"]} for path, body in members if not path.endswith("/")]
        dirs = [path for path, _ in members if path.endswith("/")]
        doc = {"schema_version": 1, "version": "1.0.3", **audit.LIMITS,
               "artifact_sha1": identity[0], "artifact_sha256": identity[1],
               "artifact_size_bytes": identity[2], "artifact_files": files,
               "artifact_directories": dirs, "archive_entry_count": len(members),
               "artifact_file_count": len(files), "artifact_directory_count": len(dirs),
               "class_file_count": sum(path.endswith(".class") for path, _ in members),
               "cards": {card: hashlib.sha256(b"# fixture\n").hexdigest()},
               "catalog_objects": {"SYSTEM:fixture": card}, "aggregates": {}}
        return blob, doc, identity

    def check(self, blob, doc, identity):
        return audit.validate_archive(blob, doc, expected_identity=identity)

    def test_valid_fixture_has_bounded_claims(self):
        blob, doc, identity = self.fixture()
        result = self.check(blob, doc, identity)
        self.assertEqual("PASS_PUBLISHER_ZIP_CROSSWALK_ONLY", result["result"])
        self.assertEqual(2, result["artifact_file_count"])
        self.assertEqual(2, result["artifact_directory_count"])
        for key, value in audit.LIMITS.items():
            self.assertEqual(value, result[key])

    def test_default_pinned_validator_rejects_self_consistent_other_artifact(self):
        blob, doc, _ = self.fixture()
        with self.assertRaisesRegex(audit.AuditError, "artifact identity mismatch"):
            audit.validate_archive(blob, doc)

    def test_identity_or_scope_tampering_rejected(self):
        for key, value in (("artifact_sha1", "a" * 40), ("artifact_sha256", "b" * 64),
                           ("artifact_size_bytes", True), ("schema_version", True),
                           ("version", "other"), ("source_revision", "invented/repo@main"),
                           ("claim_scope", "CATALOG_SOURCE_SCOPE_ONLY"),
                           ("installed_artifact_identity", "VERIFIED"),
                           ("physical_qa", "PHYSICALLY_VERIFIED"),
                           ("mutating_hook", "VERIFIED_CONTRACT")):
            with self.subTest(key=key):
                blob, doc, identity = self.fixture(); doc[key] = value
                with self.assertRaises(audit.AuditError): self.check(blob, doc, identity)

    def test_duplicate_zip_member_rejected_even_with_valid_hash(self):
        blob, doc, identity = self.fixture([("same.txt", b"first"), ("same.txt", b"second")])
        doc["artifact_files"] = doc["artifact_files"][:1]
        doc["artifact_file_count"] = 1
        with self.assertRaisesRegex(audit.AuditError, "duplicate archive path"):
            self.check(blob, doc, identity)

    def test_noncanonical_zip_paths_rejected(self):
        for path in ("../x", "/x", "a//x", "a/./x", "a\\x", "a/../x", "../empty/"):
            with self.subTest(path=path):
                blob, doc, identity = self.fixture([(path, b"x")])
                with self.assertRaises(audit.AuditError): self.check(blob, doc, identity)

    def test_duplicate_manifest_member_rejected(self):
        blob, doc, identity = self.fixture()
        doc["artifact_files"].append(dict(doc["artifact_files"][0]))
        with self.assertRaises(audit.AuditError): self.check(blob, doc, identity)

    def test_missing_and_extra_member_rejected(self):
        for mode in ("missing", "extra"):
            with self.subTest(mode=mode):
                blob, doc, identity = self.fixture()
                if mode == "missing": doc["artifact_files"].pop()
                else: doc["artifact_files"].append({"path": "extra.txt", "bytes": 0,
                        "sha256": "a" * 64, "catalog_refs": ["SYSTEM:fixture"]})
                with self.assertRaisesRegex(audit.AuditError, "path mismatch"):
                    self.check(blob, doc, identity)

    def test_wrong_member_hash_size_and_types_rejected(self):
        for key, value in (("sha256", "a" * 64), ("sha256", int("1" * 64)),
                           ("bytes", True), ("bytes", -1), ("bytes", 999)):
            with self.subTest(key=key, value=value):
                blob, doc, identity = self.fixture(); doc["artifact_files"][0][key] = value
                with self.assertRaises(audit.AuditError): self.check(blob, doc, identity)

    def test_directory_path_set_matters_even_with_equal_count(self):
        blob, doc, identity = self.fixture()
        doc["artifact_directories"][1] = "other-empty/"
        with self.assertRaisesRegex(audit.AuditError, "path mismatch"):
            self.check(blob, doc, identity)

    def test_directory_alias_and_duplicate_rejected(self):
        for value in ("./empty/", "example/", "empty//"):
            with self.subTest(value=value):
                blob, doc, identity = self.fixture(); doc["artifact_directories"][1] = value
                with self.assertRaises(audit.AuditError): self.check(blob, doc, identity)

    def test_count_types_and_values_rejected(self):
        for key in ("artifact_file_count", "class_file_count", "archive_entry_count",
                    "artifact_directory_count"):
            for value in (True, 0):
                with self.subTest(key=key, value=value):
                    blob, doc, identity = self.fixture(); doc[key] = value
                    with self.assertRaises(audit.AuditError): self.check(blob, doc, identity)

    def test_class_header_and_declared_major_rejected(self):
        for body in (b"bad", b"\xca\xfe\xba\xbe\x00\x00\x00\x40"):
            blob, doc, identity = self.fixture([("Actor.class", body)])
            with self.assertRaisesRegex(audit.AuditError, "classfile header"):
                self.check(blob, doc, identity)
        blob, doc, identity = self.fixture(); doc["artifact_files"][0]["class_major_version"] = True
        with self.assertRaisesRegex(audit.AuditError, "classfile major mismatch"):
            self.check(blob, doc, identity)

    def test_crosswalk_unknown_or_orphan_object_rejected(self):
        for mode in ("unknown", "orphan", "alias"):
            with self.subTest(mode=mode):
                blob, doc, identity = self.fixture()
                if mode == "unknown": doc["artifact_files"][0]["catalog_refs"] = ["MISSING:id"]
                elif mode == "orphan":
                    doc["aggregates"]["SUPPORT:id"] = {}
                    for item in doc["artifact_files"]: item["catalog_refs"] = ["SUPPORT:id"]
                else: doc["catalog_objects"]["EXTRA:id"] = next(iter(doc["cards"]))
                with self.assertRaises(audit.AuditError): self.check(blob, doc, identity)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text('{"schema_version":1,"schema_version":1}')
            with self.assertRaisesRegex(audit.AuditError, "duplicate JSON key"):
                audit.load_manifest(path)

    def test_real_card_content_must_match_and_stay_in_provider(self):
        _, doc, _ = self.fixture()
        with tempfile.TemporaryDirectory() as directory:
            providers = Path(directory); card = providers / next(iter(doc["cards"]))
            card.parent.mkdir(parents=True); card.write_bytes(b"# fixture\n")
            audit.validate_card_files(doc, providers)
            card.write_bytes(b"# changed\n")
            with self.assertRaisesRegex(audit.AuditError, "card hash mismatch"):
                audit.validate_card_files(doc, providers)
            doc["cards"] = {"../outside.md": "a" * 64}
            with self.assertRaises(audit.AuditError): audit.validate_card_files(doc, providers)


if __name__ == "__main__":
    unittest.main()
