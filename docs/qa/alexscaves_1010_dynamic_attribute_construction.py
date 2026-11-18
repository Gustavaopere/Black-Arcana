#!/usr/bin/env python3
"""Bounded attribute-construction and external-reference audit, not certification.

Reuse the exact publisher identity/census from #1116. Follow its modifier
producers and symbolic bootstrap handles rather than reimplementing native code.
The engine reference is official 21.1.250 universal/userdev, not the installed
transformed game. No third-party class or source file is committed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import zipfile

from alexscaves_1010_armor_material_audit import (
    AuditError, ClassReader, canonical, digest, require, rows,
)
from alexscaves_1010_action_contract_audit import parse_javap
from alexscaves_1010_dynamic_attribute_probe import inspect, PREFIX, TARGET, HELPER
from alexscaves_1010_destroyed_item_engine_reference import (
    verify_artifact as verify_engine, ARTIFACTS,
)

ITEM = PREFIX + "server/item/"
REGISTRY = ITEM + "ACItemRegistry"
FIELDS = {"defaultModifiers", "divingArmorAttributes",
          "gingerbreadDurabilityDependentAttributes", "acDefense", "acSlot"}
NATIVE_NAMES = {"<init>", "<clinit>", "acModifiers",
                "getDefaultAttributeModifiers", "getAttributeModifiers",
                "getOrCreateDurabilityAttributes", "getStatsForEnchantmentLevel"}
HELPER_NAMES = {"itemAttributes", "attributeModifier"}
ENGINE_OWNERS = (
    "net/neoforged/neoforge/common/extensions/IItemExtension",
    "net/neoforged/neoforge/common/extensions/IItemStackExtension",
)
ENGINE_NAMES = {"getAttributeModifiers", "getDefaultAttributeModifiers",
                "forEachModifier", "getAttributeModifiersFromComponents"}
PATCH_TOKENS = re.compile(r"get(?:Default)?AttributeModifiers|forEachModifier|ItemAttributeModifierEvent|ATTRIBUTE_MODIFIERS|modifyItemAttributes")


def disasm(path, javap, name):
    p = subprocess.run([str(javap), "-classpath", str(path), "-p", "-c", "-s",
                        name.replace("/", ".")], capture_output=True, text=True,
                        timeout=90, check=False)
    require(p.returncode == 0, "javap failed: " + name + ": " + p.stderr[:300])
    return parse_javap(p.stdout, name)


def indexed_bootstraps(reader, body):
    result = []
    for offset, (_, operand, symbol) in body.items():
        m = re.search(r"InvokeDynamic #(\d+):", symbol)
        if m:
            idx = int(m.group(1))
            bootstrap = reader.attributes.get("bootstrap_methods", [])
            require(idx < len(bootstrap), "invalid bootstrap index")
            result.append({"offset": offset, "index": idx,
                           "bootstrap": bootstrap[idx]})
    return result


def method_row(reader, key, body):
    decl = [m for m in reader.methods if (m["name"], m["descriptor"]) == key]
    require(len(decl) == 1, "method declaration not unique: " + str(key))
    return {"name": key[0], "descriptor": key[1], "declaration": decl[0],
            "instruction_count": len(body), "instruction_sha256":
            digest(canonical(rows(body)).encode()), "instructions": rows(body),
            "bootstrap_call_sites": indexed_bootstraps(reader, body)}


def native_projection(jar, javap):
    census = inspect(jar)
    owners = sorted({*census["direct_implementers"], *census["inherited_implementers"], HELPER})
    result = {}
    with zipfile.ZipFile(jar) as z:
        for owner in owners:
            raw = z.read(owner + ".class")
            reader = ClassReader(raw)
            parsed = disasm(jar, javap, owner)
            selected = []
            for key, body in sorted(parsed.items()):
                name = key[0]
                if owner == HELPER:
                    keep = name in HELPER_NAMES or name.startswith("lambda$itemAttributes$")
                else:
                    keep = (name in NATIVE_NAMES or
                            name.startswith("lambda$getDefaultAttributeModifiers$")) and name != "<clinit>"
                if keep:
                    selected.append(method_row(reader, key, body))
            require(any(x["name"] == "<init>" for x in selected) or owner == HELPER,
                    "constructor missing for " + owner)
            result[owner] = {"class_sha256": digest(raw), "parent": reader.parent,
                             "interfaces": reader.interfaces,
                             "fields": [f for f in reader.fields if f["name"] in FIELDS],
                             "methods": selected}
        raw = z.read(REGISTRY + ".class")
        reader = ClassReader(raw)
        methods = disasm(jar, javap, REGISTRY)
        factory_rows = []
        owner_tokens = tuple(o for o in owners if o != HELPER)
        for key, body in sorted(methods.items()):
            if key[0] == "<clinit>":
                continue
            if any(op in ("new", "invokespecial") and any(t in symbol for t in owner_tokens)
                   for op, _, symbol in body.values()):
                factory_rows.append(method_row(reader, key, body))
        # Finite candidate windows in <clinit> tied to exact factory handles.
        names = {f["name"] for f in factory_rows}
        clinit = methods[("<clinit>", "()V")]
        offsets = sorted(clinit)
        connections = []
        for site in indexed_bootstraps(reader, clinit):
            args = site["bootstrap"]["arguments"]
            linked = []
            for arg in args:
                if isinstance(arg, dict):
                    ref = arg.get("reference")
                    if isinstance(ref, list) and len(ref) == 3 and ref[1] == REGISTRY:
                        sig = ref[2]
                        if isinstance(sig, list) and sig[1] in names:
                            linked.append(sig[1])
            if not linked:
                continue
            at = offsets.index(site["offset"])
            window = offsets[max(0, at-5):at+9]
            connections.append({"factory_names": linked, **site,
                                "window": rows({i: clinit[i] for i in window})})
        require(len(factory_rows) <= 80, "unexpected registry factory fanout")
        registry = {"class_sha256": digest(raw), "factories": factory_rows,
                    "clinit_bootstrap_windows": connections,
                    "boundary": "symbolic constructor candidates and local clinit windows; no registry execution"}
    return {"census_class_count": census["class_entries_scanned"],
            "publisher_artifact": census["artifact"], "native_owners": result,
            "registry": registry}


def engine_projection(universal, userdev, javap):
    verify_engine(universal, "universal")
    verify_engine(userdev, "userdev")
    owners = {}
    with zipfile.ZipFile(universal) as z:
        for name in ENGINE_OWNERS:
            raw = z.read(name + ".class")
            reader = ClassReader(raw)
            parsed = disasm(universal, javap, name)
            selected = [method_row(reader, k, b) for k, b in sorted(parsed.items())
                        if k[0] in ENGINE_NAMES or "AttributeModifier" in k[0]]
            owners[name] = {"class_sha256": digest(raw), "methods": selected}
    patch_rows = []
    with zipfile.ZipFile(userdev) as z:
        for name in ("patches/net/minecraft/world/item/Item.java.patch",
                     "patches/net/minecraft/world/item/ItemStack.java.patch"):
            raw = z.read(name)
            matches = [{"line": i+1, "text": line} for i, line in
                       enumerate(raw.decode("utf-8").splitlines()) if PATCH_TOKENS.search(line)]
            patch_rows.append({"entry": name, "sha256": digest(raw),
                               "matching_lines": matches})
    return {"version": "21.1.250", "artifacts": ARTIFACTS,
            "universal": owners, "patches": patch_rows,
            "boundary": "official pinned reference only; not installed execution"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "universal", "userdev", "javap", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    require(a.javap.is_file(), "javap missing")
    require(a.output.suffix == ".json" and not a.output.exists(), "new JSON required")
    report = {"scope": "BOUNDED_CONSTRUCTION_DISCOVERY_NOT_CERTIFIED",
              "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED",
              "mutation": "NO_MUTATION", "provider_universe_closed": False,
              "provider": native_projection(a.jar, a.javap),
              "engine_reference": engine_projection(a.universal, a.userdev, a.javap)}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(canonical(report), encoding="utf-8")
    print("REPORT_SHA256", digest(a.output.read_bytes()))
    for owner, entry in report["provider"]["native_owners"].items():
        print("OWNER", owner, entry["class_sha256"])
        for m in entry["methods"]:
            if m["name"] not in ("<init>", "attributeModifier") and not m["name"].startswith("lambda$itemAttributes$"):
                if m["name"] == "getDefaultAttributeModifiers":
                    print("BOOTSTRAPS", m["name"], json.dumps(m["bootstrap_call_sites"]))
                continue
            print("METHOD", m["name"], m["descriptor"], m["instruction_count"], m["declaration"].get("code_sha256"))
            for i in m["instructions"]:
                print(" ", i["offset"], i["opcode"], i["operand"], i["symbol"])
    for m in report["provider"]["registry"]["factories"]:
        print("FACTORY", m["name"], m["descriptor"], m["instruction_count"])
        for i in m["instructions"]:
            print(" ", i["offset"], i["opcode"], i["operand"], i["symbol"])
    for b in report["provider"]["registry"]["clinit_bootstrap_windows"]:
        print("REGISTRY_WINDOW", json.dumps(b, ensure_ascii=False))
    for owner, entry in report["engine_reference"]["universal"].items():
        print("ENGINE_OWNER", owner, entry["class_sha256"])
        for m in entry["methods"]:
            print("ENGINE_METHOD", m["name"], m["descriptor"], json.dumps(m["instructions"]))
    for patch in report["engine_reference"]["patches"]:
        print("ENGINE_PATCH", patch["entry"], patch["sha256"], json.dumps(patch["matching_lines"]))
    print("END_CONSTRUCTION_DISCOVERY NO_MUTATION")


if __name__ == "__main__":
    main()
