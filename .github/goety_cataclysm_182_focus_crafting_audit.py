"""Clean-room exact-JAR Goety Cataclysm 1.8.2 standard crafting identity audit.

Only text-safe resource paths, recipe type, output identity, optional top-level
condition metadata; never retain or print recipes, inputs, bytecode, assets.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

JAR = Path(os.environ["EXACT_JAR_PATH"])
ROOT = "data/goety_cataclysm/recipe/"
EXPECTED_SHA1 = "4e3052a082200371b36e1a88fdce05e294d82757"
FOCUS_IDS = {
    "goety_cataclysm:amethyst_cluster_focus",
    "goety_cataclysm:ashen_breath_focus",
    "goety_cataclysm:void_rune_focus",
    "goety_cataclysm:water_spear_focus",
}
PAT = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
actual_sha1 = hashlib.sha1(JAR.read_bytes()).hexdigest()
assert actual_sha1 == EXPECTED_SHA1, "artifact differs from physical modlist: FAIL CLOSED"
print(f"EXACT_SHA1={actual_sha1}")
print(f"JAR_BYTES={JAR.stat().st_size}")

def item_ids(value):
    if isinstance(value, str):
        return {value} if PAT.fullmatch(value) else set()
    if isinstance(value, list):
        result = set()
        for entry in value:
            result |= item_ids(entry)
        return result
    if isinstance(value, dict):
        result = set()
        for key in ("id", "item", "result", "output", "stack"):
            if key in value:
                result |= item_ids(value[key])
        return result
    return set()

rows = []
with zipfile.ZipFile(JAR) as z:
    for path in sorted(z.namelist()):
        if not path.startswith(ROOT) or not path.endswith(".json"):
            continue
        try:
            body = json.loads(z.read(path).decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(body, dict):
            continue
        outputs = item_ids(body.get("result")) | item_ids(body.get("output"))
        if not (outputs & FOCUS_IDS):
            continue
        if len(outputs & FOCUS_IDS) != 1:
            raise AssertionError(f"Ambiguous Focus output in {path}: FAIL CLOSED")
        types = body.get("type")
        if not isinstance(types, str) or not PAT.fullmatch(types):
            raise AssertionError(f"Unverified recipe type at {path}: FAIL CLOSED")
        condition_count = 0
        conditions = body.get("neoforge:conditions", body.get("conditions"))
        if conditions is not None:
            condition_count = len(conditions) if isinstance(conditions, list) else 1
        result = {
            "path": path,
            "recipe_type": types,
            "focus_result_id": next(iter(outputs & FOCUS_IDS)),
            "top_level_condition_count": condition_count,
        }
        rows.append(result)

assert len(rows) == 4, f"Expected exactly four ordinary crafting Focus paths, got {len(rows)}"
assert {r["focus_result_id"] for r in rows} == FOCUS_IDS
assert len({r["path"] for r in rows}) == 4
assert all(r["recipe_type"] != "goety:ritual" for r in rows), "Focus path reclassified as ritual"
assert all(r["top_level_condition_count"] == 0 for r in rows), "Unexpected top-level condition"
for row in rows:
    print("CRAFTING_ROW=" + json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
print("FOUR_ORDINARY_FOCUS_CRAFTING_PATHS_VERIFIED=4")
