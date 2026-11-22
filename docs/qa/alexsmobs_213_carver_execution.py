#!/usr/bin/env python3
"""Seal the Carver item, portal, and native teleport-queue execution paths."""

import argparse
import json
from pathlib import Path
import re
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexsmobs_213_carver_portal_lifecycle_probe import SHA1, SHA256, SIZE, audit, require, verify_snapshot

PROVIDER = Path(__file__).resolve().parents[2] / "wiki/modpack-catalog/providers/✅-alexs-mobs-continued"
OLD_SEAL = PROVIDER / "EXACT-CARVER-PORTAL-LIFECYCLE-2.1.13.json"
SEAL = PROVIDER / "EXACT-CARVER-EXECUTION-2.1.13.json"
PREFIX = "com/github/alexthe666/alexsmobs/"
CARVER = "item/ItemDimensionalCarver"
PORTAL = "entity/EntityVoidPortal"
QUEUE = "misc/AMTeleportQueue"
TARGETS = (CARVER, PORTAL, QUEUE)
METHODS = {
    CARVER: None, PORTAL: None, QUEUE: None,
    "item/ItemShatteredDimensionalCarver": {"onPortalOpen"},
    "entity/AMEntityRegistry": {"<clinit>", "lambda$static$66", "registerEntity"},
    "item/AMItemRegistry": {"<clinit>", "lambda$static$91", "lambda$static$92", "regItem"},
    "event/ServerEvents": {"onServerTickPre", "onServerTickPost", "onLevelTick"},
    "misc/AMCompat": {"getOrCreateTag", "setTag", "addCooldown", "hurtAndBreak", "isMultipart", "create"},
}
EXCERPTS = {
    (CARVER, "onUseTick"): ((0, 65), (192, 432)),
    (PORTAL, "tick"): ((0, 83), (456, 953)),
    ("item/AMItemRegistry", "<clinit>"): ((1898, 1937),),
    ("entity/AMEntityRegistry", "<clinit>"): ((1134, 1148),),
    ("event/ServerEvents", "onLevelTick"): ((0, 8), (52, 295)),
}
RESOURCES = (
    "data/alexsmobs/recipe/dimensional_carver.json",
    "data/alexsmobs/advancement/alexsmobs/dimensional_carver.json",
    "data/alexsmobs/loot_table/entities/void_worm.json",
    "data/alexsmobs/tags/entity_type/void_portal_ignores.json",
    "assets/alexsmobs/models/item/dimensional_carver.json",
)


def inspect(jar, javap):
    verify_snapshot(audit(jar, str(javap)), json.loads(OLD_SEAL.read_text(encoding="utf-8")))
    with ZipFile(jar) as archive:
        paths = sorted(p for p in archive.namelist() if p.endswith(".class"))
        require(len(paths) == 1270, "publisher class roster drift")
        owners = {}
        for path in paths:
            reader = ClassReader(archive.read(path))
            refs = {name: reader.typed_refs(PREFIX + name) for name in TARGETS}
            if any(refs.values()):
                owners[reader.name.removeprefix(PREFIX)] = {key: value for key, value in refs.items() if value}
        details = {}
        for relative, selected in METHODS.items():
            owner = PREFIX + relative
            raw = archive.read(owner + ".class")
            reader = ClassReader(raw)
            bodies = disassemble(jar, javap, owner)
            require(selected is None or selected <= {name for name, _ in bodies}, "missing body: " + relative)
            methods = []
            bootstrap_ids = set()
            for key, body in sorted(bodies.items()):
                name = key[0]
                if not body or (selected is not None and name not in selected):
                    continue
                method = summarize(reader, key, body)
                ranges = EXCERPTS.get((relative, name))
                if ranges:
                    method["instructions"] = [row for row in method["instructions"]
                                              if any(lo <= row["offset"] <= hi for lo, hi in ranges)]
                    method["excerpt_offsets"] = [list(r) for r in ranges]
                for row in method["instructions"]:
                    match = re.match(r"InvokeDynamic #(\d+):", row["symbol"])
                    if match:
                        bootstrap_ids.add(int(match[1]))
                methods.append(method)
            if selected is None:
                require(len(methods) == sum("code_sha256" in m for m in reader.methods),
                        "incomplete body projection: " + relative)
            details[relative] = {"class_sha256": digest(raw), "methods": methods, "fields": reader.fields,
                                 "superclass": reader.parent, "interfaces": reader.interfaces,
                                 "selected_bootstraps": {str(i): reader.attributes["bootstrap_methods"][i]
                                                         for i in sorted(bootstrap_ids)}}
        resources = {path: {"sha256": digest(archive.read(path)), "json": json.loads(archive.read(path))}
                     for path in RESOURCES}
    return {
        "artifact": {"version": "2.1.13", "file_id": 8856498, "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "lifecycle_seal_sha256": digest(OLD_SEAL.read_bytes()),
        "class_count": len(paths), "class_roster_sha256": digest(("\n".join(paths) + "\n").encode()),
        "typed_owners": owners, "classes": details, "resources": resources,
        "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY", "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
        "semantic_reachability": "CONDITIONAL", "provider_universe_closed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "new output required")
    report = canonical(inspect(args.jar, args.javap))
    require(report == SEAL.read_text(encoding="utf-8"), "Carver execution seal mismatch")
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(report)
    print("CATALOG_SHA256", digest(args.output.read_bytes()))


if __name__ == "__main__":
    main()
