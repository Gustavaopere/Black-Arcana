#!/usr/bin/env python3
"""Bounded repair eligibility/settlement reference: publisher and official engine bytes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import zipfile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_enchantable_item_boundary import CLIENT_SHA1, download
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_engine, ARTIFACTS
from minecraft_1211_mojang_mixin_target_mappings import CLASS, METHOD, official_version_downloads
from minecraft_1211_vanilla_target_callsites import jvm_type

PREFIX = "com/github/alexmodguy/alexscaves/server/"
ITEM = "net.minecraft.world.item.Item"
STACK = "net.minecraft.world.item.ItemStack"
SHIELD = "net.minecraft.world.item.ShieldItem"
ANVIL = "net.minecraft.world.inventory.AnvilMenu"
TARGETS = {
    ITEM: {"isValidRepairItem"},
    STACK: {"is", "getDamageValue", "getMaxDamage", "setDamageValue", "shrink"},
    SHIELD: {"isValidRepairItem"},
    ANVIL: {"createResult", "onTake", "mayPickup"},
}
REPAIR_DESCRIPTOR = "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;)Z"
FIELDS = {
    PREFIX + "item/ACItemRegistry": {"PURE_DARKNESS", "TECTONIC_SHARD", "HEAVY_BONE",
                                    "SCARLET_NEODYMIUM_INGOT", "AZURE_NEODYMIUM_INGOT"},
    PREFIX + "block/ACBlockRegistry": {"PACKED_GALENA"},
}


def native(jar, javap):
    verify_artifact(jar)
    result = {}
    with zipfile.ZipFile(jar) as z:
        spear = PREFIX + "item/SpearItem"
        raw = z.read(spear + ".class")
        rd = ClassReader(raw)
        key = ("isValidRepairItem", REPAIR_DESCRIPTOR)
        declarations = [m for m in rd.methods if (m["name"], m["descriptor"]) == key]
        body = disassemble(jar, javap, spear).get(key)
        require(bool(declarations) == (body is not None), "SpearItem declaration/disassembly mismatch")
        result["spear"] = {"owner": spear, "parent": rd.parent, "class_sha256": digest(raw),
                           "declarations": declarations,
                           "method": summarize(rd, key, body) if body is not None else None}
        bindings = {}
        for owner, fields in FIELDS.items():
            raw = z.read(owner + ".class")
            rd = ClassReader(raw)
            init = disassemble(jar, javap, owner)[("<clinit>", "()V")]
            ordered = sorted(init.items())
            matches = {}
            for n, (off, (op, operand, symbol)) in enumerate(ordered):
                if op != "putstatic":
                    continue
                cp = re.match(r"#(\d+)", operand)
                if not cp:
                    continue
                ref = rd.resolve(int(cp[1]))
                if not isinstance(ref, list) or ref[0] != 9 or ref[1] != owner or ref[2][1] not in fields:
                    continue
                field = ref[2][1]
                require(field not in matches, "duplicate material field write")
                previous = ordered[max(0, n - 10):n + 1]
                matches[field] = {"write": off, "context": [{"offset": o, "opcode": v[0],
                    "operand": v[1], "symbol": v[2]} for o, v in previous]}
            require(set(matches) == fields, "material binding coverage drift")
            bindings[owner] = {"class_sha256": digest(raw), "fields": matches}
        result["bindings"] = bindings
    return result


def vanilla(tmp, javap):
    meta = official_version_downloads()
    files = meta["downloads"]
    require(files["client"]["sha1"] == CLIENT_SHA1, "vanilla version drift")
    jar, mapping = tmp / "client.jar", tmp / "mappings.txt"
    client = download(jar, files["client"], 35000000)
    mappings = download(mapping, files["client_mappings"], 15000000)
    require(client["sha256"] == "499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99", "client hash drift")
    require(mappings["sha256"] == "140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec", "mapping hash drift")
    lines = mapping.read_text(encoding="utf8").splitlines()
    names = dict(line[:-1].split(" -> ") for line in lines if CLASS.fullmatch(line))
    reverse = {v.replace(".", "/"): k for k, v in names.items()}

    def desc_type(t):
        dims = 0
        while t.endswith("[]"):
            dims += 1
            t = t[:-2]
        return "[" * dims + jvm_type(t, names if t in names else {t: t})

    mapped = {}
    member_map = {}
    own = None
    field_re = re.compile(r"^(\S+)\s+([\w$]+)\s+->\s+(\S+)$")
    for line in lines:
        if CLASS.fullmatch(line):
            own = line.split(" -> ")[0]
            continue
        m = METHOD.fullmatch(line.strip())
        f = field_re.fullmatch(line.strip())
        if own is None or not (m or f):
            continue
        if m:
            ret, name, rawargs = m.groups()
            args = tuple(rawargs.split(",")) if rawargs else ()
            desc = "(" + "".join(desc_type(a) for a in args) + ")" + desc_type(ret)
            obf = line.strip().rsplit(" -> ", 1)[1]
            if own in TARGETS and name in TARGETS[own]:
                mapped.setdefault(own, {})[(obf, desc)] = name
        else:
            ret, name, obf = f.groups()
            desc = desc_type(ret)
        member_map.setdefault((names[own].replace(".", "/"), obf, desc), set()).add(own + "." + name)
    result = {}
    with zipfile.ZipFile(jar) as z:
        for owner in TARGETS:
            obf = names[owner].replace(".", "/")
            raw = z.read(obf + ".class")
            rd = ClassReader(raw)
            parsed = disassemble(jar, javap, obf)
            methods = []
            for k, name in sorted(mapped.get(owner, {}).items()):
                require(k in parsed and len(parsed[k]) <= 2500, "mapped body absent or over bound")
                s = summarize(rd, k, parsed[k])
                refs = []
                for row in s["instructions"]:
                    if not (row["opcode"].startswith("invoke") or row["opcode"] in ("getfield", "putfield", "getstatic", "putstatic")):
                        continue
                    cp = re.match(r"#(\d+)", row["operand"])
                    if not cp:
                        continue
                    ref = rd.resolve(int(cp[1]))
                    if isinstance(ref, list) and ref[0] in (9, 10, 11):
                        refs.append({"offset": row["offset"], "member": ref,
                                     "named_candidates": sorted(member_map.get((ref[1], ref[2][1], ref[2][2]), ()))})
                s["named_method"] = name
                s["refs"] = refs
                methods.append(s)
            require(TARGETS[owner] <= {m["named_method"] for m in methods}, "missing reference method " + owner)
            result[owner] = {"obfuscated_owner": obf, "parent": reverse.get(rd.parent, rd.parent),
                             "class_sha256": digest(raw), "methods": methods}
    return {"client": client, "mappings": mappings, "classes": result}


def neo(universal, userdev, javap):
    verify_engine(universal, "universal")
    verify_engine(userdev, "userdev")
    relevant = re.compile(r"repair|anvil", re.IGNORECASE)
    classes = {}
    with zipfile.ZipFile(universal) as z:
        owners = ("net/neoforged/neoforge/common/CommonHooks",
                  "net/neoforged/neoforge/common/extensions/IItemExtension",
                  "net/neoforged/neoforge/common/extensions/IItemStackExtension",
                  "net/neoforged/neoforge/event/AnvilUpdateEvent",
                  "net/neoforged/neoforge/event/entity/player/AnvilRepairEvent")
        for owner in owners:
            if owner + ".class" not in z.namelist():
                classes[owner] = {"present": False}
                continue
            raw = z.read(owner + ".class")
            rd = ClassReader(raw)
            parsed = disassemble(universal, javap, owner)
            methods = [summarize(rd, k, body) for k, body in sorted(parsed.items())
                       if body and (relevant.search(k[0]) or "Event" in owner)]
            classes[owner] = {"present": True, "class_sha256": digest(raw), "methods": methods,
                              "declarations": [m for m in rd.methods if relevant.search(m["name"])]}
    patches = {}
    with zipfile.ZipFile(userdev) as z:
        for owner in ("world/item/Item.java", "world/item/ItemStack.java", "world/item/ShieldItem.java",
                      "world/inventory/AnvilMenu.java", "world/inventory/ItemCombinerMenu.java"):
            p = "patches/net/minecraft/" + owner + ".patch"
            if p not in z.namelist():
                patches[p] = {"present": False}
                continue
            raw = z.read(p)
            lines = raw.decode("utf8").splitlines()
            hits = {i for i, s in enumerate(lines) if relevant.search(s) and not s.startswith(("+++", "---"))}
            selected = {n for i in hits for n in range(max(0, i - 3), min(len(lines), i + 4))}
            patches[p] = {"present": True, "sha256": digest(raw), "selected": [{"line": i + 1, "text": lines[i]} for i in sorted(selected)]}
    return {"artifacts": ARTIFACTS, "classes": classes, "patches": patches}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "universal", "userdev", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    require(not a.output.exists(), "new output required")
    tmp = a.output.parent / "repair-reference"
    tmp.mkdir()
    report = {"scope": "STATIC_REFERENCE_ONLY", "native": native(a.jar, a.javap),
              "vanilla": vanilla(tmp, a.javap), "neoforge": neo(a.universal, a.userdev, a.javap),
              "mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED"}
    a.output.write_text(canonical(report), encoding="utf8")
    print("BOUNDARY_SHA256", digest(a.output.read_bytes()))
    print("NATIVE_BOUNDARY", json.dumps(report["native"], sort_keys=True))
    for owner, data in report["vanilla"]["classes"].items():
        print("VANILLA_OWNER", owner, data["obfuscated_owner"], data["class_sha256"], data["parent"])
        for m in data["methods"]:
            print("VANILLA_METHOD", owner, json.dumps(m, sort_keys=True))
    for owner, data in report["neoforge"]["classes"].items():
        print("NEO_OWNER", owner, json.dumps(data, sort_keys=True))
    for path, data in report["neoforge"]["patches"].items():
        print("NEO_PATCH", path, json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    main()
