#!/usr/bin/env python3
"""Synthetic regression tests for exact-resource extraction; not actual JAR verification."""
import io
import json
import unittest
import zipfile
from alexscaves_1010_damage_type_probe import IDS, PREFIX, extract


def archive_bytes(*, missing=None, extra=False, duplicate_json=False, tags=False):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as archive:
        for item in IDS:
            if item == missing:
                continue
            content = '{"message_id":"example","scaling":"never","exhaustion":0.0}'
            if duplicate_json and item == "acid":
                content = '{"message_id":"example","message_id":"duplicate"}'
            archive.writestr(PREFIX + item + ".json", content)
        if extra:
            archive.writestr(PREFIX + "made_up.json", "{}")
        if tags:
            archive.writestr("data/minecraft/tags/damage_type/is_projectile.json",
                             json.dumps({"values": ["alexscaves:dark_arrow", "#minecraft:irrelevant"]}))
    output.seek(0)
    return output


class ProbeTests(unittest.TestCase):
    def test_exact_eleven_members(self):
        with zipfile.ZipFile(archive_bytes()) as archive:
            result = extract(archive)
        self.assertEqual(sorted(result["damage_types"]), sorted(IDS))
        self.assertEqual(result["consumer_bytecode"], "NOT_AUDITED")

    def test_reject_missing(self):
        with zipfile.ZipFile(archive_bytes(missing="nuke")) as archive:
            with self.assertRaisesRegex(ValueError, "identity set differs"):
                extract(archive)

    def test_reject_extra(self):
        with zipfile.ZipFile(archive_bytes(extra=True)) as archive:
            with self.assertRaisesRegex(ValueError, "identity set differs"):
                extract(archive)

    def test_reject_duplicate_json_key(self):
        with zipfile.ZipFile(archive_bytes(duplicate_json=True)) as archive:
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                extract(archive)

    def test_tag_is_direct_only(self):
        with zipfile.ZipFile(archive_bytes(tags=True)) as archive:
            result = extract(archive)
        self.assertEqual(result["direct_tag_entries"]["dark_arrow"], ["minecraft:is_projectile"])
        self.assertEqual(result["direct_tag_entries"]["acid"], [])
        self.assertFalse(result["provider_universe_closed"])


if __name__ == "__main__":
    unittest.main()
