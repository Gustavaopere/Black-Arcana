#!/usr/bin/env python3
"""
Read-only Black Arcana provider-catalog evidence collector.

This script does not modify the Minecraft instance. It emits only:
- selected mod JAR hashes;
- selected config keys required by canonical provider checklists;
- presence of exact datapack override paths;
- bounded references to exact catalog IDs in deployed customization surfaces.

It intentionally does not dump full config files, script bodies, quest text or unrelated instance data.
When a Black Arcana catalog runtime probe log is available, it retains only
strictly whitelisted structured fields from the last complete probe block.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import struct
import sys
import tomllib
import zipfile
from pathlib import Path
from typing import Any

TRAVELOPTICS_ORIGINAL_SHA1 = "3808493ce45cdfeb6408e85578adecf13df698e8"
TRAVELOPTICS_PATCH_SHA1 = "680fa679d8ea2419a79571f455436367222f6f9d"
DEEPER_DARKER_141_PHYSICAL_SHA1 = "83f7edd0a8516b2767c2cda7a3b2402f9e290d88"
ASTERISM_010_PHYSICAL_SHA1 = "4a25ba80116168ddcc812f71467c0598127e774a"
SOMAKE_109_RELEASE_SHA1 = "171841ac9f802be9309ecc166c1d972ac6d404c0"
GAZE_1171_SHA1 = "a8cb3190bde157f78160ce65c202ce2d47fb2041"
NEG_462_RELEASE_SHA1 = "32eea2c478a346ee7499f6a0db156241116f73e9"
TOMBSTONE_956_RELEASE_SHA1 = "d830d16caa20b0d23a44ed6b1d339bc22afc2460"
MOWZIES_MOBS_182_PHYSICAL_SHA1 = "d64475cd77444b056ece6472c79d40293dc63c6c"
ICE_AND_FIRE_CE_212_RELEASE_SHA1 = "0786f4142b7cabd958688f68beef3e63e9c0ae8b"
SIMPLY_CATACLYSM_102_PHYSICAL_SHA1 = "a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469"
SHADOWSZ_119_PHYSICAL_SHA1 = "f946eb3a8181e1964279f163f430ccbba6c4edcd"
SIMPLY_MORE_ALPHA5_PHYSICAL_SHA1 = "51636477cd5c378f42d9700e1fe35cd952c8f4f1"
SIMPLY_SWORDS_1702_PHYSICAL_SHA1 = "05b074ff774467f1fe9fb5592151b7845c321cbc"
KUBEJSARSNOUVEAU_132_PHYSICAL_SHA1 = "f39f4f409e628731be551fd961fac2964768d358"
IRONS_SPELLS_JS_403_PHYSICAL_SHA1 = "0481395c5847e2920d1425e77833bef87df63139"
IRONS_SPELLBOOKS_3163_PHYSICAL_SHA1 = "017fd8140c477f9ae602cf95594f1c23bef1d6e3"
KUBEJS_2101_7_2_BUILD_377_PHYSICAL_SHA1 = "150c5d6efc09b969ac350ea205128dff832e0850"

SIMPLY_MORE_MIMICRY_FORMS = [
    "longsword",
    "twinblade",
    "rapier",
    "sai",
    "cutlass",
    "chakram",
    "warglaive",
    "spear",
    "glaive",
    "claymore",
    "scythe",
    "greataxe",
    "greathammer",
    "dagger",
    "khopesh",
    "katana",
    "grandsword",
    "pernach",
    "lance",
    "great_spear",
    "quarterstaff",
    "halberd",
    "backhand_blade",
    "deer_horns",
    "great_katana",
]

SIMPLY_CATACLYSM_STARTUP_CONFIG_KEYS = [
    "accursedRageChance",
    "blazingBrandChance",
    "mechaPulseChargeChance",
    "mechaSmiteHarmfulEffectsChance",
    "mechaSmiteFireDuration",
    "mechaSmiteWitherDuration",
    "mechaSmiteRegenChance",
    "mechaSmiteRegenUsesPercentage",
    "mechaSmiteRegenPercentage",
    "mechaSmiteRegenThreshold",
]

TOMBSTONE_ALLOWED_MAGIC_ITEM_KEYS = [
    "allow_tablet_of_assistance",
    "allow_tablet_of_cupidity",
    "allow_tablet_of_guard",
    "allow_tablet_of_home",
    "allow_tablet_of_recall",
    "allow_gemstone_of_familiar",
    "allow_gemstone_of_guardian",
    "allow_gemstone_of_merchant",
    "allow_grave_key",
    "allow_lost_tablet",
    "allow_magic_scroll",
    "allow_scroll_of_knowledge",
]

NEG_CONFIGS = [
    ("not_enough_glyphs:glyph_plow", "not_enough_glyphs/glyph_plow.toml"),
    ("not_enough_glyphs:glyph_trail", "not_enough_glyphs/glyph_trail.toml"),
    ("not_enough_glyphs:glyph_ride", "not_enough_glyphs/glyph_ride.toml"),
    ("not_enough_glyphs:glyph_feed", "not_enough_glyphs/glyph_feed.toml"),
    ("not_enough_glyphs:glyph_filter_light", "not_enough_glyphs/glyph_filter_light.toml"),
    ("not_enough_glyphs:glyph_filter_dark", "not_enough_glyphs/glyph_filter_dark.toml"),
    ("not_enough_glyphs:glyph_contingency_fall", "not_enough_glyphs/glyph_contingency_fall.toml"),
    ("not_enough_glyphs:glyph_contingency_heal", "not_enough_glyphs/glyph_contingency_heal.toml"),
    ("not_enough_glyphs:glyph_contingency_health", "not_enough_glyphs/glyph_contingency_health.toml"),
    ("not_enough_glyphs:glyph_contingency_death", "not_enough_glyphs/glyph_contingency_death.toml"),
    ("not_enough_glyphs:glyph_contingency_fire", "not_enough_glyphs/glyph_contingency_fire.toml"),
    ("not_enough_glyphs:glyph_contingency_blink", "not_enough_glyphs/glyph_contingency_blink.toml"),
    ("not_enough_glyphs:glyph_contingency_time", "not_enough_glyphs/glyph_contingency_time.toml"),
    ("not_enough_glyphs:glyph_propagate_plane", "not_enough_glyphs/glyph_propagate_plane.toml"),
    ("toomanyglyphs:glyph_ray", "toomanyglyphs/glyph_ray.toml"),
    ("toomanyglyphs:glyph_reverse_direction", "toomanyglyphs/glyph_reverse_direction.toml"),
    ("toomanyglyphs:glyph_chaining", "toomanyglyphs/glyph_chaining.toml"),
    ("toomanyglyphs:glyph_filter_block", "toomanyglyphs/glyph_filter_block.toml"),
    ("toomanyglyphs:glyph_filter_entity", "toomanyglyphs/glyph_filter_entity.toml"),
    ("toomanyglyphs:glyph_filter_living", "toomanyglyphs/glyph_filter_living.toml"),
    ("toomanyglyphs:glyph_filter_living_not_monster", "toomanyglyphs/glyph_filter_living_not_monster.toml"),
    ("toomanyglyphs:glyph_filter_living_not_player", "toomanyglyphs/glyph_filter_living_not_player.toml"),
    ("toomanyglyphs:glyph_filter_monster", "toomanyglyphs/glyph_filter_monster.toml"),
    ("toomanyglyphs:glyph_filter_player", "toomanyglyphs/glyph_filter_player.toml"),
    ("toomanyglyphs:glyph_filter_item", "toomanyglyphs/glyph_filter_item.toml"),
    ("toomanyglyphs:glyph_filter_animal", "toomanyglyphs/glyph_filter_animal.toml"),
    ("toomanyglyphs:glyph_filter_is_baby", "toomanyglyphs/glyph_filter_is_baby.toml"),
    ("toomanyglyphs:glyph_filter_is_mature", "toomanyglyphs/glyph_filter_is_mature.toml"),
    ("ars_trinkets:glyph_filter_self", "ars_trinkets/glyph_filter_self.toml"),
    ("ars_trinkets:glyph_filter_not_self", "ars_trinkets/glyph_filter_not_self.toml"),
    ("arsomega:glyph_flatten", "arsomega/glyph_flatten.toml"),
    ("arsomega:glyph_propagate_underfoot", "arsomega/glyph_propagate_underfoot.toml"),
    ("arsomega:glyph_propagate_projectile", "arsomega/glyph_propagate_projectile.toml"),
    ("arsomega:glyph_propagate_self", "arsomega/glyph_propagate_self.toml"),
    ("arsomega:glyph_missile", "arsomega/glyph_missile.toml"),
    ("arsomega:glyph_overhead", "arsomega/glyph_overhead.toml"),
    ("arsomega:glyph_propagate_missile", "arsomega/glyph_propagate_missile.toml"),
    ("arsomega:glyph_propagate_overhead", "arsomega/glyph_propagate_overhead.toml"),
    ("ars_scalaes:glyph_resize", "ars_scalaes/glyph_resize.toml"),
]

MOD_PATTERNS = {
    "asterism_arcanum": ["asterismarcanum-1.21.1-0.1.0.jar"],
    "deeper_and_darker": ["deeperdarker-neoforge-1.21.1-1.4.1.jar"],
    "corail_tombstone": ["tombstone-neoforge-1.21.1-9.5.6.jar"],
    "gaze": ["gaze-1.1.7.1.jar"],
    "ice_and_fire_ce": ["iceandfire-2.1.2.jar"],
    "kubejs": ["kubejs-neoforge-2101.7.2-build.377.jar"],
    "kubejsarsnouveau": ["kubejsarsnouveau-1.3.2.jar"],
    "irons_spellbooks": ["irons_spellbooks-1.21.1-3.16.3.jar"],
    "irons_spells_js": ["irons_spells_js-4.0.3.jar"],
    "not_enough_glyphs": ["not_enough_glyphs-1.21.1-4.6.2.jar"],
    "mowzies_mobs": ["mowziesmobs-1.21.1-1.8.2.jar"],
    "somake_spells": ["somakespells-1.0.9-1.21.1.jar"],
    "shadowsz": ["shadowsz-1.1.9.jar"],
    "simply_swords_cataclysm": ["simplycataclysm-1.0.2+1.21.1+neoforge.jar"],
    "simply_more": ["simplymore-forge-1.3.0_alpha.jar"],
    "simply_swords": ["simplyswords-neoforge-1.70.2-1.21.1.jar"],
    "traveloptics": [
        "traveloptics-4.4.0.1-1.21.1.jar",
        "traveloptics-4.4.0.1.1-1.21.1-patched.jar",
    ],
}

TEXT_EXTENSIONS = {".toml", ".json", ".cfg", ".conf", ".txt", ".js", ".snbt", ".zs"}
KUBEJS_IRONS_MARKER_LINE_LIMIT = 64
KUBEJS_IRONS_MARKER_PATTERNS = {
    "spell_registry_literal": re.compile(r"irons_spellbooks:spells"),
    "school_registry_literal": re.compile(r"irons_spellbooks:schools"),
    "spell_registry_key_binding": re.compile(r"\bSpellRegistry\.SPELL_REGISTRY_KEY\b"),
    "school_registry_key_binding": re.compile(r"\bSchoolRegistry\.SCHOOL_REGISTRY_KEY\b"),
    "iss_event_bridge": re.compile(r"\bISSEvents\."),
    "irons_spells_js_builder_literal": re.compile(
        r"[\"\'](?:(?:irons_spells_js:)?(?:spell|magic_sword|staff|spellbook)|"
        r"irons_spells_js:(?:spellcasting|spell_projectile))[\"\']"
    ),
}
ASTERISM_DATA_RELATIVE = "asterismarcanum/irons_spellbooks_spell_config/astral_gateway.json"
ASTERISM_DATAPACK_PATH = f"data/{ASTERISM_DATA_RELATIVE}"
TRAVELOPTICS_BLACKOUT_LITERAL = "traveloptics:blackout"

CATALOG_PROBE_PREFIX = "[BLACK_ARCANA_CATALOG_PROBE]"
CATALOG_PROBE_LOGGER = "dev.gustavopere.blackarcana.qa.catalog.CatalogRuntimeEvidence"
CATALOG_PROBE_LOG_LINE_RE = re.compile(
    rf"^\[[^\]\r\n]+\] \[[^\]\r\n]+\] "
    rf"\[{re.escape(CATALOG_PROBE_LOGGER)}/[^\]\r\n]*\]: "
    rf"{re.escape(CATALOG_PROBE_PREFIX)}(?P<payload>.*)$"
)
SUPPORTED_CATALOG_PROBE_SCHEMAS = {1, 2, 3, 4}
TARGET_PROBE_MOD_IDS = {
    "ars_nouveau",
    "asterismarcanum",
    "gaze",
    "irons_spellbooks",
    "not_enough_glyphs",
    "somakespells",
    "traveloptics",
}
TARGET_PROBE_SPELL_NAMESPACES = {
    "asterismarcanum",
    "gaze",
    "somakespells",
    "traveloptics",
}
TARGET_PROBE_LOOT_IDS = {
    "traveloptics:key_loot",
    "traveloptics:universal_loot",
}
TARGET_PROBE_GLYPH_IDS = {registry_id for registry_id, _ in NEG_CONFIGS}
RESOURCE_LOCATION_RE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
SIMPLE_ERROR_RE = re.compile(r"^[A-Za-z0-9_$]+$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SAFE_JAR_FILENAME_RE = re.compile(r"^[A-Za-z0-9_.+\-]+\.jar$")


def _probe_bool(value: str | None) -> bool | None:
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def _probe_nonnegative_int(value: str | None) -> int | None:
    try:
        parsed = int(value) if value is not None else None
    except ValueError:
        return None
    if parsed is None or parsed < 0:
        return None
    return parsed


def _probe_resource_location(value: str | None) -> str | None:
    if value is None or RESOURCE_LOCATION_RE.fullmatch(value) is None:
        return None
    return value


def _probe_error(value: str | None) -> str | None:
    if value is None or SIMPLE_ERROR_RE.fullmatch(value) is None:
        return None
    return value


def parse_catalog_probe_payload(payload: str) -> dict[str, Any] | None:
    fields: dict[str, str] = {}
    for token in payload.strip().split():
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        fields[key] = value

    row_type = fields.get("type")
    if row_type in {"begin", "end"}:
        schema = _probe_nonnegative_int(fields.get("schema"))
        if schema is None:
            return None
        return {"type": row_type, "schema": schema}

    if row_type == "mod":
        mod_id = fields.get("id")
        loaded = _probe_bool(fields.get("loaded"))
        if mod_id not in TARGET_PROBE_MOD_IDS or loaded is None:
            return None
        return {"type": "mod", "id": mod_id, "loaded": loaded}

    if row_type == "mod_file":
        mod_id = fields.get("id")
        status = fields.get("status")
        if mod_id != "traveloptics":
            return None
        if status == "HASH_UNAVAILABLE":
            error = _probe_error(fields.get("error"))
            if error is None:
                return None
            return {
                "type": "mod_file",
                "id": "traveloptics",
                "status": status,
                "error": error,
            }
        if status != "OBSERVED":
            return None

        file_name = fields.get("file_name")
        size_bytes = _probe_nonnegative_int(fields.get("size_bytes"))
        sha1 = fields.get("sha1")
        if (
            file_name is None
            or SAFE_JAR_FILENAME_RE.fullmatch(file_name) is None
            or size_bytes is None
            or sha1 is None
            or SHA1_RE.fullmatch(sha1) is None
        ):
            return None
        return {
            "type": "mod_file",
            "id": "traveloptics",
            "status": status,
            "file_name": file_name,
            "size_bytes": size_bytes,
            "sha1": sha1,
        }

    if row_type == "spell":
        registry_id = _probe_resource_location(fields.get("id"))
        status = fields.get("status")
        if registry_id is None or registry_id.split(":", 1)[0] not in TARGET_PROBE_SPELL_NAMESPACES:
            return None
        if status == "OBSERVED":
            school = _probe_resource_location(fields.get("school"))
            enabled = _probe_bool(fields.get("enabled"))
            allow_crafting = _probe_bool(fields.get("allow_crafting"))
            if school is None or enabled is None or allow_crafting is None:
                return None
            return {
                "type": "spell",
                "id": registry_id,
                "status": status,
                "school": school,
                "enabled": enabled,
                "allow_crafting": allow_crafting,
            }
        if status == "REGISTRY_VALUE_UNAVAILABLE":
            return {"type": "spell", "id": registry_id, "status": status}
        if status == "HOST_VALUE_UNAVAILABLE":
            error = _probe_error(fields.get("error"))
            if error is None:
                return None
            return {"type": "spell", "id": registry_id, "status": status, "error": error}
        return None

    if row_type == "glyph":
        registry_id = _probe_resource_location(fields.get("id"))
        status = fields.get("status")
        if registry_id not in TARGET_PROBE_GLYPH_IDS:
            return None
        if status == "OBSERVED":
            enabled = _probe_bool(fields.get("enabled"))
            if enabled is None:
                return None
            return {
                "type": "glyph",
                "id": registry_id,
                "status": status,
                "enabled": enabled,
            }
        if status == "NOT_REGISTERED":
            return {"type": "glyph", "id": registry_id, "status": status}
        if status == "HOST_VALUE_UNAVAILABLE":
            error = _probe_error(fields.get("error"))
            if error is None:
                return None
            return {
                "type": "glyph",
                "id": registry_id,
                "status": status,
                "error": error,
            }
        return None

    if row_type == "summary":
        namespace = fields.get("namespace")
        count = _probe_nonnegative_int(fields.get("registered_count"))
        if namespace not in TARGET_PROBE_SPELL_NAMESPACES or count is None:
            return None
        return {"type": "summary", "namespace": namespace, "registered_count": count}

    if row_type == "loot_modifier_serializer":
        registry_id = _probe_resource_location(fields.get("id"))
        status = fields.get("status")
        if registry_id not in TARGET_PROBE_LOOT_IDS or status not in {"OBSERVED", "NOT_PRESENT"}:
            return None
        return {"type": row_type, "id": registry_id, "status": status}

    if row_type == "loot_modifier_pair":
        if fields.get("namespace") != "traveloptics":
            return None
        status = fields.get("status")
        if status == "OBSERVED":
            distinct = _probe_bool(fields.get("distinct_codec_instances"))
            if distinct is None:
                return None
            return {
                "type": row_type,
                "namespace": "traveloptics",
                "status": status,
                "distinct_codec_instances": distinct,
            }
        if status == "INCOMPLETE":
            key_present = _probe_bool(fields.get("key_loot_present"))
            universal_present = _probe_bool(fields.get("universal_loot_present"))
            if key_present is None or universal_present is None:
                return None
            return {
                "type": row_type,
                "namespace": "traveloptics",
                "status": status,
                "key_loot_present": key_present,
                "universal_loot_present": universal_present,
            }
        if status == "REGISTRY_VALUE_UNAVAILABLE":
            error = _probe_error(fields.get("error"))
            if error is None:
                return None
            return {
                "type": row_type,
                "namespace": "traveloptics",
                "status": status,
                "error": error,
            }
        return None

    return None


def collect_catalog_runtime_probe(instance: Path, probe_log: Path | None) -> dict[str, Any]:
    path = probe_log if probe_log is not None else instance / "logs" / "latest.log"
    path = path.expanduser().resolve()

    out: dict[str, Any] = {
        "source": rel(path, instance),
        "status": "NOT_FOUND",
        "schema": None,
        "rows": [],
        "ignored_prefixed_rows": 0,
        "embedded_prefix_rows_ignored": 0,
    }
    if not path.is_file():
        return out

    saw_prefix = False
    ignored = 0
    embedded_ignored = 0
    current: dict[str, Any] | None = None
    last_complete: dict[str, Any] | None = None

    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                stripped = line.rstrip("\r\n")
                if stripped.startswith(CATALOG_PROBE_PREFIX):
                    payload = stripped[len(CATALOG_PROBE_PREFIX):]
                elif CATALOG_PROBE_PREFIX in stripped:
                    logged = CATALOG_PROBE_LOG_LINE_RE.fullmatch(stripped)
                    if logged is None:
                        embedded_ignored += 1
                        continue
                    payload = logged.group("payload")
                else:
                    continue

                saw_prefix = True
                row = parse_catalog_probe_payload(payload)
                if row is None:
                    ignored += 1
                    continue

                if row["type"] == "begin":
                    current = {"schema": row["schema"], "rows": []}
                    continue

                if current is None:
                    continue

                if row["type"] == "end":
                    if row["schema"] == current["schema"]:
                        last_complete = current
                    current = None
                    continue

                current["rows"].append(row)
    except OSError as exc:
        out["status"] = "READ_ERROR"
        out["error"] = type(exc).__name__
        return out

    out["ignored_prefixed_rows"] = ignored
    out["embedded_prefix_rows_ignored"] = embedded_ignored
    if last_complete is not None:
        out["schema"] = last_complete["schema"]
        if last_complete["schema"] not in SUPPORTED_CATALOG_PROBE_SCHEMAS:
            out["status"] = "UNSUPPORTED_SCHEMA"
            return out
        out["status"] = "COMPLETE"
        out["rows"] = last_complete["rows"]
    elif saw_prefix:
        out["status"] = "NO_COMPLETE_BLOCK"
    else:
        out["status"] = "NO_PROBE_ROWS"
    return out


def digest_file(path: Path) -> dict[str, Any]:
    h1 = hashlib.sha1()
    h256 = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h1.update(chunk)
            h256.update(chunk)
    return {
        "filename": path.name,
        "sha1": h1.hexdigest(),
        "sha256": h256.hexdigest(),
        "size_bytes": path.stat().st_size,
    }


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.name


def collect_irons_spellbooks_kubejs_markers(path: Path) -> tuple[dict[str, list[int]], bool]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return {}, False

    markers: dict[str, list[int]] = {}
    truncated = False
    for line_number, line in enumerate(lines, start=1):
        for marker_type, pattern in KUBEJS_IRONS_MARKER_PATTERNS.items():
            if pattern.search(line) is None:
                continue
            marker_lines = markers.setdefault(marker_type, [])
            if len(marker_lines) < KUBEJS_IRONS_MARKER_LINE_LIMIT:
                marker_lines.append(line_number)
            else:
                truncated = True
    return markers, truncated

def collect_kubejs_script_inventory(instance: Path) -> dict[str, Any]:
    root = instance / "kubejs"
    surfaces = {
        "startup_scripts": root / "startup_scripts",
        "server_scripts": root / "server_scripts",
        "client_scripts": root / "client_scripts",
        "data": root / "data",
    }
    rows: list[dict[str, Any]] = []
    counts = {surface: 0 for surface in surfaces}

    for surface, surface_root in surfaces.items():
        if not surface_root.is_dir():
            continue
        for path in sorted(surface_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            digest = digest_file(path)
            row = {
                "surface": surface,
                "path": rel(path, instance),
                "sha256": digest["sha256"],
                "size_bytes": digest["size_bytes"],
            }
            markers, markers_truncated = collect_irons_spellbooks_kubejs_markers(path)
            if markers:
                row["irons_spellbooks_kubejs_markers"] = markers
                if markers_truncated:
                    row["irons_spellbooks_kubejs_markers_truncated"] = True
            rows.append(row)
            counts[surface] += 1

    rows.sort(key=lambda row: row["path"])
    return {
        "kubejs_root_present": root.is_dir(),
        "file_count": len(rows),
        "surface_counts": counts,
        "files": rows,
    }


def classify_irons_spellbooks_kubejs_closure(
    mods: dict[str, Any],
    kubejs_inventory: dict[str, Any],
) -> dict[str, Any]:
    provider_entries = mods.get("irons_spells_js", [])
    artifact_observed = bool(provider_entries)
    artifact_certified = any(
        entry.get("current_physical_4_0_3_equality") is True
        for entry in provider_entries
        if isinstance(entry, dict)
    )

    irons_host_entries = mods.get("irons_spellbooks", [])
    irons_host_observed = bool(irons_host_entries)
    irons_host_certified = any(
        entry.get("current_physical_3_16_3_equality") is True
        for entry in irons_host_entries
        if isinstance(entry, dict)
    )

    host_entries = mods.get("kubejs", [])
    kubejs_host_observed = bool(host_entries)
    kubejs_host_certified = any(
        entry.get("current_physical_build_377_equality") is True
        for entry in host_entries
        if isinstance(entry, dict)
    )

    files = kubejs_inventory.get("files", [])
    marker_files = [
        row
        for row in files
        if isinstance(row, dict) and row.get("irons_spellbooks_kubejs_markers")
    ]
    marker_types = sorted(
        {
            marker_type
            for row in marker_files
            for marker_type in row.get("irons_spellbooks_kubejs_markers", {})
        }
    )
    bounded_file_count = int(kubejs_inventory.get("file_count", 0))

    if not artifact_observed:
        status = "ARTIFACT_NOT_OBSERVED"
    elif not artifact_certified:
        status = "ARTIFACT_HASH_MISMATCH"
    elif not irons_host_observed:
        status = "IRONS_HOST_NOT_OBSERVED"
    elif not irons_host_certified:
        status = "IRONS_HOST_HASH_MISMATCH"
    elif not kubejs_host_observed:
        status = "KUBEJS_HOST_NOT_OBSERVED"
    elif not kubejs_host_certified:
        status = "KUBEJS_HOST_HASH_MISMATCH"
    elif bounded_file_count == 0:
        status = "ZERO_CONTENT_REVIEW_CANDIDATE"
    else:
        status = "SCRIPT_REVIEW_REQUIRED"

    return {
        "status": status,
        "artifact_certified": artifact_certified,
        "irons_host_certified": irons_host_certified,
        "kubejs_host_certified": kubejs_host_certified,
        "kubejs_root_present": bool(kubejs_inventory.get("kubejs_root_present")),
        "bounded_file_count": bounded_file_count,
        "marker_file_count": len(marker_files),
        "marker_types": marker_types,
    }


def candidate_worlds(instance: Path, explicit: list[Path]) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()

    for world in explicit:
        resolved = world.resolve()
        if resolved.exists() and resolved not in seen:
            seen.add(resolved)
            out.append(resolved)

    saves = instance / "saves"
    if saves.is_dir():
        for child in sorted(saves.iterdir()):
            if child.is_dir():
                resolved = child.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    out.append(resolved)

    for name in ("world", "server-world"):
        child = instance / name
        if child.is_dir():
            resolved = child.resolve()
            if resolved not in seen:
                seen.add(resolved)
                out.append(resolved)

    return out


def collect_mod_hashes(instance: Path) -> dict[str, Any]:
    mods = instance / "mods"
    result: dict[str, Any] = {}
    for provider, names in MOD_PATTERNS.items():
        entries = []
        for name in names:
            path = mods / name
            if path.is_file():
                entry = digest_file(path)
                if provider == "asterism_arcanum":
                    entry["current_physical_0_1_0_equality"] = entry["sha1"] == ASTERISM_010_PHYSICAL_SHA1
                elif provider == "deeper_and_darker":
                    entry["current_physical_1_4_1_equality"] = entry["sha1"] == DEEPER_DARKER_141_PHYSICAL_SHA1
                elif provider == "traveloptics":
                    if entry["sha1"] == TRAVELOPTICS_ORIGINAL_SHA1:
                        entry["classification"] = "ORIGINAL_EXACT"
                    elif entry["sha1"] == TRAVELOPTICS_PATCH_SHA1:
                        entry["classification"] = "PATCHED_EXACT"
                    else:
                        entry["classification"] = "OTHER_VERIFIED"
                elif provider == "somake_spells":
                    entry["release_1_0_9_equality"] = entry["sha1"] == SOMAKE_109_RELEASE_SHA1
                elif provider == "gaze":
                    entry["known_1_1_7_1_equality"] = entry["sha1"] == GAZE_1171_SHA1
                elif provider == "kubejs":
                    entry["current_physical_build_377_equality"] = entry["sha1"] == KUBEJS_2101_7_2_BUILD_377_PHYSICAL_SHA1
                elif provider == "kubejsarsnouveau":
                    entry["current_physical_1_3_2_equality"] = entry["sha1"] == KUBEJSARSNOUVEAU_132_PHYSICAL_SHA1
                elif provider == "irons_spellbooks":
                    entry["current_physical_3_16_3_equality"] = entry["sha1"] == IRONS_SPELLBOOKS_3163_PHYSICAL_SHA1
                elif provider == "irons_spells_js":
                    entry["current_physical_4_0_3_equality"] = entry["sha1"] == IRONS_SPELLS_JS_403_PHYSICAL_SHA1
                elif provider == "not_enough_glyphs":
                    entry["release_4_6_2_equality"] = entry["sha1"] == NEG_462_RELEASE_SHA1
                elif provider == "corail_tombstone":
                    entry["release_9_5_6_equality"] = entry["sha1"] == TOMBSTONE_956_RELEASE_SHA1
                elif provider == "mowzies_mobs":
                    entry["current_physical_1_8_2_equality"] = entry["sha1"] == MOWZIES_MOBS_182_PHYSICAL_SHA1
                elif provider == "ice_and_fire_ce":
                    entry["release_2_1_2_equality"] = entry["sha1"] == ICE_AND_FIRE_CE_212_RELEASE_SHA1
                elif provider == "shadowsz":
                    entry["current_physical_1_1_9_equality"] = entry["sha1"] == SHADOWSZ_119_PHYSICAL_SHA1
                elif provider == "simply_swords_cataclysm":
                    entry["current_physical_1_0_2_equality"] = entry["sha1"] == SIMPLY_CATACLYSM_102_PHYSICAL_SHA1
                elif provider == "simply_more":
                    entry["current_physical_alpha5_equality"] = entry["sha1"] == SIMPLY_MORE_ALPHA5_PHYSICAL_SHA1
                elif provider == "simply_swords":
                    entry["current_physical_1_70_2_equality"] = entry["sha1"] == SIMPLY_SWORDS_1702_PHYSICAL_SHA1
                entries.append(entry)
        result[provider] = entries
    return result


def load_json_selected(path: Path, keys: list[str]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}

    selected: dict[str, Any] = {}
    for key in keys:
        short = key.split(":", 1)[-1]
        if key in data:
            selected[key] = data[key]
        elif short in data:
            selected[key] = data[short]
    return selected


def collect_asterism(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    local = instance / "config" / "irons_spellbooks_spell_config" / "asterismarcanum" / "astral_gateway.json"
    global_config = instance / "config" / "irons_spellbooks_spell_config" / "global_config.json"
    selected_keys = [
        "irons_spellbooks:enabled",
        "irons_spellbooks:school",
        "irons_spellbooks:allow_crafting",
    ]

    out: dict[str, Any] = {
        "per_spell_local": None,
        "global_config": None,
        "datapack_overrides": [],
    }

    if local.is_file():
        out["per_spell_local"] = {
            "path": rel(local, instance),
            "selected": load_json_selected(local, selected_keys),
        }

    if global_config.is_file():
        out["global_config"] = {
            "path": rel(global_config, instance),
            "selected": load_json_selected(global_config, selected_keys),
        }

    kubejs_override = instance / "kubejs" / "data" / ASTERISM_DATA_RELATIVE
    if kubejs_override.is_file():
        out["datapack_overrides"].append({
            "source": "kubejs_data",
            "path": rel(kubejs_override, instance),
            "selected": load_json_selected(kubejs_override, selected_keys),
        })

    for world in worlds:
        datapacks = world / "datapacks"
        if not datapacks.is_dir():
            continue
        for path in sorted(datapacks.rglob("astral_gateway.json")):
            normalized = path.as_posix()
            if normalized.endswith(ASTERISM_DATAPACK_PATH):
                out["datapack_overrides"].append({
                    "source": "world_datapack",
                    "path": rel(path, instance),
                    "selected": load_json_selected(path, selected_keys),
                })
        for archive in sorted(datapacks.glob("*.zip")):
            try:
                with zipfile.ZipFile(archive) as zf:
                    if ASTERISM_DATAPACK_PATH in zf.namelist():
                        raw = zf.read(ASTERISM_DATAPACK_PATH).decode("utf-8")
                        data = json.loads(raw)
                        selected = {}
                        for key in selected_keys:
                            short = key.split(":", 1)[-1]
                            if key in data:
                                selected[key] = data[key]
                            elif short in data:
                                selected[key] = data[short]
                        out["datapack_overrides"].append({
                            "source": "world_datapack_zip",
                            "path": f"{rel(archive, instance)}!/{ASTERISM_DATAPACK_PATH}",
                            "selected": selected,
                        })
            except Exception as exc:
                out["datapack_overrides"].append({
                    "path": rel(archive, instance),
                    "error": f"{type(exc).__name__}: {exc}",
                })

    return out


def iter_text_files(roots: list[Path]):
    seen: set[Path] = set()
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield path


def collect_exact_literal_references(
    instance: Path,
    roots: list[tuple[str, Path]],
    literal: str,
) -> list[dict[str, Any]]:
    """Return path/line evidence for one exact literal without retaining source text."""
    matches: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()

    for source, root in roots:
        for path in iter_text_files([root]):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if literal not in line:
                    continue
                key = (rel(path, instance), lineno, source)
                if key in seen:
                    continue
                seen.add(key)
                matches.append({
                    "source": source,
                    "path": key[0],
                    "line": lineno,
                    "literal": literal,
                })

    return matches


def collect_zip_literal_references(
    instance: Path,
    archives: list[tuple[str, Path]],
    literal: str,
) -> list[dict[str, Any]]:
    """Search text-like ZIP entries for one exact literal without retaining entry contents."""
    matches: list[dict[str, Any]] = []

    for source, archive in archives:
        if not archive.is_file():
            continue
        try:
            with zipfile.ZipFile(archive) as zf:
                for name in sorted(zf.namelist()):
                    if Path(name).suffix.lower() not in TEXT_EXTENSIONS:
                        continue
                    try:
                        text = zf.read(name).decode("utf-8", errors="replace")
                    except Exception:
                        continue
                    for lineno, line in enumerate(text.splitlines(), start=1):
                        if literal in line:
                            matches.append({
                                "source": source,
                                "path": f"{rel(archive, instance)}!/{name}",
                                "line": lineno,
                                "literal": literal,
                            })
        except (OSError, zipfile.BadZipFile):
            continue

    return matches


def _find_key_recursive(value: Any, target: str, prefix: tuple[str, ...] = ()) -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            next_prefix = (*prefix, key_text)
            if key_text.lower() == target.lower():
                found.append((".".join(next_prefix), child))
            found.extend(_find_key_recursive(child, target, next_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_key_recursive(child, target, (*prefix, str(index))))
    return found


def collect_selected_key(instance: Path, roots: list[Path], key: str) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    fallback = re.compile(rf"\\b{re.escape(key)}\\b", re.IGNORECASE)

    for path in iter_text_files(roots):
        suffix = path.suffix.lower()

        if suffix == ".toml":
            try:
                with path.open("rb") as handle:
                    data = tomllib.load(handle)
                for key_path, value in _find_key_recursive(data, key):
                    matches.append({
                        "path": rel(path, instance),
                        "key_path": key_path,
                        "value": value,
                        "parser": "tomllib",
                    })
                continue
            except Exception as exc:
                matches.append({
                    "path": rel(path, instance),
                    "parser": "tomllib",
                    "error": f"{type(exc).__name__}: {exc}",
                })
                continue

        if suffix == ".json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                for key_path, value in _find_key_recursive(data, key):
                    matches.append({
                        "path": rel(path, instance),
                        "key_path": key_path,
                        "value": value,
                        "parser": "json",
                    })
                continue
            except Exception as exc:
                matches.append({
                    "path": rel(path, instance),
                    "parser": "json",
                    "error": f"{type(exc).__name__}: {exc}",
                })
                continue

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";", "//")):
                continue
            if fallback.search(line):
                matches.append({
                    "path": rel(path, instance),
                    "line": lineno,
                    "match": stripped,
                    "parser": "text-fallback",
                })

    return matches



def collect_deeper_and_darker(instance: Path) -> dict[str, Any]:
    path = instance / "config" / "deeperdarker-common.toml"
    evidence: dict[str, Any] = {
        "path": rel(path, instance),
        "key_path": "soulElytraCooldown",
        "status": "NOT_FOUND",
    }
    if not path.is_file():
        return {"soul_elytra_cooldown": evidence}

    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except Exception as exc:
        evidence["status"] = "PARSE_ERROR"
        evidence["error"] = type(exc).__name__
        return {"soul_elytra_cooldown": evidence}

    matches = _find_key_recursive(data, "soulElytraCooldown")
    if not matches:
        evidence["status"] = "KEY_NOT_FOUND"
        return {"soul_elytra_cooldown": evidence}
    if len(matches) != 1:
        evidence["status"] = "AMBIGUOUS_KEY"
        evidence["match_count"] = len(matches)
        return {"soul_elytra_cooldown": evidence}

    key_path, value = matches[0]
    evidence["key_path"] = key_path
    if isinstance(value, bool) or not isinstance(value, int):
        evidence["status"] = "INVALID_TYPE"
        evidence["value_type"] = type(value).__name__
        return {"soul_elytra_cooldown": evidence}

    evidence["value"] = value
    if value < -1 or value > 12000:
        evidence["status"] = "OUT_OF_RANGE"
        return {"soul_elytra_cooldown": evidence}

    evidence["status"] = "OBSERVED"
    return {"soul_elytra_cooldown": evidence}


def collect_ice_and_fire_ce(instance: Path) -> dict[str, Any]:
    path = instance / "config" / "iceandfire" / "iaf-common.json"
    evidence: dict[str, Any] = {
        "path": rel(path, instance),
        "key_path": "tools.phantasmalBladeAbility",
        "status": "NOT_FOUND",
    }
    if not path.is_file():
        return {"phantasmal_blade_ability": evidence}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        evidence["status"] = "PARSE_ERROR"
        evidence["error"] = type(exc).__name__
        return {"phantasmal_blade_ability": evidence}

    tools = data.get("tools") if isinstance(data, dict) else None
    if not isinstance(tools, dict) or "phantasmalBladeAbility" not in tools:
        evidence["status"] = "KEY_NOT_FOUND"
        return {"phantasmal_blade_ability": evidence}

    value = tools["phantasmalBladeAbility"]
    if not isinstance(value, bool):
        evidence["status"] = "INVALID_TYPE"
        evidence["value_type"] = type(value).__name__
        return {"phantasmal_blade_ability": evidence}

    evidence["status"] = "OBSERVED"
    evidence["value"] = value
    return {"phantasmal_blade_ability": evidence}



class _NbtReader:
    """Minimal big-endian NBT reader for saved-world level.dat evidence."""

    MAX_COLLECTION_LENGTH = 10_000_000

    def __init__(self, handle):
        self.handle = handle

    def _read_exact(self, size: int) -> bytes:
        data = self.handle.read(size)
        if len(data) != size:
            raise ValueError("Unexpected end of NBT payload")
        return data

    def _unpack(self, fmt: str):
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self._read_exact(size))[0]

    def read_u8(self) -> int:
        return self._unpack(">B")

    def read_string(self) -> str:
        length = self._unpack(">H")
        return self._read_exact(length).decode("utf-8")

    def read_length(self) -> int:
        length = self._unpack(">i")
        if length < 0 or length > self.MAX_COLLECTION_LENGTH:
            raise ValueError(f"Invalid NBT collection length: {length}")
        return length

    def read_payload(self, tag_id: int):
        if tag_id == 0:
            return None
        if tag_id == 1:
            return self._unpack(">b")
        if tag_id == 2:
            return self._unpack(">h")
        if tag_id == 3:
            return self._unpack(">i")
        if tag_id == 4:
            return self._unpack(">q")
        if tag_id == 5:
            return self._unpack(">f")
        if tag_id == 6:
            return self._unpack(">d")
        if tag_id == 7:
            return self._read_exact(self.read_length())
        if tag_id == 8:
            return self.read_string()
        if tag_id == 9:
            child_tag = self.read_u8()
            length = self.read_length()
            return [self.read_payload(child_tag) for _ in range(length)]
        if tag_id == 10:
            out: dict[str, Any] = {}
            while True:
                child_tag = self.read_u8()
                if child_tag == 0:
                    return out
                name = self.read_string()
                out[name] = self.read_payload(child_tag)
        if tag_id == 11:
            return [self._unpack(">i") for _ in range(self.read_length())]
        if tag_id == 12:
            return [self._unpack(">q") for _ in range(self.read_length())]
        raise ValueError(f"Unsupported NBT tag id: {tag_id}")


def read_level_dat_gamerule(path: Path, key: str) -> dict[str, Any]:
    """Read exactly one boolean gamerule from a saved level.dat, fail-closed."""

    try:
        with gzip.open(path, "rb") as handle:
            reader = _NbtReader(handle)
            root_tag = reader.read_u8()
            if root_tag != 10:
                return {"status": "INVALID_ROOT_TAG"}
            reader.read_string()
            root = reader.read_payload(root_tag)
    except (OSError, EOFError, UnicodeDecodeError, ValueError, struct.error) as exc:
        return {"status": "READ_ERROR", "error": type(exc).__name__}

    if not isinstance(root, dict):
        return {"status": "INVALID_ROOT"}

    data = root.get("Data")
    if not isinstance(data, dict):
        return {"status": "DATA_NOT_FOUND"}

    gamerules = data.get("GameRules")
    if not isinstance(gamerules, dict):
        return {"status": "GAMERULES_NOT_FOUND"}

    value = gamerules.get(key)
    if value == "true":
        return {"status": "OBSERVED", "value": True}
    if value == "false":
        return {"status": "OBSERVED", "value": False}
    if value is None:
        return {"status": "KEY_NOT_FOUND"}
    return {"status": "INVALID_VALUE", "value_type": type(value).__name__}


def collect_shadowsz(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots = [instance / "config", instance / "defaultconfigs"]
    roots.extend(world / "serverconfig" for world in worlds)

    gamerules: list[dict[str, Any]] = []
    for world in worlds:
        path = world / "level.dat"
        row: dict[str, Any] = {
            "world": rel(world, instance),
            "path": rel(path, instance),
            "status": "NOT_FOUND",
        }
        if path.is_file():
            observed = read_level_dat_gamerule(path, "shadowszRestrictPowers")
            row.update(observed)
        gamerules.append(row)

    return {
        "fusion_enabled_matches": collect_selected_key(
            instance,
            roots,
            "fusionEnabled",
        ),
        "restrict_powers_gamerules": gamerules,
    }

def collect_simply_cataclysm(instance: Path) -> dict[str, Any]:
    path = instance / "config" / "simplycataclysm-startup.toml"
    evidence: dict[str, Any] = {
        "path": rel(path, instance),
        "status": "NOT_FOUND",
        "selected": {},
    }
    if not path.is_file():
        return {"startup_config": evidence}

    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except Exception as exc:
        evidence["status"] = "PARSE_ERROR"
        evidence["error"] = type(exc).__name__
        return {"startup_config": evidence}

    selected: dict[str, Any] = {}
    complete = True
    for key in SIMPLY_CATACLYSM_STARTUP_CONFIG_KEYS:
        matches = _find_key_recursive(data, key)
        if len(matches) == 1:
            key_path, value = matches[0]
            selected[key] = {
                "status": "OBSERVED",
                "key_path": key_path,
                "value": value,
            }
        elif not matches:
            complete = False
            selected[key] = {"status": "KEY_NOT_FOUND"}
        else:
            complete = False
            selected[key] = {
                "status": "AMBIGUOUS",
                "match_count": len(matches),
            }

    evidence["selected"] = selected
    evidence["status"] = "OBSERVED" if complete else "INCOMPLETE"
    return {"startup_config": evidence}


def collect_simply_more(instance: Path) -> dict[str, Any]:
    path = instance / "config" / "simplymore" / "unique_effect.toml"
    evidence: dict[str, Any] = {
        "path": rel(path, instance),
        "status": "NOT_FOUND",
        "forms": [],
    }
    result: dict[str, Any] = {
        "expected_form_count": len(SIMPLY_MORE_MIMICRY_FORMS),
        "mimicry_form_disable_config": evidence,
    }
    if not path.is_file():
        return result

    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except Exception as exc:
        evidence["status"] = "PARSE_ERROR"
        evidence["error"] = type(exc).__name__
        return result

    mimicry = data.get("mimicry")
    config = mimicry.get("config") if isinstance(mimicry, dict) else None
    complete = True
    rows: list[dict[str, Any]] = []
    for form in SIMPLY_MORE_MIMICRY_FORMS:
        row: dict[str, Any] = {"form": form, "status": "KEY_NOT_FOUND"}
        section = config.get(form) if isinstance(config, dict) else None
        if isinstance(section, dict) and "disabled" in section:
            value = section["disabled"]
            if isinstance(value, bool):
                row = {
                    "form": form,
                    "status": "OBSERVED",
                    "disabled": value,
                }
            else:
                row = {
                    "form": form,
                    "status": "INVALID_VALUE",
                    "value_type": type(value).__name__,
                }
                complete = False
        else:
            complete = False
        rows.append(row)

    evidence["forms"] = rows
    evidence["status"] = "OBSERVED" if complete else "INCOMPLETE"
    return result


def collect_simply_swords(instance: Path) -> dict[str, Any]:
    general_path = instance / "config" / "simplyswords" / "general.toml"
    loot_path = instance / "config" / "simplyswords" / "loot.toml"

    awakening: dict[str, Any] = {
        "path": rel(general_path, instance),
        "status": "NOT_FOUND",
        "enableUniqueWeaponAwakening": {"status": "FILE_NOT_FOUND"},
    }

    if general_path.is_file():
        try:
            with general_path.open("rb") as handle:
                general_data = tomllib.load(handle)
        except Exception as exc:
            awakening["status"] = "PARSE_ERROR"
            awakening["error"] = type(exc).__name__
            awakening["enableUniqueWeaponAwakening"] = {"status": "PARSE_ERROR"}
        else:
            matches = _find_key_recursive(general_data, "enableUniqueWeaponAwakening")
            if len(matches) == 1:
                key_path, value = matches[0]
                if isinstance(value, bool):
                    awakening["status"] = "OBSERVED"
                    awakening["enableUniqueWeaponAwakening"] = {
                        "status": "OBSERVED",
                        "key_path": key_path,
                        "value": value,
                    }
                else:
                    awakening["status"] = "INVALID_VALUE"
                    awakening["enableUniqueWeaponAwakening"] = {
                        "status": "INVALID_VALUE",
                        "key_path": key_path,
                        "value_type": type(value).__name__,
                    }
            elif not matches:
                awakening["status"] = "INCOMPLETE"
                awakening["enableUniqueWeaponAwakening"] = {"status": "KEY_NOT_FOUND"}
            else:
                awakening["status"] = "INCOMPLETE"
                awakening["enableUniqueWeaponAwakening"] = {
                    "status": "AMBIGUOUS",
                    "match_count": len(matches),
                }

    loot: dict[str, Any] = {
        "path": rel(loot_path, instance),
        "status": "NOT_FOUND",
    }
    scalar_specs = {
        "enableLootDrops": "bool",
        "runicLootTableWeight": "number",
        "uniqueLootTableWeight": "number",
        "enableContainedRemnants": "bool",
    }
    for key in scalar_specs:
        loot[key] = {"status": "FILE_NOT_FOUND"}
    loot["disabledUniqueWeaponLoot"] = {
        "status": "FILE_NOT_FOUND",
        "values": [],
        "invalid_entry_count": 0,
    }
    loot["uniqueLootTableOptions"] = {
        "status": "FILE_NOT_FOUND",
        "entries": [],
        "invalid_entry_count": 0,
    }

    if loot_path.is_file():
        try:
            with loot_path.open("rb") as handle:
                loot_data = tomllib.load(handle)
        except Exception as exc:
            loot["status"] = "PARSE_ERROR"
            loot["error"] = type(exc).__name__
            for key in scalar_specs:
                loot[key] = {"status": "PARSE_ERROR"}
            loot["disabledUniqueWeaponLoot"] = {
                "status": "PARSE_ERROR",
                "values": [],
                "invalid_entry_count": 0,
            }
            loot["uniqueLootTableOptions"] = {
                "status": "PARSE_ERROR",
                "entries": [],
                "invalid_entry_count": 0,
            }
        else:
            complete = True

            for key, expected in scalar_specs.items():
                matches = _find_key_recursive(loot_data, key)
                if len(matches) == 1:
                    key_path, value = matches[0]
                    valid = (
                        isinstance(value, bool)
                        if expected == "bool"
                        else isinstance(value, (int, float)) and not isinstance(value, bool)
                    )
                    if valid:
                        loot[key] = {
                            "status": "OBSERVED",
                            "key_path": key_path,
                            "value": value,
                        }
                    else:
                        complete = False
                        loot[key] = {
                            "status": "INVALID_VALUE",
                            "key_path": key_path,
                            "value_type": type(value).__name__,
                        }
                elif not matches:
                    complete = False
                    loot[key] = {"status": "KEY_NOT_FOUND"}
                else:
                    complete = False
                    loot[key] = {
                        "status": "AMBIGUOUS",
                        "match_count": len(matches),
                    }

            disabled_matches = _find_key_recursive(loot_data, "disabledUniqueWeaponLoot")
            if len(disabled_matches) == 1:
                key_path, value = disabled_matches[0]
                if isinstance(value, list):
                    valid_ids = sorted(
                        item for item in value
                        if isinstance(item, str) and RESOURCE_LOCATION_RE.fullmatch(item)
                    )
                    invalid_count = len(value) - len(valid_ids)
                    loot["disabledUniqueWeaponLoot"] = {
                        "status": "OBSERVED" if invalid_count == 0 else "INVALID_VALUE",
                        "key_path": key_path,
                        "values": valid_ids,
                        "invalid_entry_count": invalid_count,
                    }
                    if invalid_count:
                        complete = False
                else:
                    complete = False
                    loot["disabledUniqueWeaponLoot"] = {
                        "status": "INVALID_VALUE",
                        "key_path": key_path,
                        "values": [],
                        "invalid_entry_count": 1,
                        "value_type": type(value).__name__,
                    }
            elif not disabled_matches:
                complete = False
                loot["disabledUniqueWeaponLoot"] = {
                    "status": "KEY_NOT_FOUND",
                    "values": [],
                    "invalid_entry_count": 0,
                }
            else:
                complete = False
                loot["disabledUniqueWeaponLoot"] = {
                    "status": "AMBIGUOUS",
                    "values": [],
                    "invalid_entry_count": 0,
                    "match_count": len(disabled_matches),
                }

            option_matches = _find_key_recursive(loot_data, "uniqueLootTableOptions")
            if len(option_matches) == 1:
                key_path, value = option_matches[0]
                if isinstance(value, dict):
                    entries: list[dict[str, Any]] = []
                    invalid_count = 0
                    for raw_id, raw_value in value.items():
                        if (
                            isinstance(raw_id, str)
                            and RESOURCE_LOCATION_RE.fullmatch(raw_id)
                            and isinstance(raw_value, (int, float))
                            and not isinstance(raw_value, bool)
                        ):
                            entries.append({"id": raw_id, "value": raw_value})
                        else:
                            invalid_count += 1
                    entries.sort(key=lambda row: row["id"])
                    loot["uniqueLootTableOptions"] = {
                        "status": "OBSERVED" if invalid_count == 0 else "INVALID_VALUE",
                        "key_path": key_path,
                        "entries": entries,
                        "invalid_entry_count": invalid_count,
                    }
                    if invalid_count:
                        complete = False
                else:
                    complete = False
                    loot["uniqueLootTableOptions"] = {
                        "status": "INVALID_VALUE",
                        "key_path": key_path,
                        "entries": [],
                        "invalid_entry_count": 1,
                        "value_type": type(value).__name__,
                    }
            elif not option_matches:
                complete = False
                loot["uniqueLootTableOptions"] = {
                    "status": "KEY_NOT_FOUND",
                    "entries": [],
                    "invalid_entry_count": 0,
                }
            else:
                complete = False
                loot["uniqueLootTableOptions"] = {
                    "status": "AMBIGUOUS",
                    "entries": [],
                    "invalid_entry_count": 0,
                    "match_count": len(option_matches),
                }

            loot["status"] = "OBSERVED" if complete else "INCOMPLETE"

    return {
        "awakening_config": awakening,
        "loot_config": loot,
    }


def collect_gaze(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots = [instance / "config", instance / "defaultconfigs"]
    roots.extend(world / "serverconfig" for world in worlds)
    return {
        "disableGazeRites_matches": collect_selected_key(
            instance,
            roots,
            "disableGazeRites",
        )
    }


def toml_general_enabled(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
        general = data.get("general")
        if isinstance(general, dict) and "enabled" in general:
            return {"enabled": general["enabled"]}
        return {"enabled": None}
    except Exception as exc:
        return {"enabled": None, "error": f"{type(exc).__name__}: {exc}"}


def collect_neg(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots: list[tuple[str, Path]] = [
        ("config", instance / "config"),
        ("defaultconfigs", instance / "defaultconfigs"),
    ]
    roots.extend((f"world_serverconfig:{rel(world, instance)}", world / "serverconfig") for world in worlds)

    rows = []
    for registry_id, relative in NEG_CONFIGS:
        found = []
        for source, root in roots:
            path = root / relative
            if path.is_file():
                found.append({
                    "source": source,
                    "path": rel(path, instance),
                    **toml_general_enabled(path),
                })
        rows.append({
            "registry_id": registry_id,
            "relative_path": relative,
            "observations": found,
        })

    return {
        "expected_candidate_count": len(NEG_CONFIGS),
        "rows": rows,
    }


def collect_irons_spell_namespace_overrides(
    instance: Path,
    worlds: list[Path],
    namespace: str,
) -> dict[str, Any]:
    """Collect only bounded Iron's spell-config keys for one provider namespace."""
    selected_keys = [
        "irons_spellbooks:enabled",
        "irons_spellbooks:school",
        "irons_spellbooks:allow_crafting",
    ]
    datapack_prefix = f"data/{namespace}/irons_spellbooks_spell_config/"

    out: dict[str, Any] = {
        "local_spell_configs": [],
        "global_config": None,
        "datapack_overrides": [],
    }

    local_dir = instance / "config" / "irons_spellbooks_spell_config" / namespace
    if local_dir.is_dir():
        for config_path in sorted(local_dir.glob("*.json")):
            out["local_spell_configs"].append({
                "path": rel(config_path, instance),
                "selected": load_json_selected(config_path, selected_keys),
            })

    global_config = instance / "config" / "irons_spellbooks_spell_config" / "global_config.json"
    if global_config.is_file():
        out["global_config"] = {
            "path": rel(global_config, instance),
            "selected": load_json_selected(global_config, selected_keys),
        }

    kubejs_dir = instance / "kubejs" / "data" / namespace / "irons_spellbooks_spell_config"
    if kubejs_dir.is_dir():
        for config_path in sorted(kubejs_dir.rglob("*.json")):
            out["datapack_overrides"].append({
                "source": "kubejs_data",
                "path": rel(config_path, instance),
                "selected": load_json_selected(config_path, selected_keys),
            })

    for world in worlds:
        datapacks = world / "datapacks"
        if not datapacks.is_dir():
            continue

        for config_path in sorted(datapacks.rglob("*.json")):
            normalized = config_path.as_posix()
            if f"/{datapack_prefix}" not in normalized:
                continue
            out["datapack_overrides"].append({
                "source": "world_datapack",
                "path": rel(config_path, instance),
                "selected": load_json_selected(config_path, selected_keys),
            })

        for archive in sorted(datapacks.glob("*.zip")):
            try:
                with zipfile.ZipFile(archive) as zf:
                    for name in sorted(zf.namelist()):
                        if not name.startswith(datapack_prefix) or not name.endswith(".json"):
                            continue
                        raw = zf.read(name).decode("utf-8")
                        data = json.loads(raw)
                        selected = {}
                        for key in selected_keys:
                            short = key.split(":", 1)[-1]
                            if key in data:
                                selected[key] = data[key]
                            elif short in data:
                                selected[key] = data[short]
                        out["datapack_overrides"].append({
                            "source": "world_datapack_zip",
                            "path": f"{rel(archive, instance)}!/{name}",
                            "selected": selected,
                        })
            except Exception as exc:
                out["datapack_overrides"].append({
                    "path": rel(archive, instance),
                    "error": f"{type(exc).__name__}: {exc}",
                })

    return out


def collect_mowzies_mobs(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots = [instance / "config", instance / "defaultconfigs"]
    roots.extend(world / "serverconfig" for world in worlds)
    return {
        "enable_tunneling_matches": collect_selected_key(
            instance,
            roots,
            "enable_tunneling",
        )
    }


def collect_tombstone(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots = [instance / "config", instance / "defaultconfigs"]
    roots.extend(world / "serverconfig" for world in worlds)

    rows = []
    for key in TOMBSTONE_ALLOWED_MAGIC_ITEM_KEYS:
        rows.append({
            "config_key": key,
            "observations": collect_selected_key(instance, roots, key),
        })

    return {
        "expected_candidate_count": len(TOMBSTONE_ALLOWED_MAGIC_ITEM_KEYS),
        "rows": rows,
    }


def collect_somake(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots = [instance / "config", instance / "defaultconfigs"]
    roots.extend(world / "serverconfig" for world in worlds)
    return {
        "enableSpellLockSystem_matches": collect_selected_key(
            instance,
            roots,
            "enableSpellLockSystem",
        ),
        "irons_spell_config_evidence": collect_irons_spell_namespace_overrides(
            instance,
            worlds,
            "somakespells",
        ),
    }


def collect_traveloptics(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots: list[tuple[str, Path]] = [
        ("kubejs_server_scripts", instance / "kubejs" / "server_scripts"),
        ("kubejs_data", instance / "kubejs" / "data"),
        ("ftbquests_config", instance / "config" / "ftbquests"),
        ("ftbquests_defaultconfigs", instance / "defaultconfigs" / "ftbquests"),
    ]
    roots.extend(
        (f"world_datapack:{rel(world, instance)}", world / "datapacks")
        for world in worlds
    )

    archives: list[tuple[str, Path]] = []
    for world in worlds:
        datapacks = world / "datapacks"
        if datapacks.is_dir():
            archives.extend(
                (f"world_datapack_zip:{rel(world, instance)}", archive)
                for archive in sorted(datapacks.glob("*.zip"))
            )

    direct = collect_exact_literal_references(
        instance,
        roots,
        TRAVELOPTICS_BLACKOUT_LITERAL,
    )
    zipped = collect_zip_literal_references(
        instance,
        archives,
        TRAVELOPTICS_BLACKOUT_LITERAL,
    )

    return {
        "classification_rule": {
            TRAVELOPTICS_ORIGINAL_SHA1: "ORIGINAL_EXACT",
            TRAVELOPTICS_PATCH_SHA1: "PATCHED_EXACT",
            "other": "OTHER_VERIFIED",
        },
        "blackout_reference_matches": direct + zipped,
        "blackout_reference_note": (
            "A literal match is candidate deployed-route evidence only. "
            "It does not by itself prove that the referenced script/quest/datapack grants "
            "traveloptics:blackout in survival."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", type=Path, help="Minecraft/modpack instance root containing mods/ and config/")
    parser.add_argument(
        "--world",
        action="append",
        default=[],
        type=Path,
        help="Optional explicit world directory. May be passed multiple times.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("provider-catalog-deployed-evidence.json"),
        help="Output JSON path (default: provider-catalog-deployed-evidence.json)",
    )
    parser.add_argument(
        "--probe-log",
        type=Path,
        default=None,
        help="Optional explicit catalog runtime probe log. Defaults to <instance>/logs/latest.log when present.",
    )
    args = parser.parse_args()

    instance = args.instance.expanduser().resolve()
    if not instance.is_dir():
        print(f"ERROR: instance directory does not exist: {instance}", file=sys.stderr)
        return 2

    worlds = candidate_worlds(instance, [p.expanduser() for p in args.world])
    mods = collect_mod_hashes(instance)
    kubejs_inventory = collect_kubejs_script_inventory(instance)

    report = {
        "schema": 3,
        "collector": "Black Arcana provider catalog deployed evidence",
        "instance_root_redacted": True,
        "worlds_scanned": [rel(w, instance) for w in worlds],
        "mods": mods,
        "runtime_probe": collect_catalog_runtime_probe(
            instance,
            args.probe_log.expanduser() if args.probe_log is not None else None,
        ),
        "kubejs_script_inventory": kubejs_inventory,
        "irons_spellbooks_kubejs_closure": classify_irons_spellbooks_kubejs_closure(
            mods,
            kubejs_inventory,
        ),
        "asterism_arcanum": collect_asterism(instance, worlds),
        "corail_tombstone": collect_tombstone(instance, worlds),
        "deeper_and_darker": collect_deeper_and_darker(instance),
        "gaze": collect_gaze(instance, worlds),
        "ice_and_fire_ce": collect_ice_and_fire_ce(instance),
        "mowzies_mobs": collect_mowzies_mobs(instance, worlds),
        "not_enough_glyphs": collect_neg(instance, worlds),
        "shadowsz": collect_shadowsz(instance, worlds),
        "simply_swords_cataclysm": collect_simply_cataclysm(instance),
        "simply_more": collect_simply_more(instance),
        "simply_swords": collect_simply_swords(instance),
        "somake_spells": collect_somake(instance, worlds),
        "traveloptics": collect_traveloptics(instance, worlds),
        "notes": [
            "This collector is read-only.",
            "Missing files/keys are observations, not proof that provider defaults are active.",
            "defaultconfigs is template evidence and must not override an observed world/serverconfig value.",
            "No full config/script/quest/log payloads are copied into the report; only selected keys, hashes, bounded literal-reference locations, and whitelisted fields from the last complete catalog-probe block are emitted.",
            "KubeJS inventory records only relative paths, surface labels, SHA-256 digests and byte sizes for bounded startup/server/client/data text files; script/data bodies are never copied.",
            "Runtime probe ingestion never retains raw log lines, timestamps, thread names, or unrelated log content.",
            "A deployed reference to traveloptics:blackout is evidence input, not automatic proof of a survival acquisition route.",
            "Observed Somake Iron's spell-config files are override evidence only; file presence is not treated as proof of registration or reachability.",
            "Observed Tombstone AllowedMagicItems values are eligibility evidence only; they do not by themselves prove semantic deduplication, acquisition, or runtime reachability.",
            "Observed Ice And Fire CE tools.phantasmalBladeAbility is deployed gate evidence only; missing/invalid values never fall back to the source default.",
            "Observed ShadowsZ fusionEnabled values are bounded config evidence; effective shadowszRestrictPowers is read only from the saved world level.dat GameRules compound and missing/invalid values remain fail-closed.",
            "Observed Simply Swords: Cataclysm STARTUP values come only from config/simplycataclysm-startup.toml; missing or incomplete keys never fall back to source defaults.",
            "Observed Simply More Mimicry state comes only from config/simplymore/unique_effect.toml at mimicry.config.<form>.disabled for the exact 25 Alpha-5 forms; missing, malformed, or non-boolean values remain fail-closed.",
            "Observed Simply Swords reachability config comes only from config/simplyswords/general.toml and loot.toml; it records the Awakening gate and bounded loot/remnant fields but never infers per-stack Awakening level or ability unlock state.",
        ],
    }

    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())