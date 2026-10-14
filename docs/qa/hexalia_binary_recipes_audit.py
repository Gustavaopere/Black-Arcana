#!/usr/bin/env python3
"""Read-only exact-JAR recipe ID and bounded schema audit for Hexalia 1.3.7.

Evidence is restricted to packaged datapack recipe declarations, never
NeoForge recipe reload, client rendering, survival or actual ritual settlement.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import zipfile
from pathlib import Path

EXPECTED_JAR = "hexalia-neoforge-1.3.7.jar"
EXPECTED_SHA1 = "ca90edf1664cf6d44fe7e5318c71069050499c7e"
MOD_ID = "hexalia"
SCHEMA = "EXACT_HASH_PACKAGED_HEXALIA_RECIPE_IDS_NOT_RUNTIME_QA"
NATURE = (
    "fire_node_from_ritual_table",
    "air_node_from_ritual_table",
    "water_node_from_ritual_table",
    "earth_node_from_ritual_table",
    "astrylis_from_ritual_table",
    "kelpweave_blade_from_ritual_table",
    "rootshaper_from_ritual_table",
    "sage_pendant_from_ritual_table",
    "bloomwrap_hat_from_ritual_table",
    "bloomwrap_robes_from_ritual_table",
    "bloomwrap_leggings_from_ritual_table",
    "bloomwrap_boots_from_ritual_table",
    "grimshade_from_ritual_table",
    "rabbage_seeds_from_ritual_table",
    "nautilite_from_ritual_table",
    "windsong_from_ritual_table",
    "lourdes_from_ritual_table",
    "aegiflora_from_ritual_table",
    "morphora_from_ritual_table",
    "cinderhew_from_ritual_table",
    "heartseed_from_ritual_table",
    "summon_silk_moth",
    "summon_cacofey",
)
CELESTIAL = (
    "galeberries_from_celestial_infusion",
    "celestial_crystal_from_celestial_infusion",
    "moonweave_hood_from_celestial_infusion",
    "moonweave_mantle_from_celestial_infusion",
    "moonweave_bindings_from_celestial_infusion",
    "moonweave_footwraps_from_celestial_infusion",
)
SOUL = {
    "summon_silk_moth": "hexalia:silk_moth",
    "summon_cacofey": "hexalia:cacofey",
}
TYPE_NATURE = "hexalia:natures_ritual"
TYPE_CELESTIAL = "hexalia:celestial_infusion"
RECIPE_PATH = re.compile(r"^data/hexalia/recipe/([a-z][a-z0-9_]*)\.json$")
MAX_JAR_BYTES = 12 * 1024 * 1024
MAX_ZIP_ENTRIES = 20000
MAX_RECIPE_JSON = 64 * 1024


class EvidenceError(Exception):
    """Unverified input or mismatch of documented recipe boundary."""


def unique_pairs(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise EvidenceError("duplicate JSON property " + repr(k))
        obj[k] = v
    return obj


def examine_json_docs(documents: dict[str, bytes],
                      nature: tuple[str, ...] = NATURE,
                      celestial: tuple[str, ...] = CELESTIAL) -> dict:
    """No Minecraft class loading; only recipes of two declared provider types."""
    if len(nature) != len(set(nature)) or len(celestial) != len(set(celestial)):
        raise EvidenceError("expected catalog IDs duplicated")
    if set(nature) & set(celestial):
        raise EvidenceError("expected catalog types overlap")
    ids = {TYPE_NATURE: [], TYPE_CELESTIAL: []}
    errors = []
    for path, blob in documents.items():
        match = RECIPE_PATH.fullmatch(path)
        if match is None:
            continue
        if len(blob) > MAX_RECIPE_JSON:
            raise EvidenceError(f"oversized recipe {path}")
        try:
            item = json.loads(blob.decode("utf-8"), object_pairs_hook=unique_pairs)
        except (UnicodeError, ValueError) as exc:
            raise EvidenceError(f"invalid recipe JSON in {path}: {exc}") from exc
        if not isinstance(item, dict):
            raise EvidenceError(f"recipe not an object: {path}")
        kind = item.get("type")
        if kind not in ids:
            continue
        name = match.group(1)
        ids[kind].append(name)
        if kind == TYPE_NATURE:
            if not isinstance(item.get("center"), dict) or not isinstance(item.get("offerings"), list):
                errors.append(f"{name}: missing nature center/offerings")
            elif not item["offerings"] or not all(isinstance(x, dict) for x in item["offerings"]):
                errors.append(f"{name}: malformed nature offerings")
            soul = name in SOUL
            if bool(item.get("requires_soul", False)) != soul:
                errors.append(f"{name}: unexpected soul requirement")
            if soul:
                result = item.get("result")
                if not isinstance(result, dict) or result.get("type") != "entity" or (
                    result.get("entity") != SOUL[name] or result.get("count") != 1
                ):
                    errors.append(f"{name}: soul summon target/count mismatch")
            elif not isinstance(item.get("output"), str) or not item["output"].startswith(("hexalia:", "minecraft:")):
                errors.append(f"{name}: non-summon output missing")
        else:
            if not isinstance(item.get("input"), dict) or not isinstance(item.get("output"), str):
                errors.append(f"{name}: invalid celestial input/output")
    deviations = {
        "missing_natures_ritual": sorted(set(nature) - set(ids[TYPE_NATURE])),
        "extra_natures_ritual": sorted(set(ids[TYPE_NATURE]) - set(nature)),
        "missing_celestial_infusion": sorted(set(celestial) - set(ids[TYPE_CELESTIAL])),
        "extra_celestial_infusion": sorted(set(ids[TYPE_CELESTIAL]) - set(celestial)),
        "duplicate_nature_ids": sorted(x for x in set(ids[TYPE_NATURE]) if ids[TYPE_NATURE].count(x) != 1),
        "duplicate_celestial_ids": sorted(x for x in set(ids[TYPE_CELESTIAL]) if ids[TYPE_CELESTIAL].count(x) != 1),
        "count_wrong": len(ids[TYPE_NATURE]) != len(nature) or len(ids[TYPE_CELESTIAL]) != len(celestial),
        "shape_errors": errors,
    }
    return {
        "status": "PASS" if not any(deviations.values()) else "UNPROVEN_OR_MISMATCH",
        "natures_ritual_expected": len(nature),
        "natures_ritual_observed": len(ids[TYPE_NATURE]),
        "celestial_infusion_expected": len(celestial),
        "celestial_infusion_observed": len(ids[TYPE_CELESTIAL]),
        "unique_magic_recipe_ids": len(set(ids[TYPE_NATURE] + ids[TYPE_CELESTIAL])),
        "summon_recipe_ids": sorted(set(ids[TYPE_NATURE]) & set(SOUL)),
        "deviations": {k: v for k, v in deviations.items() if v},
    }


def audit_jar(jar: Path, *, expected_sha1: str = EXPECTED_SHA1) -> dict:
    if jar.name != EXPECTED_JAR or jar.is_symlink() or not jar.is_file():
        raise EvidenceError("JAR must have expected filename and be a non-symlink regular file")
    before = jar.stat()
    sig = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= MAX_JAR_BYTES:
        raise EvidenceError("JAR size/type invalid")
    data = jar.read_bytes()
    if sig(jar.stat()) != sig(before):
        raise EvidenceError("JAR changed while reading")
    sha1, sha256 = hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest()
    if sha1 != expected_sha1:
        raise EvidenceError(f"JAR physical SHA-1 mismatch: {sha1}")
    with zipfile.ZipFile(io.BytesIO(data)) as arc:
        names = arc.namelist()
        if len(names) != len(set(names)) or len(names) > MAX_ZIP_ENTRIES:
            raise EvidenceError("ZIP duplicate entries or archive entries over limit")
        try:
            meta = arc.read("META-INF/neoforge.mods.toml")
        except KeyError as exc:
            raise EvidenceError("NeoForge mod metadata absent") from exc
        if len(meta) > 256 * 1024 or not re.search(
            rb'\bmodId\s*=\s*["\x27]hexalia["\x27]', meta
        ):
            raise EvidenceError("NeoForge mod ID not hexalia")
        docs = {}
        for entry in arc.infolist():
            if RECIPE_PATH.fullmatch(entry.filename):
                if entry.file_size > MAX_RECIPE_JSON:
                    raise EvidenceError("oversized recipe member")
                docs[entry.filename] = arc.read(entry)
    if sig(jar.stat()) != sig(before) or hashlib.sha256(jar.read_bytes()).hexdigest() != sha256:
        raise EvidenceError("JAR changed during inspection")
    report = examine_json_docs(docs)
    return {
        "evidence_class": SCHEMA,
        "provider": MOD_ID,
        "version": "1.3.7",
        "file": jar.name,
        "size_bytes": len(data),
        "sha1": sha1,
        "sha256": sha256,
        "result": report["status"],
        "recipes": report,
        "not_proven": [
            "all source JSON fields byte-equal to release source",
            "recipes loaded by NeoForge or retained after datapack reload",
            "client/dedicated server startup", "Survival inputs/offering consumption",
            "50-tick soul manifestation", "world safety/claims",
            "RPG Skill Tree adapters", "Stage 09 physical QA",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = audit_jar(args.jar)
        status = 0 if report["result"] == "PASS" else 1
    except (EvidenceError, UnicodeError, OSError, zipfile.BadZipFile) as exc:
        report = {"evidence_class": "UNVERIFIED", "result": "FAIL_CLOSED", "reason": str(exc)}
        status = 1
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
