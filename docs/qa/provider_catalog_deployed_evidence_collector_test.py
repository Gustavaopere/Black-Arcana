#!/usr/bin/env python3
from __future__ import annotations

import gzip
import importlib.util
import json
import struct
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COLLECTOR_PATH = ROOT / "docs" / "qa" / "provider-catalog-deployed-evidence-collector.py"

spec = importlib.util.spec_from_file_location("provider_catalog_collector", COLLECTOR_PATH)
collector = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(collector)


class TombstoneCollectorTest(unittest.TestCase):
    def test_collects_only_bounded_allowed_magic_item_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "config").mkdir(parents=True)
            (instance / "defaultconfigs").mkdir(parents=True)
            world = instance / "world"
            (world / "serverconfig").mkdir(parents=True)

            (instance / "config" / "tombstone-common.toml").write_text(
                """
[allowed_magic_items]
allow_tablet_of_assistance = true
allow_gemstone_of_familiar = false
allow_grave_key = true
""".strip()
                + "\n",
                encoding="utf-8",
            )
            (instance / "defaultconfigs" / "tombstone-common.toml").write_text(
                """
[allowed_magic_items]
allow_tablet_of_assistance = false
allow_magic_scroll = true
""".strip()
                + "\n",
                encoding="utf-8",
            )
            (world / "serverconfig" / "tombstone-common.toml").write_text(
                """
[allowed_magic_items]
allow_scroll_of_knowledge = true
allow_lost_tablet = false
""".strip()
                + "\n",
                encoding="utf-8",
            )

            worlds = collector.candidate_worlds(instance, [])
            result = collector.collect_tombstone(instance, worlds)

            self.assertEqual(12, result["expected_candidate_count"])
            rows = {row["config_key"]: row for row in result["rows"]}

            assistance = rows["allow_tablet_of_assistance"]["observations"]
            self.assertEqual(
                [
                    ("config/tombstone-common.toml", True),
                    ("defaultconfigs/tombstone-common.toml", False),
                ],
                [(obs["path"], obs["value"]) for obs in assistance],
            )

            self.assertEqual(
                [("config/tombstone-common.toml", False)],
                [
                    (obs["path"], obs["value"])
                    for obs in rows["allow_gemstone_of_familiar"]["observations"]
                ],
            )
            self.assertEqual(
                [("world/serverconfig/tombstone-common.toml", True)],
                [
                    (obs["path"], obs["value"])
                    for obs in rows["allow_scroll_of_knowledge"]["observations"]
                ],
            )
            self.assertEqual(
                [("world/serverconfig/tombstone-common.toml", False)],
                [
                    (obs["path"], obs["value"])
                    for obs in rows["allow_lost_tablet"]["observations"]
                ],
            )

            self.assertNotIn("allow_gemstone_of_prayer", rows)
            self.assertNotIn("allow_scroll_of_preservation", rows)

    def test_hash_inventory_includes_tombstone_without_assuming_equality(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "tombstone-neoforge-1.21.1-9.5.6.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("corail_tombstone", result)
            self.assertEqual(1, len(result["corail_tombstone"]))
            entry = result["corail_tombstone"][0]
            self.assertEqual("tombstone-neoforge-1.21.1-9.5.6.jar", entry["filename"])
            self.assertFalse(entry["release_9_5_6_equality"])


    def test_hash_inventory_checks_irons_spellbooks_kubejs_403_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "irons_spells_js-4.0.3.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("irons_spells_js", result)
            self.assertEqual(1, len(result["irons_spells_js"]))
            entry = result["irons_spells_js"][0]
            self.assertEqual("irons_spells_js-4.0.3.jar", entry["filename"])
            self.assertIn("current_physical_4_0_3_equality", entry)
            self.assertFalse(entry["current_physical_4_0_3_equality"])


    def test_hash_inventory_checks_current_irons_spellbooks_3163_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "irons_spellbooks-1.21.1-3.16.3.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("irons_spellbooks", result)
            self.assertEqual(1, len(result["irons_spellbooks"]))
            entry = result["irons_spellbooks"][0]
            self.assertEqual("irons_spellbooks-1.21.1-3.16.3.jar", entry["filename"])
            self.assertIn("current_physical_3_16_3_equality", entry)
            self.assertFalse(entry["current_physical_3_16_3_equality"])


    def test_hash_inventory_checks_current_kubejs_build_377_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "kubejs-neoforge-2101.7.2-build.377.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("kubejs", result)
            self.assertEqual(1, len(result["kubejs"]))
            entry = result["kubejs"][0]
            self.assertEqual("kubejs-neoforge-2101.7.2-build.377.jar", entry["filename"])
            self.assertIn("current_physical_build_377_equality", entry)
            self.assertFalse(entry["current_physical_build_377_equality"])


    def test_hash_inventory_checks_kubejsarsnouveau_132_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "kubejsarsnouveau-1.3.2.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("kubejsarsnouveau", result)
            self.assertEqual(1, len(result["kubejsarsnouveau"]))
            entry = result["kubejsarsnouveau"][0]
            self.assertEqual("kubejsarsnouveau-1.3.2.jar", entry["filename"])
            self.assertIn("current_physical_1_3_2_equality", entry)
            self.assertFalse(entry["current_physical_1_3_2_equality"])


    def test_hash_inventory_checks_current_mowzies_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            jar = mods / "mowziesmobs-1.21.1-1.8.2.jar"
            jar.write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("mowzies_mobs", result)
            self.assertEqual(1, len(result["mowzies_mobs"]))
            entry = result["mowzies_mobs"][0]
            self.assertEqual("mowziesmobs-1.21.1-1.8.2.jar", entry["filename"])
            self.assertIn("current_physical_1_8_2_equality", entry)
            self.assertFalse(entry["current_physical_1_8_2_equality"])


    def test_hash_inventory_checks_current_asterism_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            jar = mods / "asterismarcanum-1.21.1-0.1.0.jar"
            jar.write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("asterism_arcanum", result)
            self.assertEqual(1, len(result["asterism_arcanum"]))
            entry = result["asterism_arcanum"][0]
            self.assertEqual("asterismarcanum-1.21.1-0.1.0.jar", entry["filename"])
            self.assertIn("current_physical_0_1_0_equality", entry)
            self.assertFalse(entry["current_physical_0_1_0_equality"])


    def test_neg_config_targets_use_canonical_glyph_resource_paths(self) -> None:
        self.assertEqual(39, len(collector.NEG_CONFIGS))
        for registry_id, relative_path in collector.NEG_CONFIGS:
            namespace, path = registry_id.split(":", 1)
            self.assertTrue(path.startswith("glyph_"), registry_id)
            self.assertEqual(namespace, Path(relative_path).parent.as_posix())
            self.assertTrue(Path(relative_path).name.startswith("glyph_"), relative_path)


    def test_runtime_probe_accepts_schema3_neg_glyph_observation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            logs = instance / "logs"
            logs.mkdir(parents=True)
            (logs / "latest.log").write_text(
                "\n".join(
                    [
                        "[BLACK_ARCANA_CATALOG_PROBE] type=begin schema=3",
                        "[BLACK_ARCANA_CATALOG_PROBE] type=glyph id=not_enough_glyphs:glyph_plow status=OBSERVED enabled=true",
                        "[BLACK_ARCANA_CATALOG_PROBE] type=end schema=3",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = collector.collect_catalog_runtime_probe(instance, None)

            self.assertEqual("COMPLETE", result["status"])
            self.assertEqual(3, result["schema"])
            self.assertEqual(
                [
                    {
                        "type": "glyph",
                        "id": "not_enough_glyphs:glyph_plow",
                        "status": "OBSERVED",
                        "enabled": True,
                    }
                ],
                result["rows"],
            )


    def test_runtime_probe_accepts_schema4_traveloptics_mod_file_observation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            logs = instance / "logs"
            logs.mkdir(parents=True)
            (logs / "latest.log").write_text(
                "\n".join(
                    [
                        "[BLACK_ARCANA_CATALOG_PROBE] type=begin schema=4",
                        "[BLACK_ARCANA_CATALOG_PROBE] type=mod_file id=traveloptics status=OBSERVED file_name=traveloptics-4.4.0.1-1.21.1.jar size_bytes=18393641 sha1=7b74816e89cc15dd0b5a31d9ea1e456024e8fae4",
                        "[BLACK_ARCANA_CATALOG_PROBE] type=end schema=4",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = collector.collect_catalog_runtime_probe(instance, None)

            self.assertEqual("COMPLETE", result["status"])
            self.assertEqual(4, result["schema"])
            self.assertEqual(
                [
                    {
                        "type": "mod_file",
                        "id": "traveloptics",
                        "status": "OBSERVED",
                        "file_name": "traveloptics-4.4.0.1-1.21.1.jar",
                        "size_bytes": 18393641,
                        "sha1": "7b74816e89cc15dd0b5a31d9ea1e456024e8fae4",
                    }
                ],
                result["rows"],
            )

    def test_runtime_probe_retains_traveloptics_mod_file_hash_failure(self) -> None:
        row = collector.parse_catalog_probe_payload(
            "type=mod_file id=traveloptics status=HASH_UNAVAILABLE error=IOException"
        )

        self.assertEqual(
            {
                "type": "mod_file",
                "id": "traveloptics",
                "status": "HASH_UNAVAILABLE",
                "error": "IOException",
            },
            row,
        )

    def test_runtime_probe_rejects_unbounded_mod_file_observation(self) -> None:
        row = collector.parse_catalog_probe_payload(
            "type=mod_file id=somakespells status=OBSERVED "
            "file_name=somakespells-1.0.9-1.21.1.jar size_bytes=123 sha1="
            "171841ac9f802be9309ecc166c1d972ac6d404c0"
        )

        self.assertIsNone(row)


    def test_runtime_probe_rejects_legacy_unprefixed_neg_glyph_id(self) -> None:
        row = collector.parse_catalog_probe_payload(
            "type=glyph id=not_enough_glyphs:plow status=OBSERVED enabled=true"
        )

        self.assertIsNone(row)


    def test_runtime_probe_rejects_unbounded_glyph_observation(self) -> None:
        row = collector.parse_catalog_probe_payload(
            "type=glyph id=ars_nouveau:break status=OBSERVED enabled=true"
        )

        self.assertIsNone(row)


    def test_collects_mowzies_tunneling_gate_without_assuming_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "config").mkdir(parents=True)
            (instance / "defaultconfigs").mkdir(parents=True)
            world = instance / "world"
            (world / "serverconfig").mkdir(parents=True)

            (instance / "config" / "mowziesmobs-common.toml").write_text(
                """
[tools_and_abilities.earthrend_gauntlet]
enable_tunneling = false
""".strip()
                + "\n",
                encoding="utf-8",
            )
            (instance / "defaultconfigs" / "mowziesmobs-common.toml").write_text(
                """
[tools_and_abilities.earthrend_gauntlet]
enable_tunneling = true
""".strip()
                + "\n",
                encoding="utf-8",
            )

            worlds = collector.candidate_worlds(instance, [])
            result = collector.collect_mowzies_mobs(instance, worlds)

            self.assertEqual(
                [
                    ("config/mowziesmobs-common.toml", False),
                    ("defaultconfigs/mowziesmobs-common.toml", True),
                ],
                [
                    (obs["path"], obs["value"])
                    for obs in result["enable_tunneling_matches"]
                ],
            )


    def test_main_report_includes_mowzies_tunneling_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "mods").mkdir(parents=True)
            (instance / "config").mkdir(parents=True)
            (instance / "config" / "mowziesmobs-common.toml").write_text(
                """
[tools_and_abilities.earthrend_gauntlet]
enable_tunneling = false
""".strip()
                + "\n",
                encoding="utf-8",
            )
            output = instance / "evidence.json"

            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                [("config/mowziesmobs-common.toml", False)],
                [
                    (obs["path"], obs["value"])
                    for obs in report["mowzies_mobs"]["enable_tunneling_matches"]
                ],
            )


    def test_collects_bounded_kubejs_script_inventory_without_copying_bodies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            startup = instance / "kubejs" / "startup_scripts"
            server = instance / "kubejs" / "server_scripts"
            client = instance / "kubejs" / "client_scripts"
            data = instance / "kubejs" / "data" / "pack"
            for root in (startup, server, client, data):
                root.mkdir(parents=True)

            (startup / "spells.js").write_text("StartupEvents.registry('example', e => {})\n", encoding="utf-8")
            (server / "recipes.js").write_text("ServerEvents.recipes(e => {})\n", encoding="utf-8")
            (client / "hud.js").write_text("ClientEvents.tick(e => {})\n", encoding="utf-8")
            (data / "payload.json").write_text('{"value": 1}\n', encoding="utf-8")
            (instance / "kubejs" / "notes.md").write_text("do not collect\n", encoding="utf-8")

            result = collector.collect_kubejs_script_inventory(instance)

            self.assertTrue(result["kubejs_root_present"])
            self.assertEqual(4, result["file_count"])
            self.assertEqual(
                {
                    "startup_scripts": 1,
                    "server_scripts": 1,
                    "client_scripts": 1,
                    "data": 1,
                },
                result["surface_counts"],
            )
            self.assertEqual(
                [
                    "kubejs/client_scripts/hud.js",
                    "kubejs/data/pack/payload.json",
                    "kubejs/server_scripts/recipes.js",
                    "kubejs/startup_scripts/spells.js",
                ],
                [row["path"] for row in result["files"]],
            )
            for row in result["files"]:
                self.assertIn("sha256", row)
                self.assertIn("size_bytes", row)
                self.assertNotIn("content", row)
                self.assertNotIn("irons_spellbooks_kubejs_markers", row)

    def test_kubejs_inventory_marks_irons_spellbooks_candidate_lines_without_copying_bodies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            startup = instance / "kubejs" / "startup_scripts"
            server = instance / "kubejs" / "server_scripts"
            client = instance / "kubejs" / "client_scripts"
            for root in (startup, server, client):
                root.mkdir(parents=True)

            (startup / "spells.js").write_text(
                "StartupEvents.registry('irons_spellbooks:spells', event => {})\n"
                "StartupEvents.registry('irons_spellbooks:schools', event => {})\n"
                "const spellKey = SpellRegistry.SPELL_REGISTRY_KEY\n"
                "const schoolKey = SchoolRegistry.SCHOOL_REGISTRY_KEY\n"
                "event.create('codex', 'irons_spells_js:spellbook')\n",
                encoding="utf-8",
            )
            (server / "events.js").write_text(
                "ISSEvents.spellOnCast(event => {})\n",
                encoding="utf-8",
            )
            (client / "hud.js").write_text("ClientEvents.tick(event => {})\n", encoding="utf-8")

            result = collector.collect_kubejs_script_inventory(instance)
            rows = {row["path"]: row for row in result["files"]}

            self.assertEqual(
                {
                    "spell_registry_literal": [1],
                    "school_registry_literal": [2],
                    "spell_registry_key_binding": [3],
                    "school_registry_key_binding": [4],
                    "irons_spells_js_builder_literal": [5],
                },
                rows["kubejs/startup_scripts/spells.js"]["irons_spellbooks_kubejs_markers"],
            )
            self.assertEqual(
                {"iss_event_bridge": [1]},
                rows["kubejs/server_scripts/events.js"]["irons_spellbooks_kubejs_markers"],
            )
            self.assertNotIn("irons_spellbooks_kubejs_markers", rows["kubejs/client_scripts/hud.js"])
            for row in rows.values():
                self.assertNotIn("content", row)


    def test_kubejs_inventory_marks_official_403_short_builder_literals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            startup = instance / "kubejs" / "startup_scripts"
            startup.mkdir(parents=True)
            (startup / "official_403_style.js").write_text(
                "StartupEvents.registry('attribute', event => {\n"
                "  event.create('test_spell_power', 'spell')\n"
                "})\n"
                "StartupEvents.registry('item', event => {\n"
                "  event.create('test_spellbook', 'spellbook')\n"
                "  event.create('test_staff', 'staff')\n"
                "  event.create('test_magic_sword', 'magic_sword')\n"
                "})\n",
                encoding="utf-8",
            )

            result = collector.collect_kubejs_script_inventory(instance)
            row = result["files"][0]

            self.assertEqual(
                [2, 5, 6, 7],
                row["irons_spellbooks_kubejs_markers"]["irons_spells_js_builder_literal"],
            )

    def test_kubejs_irons_marker_lines_are_bounded_and_flag_truncation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            startup = instance / "kubejs" / "startup_scripts"
            startup.mkdir(parents=True)
            (startup / "events.js").write_text(
                "".join("ISSEvents.spellOnCast(event => {})\n" for _ in range(65)),
                encoding="utf-8",
            )

            result = collector.collect_kubejs_script_inventory(instance)
            row = result["files"][0]

            self.assertEqual(
                list(range(1, 65)),
                row["irons_spellbooks_kubejs_markers"]["iss_event_bridge"],
            )
            self.assertTrue(row["irons_spellbooks_kubejs_markers_truncated"])


    def test_classifies_irons_spellbooks_kubejs_closure_fail_closed_without_current_irons_host(self) -> None:
        result = collector.classify_irons_spellbooks_kubejs_closure(
            {
                "irons_spells_js": [{"current_physical_4_0_3_equality": True}],
                "kubejs": [{"current_physical_build_377_equality": True}],
                "irons_spellbooks": [],
            },
            {
                "kubejs_root_present": False,
                "file_count": 0,
                "surface_counts": {},
                "files": [],
            },
        )

        self.assertEqual("IRONS_HOST_NOT_OBSERVED", result["status"])
        self.assertFalse(result.get("irons_host_certified", False))


    def test_classifies_irons_spellbooks_kubejs_closure_evidence_fail_closed(self) -> None:
        empty_inventory = {
            "kubejs_root_present": False,
            "file_count": 0,
            "surface_counts": {},
            "files": [],
        }
        current_host = {
            "irons_spellbooks": [{"current_physical_3_16_3_equality": True}],
            "kubejs": [{"current_physical_build_377_equality": True}],
        }

        self.assertEqual(
            "ARTIFACT_NOT_OBSERVED",
            collector.classify_irons_spellbooks_kubejs_closure(
                {"irons_spells_js": [], **current_host},
                empty_inventory,
            )["status"],
        )
        self.assertEqual(
            "ARTIFACT_HASH_MISMATCH",
            collector.classify_irons_spellbooks_kubejs_closure(
                {
                    "irons_spells_js": [{"current_physical_4_0_3_equality": False}],
                    **current_host,
                },
                empty_inventory,
            )["status"],
        )
        self.assertEqual(
            "IRONS_HOST_HASH_MISMATCH",
            collector.classify_irons_spellbooks_kubejs_closure(
                {
                    "irons_spells_js": [{"current_physical_4_0_3_equality": True}],
                    "irons_spellbooks": [{"current_physical_3_16_3_equality": False}],
                    "kubejs": [{"current_physical_build_377_equality": True}],
                },
                empty_inventory,
            )["status"],
        )
        self.assertEqual(
            "KUBEJS_HOST_HASH_MISMATCH",
            collector.classify_irons_spellbooks_kubejs_closure(
                {
                    "irons_spells_js": [{"current_physical_4_0_3_equality": True}],
                    "irons_spellbooks": [{"current_physical_3_16_3_equality": True}],
                    "kubejs": [{"current_physical_build_377_equality": False}],
                },
                empty_inventory,
            )["status"],
        )

        zero_candidate = collector.classify_irons_spellbooks_kubejs_closure(
            {
                "irons_spells_js": [{"current_physical_4_0_3_equality": True}],
                **current_host,
            },
            empty_inventory,
        )
        self.assertEqual("ZERO_CONTENT_REVIEW_CANDIDATE", zero_candidate["status"])
        self.assertTrue(zero_candidate["artifact_certified"])
        self.assertTrue(zero_candidate["kubejs_host_certified"])
        self.assertEqual(0, zero_candidate["bounded_file_count"])

        script_review = collector.classify_irons_spellbooks_kubejs_closure(
            {
                "irons_spells_js": [{"current_physical_4_0_3_equality": True}],
                **current_host,
            },
            {
                "kubejs_root_present": True,
                "file_count": 2,
                "surface_counts": {"startup_scripts": 2},
                "files": [
                    {
                        "path": "kubejs/startup_scripts/spells.js",
                        "irons_spellbooks_kubejs_markers": {
                            "spell_registry_literal": [1],
                            "iss_event_bridge": [4],
                        },
                    },
                    {"path": "kubejs/startup_scripts/other.js"},
                ],
            },
        )
        self.assertEqual("SCRIPT_REVIEW_REQUIRED", script_review["status"])
        self.assertEqual(1, script_review["marker_file_count"])
        self.assertEqual(
            ["iss_event_bridge", "spell_registry_literal"],
            script_review["marker_types"],
        )


    def test_main_report_includes_empty_kubejs_inventory_as_explicit_absence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "mods").mkdir(parents=True)
            (instance / "config").mkdir(parents=True)
            output = instance / "evidence.json"

            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertFalse(report["kubejs_script_inventory"]["kubejs_root_present"])
            self.assertEqual(0, report["kubejs_script_inventory"]["file_count"])
            self.assertEqual([], report["kubejs_script_inventory"]["files"])


    def test_main_report_keeps_irons_kubejs_closure_fail_closed_without_current_kubejs_host(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "mods").mkdir(parents=True)
            (instance / "config").mkdir(parents=True)
            output = instance / "evidence.json"

            with patch.object(
                collector,
                "collect_mod_hashes",
                return_value={
                    "irons_spells_js": [{"current_physical_4_0_3_equality": True}],
                    "irons_spellbooks": [{"current_physical_3_16_3_equality": True}],
                    "kubejs": [],
                },
            ), patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            closure = report.get("irons_spellbooks_kubejs_closure", {})
            self.assertEqual("KUBEJS_HOST_NOT_OBSERVED", closure.get("status"))
            self.assertFalse(closure.get("kubejs_host_certified", False))


    def test_main_report_collects_exact_ice_and_fire_jupiter_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            config = instance / "config" / "iceandfire"
            mods.mkdir(parents=True)
            config.mkdir(parents=True)

            (mods / "iceandfire-2.1.2.jar").write_bytes(b"fixture")
            (config / "iaf-common.json").write_text(
                json.dumps(
                    {
                        "phantasmalBladeAbility": False,
                        "tools": {
                            "phantasmalBladeAbility": True,
                            "unrelated": "do-not-collect",
                        },
                        "other": {"secret": "do-not-collect"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            output = instance / "evidence.json"

            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertIn("ice_and_fire_ce", report)
            self.assertEqual(
                {
                    "path": "config/iceandfire/iaf-common.json",
                    "key_path": "tools.phantasmalBladeAbility",
                    "status": "OBSERVED",
                    "value": True,
                },
                report["ice_and_fire_ce"]["phantasmal_blade_ability"],
            )
            self.assertEqual(1, len(report["mods"]["ice_and_fire_ce"]))
            self.assertFalse(
                report["mods"]["ice_and_fire_ce"][0]["release_2_1_2_equality"]
            )
            serialized = json.dumps(report["ice_and_fire_ce"])
            self.assertNotIn("unrelated", serialized)
            self.assertNotIn("secret", serialized)


    def test_collects_simply_cataclysm_startup_gates_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config = instance / "config"
            config.mkdir(parents=True)

            (config / "simplycataclysm-startup.toml").write_text(
                """
["Accursed Rage Options"]
accursedRageChance = 0.5

["Blazing Brand Options"]
blazingBrandChance = 0.75

["Mecha Pulse Options"]
mechaPulseChargeChance = 0.75

["Mecha Smite Options"]
mechaSmiteHarmfulEffectsChance = 1.0
mechaSmiteFireDuration = 5
mechaSmiteWitherDuration = 100
mechaSmiteRegenChance = 0.5
mechaSmiteRegenUsesPercentage = true
mechaSmiteRegenPercentage = 0.5
mechaSmiteRegenThreshold = 10
unrelatedSecret = "do-not-collect"
""".strip()
                + "\n",
                encoding="utf-8",
            )

            result = collector.collect_simply_cataclysm(instance)
            startup = result["startup_config"]

            self.assertEqual("OBSERVED", startup["status"])
            self.assertEqual("config/simplycataclysm-startup.toml", startup["path"])
            self.assertEqual(
                {
                    "accursedRageChance": 0.5,
                    "blazingBrandChance": 0.75,
                    "mechaPulseChargeChance": 0.75,
                    "mechaSmiteHarmfulEffectsChance": 1.0,
                    "mechaSmiteFireDuration": 5,
                    "mechaSmiteWitherDuration": 100,
                    "mechaSmiteRegenChance": 0.5,
                    "mechaSmiteRegenUsesPercentage": True,
                    "mechaSmiteRegenPercentage": 0.5,
                    "mechaSmiteRegenThreshold": 10,
                },
                {
                    key: row["value"]
                    for key, row in startup["selected"].items()
                },
            )
            serialized = json.dumps(result)
            self.assertNotIn("unrelatedSecret", serialized)
            self.assertNotIn("do-not-collect", serialized)

    def test_hash_inventory_checks_simply_cataclysm_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            jar = mods / "simplycataclysm-1.0.2+1.21.1+neoforge.jar"
            jar.write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("simply_swords_cataclysm", result)
            self.assertEqual(1, len(result["simply_swords_cataclysm"]))
            entry = result["simply_swords_cataclysm"][0]
            self.assertEqual(
                "simplycataclysm-1.0.2+1.21.1+neoforge.jar",
                entry["filename"],
            )
            self.assertIn("current_physical_1_0_2_equality", entry)
            self.assertFalse(entry["current_physical_1_0_2_equality"])

    def test_main_report_includes_simply_cataclysm_startup_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "mods").mkdir(parents=True)
            config = instance / "config"
            config.mkdir(parents=True)
            (config / "simplycataclysm-startup.toml").write_text(
                """
["Accursed Rage Options"]
accursedRageChance = 0.0

["Blazing Brand Options"]
blazingBrandChance = 0.75

["Mecha Pulse Options"]
mechaPulseChargeChance = 0.75

["Mecha Smite Options"]
mechaSmiteHarmfulEffectsChance = 1.0
mechaSmiteFireDuration = 0
mechaSmiteWitherDuration = 100
mechaSmiteRegenChance = 0.5
mechaSmiteRegenUsesPercentage = false
mechaSmiteRegenPercentage = 0.5
mechaSmiteRegenThreshold = 10
""".strip()
                + "\n",
                encoding="utf-8",
            )
            output = instance / "evidence.json"

            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertIn("simply_swords_cataclysm", report)
            self.assertEqual(
                0.0,
                report["simply_swords_cataclysm"]["startup_config"]["selected"]["accursedRageChance"]["value"],
            )
            self.assertEqual(
                0,
                report["simply_swords_cataclysm"]["startup_config"]["selected"]["mechaSmiteFireDuration"]["value"],
            )
            self.assertEqual(
                100,
                report["simply_swords_cataclysm"]["startup_config"]["selected"]["mechaSmiteWitherDuration"]["value"],
            )
            self.assertFalse(
                report["simply_swords_cataclysm"]["startup_config"]["selected"]["mechaSmiteRegenUsesPercentage"]["value"]
            )


    def test_collects_shadowsz_deployed_fusion_and_gamerule_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            config = instance / "config"
            world = instance / "world"
            mods.mkdir(parents=True)
            config.mkdir(parents=True)
            world.mkdir(parents=True)

            (mods / "shadowsz-1.1.9.jar").write_bytes(b"fixture")
            (config / "shadowsz-common.toml").write_text(
                """
[gameplay]
fusionEnabled = true
unrelatedSecret = "do-not-collect"
""".strip()
                + "\n",
                encoding="utf-8",
            )

            def nbt_name(value: str) -> bytes:
                raw = value.encode("utf-8")
                return struct.pack(">H", len(raw)) + raw

            def nbt_string(value: str) -> bytes:
                raw = value.encode("utf-8")
                return struct.pack(">H", len(raw)) + raw

            level_dat = (
                b"\x0a" + nbt_name("")
                + b"\x0a" + nbt_name("Data")
                + b"\x0a" + nbt_name("GameRules")
                + b"\x08" + nbt_name("shadowszRestrictPowers") + nbt_string("false")
                + b"\x00"
                + b"\x00"
                + b"\x00"
            )
            with gzip.open(world / "level.dat", "wb") as handle:
                handle.write(level_dat)

            worlds = collector.candidate_worlds(instance, [])
            result = collector.collect_shadowsz(instance, worlds)

            self.assertEqual(
                [("config/shadowsz-common.toml", True)],
                [
                    (obs["path"], obs["value"])
                    for obs in result["fusion_enabled_matches"]
                ],
            )
            self.assertEqual(
                [
                    {
                        "world": "world",
                        "path": "world/level.dat",
                        "status": "OBSERVED",
                        "value": False,
                    }
                ],
                result["restrict_powers_gamerules"],
            )
            self.assertNotIn("unrelatedSecret", json.dumps(result))
            self.assertNotIn("do-not-collect", json.dumps(result))

    def test_hash_inventory_checks_shadowsz_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "shadowsz-1.1.9.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("shadowsz", result)
            self.assertEqual(1, len(result["shadowsz"]))
            entry = result["shadowsz"][0]
            self.assertEqual("shadowsz-1.1.9.jar", entry["filename"])
            self.assertIn("current_physical_1_1_9_equality", entry)
            self.assertFalse(entry["current_physical_1_1_9_equality"])

    def test_main_report_includes_shadowsz_deployed_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "mods").mkdir(parents=True)
            config = instance / "config"
            world = instance / "world"
            config.mkdir(parents=True)
            world.mkdir(parents=True)

            (config / "shadowsz-common.toml").write_text(
                "[gameplay]\nfusionEnabled = false\n",
                encoding="utf-8",
            )

            def nbt_name(value: str) -> bytes:
                raw = value.encode("utf-8")
                return struct.pack(">H", len(raw)) + raw

            def nbt_string(value: str) -> bytes:
                raw = value.encode("utf-8")
                return struct.pack(">H", len(raw)) + raw

            level_dat = (
                b"\x0a" + nbt_name("")
                + b"\x0a" + nbt_name("Data")
                + b"\x0a" + nbt_name("GameRules")
                + b"\x08" + nbt_name("shadowszRestrictPowers") + nbt_string("true")
                + b"\x00"
                + b"\x00"
                + b"\x00"
            )
            with gzip.open(world / "level.dat", "wb") as handle:
                handle.write(level_dat)

            output = instance / "evidence.json"
            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                False,
                report["shadowsz"]["fusion_enabled_matches"][0]["value"],
            )
            self.assertEqual(
                True,
                report["shadowsz"]["restrict_powers_gamerules"][0]["value"],
            )


    def test_collects_only_exact_simply_more_mimicry_disabled_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config_dir = instance / "config" / "simplymore"
            config_dir.mkdir(parents=True)

            forms = list(collector.SIMPLY_MORE_MIMICRY_FORMS)
            sections = []
            for index, form in enumerate(forms):
                sections.append(
                    f"[mimicry.config.{form}]\n"
                    f"disabled = {'true' if index == 0 else 'false'}\n"
                    f"unrelatedSecret = \"sentinel-{form}\"\n"
                )
            (config_dir / "unique_effect.toml").write_text(
                "\n".join(sections),
                encoding="utf-8",
            )

            result = collector.collect_simply_more(instance)

            self.assertEqual("OBSERVED", result["mimicry_form_disable_config"]["status"])
            self.assertEqual(
                "config/simplymore/unique_effect.toml",
                result["mimicry_form_disable_config"]["path"],
            )
            self.assertEqual(25, result["expected_form_count"])
            rows = {row["form"]: row for row in result["mimicry_form_disable_config"]["forms"]}
            self.assertEqual(set(forms), set(rows))
            self.assertIs(True, rows[forms[0]]["disabled"])
            self.assertIs(False, rows[forms[1]]["disabled"])
            self.assertTrue(all(row["status"] == "OBSERVED" for row in rows.values()))
            serialized = json.dumps(result)
            self.assertNotIn("unrelatedSecret", serialized)
            self.assertNotIn("sentinel-", serialized)

    def test_simply_more_mimicry_missing_flags_stay_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config_dir = instance / "config" / "simplymore"
            config_dir.mkdir(parents=True)
            (config_dir / "unique_effect.toml").write_text(
                "[mimicry.config.longsword]\ndisabled = false\n",
                encoding="utf-8",
            )

            result = collector.collect_simply_more(instance)

            self.assertEqual("INCOMPLETE", result["mimicry_form_disable_config"]["status"])
            rows = {row["form"]: row for row in result["mimicry_form_disable_config"]["forms"]}
            self.assertEqual("OBSERVED", rows["longsword"]["status"])
            self.assertEqual("KEY_NOT_FOUND", rows["great_katana"]["status"])

    def test_hash_inventory_checks_simply_more_alpha5_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "simplymore-forge-1.3.0_alpha.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("simply_more", result)
            self.assertEqual(1, len(result["simply_more"]))
            entry = result["simply_more"][0]
            self.assertEqual("simplymore-forge-1.3.0_alpha.jar", entry["filename"])
            self.assertIn("current_physical_alpha5_equality", entry)
            self.assertFalse(entry["current_physical_alpha5_equality"])

    def test_main_report_includes_simply_more_mimicry_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "mods").mkdir(parents=True)
            config_dir = instance / "config" / "simplymore"
            config_dir.mkdir(parents=True)

            sections = []
            for form in collector.SIMPLY_MORE_MIMICRY_FORMS:
                sections.append(f"[mimicry.config.{form}]\ndisabled = false\n")
            (config_dir / "unique_effect.toml").write_text(
                "\n".join(sections),
                encoding="utf-8",
            )

            output = instance / "evidence.json"
            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                "OBSERVED",
                report["simply_more"]["mimicry_form_disable_config"]["status"],
            )
            self.assertEqual(
                25,
                len(report["simply_more"]["mimicry_form_disable_config"]["forms"]),
            )


    def test_collects_bounded_simply_swords_reachability_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config_dir = instance / "config" / "simplyswords"
            config_dir.mkdir(parents=True)

            (config_dir / "general.toml").write_text(
                "enableUniqueWeaponAwakening = false\n"
                "unrelatedSecret = \"general-sentinel\"\n",
                encoding="utf-8",
            )
            (config_dir / "loot.toml").write_text(
                "enableLootDrops = true\n"
                "runicLootTableWeight = 0.7\n"
                "uniqueLootTableWeight = 0.05\n"
                "enableContainedRemnants = false\n"
                "disabledUniqueWeaponLoot = [\"simplyswords:emberblade\"]\n"
                "unrelatedSecret = \"loot-sentinel\"\n"
                "\n"
                "[uniqueLootTableOptions]\n"
                "\"minecraft:chests/end_city_treasure\" = 0.25\n"
                "\"minecraft:entities/ender_dragon\" = 5.0\n",
                encoding="utf-8",
            )

            result = collector.collect_simply_swords(instance)

            self.assertEqual("OBSERVED", result["awakening_config"]["status"])
            self.assertEqual(
                "config/simplyswords/general.toml",
                result["awakening_config"]["path"],
            )
            self.assertIs(
                False,
                result["awakening_config"]["enableUniqueWeaponAwakening"]["value"],
            )

            loot = result["loot_config"]
            self.assertEqual("OBSERVED", loot["status"])
            self.assertEqual("config/simplyswords/loot.toml", loot["path"])
            self.assertIs(True, loot["enableLootDrops"]["value"])
            self.assertEqual(0.7, loot["runicLootTableWeight"]["value"])
            self.assertEqual(0.05, loot["uniqueLootTableWeight"]["value"])
            self.assertIs(False, loot["enableContainedRemnants"]["value"])
            self.assertEqual(
                ["simplyswords:emberblade"],
                loot["disabledUniqueWeaponLoot"]["values"],
            )
            self.assertEqual(
                [
                    {"id": "minecraft:chests/end_city_treasure", "value": 0.25},
                    {"id": "minecraft:entities/ender_dragon", "value": 5.0},
                ],
                loot["uniqueLootTableOptions"]["entries"],
            )

            serialized = json.dumps(result)
            self.assertNotIn("unrelatedSecret", serialized)
            self.assertNotIn("general-sentinel", serialized)
            self.assertNotIn("loot-sentinel", serialized)

    def test_simply_swords_missing_or_invalid_reachability_values_stay_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config_dir = instance / "config" / "simplyswords"
            config_dir.mkdir(parents=True)

            (config_dir / "general.toml").write_text(
                "enableUniqueWeaponAwakening = \"yes\"\n",
                encoding="utf-8",
            )
            (config_dir / "loot.toml").write_text(
                "enableLootDrops = true\n"
                "uniqueLootTableWeight = 0.05\n"
                "disabledUniqueWeaponLoot = [\"not a resource id\"]\n"
                "\n"
                "[uniqueLootTableOptions]\n"
                "\"not a resource id\" = 1.0\n",
                encoding="utf-8",
            )

            result = collector.collect_simply_swords(instance)

            self.assertEqual("INVALID_VALUE", result["awakening_config"]["status"])
            self.assertEqual(
                "INVALID_VALUE",
                result["awakening_config"]["enableUniqueWeaponAwakening"]["status"],
            )
            self.assertEqual("INCOMPLETE", result["loot_config"]["status"])
            self.assertEqual(
                "KEY_NOT_FOUND",
                result["loot_config"]["runicLootTableWeight"]["status"],
            )
            self.assertEqual(
                "KEY_NOT_FOUND",
                result["loot_config"]["enableContainedRemnants"]["status"],
            )
            self.assertEqual(
                1,
                result["loot_config"]["disabledUniqueWeaponLoot"]["invalid_entry_count"],
            )
            self.assertEqual(
                1,
                result["loot_config"]["uniqueLootTableOptions"]["invalid_entry_count"],
            )
            serialized = json.dumps(result)
            self.assertNotIn("not a resource id", serialized)

    def test_hash_inventory_checks_simply_swords_1702_physical_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "simplyswords-neoforge-1.70.2-1.21.1.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertIn("simply_swords", result)
            self.assertEqual(1, len(result["simply_swords"]))
            entry = result["simply_swords"][0]
            self.assertEqual(
                "simplyswords-neoforge-1.70.2-1.21.1.jar",
                entry["filename"],
            )
            self.assertIn("current_physical_1_70_2_equality", entry)
            self.assertFalse(entry["current_physical_1_70_2_equality"])

    def test_main_report_includes_simply_swords_reachability_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            (instance / "mods").mkdir(parents=True)
            config_dir = instance / "config" / "simplyswords"
            config_dir.mkdir(parents=True)
            (config_dir / "general.toml").write_text(
                "enableUniqueWeaponAwakening = true\n",
                encoding="utf-8",
            )
            (config_dir / "loot.toml").write_text(
                "enableLootDrops = true\n"
                "runicLootTableWeight = 0.7\n"
                "uniqueLootTableWeight = 0.05\n"
                "enableContainedRemnants = true\n"
                "disabledUniqueWeaponLoot = []\n"
                "\n"
                "[uniqueLootTableOptions]\n"
                "\"minecraft:entities/ender_dragon\" = 5.0\n",
                encoding="utf-8",
            )

            output = instance / "evidence.json"
            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertIs(
                True,
                report["simply_swords"]["awakening_config"]["enableUniqueWeaponAwakening"]["value"],
            )
            self.assertEqual(
                5.0,
                report["simply_swords"]["loot_config"]["uniqueLootTableOptions"]["entries"][0]["value"],
            )


    def test_collects_deeper_and_darker_current_physical_and_cooldown_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            config = instance / "config"
            mods.mkdir(parents=True)
            config.mkdir(parents=True)

            (mods / "deeperdarker-neoforge-1.21.1-1.4.1.jar").write_bytes(b"fixture")
            (config / "deeperdarker-common.toml").write_text(
                """
[general]
soulElytraCooldown = -1
unrelatedSecret = "do-not-copy"
""".strip()
                + "\n",
                encoding="utf-8",
            )

            hashes = collector.collect_mod_hashes(instance)
            self.assertIn("deeper_and_darker", hashes)
            self.assertEqual(1, len(hashes["deeper_and_darker"]))
            entry = hashes["deeper_and_darker"][0]
            self.assertEqual(
                "deeperdarker-neoforge-1.21.1-1.4.1.jar",
                entry["filename"],
            )
            self.assertIn("current_physical_1_4_1_equality", entry)
            self.assertFalse(entry["current_physical_1_4_1_equality"])

            result = collector.collect_deeper_and_darker(instance)
            cooldown = result["soul_elytra_cooldown"]
            self.assertEqual("OBSERVED", cooldown["status"])
            self.assertEqual("config/deeperdarker-common.toml", cooldown["path"])
            self.assertEqual("general.soulElytraCooldown", cooldown["key_path"])
            self.assertEqual(-1, cooldown["value"])
            self.assertNotIn("unrelatedSecret", json.dumps(result))

    def test_deeper_and_darker_cooldown_missing_or_invalid_stays_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config = instance / "config"
            config.mkdir(parents=True)

            missing = collector.collect_deeper_and_darker(instance)
            self.assertEqual("NOT_FOUND", missing["soul_elytra_cooldown"]["status"])

            path = config / "deeperdarker-common.toml"
            path.write_text(
                """
[general]
soulElytraCooldown = 12001
""".strip()
                + "\n",
                encoding="utf-8",
            )
            invalid = collector.collect_deeper_and_darker(instance)
            self.assertEqual("OUT_OF_RANGE", invalid["soul_elytra_cooldown"]["status"])
            self.assertEqual(12001, invalid["soul_elytra_cooldown"]["value"])



    def test_main_report_includes_deeper_and_darker_deployed_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            config = instance / "config"
            mods.mkdir(parents=True)
            config.mkdir(parents=True)
            (mods / "deeperdarker-neoforge-1.21.1-1.4.1.jar").write_bytes(b"fixture")
            (config / "deeperdarker-common.toml").write_text(
                "soulElytraCooldown = 600\n",
                encoding="utf-8",
            )
            output = instance / "evidence.json"

            with patch(
                "sys.argv",
                [
                    "provider-catalog-deployed-evidence-collector.py",
                    str(instance),
                    "--output",
                    str(output),
                ],
            ):
                self.assertEqual(0, collector.main())

            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertIn("deeper_and_darker", report["mods"])
            self.assertFalse(
                report["mods"]["deeper_and_darker"][0]["current_physical_1_4_1_equality"]
            )
            self.assertEqual(
                {
                    "path": "config/deeperdarker-common.toml",
                    "key_path": "soulElytraCooldown",
                    "status": "OBSERVED",
                    "value": 600,
                },
                report["deeper_and_darker"]["soul_elytra_cooldown"],
            )



    def test_traveloptics_hash_inventory_marks_current_other_verified_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            (mods / "traveloptics-4.4.0.1-1.21.1.jar").write_bytes(b"fixture")

            result = collector.collect_mod_hashes(instance)

            self.assertEqual(1, len(result["traveloptics"]))
            entry = result["traveloptics"][0]
            self.assertEqual("OTHER_VERIFIED", entry["classification"])
            self.assertIn("current_physical_known_equality", entry)
            self.assertFalse(entry["current_physical_known_equality"])

    def test_traveloptics_collects_bounded_generic_acquisition_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            startup = instance / "kubejs" / "startup_scripts"
            server = instance / "kubejs" / "server_scripts"
            data = instance / "kubejs" / "data" / "pack"
            quests = instance / "config" / "ftbquests"
            world_datapacks = instance / "world" / "datapacks" / "pack" / "data" / "example"
            for root in (startup, server, data, quests, world_datapacks):
                root.mkdir(parents=True)

            (startup / "registry.js").write_text(
                'const route = SpellFilter; const secret = "do-not-copy-startup";\n',
                encoding="utf-8",
            )
            (server / "grant.js").write_text(
                'const id = "traveloptics:blackout"; const secret = "do-not-copy-server";\n',
                encoding="utf-8",
            )
            (data / "loot.json").write_text(
                '{"type":"randomize_spell","secret":"do-not-copy-data"}\n',
                encoding="utf-8",
            )
            (quests / "quest.snbt").write_text(
                'filter: "spell_filter", secret: "do-not-copy-quest"\n',
                encoding="utf-8",
            )
            (world_datapacks / "route.json").write_text(
                '{"bridge":"RandomizeSpellFunction","secret":"do-not-copy-world"}\n',
                encoding="utf-8",
            )

            worlds = collector.candidate_worlds(instance, [])
            result = collector.collect_traveloptics(instance, worlds)

            self.assertEqual(
                {
                    "SpellFilter",
                    "RandomizeSpellFunction",
                    "spell_filter",
                    "randomize_spell",
                },
                {row["literal"] for row in result["generic_acquisition_marker_matches"]},
            )
            self.assertIn(
                "kubejs/startup_scripts/registry.js",
                {row["path"] for row in result["generic_acquisition_marker_matches"]},
            )
            self.assertIn(
                "kubejs/server_scripts/grant.js",
                {row["path"] for row in result["blackout_reference_matches"]},
            )
            serialized = json.dumps(result)
            for secret in (
                "do-not-copy-startup",
                "do-not-copy-server",
                "do-not-copy-data",
                "do-not-copy-quest",
                "do-not-copy-world",
            ):
                self.assertNotIn(secret, serialized)



    def test_traveloptics_collects_bounded_irons_spell_config_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            local = (
                instance
                / "config"
                / "irons_spellbooks_spell_config"
                / "traveloptics"
            )
            local.mkdir(parents=True)
            (local / "blackout.json").write_text(
                json.dumps(
                    {
                        "irons_spellbooks:enabled": True,
                        "irons_spellbooks:school": "irons_spellbooks:eldritch",
                        "irons_spellbooks:allow_crafting": True,
                        "unrelatedSecret": "do-not-copy-traveloptics-config",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            worlds = collector.candidate_worlds(instance, [])
            result = collector.collect_traveloptics(instance, worlds)

            self.assertEqual(
                [
                    {
                        "path": "config/irons_spellbooks_spell_config/traveloptics/blackout.json",
                        "selected": {
                            "irons_spellbooks:enabled": True,
                            "irons_spellbooks:school": "irons_spellbooks:eldritch",
                            "irons_spellbooks:allow_crafting": True,
                        },
                    }
                ],
                result["irons_spell_config_evidence"]["local_spell_configs"],
            )
            self.assertNotIn(
                "do-not-copy-traveloptics-config",
                json.dumps(result),
            )




class AdditionalProviderGateEvidenceTest(unittest.TestCase):
    def test_bomd_exact_nested_gate_ignores_unrelated_switch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config = instance / "config"
            config.mkdir(parents=True)
            (config / "bosses_of_mass_destruction-common.toml").write_text(
                "[other]\nisEnabled = false\n"
                "[lichConfig.summonMechanic]\nisEnabled = true\n"
                "unrelatedSecret = 'do-not-copy-bomd'\n",
                encoding="utf-8",
            )
            (config / "other_mod.toml").write_text(
                "[lichConfig.summonMechanic]\nisEnabled = false\n",
                encoding="utf-8",
            )
            result = collector.collect_bosses_mass_destruction(instance, [])
            self.assertEqual("OBSERVED_CANDIDATE", result["status"])
            self.assertEqual(
                [("lichConfig.summonMechanic.isEnabled", True)],
                [(row["key_path"], row["value"]) for row in result["observations"]],
            )
            self.assertNotIn("do-not-copy-bomd", json.dumps(result))

    def test_alex_mobs_validates_boolean_and_dimension_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config = instance / "config"
            config.mkdir(parents=True)
            (config / "alexsmobs-common.toml").write_text(
                "[all]\nvoidWormSummonable = true\n"
                'voidWormSpawnDimensions = ["minecraft:the_end"]\n'
                'unrelatedSecret = "do-not-copy-alex"\n',
                encoding="utf-8",
            )
            result = collector.collect_alexs_mobs(instance, [])
            self.assertEqual(
                True, result["voidWormSummonable"][0]["value"])
            self.assertEqual(
                ["minecraft:the_end"], result["voidWormSpawnDimensions"][0]["value"])
            self.assertNotIn("do-not-copy-alex", json.dumps(result))

    def test_absent_deployment_is_not_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            instance.mkdir(exist_ok=True)
            self.assertEqual(
                "NOT_VERIFIED",
                collector.collect_bosses_mass_destruction(instance, [])["status"],
            )
            self.assertEqual(
                [], collector.collect_alexs_mobs(instance, [])["voidWormSummonable"])
            self.assertEqual(
                "ACTION_ELIGIBILITY_UNVERIFIED",
                collector.collect_vampiric_ageing(instance, [])["status"])
            self.assertEqual(
                "NORMAL_SURVIVAL_ACQUISITION_UNVERIFIED",
                collector.collect_weapons_of_miracles_nova(instance, [])["status"])

    def test_fingerprint_only_never_copies_config_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            config = instance / "config"
            config.mkdir(parents=True)
            (config / "vampiricageing-common.toml").write_text(
                'secret = "do-not-copy-ageing"\n',
                encoding="utf-8",
            )
            (config / "specs_irons_spellbooks.json").write_text(
                '{"secret": "do-not-copy-specs"}\n',
                encoding="utf-8",
            )
            ageing = collector.collect_vampiric_ageing(instance, [])
            specs = collector.collect_spell_codex_specs(instance, [])
            self.assertEqual(1, len(ageing["config_files"]))
            self.assertEqual(1, len(specs["config_files"]))
            self.assertEqual("FINGERPRINT_ONLY", ageing["config_files"][0]["status"])
            self.assertEqual(64, len(specs["config_files"][0]["sha256"]))
            self.assertNotIn("do-not-copy", json.dumps([ageing, specs]))

    def test_fingerprint_skips_symlinks_outside_instance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp) / "instance"
            config = instance / "config"
            config.mkdir(parents=True)
            external = Path(tmp) / "vampiricageing-external.toml"
            external.write_text('secret = "not-a-pack-config"\n', encoding="utf-8")
            (config / "vampiricageing-link.toml").symlink_to(external)
            result = collector.collect_vampiric_ageing(instance, [])
            self.assertEqual([], result["config_files"])
    def test_new_provider_jar_names_fingerprint_without_false_equality(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            mods = instance / "mods"
            mods.mkdir(parents=True)
            names = {
                "bosses_of_mass_destruction": "BOMD-NeoForge-1.21-1.3.3.jar",
                "alexs_mobs_continued": "alexsmobs-2.1.13-neoforge+1.21.1.jar",
                "vampiric_ageing": "vampiricageing-1.21-1.4.21.jar",
                "spell_codex_specs": "specs_irons_spellbooks-1.6.5.jar",
                "weapons_of_miracles": "WeaponsOfMiracles-2.0.178.jar",
            }
            for filename in names.values():
                (mods / filename).write_bytes(b"fixture-not-a-real-jar")
            observed = collector.collect_mod_hashes(instance)
            for provider, filename in names.items():
                self.assertEqual(filename, observed[provider][0]["filename"])
                self.assertEqual(40, len(observed[provider][0]["sha1"]))
                for key, value in observed[provider][0].items():
                    if key.endswith("_equality"):
                        self.assertIs(False, value)
    def test_wom_reference_is_candidate_not_acquisition_proof(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            script = instance / "kubejs" / "server_scripts" / "wom.js"
            script.parent.mkdir(parents=True)
            script.write_text(
                'const id = "wom:nova"; // do-not-copy-wom\n',
                encoding="utf-8",
            )
            result = collector.collect_weapons_of_miracles_nova(instance, [])
            self.assertEqual(
                "NORMAL_SURVIVAL_ACQUISITION_UNVERIFIED", result["status"])
            self.assertEqual(
                ["kubejs/server_scripts/wom.js"],
                [row["path"] for row in result["candidate_script_or_datapack_references"]],
            )
            self.assertNotIn("do-not-copy-wom", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
