#!/usr/bin/env python3
"""Reproduce the exact Floater and Frostmint Spear item contracts."""

import argparse
import json
from pathlib import Path
import re
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_bottle_fertilizer_catalog import MOJANG, verified_mojang
from alexscaves_1010_destroyed_item_engine_reference import artifact_identity, verify_artifact as verify_neo
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

PROVIDER = Path(__file__).resolve().parents[2] / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.json"
PREFIX = "com/github/alexmodguy/alexscaves/"
REGISTRIES = (PREFIX + "server/item/ACItemRegistry", PREFIX + "server/entity/ACEntityRegistry")
FIELDS = {"FLOATER", "FROSTMINT_SPEAR", "FROSTMINT_SPEAR_SPRITE"}
IDS = {"floater", "frostmint_spear", "frostmint_spear_inventory"}
TARGETS = {
    "server/item/FloaterItem": 2, "server/entity/item/FloaterEntity": 14,
    "server/item/FrostmintSpearItem": 3, "server/entity/item/FrostmintSpearEntity": 16,
}
ACCESSOR = "server/entity/util/FrostmintFreezableAccessor"
# Each selected method keeps the full code and instruction hashes. Large
# registry, render and explosion bodies retain only their relevant slices.
METHODS = {
    **{owner: None for owner in TARGETS},
    ACCESSOR: set(),
    "client/ClientProxy": {"clientInit"},
    "client/model/FloaterModel": {"setupAnim"},
    "client/render/entity/FloaterRenderer": None,
    "client/render/entity/FrostmintSpearRenderer": {"render", "getTextureLocation", "<clinit>"},
    "mixin/LivingEntityMixin": {"ac_livingTick", "setFrostmintFreezing", "isFreezingFromFrostmint"},
    "server/entity/ACEntityRegistry": {"<clinit>", "lambda$static$51", "lambda$static$82"},
    "server/entity/util/FrostmintExplosion": {"<init>", "explode", "finalizeExplosion", "getSeenPercent",
                                            "getDirectSourceEntity", "getIndirectSourceEntity", "interactsWithBlocks"},
    "server/item/ACItemRegistry": {"<clinit>", "lambda$static$103", "lambda$static$192", "lambda$static$193"},
    "server/item/SpearItem": {"<init>", "getPowerForTime", "use", "mineBlock", "acHurtEnemy", "hurtEnemy",
                             "getUseDuration", "getUseAnimation", "acModifiers", "getDefaultAttributeModifiers"},
    "server/misc/ACCompat": {"createEntity", "isInWaterOrBubble", "useSidedSuccess", "usePass", "itemParticle",
                            "damageBonus", "postAttackEffects", "hurt", "explosionKnockback"},
    "server/misc/ACPlatform": {"myRidingOffset", "getEntitySpawningPacket", "ignoreExplosion", "explosion"},
}
EXCERPTS = {
    ("client/ClientProxy", "clientInit"): ((1276, 1292), (1846, 1862), (2146, 2171)),
    ("server/entity/ACEntityRegistry", "<clinit>"): ((0, 25), (891, 905), (1418, 1435)),
    ("server/item/ACItemRegistry", "<clinit>"): ((0, 25), (1953, 1967), (3381, 3412)),
    ("server/entity/util/FrostmintExplosion", "explode"): ((399, 526), (611, 647), (755, 849), (917, 931),
                                                        (988, 1034)),
    ("server/entity/util/FrostmintExplosion", "finalizeExplosion"): ((0, 141),),
    ("server/entity/util/FrostmintExplosion", "getSeenPercent"): (),
}
REFERENCES = (
    "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json", "EXACT-DYNAMIC-ATTRIBUTE-CONTRACT-1.0.10.json",
    "EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json",
)
CLIENT_METHODS = {
    "bqs": ("net.minecraft.world.InteractionResultHolder", {
        ("a", "(Ljava/lang/Object;Z)Lbqs;"),
    }),
    "bsr": ("net.minecraft.world.entity.Entity", {
        ("n", "(Lbsr;)Z"), ("a", "(Lbsr;Z)Z"), ("bi", "()Z"), ("v", "(Lbsr;)V"), ("cZ", "()Lbsr;"),
    }),
    "bsx": ("net.minecraft.world.entity.EntityType", {("a", "(Ldcw;)Lbsr;")}),
}
PATCHES = ("world/entity/Entity", "world/entity/EntityType", "world/entity/projectile/AbstractArrow")


def class_census(archive):
    paths = archive.namelist()
    classes = sorted(path for path in paths if path.endswith(".class"))
    require(len(classes) == 1555 and len(paths) == len(set(paths)), "publisher roster drift")
    targets = tuple(PREFIX + owner for owner in (*TARGETS, ACCESSOR))
    owners = {}
    for path in classes:
        reader = ClassReader(archive.read(path))
        require(path == reader.name + ".class" and reader.major == 65, "publisher class identity drift")
        refs = {target: reader.typed_refs(target) for target in targets}
        for registry in REGISTRIES:
            refs[registry] = [ref for ref in reader.typed_refs(registry)
                              if ref["kind"] == "field_reference" and ref["name"] in FIELDS]
        relevant = {key: value for key, value in refs.items() if value}
        if relevant:
            owners[reader.name] = relevant
    return classes, owners


def method_evidence(reader, key, body, bounds=None):
    method = summarize(reader, key, body)
    if bounds is not None:
        method["instructions"] = [row for row in method["instructions"]
                                  if any(lo <= row["offset"] <= hi for lo, hi in bounds)]
        method["excerpt_offsets"] = [list(pair) for pair in bounds]
    return method


def publisher_evidence(archive, jar, javap):
    classes, owners = class_census(archive)
    details = {}
    for owner in sorted(set(owners) | {PREFIX + name for name in METHODS}):
        raw = archive.read(owner + ".class")
        reader = ClassReader(raw)
        relative = owner.removeprefix(PREFIX)
        selected = METHODS.get(relative, set())
        bodies = disassemble(jar, javap, owner) if any("code_sha256" in m for m in reader.methods) else {}
        require(selected is None or selected <= {name for name, _ in bodies}, "missing body: " + owner)
        if relative in TARGETS:
            require(len(bodies) == TARGETS[relative], "own method coverage drift: " + owner)
        indexes = {ref["index"] for group in owners.get(owner, {}).values()
                   for ref in group if ref["kind"] in ("class_constant", "method_reference",
                                                       "interface_method_reference", "field_reference")}
        methods = []
        sites = []
        bootstraps = set()
        for key, body in sorted(bodies.items()):
            name, descriptor = key
            if body and (selected is None or name in selected):
                method = method_evidence(reader, key, body, EXCERPTS.get((relative, name)))
                methods.append(method)
                for row in method["instructions"]:
                    match = re.match(r"InvokeDynamic #(\d+):", row["symbol"])
                    if match:
                        bootstraps.add(int(match[1]))
            for offset, (op, operand, symbol) in sorted(body.items()):
                match = re.match(r"#(\d+)", operand)
                if match and int(match[1]) in indexes:
                    sites.append({"method": name, "descriptor": descriptor, "offset": offset,
                                  "opcode": op, "symbol": symbol})
        details[relative] = {
            "class_sha256": digest(raw), "superclass": reader.parent, "interfaces": reader.interfaces,
            "methods": methods, "reference_sites": sites,
            "selected_bootstraps": {str(index): reader.attributes["bootstrap_methods"][index]
                                    for index in sorted(bootstraps)},
        }
        if relative in TARGETS or relative == ACCESSOR:
            details[relative].update(fields=reader.fields, declarations=reader.methods)
    return {"class_count": len(classes), "class_roster_sha256": digest(("\n".join(classes) + "\n").encode()),
            "typed_owners": owners, "classes": details}


def resources(archive):
    ids = {f'"alexscaves:{name}"'.encode() for name in IDS}
    data = {}
    for path in sorted(archive.namelist()):
        if path.startswith("data/") and path.endswith(".json"):
            raw = archive.read(path)
            if any(item in raw for item in ids) or path.endswith("/weapon_attributes/frostmint_spear.json"):
                data[path] = {"sha256": digest(raw), "json": json.loads(raw)}
    for name in ("floater", "frostmint_spear"):
        require(f"data/alexscaves/recipe/{name}.json" in data, "missing item recipe")
    assets = (
        "alexscaves.mixins.json",
        "assets/alexscaves/books/abyssal_chasm/utilities.json",
        "assets/alexscaves/books/candy_cavity/utilities.json",
        "assets/alexscaves/models/item/floater.json", "assets/alexscaves/models/item/frostmint_spear.json",
        "assets/alexscaves/models/item/frostmint_spear_inventory.json",
        "assets/alexscaves/models/item/frostmint_spear_throwing.json",
        "assets/alexscaves/textures/entity/floater.png", "assets/alexscaves/textures/entity/frostmint_spear.png",
        "assets/alexscaves/textures/item/floater.png", "assets/alexscaves/textures/item/frostmint_spear.png",
        "assets/alexscaves/particles/frostmint_explosion.json", "assets/alexscaves/sounds.json",
    )
    locales = {}
    for locale in ("en_us", "pt_br"):
        raw = archive.read(f"assets/alexscaves/lang/{locale}.json")
        labels = json.loads(raw)
        locales[locale] = {"sha256": digest(raw), "names": {
            name: labels.get("item.alexscaves." + name) for name in sorted(IDS)}}
    return {"data": data, "locales": locales, "assets_sha256": {path: digest(archive.read(path)) for path in assets}}


def engine_reference(args):
    verified_mojang(args.client, "client")
    mappings = verified_mojang(args.mappings, "mappings").decode("utf-8")
    verify_neo(args.universal, "universal")
    verify_neo(args.userdev, "userdev")
    minecraft = {}
    with ZipFile(args.client) as archive:
        for owner, (mapped, keys) in CLIENT_METHODS.items():
            require(f"{mapped} -> {owner}:" in mappings, "missing mapped class " + mapped)
            raw = archive.read(owner + ".class")
            reader = ClassReader(raw)
            bodies = disassemble(args.client, args.javap, owner)
            require(keys <= bodies.keys(), "engine method drift: " + mapped)
            minecraft[mapped] = {"owner": owner, "class_sha256": digest(raw), "methods": [
                method_evidence(reader, key, bodies[key]) for key in sorted(keys)]}
    hooks = "net/neoforged/neoforge/event/EventHooks"
    with ZipFile(args.universal) as archive:
        raw = archive.read(hooks + ".class")
        reader = ClassReader(raw)
        key, body = next((key, body) for key, body in disassemble(args.universal, args.javap, hooks).items()
                         if key[0] == "canMountEntity")
        neo = {"owner": hooks, "class_sha256": digest(raw), "method": method_evidence(reader, key, body)}
    with ZipFile(args.userdev) as archive:
        names = [f"patches/net/minecraft/{name}.java.patch" for name in PATCHES]
        patches = {name: digest(archive.read(name)) for name in names}
    return {
        "scope": "PINNED_REFERENCE_NOT_INSTALLED_RUNTIME",
        "mojang_artifacts": MOJANG, "mojang_methods": minecraft,
        "neoforge_artifacts": {kind: artifact_identity(kind) for kind in ("universal", "userdev")},
        "mount_event": neo, "userdev_patch_sha256": patches,
    }


def inspect(args):
    verify_artifact(args.jar)
    registry = json.loads((PROVIDER / REFERENCES[0]).read_text(encoding="utf-8"))
    bindings = [row for row in registry["native"]["bindings"] if row["path"] in IDS]
    require(len(bindings) == 3 and {row["path"] for row in bindings} == IDS, "item bindings drift")
    with ZipFile(args.jar) as archive:
        native = publisher_evidence(archive, args.jar, args.javap)
        factories = {m["declaration"]["name"]: m["declaration"]["code_sha256"]
                     for m in native["classes"]["server/item/ACItemRegistry"]["methods"]}
        require(all(factories.get(row["factory"]["name"]) == row["factory"]["code_sha256"]
                    for row in bindings), "item factory digest mismatch")
        return {
            "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
            "references_sha256": {name: digest((PROVIDER / name).read_bytes()) for name in REFERENCES},
            "bindings": bindings, "native": native, "resources": resources(archive),
            "engine_reference": engine_reference(args),
            "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY", "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION", "provider_universe_closed": False,
            "semantic_magic_roots_added": 0,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "client", "mappings", "universal", "userdev", "javap", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "new output required")
    report = canonical(inspect(args))
    require(report == SEAL.read_text(encoding="utf-8"), "Floater and Frostmint catalog seal mismatch")
    with args.output.open("x", encoding="utf-8") as output:
        output.write(report)
    print("CATALOG_SHA256", digest(args.output.read_bytes()))


if __name__ == "__main__":
    main()
