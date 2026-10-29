#!/usr/bin/env python3
"""Synthetic ledger/index checks, including anti-false-green conditions."""
import json
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import check_perk_ready_indexes as c
import generate_perk_ready_indexes as generator

class IndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.mods = self.root / "wiki/modpack-catalog/providers"
        self.mod = self.mods / "✅-example"
        self.sub = self.mod / "spells"
        self.sub.mkdir(parents=True)
        (self.mod / "README.md").write_text("historical ✅ inventory\n", encoding="utf8")
        (self.sub / "fire-bolt.md").write_text("# Fire Bolt\n", encoding="utf8")
        (self.sub / "README.md").write_text("# Registry\n", encoding="utf8")
        self.manifest = self.root / "wiki/modpack-catalog/meta/PERK-READY-CERTIFICATIONS.json"
        self.manifest.parent.mkdir(parents=True)
        self.ledger = {"schema_version": 1, "objects": {}, "providers": {}, "known_rosters": {}}
        self.save_manifest()
        self.write_indexes()

    def tearDown(self):
        self.tmp.cleanup()

    def save_manifest(self):
        self.manifest.write_text(json.dumps(self.ledger), encoding="utf8")

    def write_indexes(self, marker="⚠️", done=0, total=1, *, catalog_done=0,
                      provider_marker="⚠️", static="⚠️ pendente",
                      hook="⚠️ não verificado", physical="⚠️ não testado"):
        # Start from a complete render, then independently override the states
        # under test so checks cover both structured rows and rendered prose.
        with patch.object(c, "PROVIDERS", self.mods), patch.object(generator, "ROOT", self.mods):
            dirs, mods, cards = c.inventory()
            alpha = generator.alphabetical_scope(mods, cards)
            texts = {folder: generator.directory_index(folder, dirs, cards, self.ledger,
                                                       alphabetical=alpha) for folder in dirs}
            global_text = generator.global_index(mods, cards, self.ledger, alphabetical=alpha)
        counts = f"{catalog_done}/{total} ({100 * catalog_done / total:.1f}%)"
        for folder, text in texts.items():
            folder_marker = provider_marker if folder == self.mod else marker
            text = c.CATALOG_STATE.sub("**Catálogo desta árvore:** " + folder_marker, text)
            text = c.CATALOG_FOLDER.sub(
                f"**Fichas catalogadas (somente fichas detectadas): {catalog_done}/{total}.**", text)
            text = c.PER_FOLDER.sub(
                f"**Homologadas para perks (somente fichas detectadas): {done}/{total}.**", text)
            relative = "spells/fire-bolt.md" if folder == self.mod else "fire-bolt.md"
            label = "spells/fire-bolt.md" if folder == self.mod else "ficha/fire-bolt.md"
            text = c.CARD_ROW.sub(
                f"| {marker} | Fire Bolt | [{label}]({relative}) | {static} | {hook} | {physical} |", text)
            text = c.CHILD_ROW.sub(
                f"| {marker} | Spells | {counts} | {done} | [Abrir índice](spells/INDEX.md) |", text)
            (folder / "INDEX.md").write_text(text, encoding="utf8")
        global_text = c.GLOBAL_CATALOG.sub(
            f"**Providers com catálogo concluído: {int(provider_marker == '✅')}/1.**", global_text)
        global_text = c.GLOBAL_CATALOG_OBJECTS.sub(
            f"**Fichas catalogadas (somente fichas detectadas): {catalog_done}/1.**", global_text)
        global_text = c.GLOBAL_OBJECTS.sub(
            f"**Fichas com contrato técnico estático certificado: {done}/1.**", global_text)
        global_text = c.PROVIDER_ROW.sub(
            lambda match: match[0].replace(match[1], provider_marker, 1).replace(
                match[2], counts, 1).replace(" | " + match[3] + " | ", " | " + str(done) + " | ", 1),
            global_text)
        (self.mods / "INDEX.md").write_text(global_text, encoding="utf8")

    def install_catalog_closure(self):
        revision = "example/provider@" + "b" * 40
        proof = self.mod / "SOURCE-CLOSURE.md"
        proof.write_text("\n".join(("CATALOG_SOURCE_SCOPE_ONLY", revision,
                         "version=1.0", "artifact_sha1=" + "a" * 40,
                         "physical_qa=NOT_TESTED", "mutating_hook=NOT_VERIFIED")))
        card = self.sub / "fire-bolt.md"
        relative = card.relative_to(self.mods).as_posix()
        manifest = self.mod / "SOURCE-MANIFEST.json"
        manifest.write_text(json.dumps({
            "schema_version": 1, "source_revision": revision, "version": "1.0",
            "artifact_sha1": "a" * 40, "claim_scope": "CATALOG_SOURCE_SCOPE_ONLY",
            "physical_qa": "NOT_TESTED", "mutating_hook": "NOT_VERIFIED",
            "cards": {relative: hashlib.sha256(card.read_bytes()).hexdigest()},
            "catalog_objects": {"SPELL:fire-bolt": relative}, "aggregates": {},
            "source_file_count": 1, "java_file_count": 1,
            "source_files": [{"path": "example/Spell.java", "sha256": "c" * 64,
                              "catalog_refs": ["SPELL:fire-bolt"]}],
        }))
        (self.manifest.parent / "ALPHABETICAL-CATALOG-STATUS.json").write_text(json.dumps({
            "schema_version": 1, "order": "provider_directory_name_ascending",
            "completed_prefix": [{"provider": self.mod.name,
                "state": "SOURCE_VERSION_CATALOG_CLOSED", "source_revision": revision,
                "version": "1.0", "artifact_sha1": "a" * 40,
                "physical_qa": "NOT_TESTED", "mutating_hook": "NOT_VERIFIED",
                "evidence": proof.relative_to(self.mods).as_posix(),
                "catalog_manifest": manifest.relative_to(self.mods).as_posix()}],
            "next_provider": None,
        }))
        self.write_indexes(marker="✅", catalog_done=1, provider_marker="✅")

    def test_valid_snapshot_with_warning(self):
        result = c.check(self.root)
        self.assertEqual([], result["problems"])
        self.assertEqual((2, 1, 1, 0),
                         (result["directories"], result["providers"], result["candidate_cards"],
                          result["certified_cards"]))

    def test_old_green_directory_is_not_perk_complete(self):
        result = c.check(self.root)
        self.assertEqual(0, result["certified_providers"])

    def test_missing_subfolder_index_rejected(self):
        (self.sub / "INDEX.md").unlink()
        self.assertTrue(any("missing subfolder" in x for x in c.check(self.root)["problems"]))

    def test_stale_denominator_rejected(self):
        self.write_indexes(total=2)
        self.assertTrue(any("denominator" in x for x in c.check(self.root)["problems"]))

    def test_false_green_item_rejected(self):
        self.write_indexes(marker="✅")
        self.assertTrue(any("wrong card status" in x for x in c.check(self.root)["problems"]))

    def test_validated_catalog_closure_is_green_without_certifying_perks(self):
        self.install_catalog_closure()
        result = c.check(self.root)
        self.assertEqual([], result["problems"])
        self.assertEqual((1, 1, 0, 0), (result["cataloged_cards"], result["cataloged_providers"],
                                     result["certified_cards"], result["certified_providers"]))

    def test_closed_catalog_cannot_promote_static_hook_or_qa_columns(self):
        self.install_catalog_closure()
        for column in ("static", "hook", "physical"):
            with self.subTest(column=column):
                self.write_indexes(marker="✅", catalog_done=1, provider_marker="✅",
                                   **{column: "✅ certificado" if column == "static" else
                                      "✅ verificado" if column == "hook" else "✅ testado"})
                self.assertTrue(any("wrong card status" in x for x in c.check(self.root)["problems"]))

    def test_forged_catalog_green_provider_and_child_rows_rejected(self):
        self.write_indexes(marker="✅", catalog_done=1, provider_marker="✅")
        problems = c.check(self.root)["problems"]
        for message in ("wrong folder catalog", "wrong card status", "wrong child-index catalog",
                        "wrong provider status", "global catalog-provider", "global catalog-object"):
            self.assertTrue(any(message in x for x in problems), message)

    def test_checker_revalidates_changed_source_card(self):
        self.install_catalog_closure()
        (self.sub / "fire-bolt.md").write_text("# Changed behavior\n")
        with self.assertRaisesRegex(ValueError, "catalog card changed"):
            c.check(self.root)

    def test_checker_rejects_new_uncovered_source_card(self):
        self.install_catalog_closure()
        (self.sub / "new-spell.md").write_text("# New Spell\n")
        with self.assertRaisesRegex(ValueError, "exactly the detected cards"):
            c.check(self.root)

    def test_checker_validates_source_proofs_once_and_restores_renderer_root(self):
        import generate_perk_ready_indexes as generator
        self.install_catalog_closure()
        previous_root = generator.ROOT
        with patch.object(generator, "source_catalog_scope", wraps=generator.source_catalog_scope) as validate:
            self.assertEqual([], c.check(self.root)["problems"])
            self.assertEqual(1, validate.call_count)
        self.assertEqual(previous_root, generator.ROOT)

    def test_standalone_checker_bootstraps_renderer_for_selected_repository(self):
        self.install_catalog_closure()
        result = subprocess.run([sys.executable, str(Path(c.__file__)), "--root", str(self.root)],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, json.loads(result.stdout)["cataloged_providers"])

    def test_package_checker_supports_module_cli_and_python_callers(self):
        self.install_catalog_closure()
        repo = Path(c.__file__).resolve().parents[2]
        env = dict(os.environ, PYTHONPATH="", PYTHONDONTWRITEBYTECODE="1")
        caller = "\n".join((
            "import json, sys",
            "from pathlib import Path",
            "from scripts.catalog import check_perk_ready_indexes as checker",
            "from scripts.catalog import generate_perk_ready_indexes as generator",
            "assert generator.qa is checker",
            "before = generator.ROOT, generator.qa",
            "result = checker.check(Path(sys.argv[1]))",
            "assert (generator.ROOT, generator.qa) == before",
            "print(json.dumps(result))",
        ))
        for args in (("-m", "scripts.catalog.check_perk_ready_indexes", "--root"),
                     ("-c", caller)):
            with self.subTest(invocation=args[0]):
                result = subprocess.run([sys.executable, *args, str(self.root)], cwd=repo,
                                        env=env, capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                snapshot = json.loads(result.stdout)
                self.assertEqual([], snapshot["problems"])
                self.assertEqual(1, snapshot["cataloged_providers"])

    def test_renderer_root_restored_after_invalid_catalog_evidence(self):
        import generate_perk_ready_indexes as generator
        self.install_catalog_closure()
        previous_root = generator.ROOT
        (self.mod / "SOURCE-CLOSURE.md").unlink()
        with self.assertRaises(ValueError):
            c.check(self.root)
        self.assertEqual(previous_root, generator.ROOT)

    def test_missing_child_navigation_rejected(self):
        content = (self.mod / "INDEX.md").read_text(encoding="utf8")
        (self.mod / "INDEX.md").write_text(content.replace("(spells/INDEX.md)", "(other/INDEX.md)"),
                                            encoding="utf8")
        self.assertTrue(any("child-index" in x for x in c.check(self.root)["problems"]))

    def test_added_card_requires_index_refresh(self):
        (self.sub / "new-ability.md").write_text("# New Ability\n", encoding="utf8")
        self.assertTrue(any("denominator" in x for x in c.check(self.root)["problems"]))

    def test_documents_do_not_inflate_object_denominator(self):
        (self.sub / "TECHNICAL-MATRIX.md").write_text("# Evidence\n", encoding="utf8")
        self.assertEqual([], c.check(self.root)["problems"])

    def test_only_exact_aces_production_examples_escape_example_folder_filter(self):
        ace = self.mods / "✅-aces-spell-utils" / "examples"
        ace.mkdir(parents=True)
        example_item = ace / "example_sheath.md"
        example_material = ace / "example_armor_material.md"
        unregistered = ace / "example_fake_spell.md"
        evidence = ace / "README.md"
        other = self.mod / "examples" / "example_sheath.md"
        other.parent.mkdir(parents=True)
        for path in (example_item, example_material, unregistered, evidence, other):
            path.write_text("# fixture\\n", encoding="utf8")
        with patch.object(c, "PROVIDERS", self.mods):
            self.assertTrue(c.is_card(example_item))
            self.assertTrue(c.is_card(example_material))
            self.assertFalse(c.is_card(unregistered))
            self.assertFalse(c.is_card(evidence))
            self.assertFalse(c.is_card(other))

    def full_synthetic_certificate(self):
        return {
            "status": "COMPLETE_PERK_READY",
            "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
            "evidence_grade": "PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY",
            "version": "test-1.0",
            "source_revision": "example/provider@" + ("b" * 40),
            "artifact_sha1": "a" * 40,
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "evidence": {
                key: {
                    "path": "wiki/modpack-catalog/providers/✅-example/spells/fire-bolt.md",
                    "reason": "Synthetic reviewed static contract; no runtime claim"
                } for key in c.REQUIRED_EVIDENCE
            },
        }

    def install_certificate(self, cert):
        self.ledger["objects"] = {"✅-example/spells/fire-bolt.md": cert}
        self.save_manifest()

    def test_unproved_certificate_rejected(self):
        self.ledger["objects"] = {"✅-example/spells/fire-bolt.md": {"status": "COMPLETE_PERK_READY"}}
        self.save_manifest()
        with self.assertRaisesRegex(c.CatalogIndexError, "scope"):
            c.check(self.root)

    def test_verified_card_requires_snapshot_update(self):
        self.install_certificate(self.full_synthetic_certificate())
        self.assertTrue(any("stale completion" in x for x in c.check(self.root)["problems"]))

    def test_static_certification_documents_card_without_closing_provider(self):
        self.install_certificate(self.full_synthetic_certificate())
        self.write_indexes(marker="✅", done=1, catalog_done=1, static="✅ certificado")
        result = c.check(self.root)
        self.assertEqual([], result["problems"])
        self.assertEqual((1, 1, 0, 0), (result["cataloged_cards"], result["certified_cards"],
                                     result["cataloged_providers"], result["certified_providers"]))

    def test_certificate_rejects_missing_local_evidence(self):
        cert = self.full_synthetic_certificate()
        cert["evidence"]["identity"]["path"] = (
            "wiki/modpack-catalog/providers/✅-example/missing-file.md"
        )
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "missing referenced evidence"):
            c.check(self.root)

    def test_certificate_rejects_url_instead_of_repo_evidence(self):
        cert = self.full_synthetic_certificate()
        cert["evidence"]["identity"]["path"] = "https://example.org/fake.md"
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "nonlocal or unsafe"):
            c.check(self.root)

    def test_certificate_rejects_path_traversal(self):
        cert = self.full_synthetic_certificate()
        cert["evidence"]["validation"]["path"] = (
            "wiki/modpack-catalog/providers/../../../outside.md"
        )
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "nonlocal or unsafe"):
            c.check(self.root)

    def test_certificate_rejects_unpinned_artifact(self):
        cert = self.full_synthetic_certificate()
        cert["artifact_sha1"] = "NOT_VERIFIED"
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "SHA-1"):
            c.check(self.root)

    def test_certificate_rejects_claim_of_untested_hook(self):
        cert = self.full_synthetic_certificate()
        cert["mutating_hook"] = "READY"
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "mutating-hook"):
            c.check(self.root)

    def test_certificate_rejects_unqualified_grade(self):
        cert = self.full_synthetic_certificate()
        cert["evidence_grade"] = "GAMEPLAY_CERTIFIED_BY_SOURCE"
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "evidence grade"):
            c.check(self.root)

    def test_stale_global_object_number_rejected(self):
        path = self.mods / "INDEX.md"
        content = path.read_text(encoding="utf8")
        path.write_text(
            content.replace("estático certificado: 0/1.", "estático certificado: 1/1."),
            encoding="utf8",
        )
        self.assertTrue(any("certified-object" in x for x in c.check(self.root)["problems"]))

    def test_source_certificate_requires_pinned_revision(self):
        cert = self.full_synthetic_certificate()
        cert["source_revision"] = "HEAD"
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "source revision"):
            c.check(self.root)

    def test_source_only_release_provenance_grade_accepted_without_binary_claim(self):
        cert = self.full_synthetic_certificate()
        cert["evidence_grade"] = "PINNED_SOURCE_WITH_RELEASE_SHA_ONLY"
        self.install_certificate(cert)
        result = c.check(self.root)
        self.assertEqual(1, result["certified_cards"])
        self.assertEqual(0, result["certified_providers"])
        self.assertTrue(any("stale completion" in x for x in result["problems"]))

    def test_source_only_release_grade_still_requires_exact_source_revision(self):
        cert = self.full_synthetic_certificate()
        cert["evidence_grade"] = "PINNED_SOURCE_WITH_RELEASE_SHA_ONLY"
        cert["source_revision"] = "main"
        self.install_certificate(cert)
        with self.assertRaisesRegex(c.CatalogIndexError, "source revision"):
            c.check(self.root)

    def test_provider_closed_requires_evidence(self):
        self.ledger["providers"] = {"✅-example": {"universe_closed": True}}
        self.save_manifest()
        with self.assertRaisesRegex(c.CatalogIndexError, "cannot close"):
            c.check(self.root)

    def test_duplicate_manifest_keys_rejected(self):
        self.manifest.write_text('{"schema_version":1,"objects":{},"objects":{},"providers":{}}', encoding="utf8")
        with self.assertRaisesRegex(c.CatalogIndexError, "duplicate JSON key"):
            c.check(self.root)

if __name__ == "__main__":
    unittest.main()
