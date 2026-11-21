#!/usr/bin/env python3
"""Reproduce the publisher evidence for the two presentation APIs and darkness items."""

import argparse
import json
from pathlib import Path
import re
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact
from alexscaves_1010_burrowing_cave_map_probe import compact, inherits
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.json"
PREFIX = "com/github/alexmodguy/alexscaves/"
ITEM = PREFIX + "server/item/"
TARGETS = tuple(ITEM + name for name in ("CustomArmorPostRender", "CustomTabBehavior",
                                       "DarkenedAppleItem", "DarknessArmorItem"))
IDS = ("darkened_apple", "hood_of_darkness", "cloak_of_darkness")
REFERENCES = (
    "EXACT-ARMOR-MATERIAL-1.0.10.json",
    "EXACT-CLIENT-EXTENSION-1.0.10.json",
    "EXACT-EFFECT-CONTRACTS-1.0.10.json",
    "EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json",
    "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json",
    "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json",
    "EXACT-TECHNICAL-CONTRACTS-1.0.10.json",
    "EXACT-TICKING-ITEM-CONTRACT-1.0.10.json",
)
SUPPLEMENT = {
    "AlexsCaves": {"<init>"},
    "client/render/item/ACArmorRenderProperties": {"getACArmorModelBase", "renderCustomArmor"},
    "mixin/client/HumanoidArmorLayerMixin": None,
    "server/config/ACServerConfig": {"<init>"},
    "server/item/ACItemRegistry": {"lambda$static$134", "lambda$static$135", "lambda$static$136"},
    "server/misc/ACAdvancementTrigger": {"triggerForEntity"},
    "server/misc/ACAdvancementTriggerRegistry": {"<clinit>"},
    "server/misc/ACCreativeTabRegistry": {"add", *(f"lambda$static${i}" for i in
                                                (1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 21, 24, 25))},
    "server/potion/DarknessIncarnateEffect": None,
}
TEXTURES = tuple(f"assets/alexscaves/textures/armor/{name}.png" for name in (
    "darkness_armor", "darkness_armor_glow", "rainbounce_boots",
    "diving_suit_0", "diving_suit_1", "gingerbread_armor_0", "gingerbread_armor_1",
    "hazmat_suit_0", "hazmat_suit_1", "primordial_armor_0", "primordial_armor_1",
))


def census(archive):
    paths = archive.namelist()
    classes = sorted(p for p in paths if p.endswith(".class"))
    require(len(classes) == 1555 and len(paths) == len(set(paths)), "unexpected publisher roster")
    typed = {name: {} for name in TARGETS}
    hierarchy = {}
    for path in classes:
        reader = ClassReader(archive.read(path))
        require(path == reader.name + ".class" and reader.major == 65, "class path or version drift")
        hierarchy[reader.name] = {"parent": reader.parent, "interfaces": reader.interfaces}
        for target, owners in typed.items():
            refs = reader.typed_refs(target)
            if refs:
                owners[reader.name] = refs
    return classes, typed, hierarchy


def relocate(archive, jar, javap):
    classes, typed, hierarchy = census(archive)
    cache = {}

    def load(owner):
        if owner not in cache:
            raw = archive.read(owner + ".class")
            reader = ClassReader(raw)
            method_bodies = disassemble(jar, javap, owner) if any("code_sha256" in m for m in reader.methods) else {}
            cache[owner] = (digest(raw), reader, method_bodies)
        return cache[owner]

    targets = {}
    for target in TARGETS:
        class_hash, reader, methods = load(target)
        own = [compact(summarize(reader, key, body)) for key, body in sorted(methods.items()) if body]
        require(len(own) == sum("code_sha256" in m for m in reader.methods), "own body coverage drift")
        users = {}
        for owner, refs in typed[target].items():
            owner_hash, _, bodies = load(owner)
            constants = {ref["index"] for ref in refs if ref["kind"] in
                         ("class_constant", "method_reference", "interface_method_reference", "field_reference")}
            sites = []
            for (method, descriptor), body in sorted(bodies.items()):
                for off, (op, operand, symbol) in body.items():
                    index = re.match(r"#(\d+)", operand)
                    if index and int(index[1]) in constants:
                        sites.append({"method": method, "descriptor": descriptor,
                                      "offset": off, "opcode": op, "symbol": symbol})
            users[owner] = {"class_sha256": owner_hash, "typed_references": refs, "sites": sites}
        descendants = sorted(name for name in hierarchy if name != target and inherits(name, target, hierarchy))
        targets[target.removeprefix(ITEM)] = {"class_sha256": class_hash, "hierarchy": hierarchy[target],
                                              "fields": reader.fields, "declarations": reader.methods,
                                              "methods": own, "assignable_classes": descendants, "typed_owners": users}
    renderers = targets["CustomArmorPostRender"]["assignable_classes"]
    require(len(renderers) == 6, "render implementer drift")
    require(not targets["CustomTabBehavior"]["assignable_classes"], "tab implementer appeared")
    texture_literals = {}
    for owner in renderers:
        _, _, bodies = load(owner)
        body, = (body for signature, body in bodies.items() if signature[0] == "getArmorTexture")
        literals = sorted({symbol.removeprefix("String alexscaves:") for _, _, symbol in body.values()
                           if symbol.startswith("String alexscaves:textures/armor/")})
        require(literals and all("assets/alexscaves/" + path in TEXTURES for path in literals),
                "unmapped armor texture: " + owner)
        texture_literals[owner] = literals
    consumers = {}
    for relative_owner, names in SUPPLEMENT.items():
        class_hash, reader, bodies = load(PREFIX + relative_owner)
        selected = [compact(summarize(reader, key, body)) for key, body in sorted(bodies.items())
                    if body and (names is None or key[0] in names)]
        if names is not None:
            require({entry["declaration"]["name"] for entry in selected} == names,
                    "missing consumer method in " + relative_owner)
        consumers[relative_owner] = {"class_sha256": class_hash, "methods": selected}
    return {
        "class_entries_scanned": len(classes),
        "class_path_roster_sha256": digest(("\n".join(classes) + "\n").encode()),
        "targets": targets,
        "consumers": consumers,
        "armor_texture_literals": texture_literals,
    }


def resources(archive):
    names = [f"data/alexscaves/recipe/{name}.json" for name in IDS]
    names += [f"assets/alexscaves/models/item/{name}.json" for name in IDS]
    names += ["data/alexscaves/advancement/alexscaves/eat_darkened_apple.json",
              "data/alexscaves/advancement/alexscaves/shadow_armor.json",
              "data/alexscaves/tags/item/repairs_darkness_armor.json", "alexscaves.mixins.json"]
    payloads = {name: archive.read(name) for name in names}
    display_names = {}
    for language in ("en_us", "pt_br"):
        locale = archive.read(f"assets/alexscaves/lang/{language}.json")
        strings = json.loads(locale)
        display_names[language] = {"sha256": digest(locale), "names": {
            name: strings[f"item.alexscaves.{name}"] for name in IDS}}
    manifest = archive.read("META-INF/neoforge.mods.toml")
    require(b"alexscaves.mixins.json" in manifest, "mixin configuration declaration missing")
    book_path = "assets/alexscaves/books/forlorn_hollows/utilities.json"
    require(b'"alexscaves:darkened_apple"' in archive.read(book_path), "apple guide recipe missing")
    return {
        "json": {name: {"sha256": digest(data), "json": json.loads(data)} for name, data in payloads.items()},
        "texture_sha256": {name: digest(archive.read(name)) for name in TEXTURES},
        "locales": display_names,
        "auxiliary_resource_sha256": {name: digest(archive.read(name))
                                       for name in ("META-INF/neoforge.mods.toml", book_path)},
    }


def inspect(jar, javap):
    verify_artifact(jar)
    registry = json.loads((PROVIDER / "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
    foods = json.loads((PROVIDER / "EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json").read_text(encoding="utf8"))
    bindings = [row for row in registry["native"]["bindings"] if row["path"] in IDS]
    require({row["resource_location"] for row in bindings} == {"alexscaves:" + name for name in IDS}
            and len(bindings) == len(IDS), "wrong item bindings")
    with ZipFile(jar) as archive:
        return {
            "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
            "references_sha256": {name: digest((PROVIDER / name).read_bytes()) for name in REFERENCES},
            "registry_bindings": bindings,
            "rarity_alias": registry["native"]["support_field_initializers"]["RARITY_DEMONIC"],
            "food_profile": foods["native"]["field_profiles"]["DARKENED_APPLE"],
            "native": relocate(archive, jar, javap),
            "resources": resources(archive),
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
    require(not args.output.exists(), "new report required")
    report = inspect(args.jar, args.javap)
    require(report == json.loads(SEAL.read_text(encoding="utf8")), "darkness items catalog seal mismatch")
    with args.output.open("x", encoding="utf8") as output:
        output.write(canonical(report))
    print("CATALOG_SHA256", digest(args.output.read_bytes()))


if __name__ == "__main__":
    main()
