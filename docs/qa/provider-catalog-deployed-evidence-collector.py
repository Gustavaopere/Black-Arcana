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
import hashlib
import json
import re
import sys
import tomllib
import zipfile
from pathlib import Path
from typing import Any

TRAVELOPTICS_ORIGINAL_SHA1 = "3808493ce45cdfeb6408e85578adecf13df698e8"
TRAVELOPTICS_PATCH_SHA1 = "680fa679d8ea2419a79571f455436367222f6f9d"
SOMAKE_109_RELEASE_SHA1 = "171841ac9f802be9309ecc166c1d972ac6d404c0"
GAZE_1171_SHA1 = "a8cb3190bde157f78160ce65c202ce2d47fb2041"
NEG_462_RELEASE_SHA1 = "32eea2c478a346ee7499f6a0db156241116f73e9"

NEG_CONFIGS = [
    ("not_enough_glyphs:plow", "not_enough_glyphs/plow.toml"),
    ("not_enough_glyphs:trail", "not_enough_glyphs/trail.toml"),
    ("not_enough_glyphs:ride", "not_enough_glyphs/ride.toml"),
    ("not_enough_glyphs:feed", "not_enough_glyphs/feed.toml"),
    ("not_enough_glyphs:filter_light", "not_enough_glyphs/filter_light.toml"),
    ("not_enough_glyphs:filter_dark", "not_enough_glyphs/filter_dark.toml"),
    ("not_enough_glyphs:contingency_fall", "not_enough_glyphs/contingency_fall.toml"),
    ("not_enough_glyphs:contingency_heal", "not_enough_glyphs/contingency_heal.toml"),
    ("not_enough_glyphs:contingency_health", "not_enough_glyphs/contingency_health.toml"),
    ("not_enough_glyphs:contingency_death", "not_enough_glyphs/contingency_death.toml"),
    ("not_enough_glyphs:contingency_fire", "not_enough_glyphs/contingency_fire.toml"),
    ("not_enough_glyphs:contingency_blink", "not_enough_glyphs/contingency_blink.toml"),
    ("not_enough_glyphs:contingency_time", "not_enough_glyphs/contingency_time.toml"),
    ("not_enough_glyphs:propagate_plane", "not_enough_glyphs/propagate_plane.toml"),
    ("toomanyglyphs:ray", "toomanyglyphs/ray.toml"),
    ("toomanyglyphs:reverse_direction", "toomanyglyphs/reverse_direction.toml"),
    ("toomanyglyphs:chaining", "toomanyglyphs/chaining.toml"),
    ("toomanyglyphs:filter_block", "toomanyglyphs/filter_block.toml"),
    ("toomanyglyphs:filter_entity", "toomanyglyphs/filter_entity.toml"),
    ("toomanyglyphs:filter_living", "toomanyglyphs/filter_living.toml"),
    ("toomanyglyphs:filter_living_not_monster", "toomanyglyphs/filter_living_not_monster.toml"),
    ("toomanyglyphs:filter_living_not_player", "toomanyglyphs/filter_living_not_player.toml"),
    ("toomanyglyphs:filter_monster", "toomanyglyphs/filter_monster.toml"),
    ("toomanyglyphs:filter_player", "toomanyglyphs/filter_player.toml"),
    ("toomanyglyphs:filter_item", "toomanyglyphs/filter_item.toml"),
    ("toomanyglyphs:filter_animal", "toomanyglyphs/filter_animal.toml"),
    ("toomanyglyphs:filter_is_baby", "toomanyglyphs/filter_is_baby.toml"),
    ("toomanyglyphs:filter_is_mature", "toomanyglyphs/filter_is_mature.toml"),
    ("ars_trinkets:filter_self", "ars_trinkets/filter_self.toml"),
    ("ars_trinkets:filter_not_self", "ars_trinkets/filter_not_self.toml"),
    ("arsomega:flatten", "arsomega/flatten.toml"),
    ("arsomega:propagate_underfoot", "arsomega/propagate_underfoot.toml"),
    ("arsomega:propagate_projectile", "arsomega/propagate_projectile.toml"),
    ("arsomega:propagate_self", "arsomega/propagate_self.toml"),
    ("arsomega:missile", "arsomega/missile.toml"),
    ("arsomega:overhead", "arsomega/overhead.toml"),
    ("arsomega:propagate_missile", "arsomega/propagate_missile.toml"),
    ("arsomega:propagate_overhead", "arsomega/propagate_overhead.toml"),
    ("ars_scalaes:resize", "ars_scalaes/resize.toml"),
]

MOD_PATTERNS = {
    "asterism_arcanum": ["asterismarcanum-1.21.1-0.1.0.jar"],
    "gaze": ["gaze-1.1.7.1.jar"],
    "not_enough_glyphs": ["not_enough_glyphs-1.21.1-4.6.2.jar"],
    "somake_spells": ["somakespells-1.0.9-1.21.1.jar"],
    "traveloptics": [
        "traveloptics-4.4.0.1-1.21.1.jar",
        "traveloptics-4.4.0.1.1-1.21.1-patched.jar",
    ],
}

TEXT_EXTENSIONS = {".toml", ".json", ".cfg", ".conf", ".txt", ".js", ".snbt", ".zs"}
ASTERISM_DATA_RELATIVE = "asterismarcanum/irons_spellbooks_spell_config/astral_gateway.json"
ASTERISM_DATAPACK_PATH = f"data/{ASTERISM_DATA_RELATIVE}"
TRAVELOPTICS_BLACKOUT_LITERAL = "traveloptics:blackout"

CATALOG_PROBE_PREFIX = "[BLACK_ARCANA_CATALOG_PROBE]"
CATALOG_PROBE_LOGGER = "dev.gustavopere.blackarcana.qa.catalog.CatalogRuntimeEvidence"
CATALOG_PROBE_LOG_LINE_RE = re.compile(
    rf"^\\[[^]\\r\\n]+\\] \\[[^]\\r\\n]+\\] "
    rf"\\[{re.escape(CATALOG_PROBE_LOGGER)}/[^]\\r\\n]*\\]: "
    rf"{re.escape(CATALOG_PROBE_PREFIX)}(?P<payload>.*)$"
)
SUPPORTED_CATALOG_PROBE_SCHEMAS = {1, 2}
TARGET_PROBE_MOD_IDS = {
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
RESOURCE_LOCATION_RE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
SIMPLE_ERROR_RE = re.compile(r"^[A-Za-z0-9_$]+$")


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
                if provider == "traveloptics":
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
                elif provider == "not_enough_glyphs":
                    entry["release_4_6_2_equality"] = entry["sha1"] == NEG_462_RELEASE_SHA1
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

    report = {
        "schema": 3,
        "collector": "Black Arcana provider catalog deployed evidence",
        "instance_root_redacted": True,
        "worlds_scanned": [rel(w, instance) for w in worlds],
        "mods": collect_mod_hashes(instance),
        "runtime_probe": collect_catalog_runtime_probe(
            instance,
            args.probe_log.expanduser() if args.probe_log is not None else None,
        ),
        "asterism_arcanum": collect_asterism(instance, worlds),
        "gaze": collect_gaze(instance, worlds),
        "not_enough_glyphs": collect_neg(instance, worlds),
        "somake_spells": collect_somake(instance, worlds),
        "traveloptics": collect_traveloptics(instance, worlds),
        "notes": [
            "This collector is read-only.",
            "Missing files/keys are observations, not proof that provider defaults are active.",
            "defaultconfigs is template evidence and must not override an observed world/serverconfig value.",
            "No full config/script/quest/log payloads are copied into the report; only selected keys, hashes, bounded literal-reference locations, and whitelisted fields from the last complete catalog-probe block are emitted.",
            "Runtime probe ingestion never retains raw log lines, timestamps, thread names, or unrelated log content.",
            "A deployed reference to traveloptics:blackout is evidence input, not automatic proof of a survival acquisition route.",
            "Observed Somake Iron's spell-config files are override evidence only; file presence is not treated as proof of registration or reachability.",
        ],
    }

    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
