#!/usr/bin/env python3
"""Reproduce the individual Diving Armor contracts from the exact publisher JAR."""

import argparse
import json
from pathlib import Path
import re
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

PROVIDER = Path(__file__).resolve().parents[2] / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-DIVING-ARMOR-CATALOG-1.0.10.json"
PREFIX = "com/github/alexmodguy/alexscaves/"
TARGET = PREFIX + "server/item/DivingArmorItem"
REGISTRY = PREFIX + "server/item/ACItemRegistry"
PIECES = ("diving_helmet", "diving_chestplate", "diving_leggings", "diving_boots")
FIELDS = {piece.upper() for piece in PIECES} | {"DIVING_SUIT_ARMOR_MATERIAL"}
REFERENCES = (
    "EXACT-ARMOR-MATERIAL-1.0.10.json",
    "EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.json",
    "EXACT-DYNAMIC-ATTRIBUTE-CONTRACT-1.0.10.json",
    "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json",
)
METHODS = {
    "client/render/item/ACArmorRenderProperties": {"getACArmorModelBase", "renderCustomArmor"},
    "server/block/MuckBlock": {"<clinit>", "getCollisionShape", "isOceanEntity", "entityInside"},
    "server/config/ACServerConfig": {"<init>"},
    "server/event/CommonEvents": {"livingTick", "onEntityJoinWorld"},
    "server/item/ACArmorMaterial": {"properties", "defense", "toughness", "knockbackResistance"},
    "server/item/ACItemRegistry": {"setup", "<clinit>", *(f"lambda$static${i}" for i in range(99, 103))},
    "server/item/DivingArmorItem": None,
    "server/misc/ACCompat": {"attribute", "attributeModifier", "itemAttributes", "lambda$itemAttributes$0",
                             "lambda$itemAttributes$1"},
    "server/misc/ACPlatform": {"swimSpeedAttribute"},
}
# Owners not in this table are still walked for executable use of the four item fields.
EXCERPTS = {
    "server/event/CommonEvents": {"livingTick": (126, 191), "onEntityJoinWorld": (43, 389)},
    "server/config/ACServerConfig": {"<init>": (177, 199)},
    "server/item/ACItemRegistry": {"setup": (54, 70)},
}


def publisher_classes(archive):
    paths = sorted(name for name in archive.namelist() if name.endswith(".class"))
    require(len(paths) == 1555 and len(set(archive.namelist())) == len(archive.namelist()),
            "publisher roster drift")
    typed_owners = {}
    for path in paths:
        reader = ClassReader(archive.read(path))
        require(path == reader.name + ".class" and reader.major == 65, "class identity drift")
        target_refs = reader.typed_refs(TARGET)
        field_refs = [r for r in reader.typed_refs(REGISTRY)
                      if r["kind"] == "field_reference" and r["name"] in FIELDS]
        if target_refs or field_refs:
            typed_owners[reader.name] = {"class": target_refs, "registry_fields": field_refs}
    return paths, typed_owners


def class_evidence(archive, jar, javap):
    paths, typed_owners = publisher_classes(archive)
    evidence = {}
    owners = set(typed_owners) | {PREFIX + owner for owner in METHODS}
    for owner in sorted(owners):
        raw = archive.read(owner + ".class")
        reader = ClassReader(raw)
        methods = disassemble(jar, javap, owner)
        relative = owner.removeprefix(PREFIX)
        selection = METHODS.get(relative, set())
        if selection is not None:
            require(selection <= {name for name, _ in methods}, "missing method in " + owner)
        selected = []
        sites = []
        refs = typed_owners.get(owner, {"registry_fields": [], "class": []})
        indexes = {ref["index"] for refs_ in refs.values() for ref in refs_ if "index" in ref}
        for signature, body in sorted(methods.items()):
            name, descriptor = signature
            if body and (selection is None or name in selection):
                method = summarize(reader, signature, body)
                bounds = EXCERPTS.get(relative, {}).get(name)
                if bounds:
                    method["instructions"] = [row for row in method["instructions"]
                                              if bounds[0] <= row["offset"] <= bounds[1]]
                    method["excerpt_offsets"] = list(bounds)
                elif name == "<clinit>" and owner == REGISTRY:
                    # Registry factory bindings and material values are already independently sealed.
                    del method["instructions"]
                selected.append(method)
            for offset, (opcode, operand, symbol) in sorted(body.items()):
                index = re.match(r"#(\d+)", operand)
                if index and int(index[1]) in indexes:
                    sites.append({"name": name, "descriptor": descriptor, "offset": offset,
                                  "opcode": opcode, "symbol": symbol})
        evidence[relative] = {"class_sha256": digest(raw), "methods": selected, "reference_sites": sites}
        if owner == TARGET:
            require(len(selected) == 7, "DivingArmorItem method coverage drift")
            evidence[relative].update(parent=reader.parent, interfaces=reader.interfaces,
                                      fields=reader.fields, bootstraps=reader.attributes["bootstrap_methods"])
    return {
        "class_count": len(paths),
        "class_roster_sha256": digest(("\n".join(paths) + "\n").encode()),
        "typed_owners": typed_owners,
        "classes": evidence,
    }


def resource_evidence(archive):
    ids = {f'"alexscaves:{name}"'.encode() for name in PIECES}
    data = {}
    related_data = {"data/alexscaves/tags/item/repairs_diving_suit_armor.json",
                    "data/alexscaves/tags/entity_type/seafloor_denizens.json"}
    guide = "assets/alexscaves/books/abyssal_chasm/utilities.json"
    matched_guide = None
    for name in sorted(archive.namelist()):
        if name.endswith(".json") and name.startswith("data/"):
            raw = archive.read(name)
            if any(item in raw for item in ids) or name in related_data:
                data[name] = {"sha256": digest(raw), "json": json.loads(raw)}
        elif name == guide:
            raw = archive.read(name)
            require(all(item in raw for item in ids), "missing guide entry")
            matched_guide = {"path": name, "sha256": digest(raw)}
    require(matched_guide and len(data) == 8, "diving gear data resource roster drift")
    assets = [f"assets/alexscaves/models/item/{name}.json" for name in PIECES]
    assets += [f"assets/alexscaves/textures/item/{name}.png" for name in PIECES]
    assets += [f"assets/alexscaves/textures/armor/diving_suit_{variant}.png" for variant in (0, 1)]
    locales = {}
    for locale in ("en_us", "pt_br"):
        raw = archive.read(f"assets/alexscaves/lang/{locale}.json")
        names = json.loads(raw)
        locales[locale] = {"sha256": digest(raw), "names": {
            name: names[f"item.alexscaves.{name}"] for name in PIECES}}
    return {"data": data, "guide": matched_guide, "locales": locales,
            "asset_sha256": {name: digest(archive.read(name)) for name in assets}}


def inspect(jar, javap):
    verify_artifact(jar)
    registry = json.loads((PROVIDER / "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
    bindings = [row for row in registry["native"]["bindings"] if row["path"] in PIECES]
    require(len(bindings) == len(PIECES) and {row["resource_location"] for row in bindings}
            == {"alexscaves:" + name for name in PIECES}, "diving gear registry binding mismatch")
    with ZipFile(jar) as archive:
        native = class_evidence(archive, jar, javap)
        factories = {m["declaration"]["name"]: m["declaration"]["code_sha256"]
                     for m in native["classes"]["server/item/ACItemRegistry"]["methods"]}
        require(all(factories.get(row["factory"]["name"]) == row["factory"]["code_sha256"]
                    for row in bindings), "diving gear factory body mismatch")
        return {
            "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
            "references_sha256": {name: digest((PROVIDER / name).read_bytes()) for name in REFERENCES},
            "registry_bindings": bindings,
            "native": native,
            "resources": resource_evidence(archive),
            "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "provider_universe_closed": False,
            "semantic_magic_roots_added": 0,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "new output required")
    report = inspect(args.jar, args.javap)
    require(canonical(report) == SEAL.read_text(encoding="utf8"), "diving armor catalog seal mismatch")
    with args.output.open("x", encoding="utf8") as stream:
        stream.write(canonical(report))
    print("CATALOG_SHA256", digest(args.output.read_bytes()))


if __name__ == "__main__":
    main()
