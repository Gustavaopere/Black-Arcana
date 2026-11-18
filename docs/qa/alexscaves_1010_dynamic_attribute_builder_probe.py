#!/usr/bin/env python3
"""Supplementary bounded audit: event builder, modifier identity and cache field use.

No execution of Minecraft, provider classes, callbacks, event handlers or mods.
The complete earlier construction report has a pinned canonical digest; this
projection additionally documents the internal builder and native state consumers.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import zipfile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_dynamic_attribute_construction import (
    disasm, method_row, ITEM, HELPER,
)
from alexscaves_1010_destroyed_item_engine_reference import (
    verify_artifact as verify_engine,
)

EVENT = "net/neoforged/neoforge/event/ItemAttributeModifierEvent"
BUILDER = EVENT + "$ItemAttributeModifiersBuilder"
GINGER = ITEM + "GingerbreadArmorItem"
PREVIOUS = "4439256ffa12570e5f20ec16d16df2912196b79297dc7757dda3a1d8dd608b77"
FIELDS = ("defaultModifiers:", "defaultAttributes:", "divingArmorAttributes:",
          "gingerbreadDurabilityDependentAttributes:", "acDefense:", "acSlot:")
NATIVE_OWNERS = (
    "DivingArmorItem", "GingerbreadArmorItem", "OrtholanceItem",
    "PrimitiveClubItem", "SharpenedCandyCaneItem", "SpearItem", "TotemOfPossessionItem",
)


def bound_methods(jar, javap, archive, name):
    raw = archive.read(name + ".class")
    reader = ClassReader(raw)
    require(reader.name == name and reader.major == 65, "unexpected owner/version")
    methods = disasm(jar, javap, name)
    return reader, methods, digest(raw)


def project(publisher, universal, javap, earlier):
    report_raw = earlier.read_bytes()
    doc = json.loads(report_raw)
    # Filename in the earlier report is metadata, not artifact identity. Normalize
    # only that known field so a caller can use the exact publisher basename.
    doc["provider"]["publisher_artifact"]["filename"] = "alexscaves-1.0.10.jar"
    require(digest(canonical(doc).encode()) == PREVIOUS,
            "earlier construction semantic report drift")
    verify_artifact(publisher)
    verify_engine(universal, "universal")
    with zipfile.ZipFile(universal) as z:
        names = sorted(p[:-6] for p in z.namelist()
                       if p.endswith(".class") and
                       (p == EVENT+".class" or p.startswith(EVENT+"$")))
        require(BUILDER in names and 2 <= len(names) <= 8,
                "event inner class roster absent/out of scope")
        engine = {}
        for name in names:
            reader, methods, sha = bound_methods(universal, javap, z, name)
            require(len(methods) <= 40, "unexpected event method roster")
            engine[name] = {
                "class_sha256": sha,
                "fields": reader.fields,
                "methods": [method_row(reader, k, v) for k, v in sorted(methods.items())],
            }
    native = {}
    with zipfile.ZipFile(publisher) as z:
        for short in NATIVE_OWNERS:
            name = ITEM + short
            reader, methods, sha = bound_methods(publisher, javap, z, name)
            uses = []
            selected = []
            for key, body in sorted(methods.items()):
                for offset, (op, operand, symbol) in sorted(body.items()):
                    if op in ("getfield", "putfield", "getstatic", "putstatic") and any(
                            t in symbol for t in FIELDS):
                        uses.append({"method": key[0], "descriptor": key[1],
                                     "offset": offset, "opcode": op, "symbol": symbol})
                if key[0] in ("getOrCreateDurabilityAttributes", "getStatsForEnchantmentLevel"):
                    selected.append(method_row(reader, key, body))
            require(len(uses) <= 100, "unexpected state-field fanout")
            native[name] = {"class_sha256": sha, "field_uses": uses,
                            "selected_methods": selected}
    return {
        "schema": "AC_DYNAMIC_ATTRIBUTE_BUILDER_DISCOVERY_V1",
        "construction_report_sha256_normalized_filename": PREVIOUS,
        "scope": "STATIC_REFERENCE_ONLY_NOT_CERTIFIED",
        "publisher_state_consumers": native, "universal_event_classes": engine,
        "mutation": "NO_MUTATION", "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED", "provider_universe_closed": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "universal", "javap", "construction-report", "output"):
        p.add_argument("--"+name, type=Path, required=True)
    a = p.parse_args()
    require(not a.output.exists() and a.output.suffix == ".json", "new JSON required")
    doc = project(a.jar, a.universal, a.javap, a.construction_report)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(canonical(doc), encoding="utf-8")
    print("BUILDER_REPORT_SHA256", digest(a.output.read_bytes()))
    for owner, entry in doc["publisher_state_consumers"].items():
        print("FIELD_USES", owner, json.dumps(entry["field_uses"], ensure_ascii=False))
        for method in entry["selected_methods"]:
            print("NATIVE_HELPER", owner, method["name"], method["descriptor"],
                  method["instruction_count"], method["declaration"].get("code_sha256"))
            print("NATIVE_BOOTSTRAPS", json.dumps(method["bootstrap_call_sites"]))
            for row in method["instructions"]:
                print(" ", row["offset"], row["opcode"], row["operand"], row["symbol"])
    for owner, entry in doc["universal_event_classes"].items():
        print("BUILDER_OWNER", owner, entry["class_sha256"])
        print("BUILDER_FIELDS", json.dumps(entry["fields"]))
        for method in entry["methods"]:
            print("BUILDER_METHOD", method["name"], method["descriptor"],
                  method["instruction_count"], method["declaration"].get("code_sha256"))
            for row in method["instructions"]:
                print(" ", row["offset"], row["opcode"], row["operand"], row["symbol"])
    print("END_BUILDER_DISCOVERY NO_MUTATION")


if __name__ == "__main__":
    main()
