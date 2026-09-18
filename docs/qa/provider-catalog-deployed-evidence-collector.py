#!/usr/bin/env python3
"""
Read-only Black Arcana provider-catalog evidence collector.

This script does not modify the Minecraft instance. It emits only:
- selected mod JAR hashes;
- selected config keys required by canonical provider checklists;
- presence of exact datapack override paths.

It intentionally does not dump full config files or unrelated instance data.
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
    "not_enough_glyphs": ["not_enough_glyphs-1.21.1-4.6.1.jar"],
    "somake_spells": ["somakespells-1.0.9-1.21.1.jar"],
    "traveloptics": [
        "traveloptics-4.4.0.1-1.21.1.jar",
        "traveloptics-4.4.0.1.1-1.21.1-patched.jar",
    ],
}

TEXT_EXTENSIONS = {".toml", ".json", ".cfg", ".conf", ".txt"}
ASTERISM_DATAPACK_PATH = "data/asterismarcanum/irons_spellbooks_spell_config/astral_gateway.json"


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

    for world in worlds:
        datapacks = world / "datapacks"
        if not datapacks.is_dir():
            continue
        for path in sorted(datapacks.rglob("astral_gateway.json")):
            normalized = path.as_posix()
            if normalized.endswith(ASTERISM_DATAPACK_PATH):
                out["datapack_overrides"].append({
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


def collect_somake(instance: Path, worlds: list[Path]) -> dict[str, Any]:
    roots = [instance / "config", instance / "defaultconfigs"]
    roots.extend(world / "serverconfig" for world in worlds)
    return {
        "enableSpellLockSystem_matches": collect_selected_key(
            instance,
            roots,
            "enableSpellLockSystem",
        )
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
    args = parser.parse_args()

    instance = args.instance.expanduser().resolve()
    if not instance.is_dir():
        print(f"ERROR: instance directory does not exist: {instance}", file=sys.stderr)
        return 2

    worlds = candidate_worlds(instance, [p.expanduser() for p in args.world])

    report = {
        "schema": 1,
        "collector": "Black Arcana provider catalog deployed evidence",
        "instance_root_redacted": True,
        "worlds_scanned": [rel(w, instance) for w in worlds],
        "mods": collect_mod_hashes(instance),
        "asterism_arcanum": collect_asterism(instance, worlds),
        "gaze": collect_gaze(instance, worlds),
        "not_enough_glyphs": collect_neg(instance, worlds),
        "somake_spells": collect_somake(instance, worlds),
        "traveloptics": {
            "classification_rule": {
                TRAVELOPTICS_ORIGINAL_SHA1: "ORIGINAL_EXACT",
                TRAVELOPTICS_PATCH_SHA1: "PATCHED_EXACT",
                "other": "OTHER_VERIFIED",
            }
        },
        "notes": [
            "This collector is read-only.",
            "Missing files/keys are observations, not proof that provider defaults are active.",
            "defaultconfigs is template evidence and must not override an observed world/serverconfig value.",
            "No full config payloads are copied into the report; only selected keys and hashes are emitted.",
        ],
    }

    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
