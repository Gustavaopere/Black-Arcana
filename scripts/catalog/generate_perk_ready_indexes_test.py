#!/usr/bin/env python3
"""Test generator and checker agree without certifying undocumented perks."""
import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import check_perk_ready_indexes as checker
import generate_perk_ready_indexes as generator

class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        self.root = self.repo / "wiki/modpack-catalog/providers"
        self.leaf = self.root / "✅-sample" / "skills" / "individual"
        self.leaf.mkdir(parents=True)
        (self.leaf / "air-dash.md").write_text("# Air Dash\n", encoding="utf8")
        self.meta = self.repo / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
        self.meta.parent.mkdir(parents=True)
        self.meta.write_text(json.dumps({
            "schema_version": 1, "objects": {}, "providers": {}, "known_rosters": {}
        }), encoding="utf8")
        self.patch1 = patch.object(checker, "PROVIDERS", self.root)
        self.patch2 = patch.object(checker, "LEDGER", self.meta)
        self.patch3 = patch.object(generator, "ROOT", self.root)
        self.patch1.start()
        self.patch2.start()
        self.patch3.start()

    def tearDown(self):
        self.patch3.stop()
        self.patch2.stop()
        self.patch1.stop()
        self.temp.cleanup()

    def render(self):
        ledger = checker.read_ledger(checker.LEDGER)
        dirs, mods, cards = checker.inventory()
        alphabetical = generator.alphabetical_scope(mods, cards)
        for folder in dirs:
            (folder / "INDEX.md").write_text(
                generator.directory_index(folder, dirs, cards, ledger,
                                          alphabetical=alphabetical), encoding="utf8")
        (self.root / "INDEX.md").write_text(
            generator.global_index(mods, cards, ledger, alphabetical=alphabetical),
            encoding="utf8")

    def source_scope_fixture(self):
        """A complete source-only catalog which must not certify executable perks."""
        provider = "✅-sample"
        revision = "example/Source@" + "a" * 40
        card = self.leaf / "air-dash.md"
        card.write_text("# Air Dash\nA source catalog card without a perk dossier.\n", encoding="utf8")
        relative = card.relative_to(self.root).as_posix()
        proof = self.root / provider / "SOURCE-CLOSURE.md"
        proof.write_text("\n".join((
            "CATALOG_SOURCE_SCOPE_ONLY", revision,
            "version=1.0", "artifact_sha1=" + "b" * 40,
            "physical_qa=NOT_TESTED", "mutating_hook=NOT_VERIFIED")), encoding="utf8")
        manifest = self.root / provider / "SOURCE-MANIFEST.json"
        manifest.write_text(json.dumps({
            "schema_version": 1, "source_revision": revision, "version": "1.0",
            "artifact_sha1": "b" * 40,
            "claim_scope": "CATALOG_SOURCE_SCOPE_ONLY",
            "physical_qa": "NOT_TESTED", "mutating_hook": "NOT_VERIFIED",
            "cards": {relative: hashlib.sha256(card.read_bytes()).hexdigest()},
            "catalog_objects": {"SYSTEM:air-dash": relative}, "aggregates": {},
            "source_file_count": 1, "java_file_count": 1,
            "source_files": [{"path": "src/main/java/Source.java",
                              "sha256": "c" * 64,
                              "catalog_refs": ["SYSTEM:air-dash"]}],
        }), encoding="utf8")
        status = self.meta.parent / "ALPHABETICAL-CATALOG-STATUS.json"
        status.write_text(json.dumps({
            "schema_version": 1, "order": "provider_directory_name_ascending",
            "completed_prefix": [{
                "provider": provider, "state": "SOURCE_VERSION_CATALOG_CLOSED",
                "source_revision": revision, "version": "1.0",
                "artifact_sha1": "b" * 40,
                "physical_qa": "NOT_TESTED", "mutating_hook": "NOT_VERIFIED",
                "evidence": proof.relative_to(self.root).as_posix(),
                "catalog_manifest": manifest.relative_to(self.root).as_posix(),
            }], "next_provider": None,
        }), encoding="utf8")
        return card, proof, manifest, status

    def test_source_scope_closure_does_not_certify_perks_or_call_library_nonmagical(self):
        card, _, _, _ = self.source_scope_fixture()
        self.assertNotIn("technical_perk_dossier", card.read_text())
        self.render()
        global_text = (self.root / "INDEX.md").read_text(encoding="utf8")
        provider_text = (self.root / "✅-sample/INDEX.md").read_text(encoding="utf8")
        self.assertIn("0 sem ações mágicas próprias e 1 com catálogo", global_text)
        self.assertIn("catálogo da versão-fonte documentado", global_text)
        self.assertIn("✅ 1/1 fichas do escopo documentado", provider_text)
        self.assertIn("Barra do catálogo da versão-fonte", provider_text)
        self.assertIn("████████████████████ 100.0%", provider_text)
        self.assertIn("⚠️ NÃO HOMOLOGADO como 100%", provider_text)
        self.assertIn("Homologadas para perks (somente fichas detectadas): 0/1", provider_text)
        self.assertEqual([], checker.check(self.repo)["problems"])

    def test_source_scope_rejects_new_uncovered_card(self):
        self.source_scope_fixture()
        (self.leaf / "new-effect.md").write_text("# Uncovered\n", encoding="utf8")
        with self.assertRaisesRegex(ValueError, "exactly the detected cards"):
            self.render()

    def test_source_scope_rejects_edited_card_without_fresh_evidence(self):
        card, _, _, _ = self.source_scope_fixture()
        card.write_text(card.read_text() + "Changed behavior\n", encoding="utf8")
        with self.assertRaisesRegex(ValueError, "card changed"):
            self.render()

    def test_source_scope_rejects_mutable_revision_and_physical_claim(self):
        for field, value in (("source_revision", "example/Source@main"),
                             ("physical_qa", "PHYSICALLY_VERIFIED")):
            with self.subTest(field=field):
                _, _, _, status = self.source_scope_fixture()
                data = json.loads(status.read_text())
                data["completed_prefix"][0][field] = value
                status.write_text(json.dumps(data), encoding="utf8")
                with self.assertRaisesRegex(ValueError, "bounded identity or QA limits"):
                    self.render()

    def test_source_scope_rejects_missing_source_only_limit(self):
        _, proof, _, _ = self.source_scope_fixture()
        proof.write_text(proof.read_text().replace("CATALOG_SOURCE_SCOPE_ONLY", ""))
        with self.assertRaisesRegex(ValueError, "source-only limits"):
            self.render()

    def test_source_scope_rejects_missing_or_partial_proof_identity(self):
        for token in ("CATALOG_SOURCE_SCOPE_ONLY", "example/Source@" + "a" * 40,
                      "version=1.0", "artifact_sha1=" + "b" * 40,
                      "physical_qa=NOT_TESTED", "mutating_hook=NOT_VERIFIED"):
            with self.subTest(token=token):
                _, proof, _, _ = self.source_scope_fixture()
                # A prefix or prose mention cannot act as an exact proof marker.
                proof.write_text(proof.read_text().replace(token, "prose " + token + "0"),
                                 encoding="utf8")
                with self.assertRaisesRegex(ValueError, "source-only limits"):
                    self.render()

    def test_source_scope_rejects_nonstring_artifact_hash(self):
        _, proof, manifest, status = self.source_scope_fixture()
        numeric_hash = 1234567890123456789012345678901234567890
        data = json.loads(status.read_text())
        data["completed_prefix"][0]["artifact_sha1"] = numeric_hash
        status.write_text(json.dumps(data), encoding="utf8")
        data = json.loads(manifest.read_text())
        data["artifact_sha1"] = numeric_hash
        manifest.write_text(json.dumps(data), encoding="utf8")
        proof.write_text(proof.read_text().replace("b" * 40, str(numeric_hash)), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "bounded identity or QA limits"):
            self.render()

    def test_source_scope_rejects_nonstring_source_hash(self):
        _, _, manifest, _ = self.source_scope_fixture()
        data = json.loads(manifest.read_text())
        data["source_files"][0]["sha256"] = int("1" * 64)
        manifest.write_text(json.dumps(data), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "invalid or unmapped"):
            self.render()

    def test_source_scope_rejects_boolean_or_float_schema_and_counts(self):
        for field in ("schema_version", "source_file_count", "java_file_count"):
            for value in (True, 1.0):
                with self.subTest(field=field, value=value):
                    _, _, manifest, _ = self.source_scope_fixture()
                    data = json.loads(manifest.read_text())
                    data[field] = value
                    manifest.write_text(json.dumps(data), encoding="utf8")
                    with self.assertRaises(ValueError):
                        self.render()

    def test_alphabetical_scope_rejects_boolean_or_float_schema(self):
        for value in (True, 1.0):
            with self.subTest(value=value):
                _, _, _, status = self.source_scope_fixture()
                data = json.loads(status.read_text())
                data["schema_version"] = value
                status.write_text(json.dumps(data), encoding="utf8")
                with self.assertRaisesRegex(ValueError, "ledger schema"):
                    self.render()

    def test_source_scope_rejects_nonstring_aggregate_reason(self):
        for reason in (["This aggregate has a long but invalid list rationale"],
                       {"explanation": "This object is not a rationale string"}):
            with self.subTest(reason=reason):
                _, proof, manifest, _ = self.source_scope_fixture()
                data = json.loads(manifest.read_text())
                data["aggregates"]["SYSTEM:aggregate"] = {
                    "reason": reason, "evidence": proof.relative_to(self.root).as_posix(),
                }
                manifest.write_text(json.dumps(data), encoding="utf8")
                with self.assertRaisesRegex(ValueError, "bounded rationale"):
                    self.render()

    def test_source_scope_accepts_mapped_aggregate_without_certifying_provider(self):
        _, proof, manifest, _ = self.source_scope_fixture()
        data = json.loads(manifest.read_text())
        data["aggregates"]["SYSTEM:helpers"] = {
            "reason": "Internal helpers are grouped without claiming individual magical actions.",
            "evidence": proof.relative_to(self.root).as_posix(),
        }
        data["source_files"][0]["catalog_refs"].append("SYSTEM:helpers")
        manifest.write_text(json.dumps(data), encoding="utf8")
        self.render()
        ledger = checker.read_ledger(checker.LEDGER)
        _, _, cards = checker.inventory()
        self.assertFalse(checker.mod_certified(self.root / "✅-sample", cards, ledger))

    def test_source_scope_rejects_duplicate_json_keys(self):
        for artifact in ("status", "manifest"):
            for key in ("schema_version", "source_revision"):
                with self.subTest(artifact=artifact, key=key):
                    _, _, manifest, status = self.source_scope_fixture()
                    path = status if artifact == "status" else manifest
                    raw = path.read_text()
                    value = "1" if key == "schema_version" else json.dumps(
                        "example/Source@" + "a" * 40)
                    # For the status source_revision lives inside completed_prefix;
                    # the pairs hook must reject nested duplicates as well.
                    needle = json.dumps(key) + ": " + value
                    path.write_text(raw.replace(needle, needle + ", " + needle, 1),
                                    encoding="utf8")
                    with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                        self.render()

    def test_source_scope_rejects_noncanonical_source_paths(self):
        for relative in ("./src/main/java/Source.java", "src//main/java/Source.java",
                         "src/main/./java/Source.java", "src\\main\\java\\Source.java",
                         "/src/main/java/Source.java", "C:/src/main/java/Source.java",
                         "src/main/java/../Source.java", "src/main/java/Source.java/"):
            with self.subTest(relative=relative):
                _, _, manifest, _ = self.source_scope_fixture()
                data = json.loads(manifest.read_text())
                data["source_files"][0]["path"] = relative
                data["java_file_count"] = int(relative.endswith(".java"))
                manifest.write_text(json.dumps(data), encoding="utf8")
                with self.assertRaisesRegex(ValueError, "invalid or unmapped"):
                    self.render()

    def test_source_scope_rejects_aliases_counted_as_separate_source_files(self):
        for alias in ("./src/main/java/Source.java", "src//main/java/Source.java"):
            with self.subTest(alias=alias):
                _, _, manifest, _ = self.source_scope_fixture()
                data = json.loads(manifest.read_text())
                data["source_files"].append(dict(data["source_files"][0], path=alias))
                data["source_file_count"] = data["java_file_count"] = 2
                manifest.write_text(json.dumps(data), encoding="utf8")
                with self.assertRaisesRegex(ValueError, "invalid or unmapped"):
                    self.render()

    def test_source_scope_rejects_noncanonical_local_evidence_paths(self):
        for field in ("evidence", "catalog_manifest"):
            for mutation in ("dot", "double-slash", "backslash", "absolute", "parent"):
                with self.subTest(field=field, mutation=mutation):
                    _, _, _, status = self.source_scope_fixture()
                    data = json.loads(status.read_text())
                    item = data["completed_prefix"][0]
                    path = item[field]
                    item[field] = {
                        "dot": path.replace("/", "/./", 1),
                        "double-slash": path.replace("/", "//", 1),
                        "backslash": path.replace("/", "\\", 1),
                        "absolute": "/" + path,
                        "parent": path.replace("/", "/../", 1),
                    }[mutation]
                    status.write_text(json.dumps(data), encoding="utf8")
                    with self.assertRaisesRegex(ValueError, "unsafe alphabetical evidence"):
                        self.render()

    def test_generator_validates_source_scope_once_per_run_without_stale_cache(self):
        card, _, _, _ = self.source_scope_fixture()
        with patch.object(generator.sys, "argv", ["generate_perk_ready_indexes.py"]), \
                patch("builtins.print"), \
                patch.object(generator, "alphabetical_scope",
                             wraps=generator.alphabetical_scope) as validate:
            self.assertEqual(0, generator.main())
            validate.assert_called_once()
            card.write_text(card.read_text() + "Changed after previous invocation\n", encoding="utf8")
            with self.assertRaisesRegex(ValueError, "card changed"):
                generator.main()

    def test_source_scope_rejects_manifest_from_different_release(self):
        _, _, manifest, _ = self.source_scope_fixture()
        data = json.loads(manifest.read_text())
        data["version"] = "wrong"
        manifest.write_text(json.dumps(data), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            self.render()

    def test_source_scope_rejects_missing_or_contradictory_manifest_limits(self):
        for field, contradictory in (("claim_scope", "SHA_EXACT_BINARY_BEHAVIOR"),
                                     ("physical_qa", "PHYSICALLY_VERIFIED"),
                                     ("mutating_hook", "VERIFIED_CONTRACT")):
            for value in (None, contradictory):
                with self.subTest(field=field, value=value):
                    _, _, manifest, _ = self.source_scope_fixture()
                    data = json.loads(manifest.read_text())
                    if value is None:
                        del data[field]
                    else:
                        data[field] = value
                    manifest.write_text(json.dumps(data), encoding="utf8")
                    with self.assertRaisesRegex(ValueError, "manifest lacks explicit source-only limits"):
                        self.render()

    def test_source_scope_rejects_collapsing_two_objects_into_one_card(self):
        _, _, manifest, _ = self.source_scope_fixture()
        data = json.loads(manifest.read_text())
        data["catalog_objects"]["SYSTEM:unjustified-alias"] = next(iter(data["cards"]))
        manifest.write_text(json.dumps(data), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "crosswalk is incomplete"):
            self.render()

    def test_source_scope_rejects_catalog_object_without_inspected_source_reference(self):
        _, _, manifest, _ = self.source_scope_fixture()
        orphan = self.leaf / "wind-shield.md"
        orphan.write_text("# Wind Shield\n", encoding="utf8")
        relative = orphan.relative_to(self.root).as_posix()
        data = json.loads(manifest.read_text())
        data["cards"][relative] = hashlib.sha256(orphan.read_bytes()).hexdigest()
        data["catalog_objects"]["SYSTEM:wind-shield"] = relative
        manifest.write_text(json.dumps(data), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "lack inspected source references"):
            self.render()

    def test_source_scope_rejects_empty_catalog_keys(self):
        for dictionary in ("catalog_objects", "aggregates"):
            with self.subTest(dictionary=dictionary):
                _, proof, manifest, _ = self.source_scope_fixture()
                data = json.loads(manifest.read_text())
                if dictionary == "catalog_objects":
                    value = data[dictionary].pop("SYSTEM:air-dash")
                    data["source_files"][0]["catalog_refs"] = ["   "]
                else:
                    value = {"reason": "Internal helpers have a bounded aggregate rationale.",
                             "evidence": proof.relative_to(self.root).as_posix()}
                data[dictionary]["   "] = value
                manifest.write_text(json.dumps(data), encoding="utf8")
                with self.assertRaisesRegex(ValueError, "crosswalk is incomplete"):
                    self.render()

    def test_source_scope_rejects_duplicate_unmapped_or_escaping_source_file(self):
        for mutation in ("duplicate", "unmapped", "escape", "count"):
            with self.subTest(mutation=mutation):
                _, _, manifest, _ = self.source_scope_fixture()
                data = json.loads(manifest.read_text())
                if mutation == "duplicate":
                    data["source_files"] *= 2
                    data["source_file_count"] = data["java_file_count"] = 2
                elif mutation == "unmapped":
                    data["source_files"][0]["catalog_refs"] = ["SYSTEM:missing"]
                elif mutation == "escape":
                    data["source_files"][0]["path"] = "../../private.java"
                else:
                    data["source_file_count"] = 0
                manifest.write_text(json.dumps(data), encoding="utf8")
                with self.assertRaises(ValueError):
                    self.render()

    def test_source_scope_rejects_local_proof_outside_provider(self):
        _, _, _, status = self.source_scope_fixture()
        data = json.loads(status.read_text())
        data["completed_prefix"][0]["evidence"] = "✅-sample/../other/SOURCE-CLOSURE.md"
        status.write_text(json.dumps(data), encoding="utf8")
        with self.assertRaisesRegex(ValueError, "unsafe alphabetical evidence"):
            self.render()

    def test_generator_produces_full_hierarchy_and_check_passes(self):
        self.render()
        result = checker.check(self.repo)
        self.assertEqual([], result["problems"])
        self.assertEqual(4, result["expected_indexes"])
        self.assertEqual(1, result["candidate_cards"])
        self.assertIn("Air Dash", (self.root / "✅-sample/INDEX.md").read_text(encoding="utf8"))

    def test_new_card_detected_until_regenerated(self):
        self.render()
        (self.leaf / "wind-shield.md").write_text("# Wind Shield\n", encoding="utf8")
        self.assertNotEqual([], checker.check(self.repo)["problems"])
        self.render()
        result = checker.check(self.repo)
        self.assertEqual([], result["problems"])
        self.assertEqual(2, result["candidate_cards"])

    def test_alphabetical_semantic_closure_is_separate_from_perk_certification(self):
        nonmagic = self.root / "✅-a-good-place"
        nonmagic.mkdir()
        (nonmagic / "README.md").write_text(
            "Provider-owned spells: **0**\\n"
            "Provider-owned rituals/rites: **0**\\n"
            "Provider-owned equivalent discrete magical actions: **0**\\n",
            encoding="utf8",
        )
        status = self.meta.parent / "ALPHABETICAL-CATALOG-STATUS.json"
        status.write_text(json.dumps({
            "schema_version": 1,
            "order": "provider_directory_name_ascending",
            "completed_prefix": [{
                "provider": "✅-a-good-place",
                "state": "NONMAGICAL_SCOPE_CLOSED",
                "owned_magic_actions": 0,
                "evidence": "✅-a-good-place/README.md",
            }],
            "next_provider": "✅-sample",
        }), encoding="utf8")
        self.render()
        global_index = (self.root / "INDEX.md").read_text(encoding="utf8")
        semantic_index = (nonmagic / "INDEX.md").read_text(encoding="utf8")
        self.assertIn("Revisão alfabética do catálogo semântico", global_index)
        self.assertIn("A Good Place — ✅ escopo semântico encerrado", global_index)
        self.assertIn("0/2.", global_index)
        self.assertIn("✅ escopo encerrado: 0 feitiços", semantic_index)
        self.assertIn("⚠️ NÃO HOMOLOGADO como 100%", semantic_index)
        self.assertIn("próximo provider a concluir", (
            self.root / "✅-sample" / "INDEX.md").read_text(encoding="utf8"))
        self.assertEqual([], checker.check(self.repo)["problems"])

    def test_alphabetical_ledger_rejects_skipping_first_provider(self):
        status = self.meta.parent / "ALPHABETICAL-CATALOG-STATUS.json"
        status.write_text(json.dumps({
            "schema_version": 1,
            "order": "provider_directory_name_ascending",
            "completed_prefix": [{
                "provider": "✅-not-first",
                "state": "NONMAGICAL_SCOPE_CLOSED",
                "owned_magic_actions": 0,
                "evidence": "✅-not-first/README.md",
            }],
            "next_provider": "✅-sample",
        }), encoding="utf8")
        with self.assertRaises(ValueError):
            self.render()

    def test_nonmagical_scope_rejects_boolean_float_or_nonzero_action_count(self):
        nonmagic = self.root / "✅-a-good-place"
        nonmagic.mkdir()
        (nonmagic / "README.md").write_text(
            "Provider-owned spells: **0**\n"
            "Provider-owned rituals/rites: **0**\n"
            "Provider-owned equivalent discrete magical actions: **0**\n",
            encoding="utf8",
        )
        status = self.meta.parent / "ALPHABETICAL-CATALOG-STATUS.json"
        for count in (False, 0.0, 1):
            with self.subTest(count=count):
                status.write_text(json.dumps({
                    "schema_version": 1, "order": "provider_directory_name_ascending",
                    "completed_prefix": [{
                        "provider": "✅-a-good-place", "state": "NONMAGICAL_SCOPE_CLOSED",
                        "owned_magic_actions": count, "evidence": "✅-a-good-place/README.md",
                    }], "next_provider": "✅-sample",
                }), encoding="utf8")
                with self.assertRaisesRegex(ValueError, "unsupported claims"):
                    self.render()

    def test_legacy_green_name_never_certifies_mod(self):
        self.render()
        self.assertIn("0/1", (self.root / "INDEX.md").read_text(encoding="utf8"))
        self.assertIn("⚠️", (self.root / "✅-sample/INDEX.md").read_text(encoding="utf8"))

if __name__ == "__main__":
    unittest.main()
