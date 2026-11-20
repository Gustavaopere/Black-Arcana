#!/usr/bin/env python3
"""Verify the catalog's exact reports and resolve the remaining registry bindings."""

import argparse
import json
from pathlib import Path
import re
import zipfile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

PACKAGE = "com/github/alexmodguy/alexscaves/"
REGISTER_WITH_MODE = "Method registerBlockAndItem:(Ljava/lang/String;Ljava/util/function/Supplier;I)"
PROVIDER = Path(__file__).resolve().parents[2] / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-ADJACENT-ITEMS-CATALOG-1.0.10.json"
REPORT_HASHES = {
    "discovery": "357381bd6a9ca6f8df9d79ef274552468033832664a40f59fc04ec2d76d99a6c",
    "boundary": "ec96f80a27cd7c12b9bc114864290210574be7bc07f49b716d93ae14ce793490",
    "extra": "4cc2c6a9c4d05d19499809cd8b870e8bde1deee488f0977321b6909767630c11",
}
REFERENCES = (
    "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json",
    "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json",
    "EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json",
    "EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.json",
)


def read_method(archive, jar, javap, owner, name, descriptor):
    payload = archive.read(owner + ".class")
    key = (name, descriptor)
    methods = disassemble(jar, javap, owner)
    return digest(payload), summarize(ClassReader(payload), key, methods[key])


def block_bindings(archive, jar, javap):
    owner = PACKAGE + "server/block/ACBlockRegistry"
    owner_hash, initializer = read_method(archive, jar, javap, owner, "<clinit>", "()V")
    rows = initializer["instructions"]
    bindings = {str(mode): [] for mode in (1, 2, 3, 9)}
    for index, call in enumerate(rows):
        if call["opcode"] != "invokestatic" or not call["symbol"].startswith(REGISTER_WITH_MODE):
            continue
        literal, factory, mode = rows[index - 3:index]
        require(literal["symbol"].startswith("String ") and factory["opcode"] == "invokedynamic",
                "unexpected block item registration shape")
        instruction = mode["opcode"]
        value = instruction.removeprefix("iconst_") if instruction.startswith("iconst_") else mode["operand"]
        require(value.isdecimal(), "unexpected block item registration mode")
        if value in bindings:
            bindings[value].append({
                "id": "alexscaves:" + literal["symbol"].removeprefix("String "),
                "literal_offset": literal["offset"],
                "block_factory_offset": factory["offset"],
                "mode_offset": mode["offset"],
                "register_offset": call["offset"],
            })
    require([len(bindings[key]) for key in ("1", "2", "3", "9")] == [29, 2, 4, 0],
            "block item binding census changed")
    registry = ClassReader(archive.read(owner + ".class"))
    bootstrap = registry.attributes["bootstrap_methods"]
    require(all(re.search(r"lambda\$getBlockSupplier\$" + str(factory) + r"\b",
                           json.dumps(bootstrap[index]))
                for index, factory in ((4, 437), (5, 438), (6, 439), (12, 445))),
            "block item factory bootstrap changed")
    return {"class_sha256": owner_hash, "initializer": initializer["declaration"],
            "bindings_by_mode": bindings}


def inspect(jar, javap, reports):
    verify_artifact(jar)
    for key, expected in REPORT_HASHES.items():
        require(digest(reports[key].read_bytes()) == expected, key + " report drift")
    with zipfile.ZipFile(jar) as archive:
        blocks = block_bindings(archive, jar, javap)
        owner, initialization = read_method(archive, jar, javap, PACKAGE + "AlexsCaves", "<init>", "()V")
        registration = [row for row in initialization["instructions"] if 155 <= row["offset"] <= 165]
        require([row["offset"] for row in registration] == [155, 158, 161, 162, 165]
                and "NeoForge.EVENT_BUS" in registration[0]["symbol"]
                and "CommonEvents" in registration[1]["symbol"]
                and "IEventBus.register" in registration[-1]["symbol"], "CommonEvents registration drift")
        locale = archive.read("assets/alexscaves/lang/en_us.json")
        translations = json.loads(locale)
        lore_keys = [entry["id"].replace(":", ".") for entry in blocks["bindings_by_mode"]["1"]]
        require(all("block." + key + ".desc" in translations for key in lore_keys), "block lore missing")
        tag = archive.read("data/alexscaves/tags/block/scaffolding.json")
        return {
            "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
            "report_sha256": REPORT_HASHES,
            "reference_sha256": {name: digest((PROVIDER / name).read_bytes()) for name in REFERENCES},
            "block_bindings": blocks,
            "anvil_registration": {"class_sha256": owner, "constructor": initialization["declaration"],
                                   "instructions": registration},
            "scaffolding_tag": {"sha256": digest(tag), "json": json.loads(tag)},
            "english_locale": {"sha256": digest(locale), "lore_keys_present": len(lore_keys),
                               "biome_treat_name": translations["item.alexscaves.biome_treat"]},
            "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
            "semantic_magic_roots_added": 0,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "discovery", "boundary", "extra", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "new report required")
    result = inspect(args.jar, args.javap, {name: getattr(args, name) for name in REPORT_HASHES})
    require(result == json.loads(SEAL.read_text(encoding="utf8")), "catalog seal mismatch")
    with args.output.open("x", encoding="utf8") as output:
        output.write(canonical(result))
    print("CATALOG_SHA256", digest(args.output.read_bytes()))


if __name__ == "__main__":
    main()
