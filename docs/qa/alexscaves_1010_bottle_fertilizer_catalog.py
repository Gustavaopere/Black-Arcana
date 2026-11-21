#!/usr/bin/env python3
"""Reproduce the bottle and fertilizer contracts and their pinned engine references."""

import argparse
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_destroyed_item_engine_reference import artifact_identity, verify_artifact as verify_neo
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

PROVIDER = Path(__file__).resolve().parents[2] / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-BOTTLE-FERTILIZER-CATALOG-1.0.10.json"
PREFIX = "com/github/alexmodguy/alexscaves/"
REGISTRY = PREFIX + "server/item/ACItemRegistry"
ITEM_NAMES = ("purple_soda_bottle", "fertilizer")
FIELDS = {name.upper() for name in ITEM_NAMES}
TARGETS = tuple(PREFIX + "server/item/" + name for name in ("DrinkableBottledItem", "FertilizerItem"))
EXPECTED_METHODS = {
    "server/event/CommonEvents": {"onRightClickItem", "getPlayerPOVHitResult"},
    "server/item/ACFoods": {"<clinit>", "lambda$static$36"},
    "server/item/ACItemRegistry": {"lambda$static$123", "lambda$static$148"},
    "server/item/DrinkableBottledItem": None,
    "server/item/FertilizerItem": None,
    "server/item/HotChocolateBottleItem": {"<init>", "finishUsingItem"},
    "server/item/SackOfSatingItem": {"overrideOtherStackedOnMe", "calculateWholeStackHungerValue"},
    "server/misc/ACCompat": {"blockReach", "sidedSuccess"},
    "server/misc/ACCreativeTabRegistry": set(),
    "server/misc/ACPlatform": {"onApplyBonemeal"},
}
REFERENCE_FILES = (
    "EXACT-EFFECT-CONTRACTS-1.0.10.json",
    "EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json",
    "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json",
    "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json",
)
MOJANG = {
    "client": {"size": 26836906, "sha1": "30c73b1c5da787909b2f73340419fdf13b9def88",
               "sha256": "499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99"},
    "mappings": {"size": 9598610, "sha1": "2244b6f072256667bcd9a73df124d6c58de77992",
                 "sha256": "140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec"},
}
# Full method/code hashes are retained; selected offsets are enough to show the engine handoffs.
CLIENT_METHODS = {
    "aqw": ("net.minecraft.server.level.ServerPlayerGameMode", {
        ("a", "(Laqv;Ldcw;Lcuq;Lbqq;Lewy;)Lbqr;"): ((246, 295),),
    }),
    "bqr": ("net.minecraft.world.InteractionResult", {("a", "(Z)Lbqr;"): None}),
    "brz": ("net.minecraft.world.effect.MobEffectInstance", {("<init>", "(Ljm;I)V"): None}),
    "cmx": ("net.minecraft.world.entity.player.Player", {("a", "(Ldcw;Lcuq;Lcpr;)Lcuq;"): None}),
    "csq": ("net.minecraft.world.item.BoneMealItem", {
        ("a", "(Lcuq;Ldcw;Ljd;)Z"): None,
        ("a", "(Lcuq;Ldcw;Ljd;Lji;)Z"): ((0, 52), (386, 475)),
    }),
    "cul": ("net.minecraft.world.item.Item", {("a", "(Lcuq;Ldcw;Lbtn;)Lcuq;"): None}),
    "cus": ("net.minecraft.world.item.ItemUtils", {("a", "(Ldcw;Lcmx;Lbqq;)Lbqs;"): None}),
}
NEO_METHODS = {
    "net/neoforged/neoforge/common/CommonHooks": {"onPlaceItemIntoWorld"},
    "net/neoforged/neoforge/event/EventHooks": {"fireBonemealEvent"},
    "net/neoforged/neoforge/event/entity/player/BonemealEvent": {"<init>", "isSuccessful", "setSuccessful"},
}
PATCHES = (
    "server/level/ServerPlayerGameMode", "world/entity/LivingEntity", "world/entity/player/Player",
    "world/item/BoneMealItem", "world/item/Item", "world/item/ItemStack",
    "world/item/ItemUtils", "world/item/context/UseOnContext",
)
RELATED_DATA = {
    "data/alexscaves/tags/fluid/purple_soda.json",
    "data/alexscaves/tags/item/explodes_sack_of_sating.json",
    "data/alexscaves/tags/item/restricted_from_sack_of_sating.json",
}


def typed_census(archive):
    entries = archive.namelist()
    paths = sorted(path for path in entries if path.endswith(".class"))
    require(len(paths) == 1555 and len(entries) == len(set(entries)), "publisher roster drift")
    owners = {}
    for path in paths:
        reader = ClassReader(archive.read(path))
        require(path == reader.name + ".class" and reader.major == 65, "class path or version drift")
        refs = {target: reader.typed_refs(target) for target in TARGETS}
        refs[REGISTRY] = [ref for ref in reader.typed_refs(REGISTRY)
                          if ref["kind"] == "field_reference" and ref["name"] in FIELDS]
        refs = {owner: matches for owner, matches in refs.items() if matches}
        if refs:
            owners[reader.name] = refs
    return paths, owners


def publisher_evidence(archive, jar, javap):
    paths, owners = typed_census(archive)
    evidence = {}
    for owner in sorted(set(owners) | {PREFIX + name for name in EXPECTED_METHODS}):
        raw = archive.read(owner + ".class")
        reader = ClassReader(raw)
        relative = owner.removeprefix(PREFIX)
        select = EXPECTED_METHODS.get(relative, set())
        parsed = disassemble(jar, javap, owner)
        if select is not None:
            require(select <= {name for name, _ in parsed}, "missing requested body: " + owner)
        indexed = {ref["index"] for refs in owners.get(owner, {}).values()
                   for ref in refs if "index" in ref and ref["kind"] != "name_and_type_descriptor"}
        methods = []
        sites = []
        for key, body in sorted(parsed.items()):
            name, descriptor = key
            if body and (select is None or name in select):
                method = summarize(reader, key, body)
                if relative == "server/item/ACFoods" and name == "<clinit>":
                    method["instructions"] = [row for row in method["instructions"] if 1353 <= row["offset"] <= 1384]
                methods.append(method)
            for offset, (opcode, operand, symbol) in sorted(body.items()):
                index = re.match(r"#(\d+)", operand)
                if index and int(index[1]) in indexed:
                    sites.append({"method": name, "descriptor": descriptor, "offset": offset,
                                  "opcode": opcode, "symbol": symbol})
        evidence[relative] = {"class_sha256": digest(raw), "parent": reader.parent,
                              "methods": methods, "reference_sites": sites}
    require([len(evidence[target.removeprefix(PREFIX)]["methods"]) for target in TARGETS] == [7, 3],
            "target method coverage drift")
    return {"class_count": len(paths), "class_roster_sha256": digest(("\n".join(paths) + "\n").encode()),
            "typed_owners": owners, "classes": evidence}


def resource_evidence(archive):
    ids = {f'"alexscaves:{name}"'.encode() for name in ITEM_NAMES}
    data = {}
    guides = {}
    for name in sorted(archive.namelist()):
        if name.endswith(".json") and name.startswith(("data/", "assets/alexscaves/books/")):
            raw = archive.read(name)
            if name in RELATED_DATA or any(item in raw for item in ids):
                if name.startswith("data/"):
                    data[name] = {"sha256": digest(raw), "json": json.loads(raw)}
                else:
                    guides[name] = digest(raw)
    assets = [f"assets/alexscaves/{folder}/{name}.{ext}" for name in ITEM_NAMES
              for folder, ext in (("models/item", "json"), ("textures/item", "png"))]
    locales = {}
    for locale in ("en_us", "pt_br"):
        raw = archive.read(f"assets/alexscaves/lang/{locale}.json")
        labels = json.loads(raw)
        locales[locale] = {"sha256": digest(raw), "names": {
            name: labels.get("item.alexscaves." + name) for name in ITEM_NAMES}}
    require(RELATED_DATA <= data.keys(), "related resource roster drift")
    return {"data": data, "guides_sha256": guides, "locales": locales,
            "asset_sha256": {name: digest(archive.read(name)) for name in assets}}


def verified_mojang(path, label):
    data = path.read_bytes()
    require(MOJANG[label] == {"size": len(data), "sha1": hashlib.sha1(data).hexdigest(),
                             "sha256": digest(data)}, label + " digest or size mismatch")
    return data


def engine_evidence(client, mappings, universal, userdev, javap):
    verified_mojang(client, "client")
    mapping_text = verified_mojang(mappings, "mappings").decode("utf-8")
    verify_neo(universal, "universal")
    verify_neo(userdev, "userdev")
    minecraft = {}
    with ZipFile(client) as archive:
        for owner, (mapped, selection) in CLIENT_METHODS.items():
            require(f"{mapped} -> {owner}:" in mapping_text, "mapping identity drift: " + mapped)
            raw = archive.read(owner + ".class")
            reader = ClassReader(raw)
            parsed = disassemble(client, javap, owner)
            methods = []
            for key, bounds in sorted(selection.items()):
                require(key in parsed and parsed[key], "missing engine body: " + mapped + str(key))
                method = summarize(reader, key, parsed[key])
                if bounds:
                    method["instructions"] = [row for row in method["instructions"]
                                              if any(lo <= row["offset"] <= hi for lo, hi in bounds)]
                methods.append(method)
            minecraft[mapped] = {"owner": owner, "class_sha256": digest(raw), "methods": methods}
    neoforge = {}
    with ZipFile(universal) as archive:
        for owner, selection in NEO_METHODS.items():
            raw = archive.read(owner + ".class")
            reader = ClassReader(raw)
            parsed = disassemble(universal, javap, owner)
            require(selection <= {name for name, _ in parsed}, "missing NeoForge body: " + owner)
            neoforge[owner] = {"class_sha256": digest(raw), "methods": [
                summarize(reader, key, body) for key, body in sorted(parsed.items()) if key[0] in selection]}
    with ZipFile(userdev) as archive:
        paths = set(archive.namelist())
        patch_names = [f"patches/net/minecraft/{name}.java.patch" for name in PATCHES]
        patches = {path: digest(archive.read(path)) if path in paths else None for path in patch_names}
    return {"scope": "PINNED_UPSTREAM_REFERENCE_NOT_INSTALLED_TRANSFORMED_RUNTIME",
            "mojang_artifacts": MOJANG, "mojang_methods": minecraft,
            "neoforge_artifacts": {kind: artifact_identity(kind) for kind in ("universal", "userdev")},
            "neoforge_methods": neoforge, "userdev_patch_sha256": patches}


def inspect(args):
    verify_artifact(args.jar)
    registry = json.loads((PROVIDER / "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json").read_text(encoding="utf-8"))
    foods = json.loads((PROVIDER / "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json").read_text(encoding="utf-8"))
    bindings = [row for row in registry["native"]["bindings"] if row["path"] in ITEM_NAMES]
    require(len(bindings) == 2 and {row["path"] for row in bindings} == set(ITEM_NAMES), "binding roster drift")
    with ZipFile(args.jar) as archive:
        native = publisher_evidence(archive, args.jar, args.javap)
        factories = {m["declaration"]["name"]: m["declaration"]["code_sha256"]
                     for m in native["classes"]["server/item/ACItemRegistry"]["methods"]}
        require(all(factories.get(row["factory"]["name"]) == row["factory"]["code_sha256"]
                    for row in bindings), "factory body drift")
        return {"artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
                "references_sha256": {name: digest((PROVIDER / name).read_bytes()) for name in REFERENCE_FILES},
                "registry_bindings": bindings, "food_profile": foods["native"]["field_profiles"]["PURPLE_SODA_BOTTLE"],
                "native": native, "resources": resource_evidence(archive),
                "engine_reference": engine_evidence(args.client, args.mappings, args.universal, args.userdev, args.javap),
                "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY", "mutating_hook": "NOT_VERIFIED",
                "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION", "provider_universe_closed": False,
                "semantic_magic_roots_added": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "client", "mappings", "universal", "userdev", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "new output required")
    report = canonical(inspect(args))
    require(report == SEAL.read_text(encoding="utf-8"), "bottle and fertilizer catalog seal mismatch")
    with args.output.open("x", encoding="utf-8") as output:
        output.write(report)
    print("CATALOG_SHA256", digest(args.output.read_bytes()))


if __name__ == "__main__":
    main()
