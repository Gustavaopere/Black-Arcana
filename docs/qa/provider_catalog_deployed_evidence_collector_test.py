#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
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


    def test_runtime_probe_accepts_schema3_neg_glyph_observation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            instance = Path(tmp)
            logs = instance / "logs"
            logs.mkdir(parents=True)
            (logs / "latest.log").write_text(
                "\n".join(
                    [
                        "[BLACK_ARCANA_CATALOG_PROBE] type=begin schema=3",
                        "[BLACK_ARCANA_CATALOG_PROBE] type=glyph id=not_enough_glyphs:plow status=OBSERVED enabled=true",
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
                        "id": "not_enough_glyphs:plow",
                        "status": "OBSERVED",
                        "enabled": True,
                    }
                ],
                result["rows"],
            )


    def test_runtime_probe_rejects_unbounded_glyph_observation(self) -> None:
        row = collector.parse_catalog_probe_payload(
            "type=glyph id=ars_nouveau:break status=OBSERVED enabled=true"
        )

        self.assertIsNone(row)


if __name__ == "__main__":
    unittest.main()
