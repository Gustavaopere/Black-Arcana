#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
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


if __name__ == "__main__":
    unittest.main()
