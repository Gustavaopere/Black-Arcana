#!/usr/bin/env python3
"""Reproduce registry, consumer, and resource evidence for six item classes."""

import argparse
from collections import Counter
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_burrowing_cave_map_probe import compact
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.json"
PREFIX = "com/github/alexmodguy/alexscaves/"
REFERENCES = (
    "EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.json",
    "EXACT-BURROWING-ARROW-ENTITY-DISCOVERY-1.0.10.json",
    "EXACT-CANDY-CANE-HOOK-DISCOVERY-1.0.10.json",
    "EXACT-CAVE-BOAT-DISCOVERY-1.0.10.json",
    "EXACT-CAVE-BOOK-DISCOVERY-1.0.10.json",
    "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json",
    "EXACT-TICKING-ITEM-CONTRACT-1.0.10.json",
    "EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json",
)
IDS = (
    "burrowing_arrow", "candy_cane_hook", "pewen_boat", "pewen_chest_boat",
    "thornwood_boat", "thornwood_chest_boat", "cave_book", "cave_tablet",
    "cave_codex", "cave_map",
)
SUPPLEMENT = {
    "server/config/ACServerConfig": {"<init>"},
    "server/entity/ACEntityRegistry": {"<clinit>", "lambda$static$0", "lambda$static$1",
                                       "lambda$static$62", "lambda$static$80"},
    "server/entity/item/BurrowingArrowEntity": None,
    "server/entity/item/CandyCaneHookEntity": None,
    "server/entity/item/AlexsCavesBoatEntity": None,
    "server/entity/item/AlexsCavesChestBoatEntity": None,
    "server/entity/util/AlexsCavesBoat$Type": None,
    "server/item/ACItemRegistry": {"setup"},
    "server/item/ACItemRegistry$6": None,
    "server/inventory/SpelunkeryTableMenu": {"onMessageFromScreen", "setupResultSlot", "lambda$setupResultSlot$0", "removed"},
    "server/misc/CaveBookProgress": None,
    "server/misc/CaveBookProgress$Subcategory": None,
    "server/misc/AbstractProjectileDispenseBehavior": None,
    "server/recipe/RecipeCaveMap": None,
    "server/level/map/CaveBiomeMapWorldWorker": None,
    "server/level/map/ACWorldWorkerManager": None,
    "server/level/storage/ACWorldData": {"fillOutCaveMap", "isCaveMapTicking"},
}


def class_evidence(archive, jar, javap):
    evidence = {}
    for relative_owner, selected in SUPPLEMENT.items():
        owner = PREFIX + relative_owner
        raw = archive.read(owner + ".class")
        reader = ClassReader(raw)
        methods = [
            compact(summarize(reader, key, body))
            for key, body in sorted(disassemble(jar, javap, owner).items())
            if body and (selected is None or key[0] in selected)
        ]
        if selected is not None:
            require({entry["declaration"]["name"] for entry in methods} == selected,
                    "consumer method set changed: " + owner)
        evidence[relative_owner] = {"class_sha256": digest(raw), "methods": methods}
    return evidence


def publisher_resources(archive):
    paths = [f"data/alexscaves/recipe/{item}.json" for item in IDS if item not in ("cave_codex", "cave_tablet")]
    paths.extend(("data/minecraft/tags/item/arrows.json",
                  "data/minecraft/tags/item/boats.json",
                  "data/minecraft/tags/item/chest_boats.json",
                  "data/alexscaves/tags/worldgen/biome/cave_map_border_on.json"))
    resources = {}
    for path in paths:
        raw = archive.read(path)
        resources[path] = {"sha256": digest(raw), "json": json.loads(raw)}
    book = {path: digest(archive.read(path)) for path in sorted(archive.namelist())
            if path.startswith("assets/alexscaves/books/") and path.endswith(".json")}
    counts = Counter(path.split("/")[3] for path in book)
    return {"registrations": resources, "book_pages": book, "book_group_counts": dict(counts)}


def inspect(jar, javap, discovery):
    verify_artifact(jar)
    references = {name: digest((PROVIDER / name).read_bytes()) for name in REFERENCES}
    seed = json.loads((PROVIDER / REFERENCES[0]).read_text(encoding="utf8"))
    report_sha = digest(discovery.read_bytes())
    require(report_sha == seed["report_sha256"], "six-class discovery replay drift")
    registry = json.loads((PROVIDER / "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
    ids = {"alexscaves:" + item for item in IDS}
    bindings = [entry for entry in registry["native"]["bindings"] if entry["resource_location"] in ids]
    require({entry["resource_location"] for entry in bindings} == ids and len(bindings) == len(ids),
            "missing or duplicate registry binding")
    with ZipFile(jar) as archive:
        return {
            "artifact": seed["artifact"],
            "discovery_sha256": report_sha,
            "references_sha256": references,
            "bindings": bindings,
            "resources": publisher_resources(archive),
            "native_supplement": class_evidence(archive, jar, javap),
            "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
            "semantic_magic_roots_added": 0,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "discovery", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "new report required")
    report = inspect(args.jar, args.javap, args.discovery)
    require(report == json.loads(SEAL.read_text(encoding="utf8")), "catalog seal mismatch")
    with args.output.open("x", encoding="utf8") as output:
        output.write(canonical(report))
    print("CATALOG_SHA256", digest(args.output.read_bytes()))


if __name__ == "__main__":
    main()
