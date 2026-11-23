#!/usr/bin/env python3
"""Read-only exact Galena ACCompat combat/movement helper discovery, 1.0.10.

Selects only direct typed calls from the already SHA-sealed Galena item and
MagneticWeaponEntity report. No source decompilation, copied provider code,
integration hooks, executable perks, world effects or physical QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import (
    ClassReader, SHA1, SHA256, SIZE, canonical, digest, require, verify_artifact,
)
from alexscaves_1010_enchantable_item_probe import disassemble, summarize

OWNER = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
ITEM = "com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem"
ENTITY = "com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity"
OWNER_SHA256 = "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b"
CALLER_SHA256 = "c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9"
CALLER_BYTES = 1780492
METHOD_NAMES = frozenset({
    "addCooldown", "attackDamageBonus", "createEntity", "damageBonus",
    "enchantLevel", "enchantLevelOn", "hurt", "hurtAndBreakUsedHand",
    "knockback", "miningEfficiencyBonus", "postAttackEffects",
    "submergedMiningFactor", "useConsume", "useFail",
})
PRIOR_AUDITED = frozenset({
    "saveStack", "loadStack", "putUUID", "getUUID", "hasUUID",
    "getCompound", "getOrCreateTag", "getTag", "setTag", "getInt",
    "spawnAtLocation",
})


def load_unique(path: Path, limit: int) -> tuple[dict, bytes]:
    raw = path.read_bytes()
    require(0 < len(raw) <= limit, "report size exceeds bound")
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, "duplicate JSON key: " + k)
            result[k] = v
        return result
    return json.loads(raw, object_pairs_hook=unique), raw


def collect_caller_sites(report_path: Path) -> tuple[list[dict], list[tuple[str, str]]]:
    caller, raw = load_unique(report_path, 2_000_000)
    require(len(raw) == CALLER_BYTES and digest(raw) == CALLER_SHA256,
            "caller evidence exact hash/byte count drift")
    require(caller["scope"] == "GALENA_GAUNTLET_FULL_CLASS_DISCOVERY_NOT_CERTIFIED",
            "caller scope drift")
    require(caller["artifact"]["sha256"] == SHA256 and
            caller["artifact"]["size_bytes"] == SIZE,
            "caller publisher identity mismatch")
    require(caller["mutation"] == "NO_MUTATION" and
            caller["physical_qa"] == "NOT_TESTED" and
            caller["mutating_hook"] == "NOT_VERIFIED",
            "unsafe caller status")
    prefix = "Method " + OWNER + "."
    sites = []
    unexpected = set()
    for group, name in (("native", ITEM), ("entity_native", ENTITY)):
        native = caller[group]["targets"]
        require(set(native) == {name}, "Galena owner census changed")
        for m in native[name]["methods"]:
            d = m["declaration"]
            for ins in m["instructions"]:
                if ins["opcode"] != "invokestatic" or not ins["symbol"].startswith(prefix):
                    continue
                method, sep, descriptor = ins["symbol"][len(prefix):].partition(":")
                require(sep and descriptor.startswith("("), "invalid typed descriptor")
                if method not in METHOD_NAMES:
                    if method not in PRIOR_AUDITED:
                        unexpected.add(method)
                    continue
                sites.append({
                    "caller_owner": name, "caller_name": d["name"],
                    "caller_descriptor": d["descriptor"], "offset": ins["offset"],
                    "opcode": ins["opcode"], "callee_name": method,
                    "callee_descriptor": descriptor,
                })
    require(not unexpected, "unassigned direct helper owners: " + repr(sorted(unexpected)))
    require({x["callee_name"] for x in sites} == METHOD_NAMES,
            "selected helper set does not cover all typed source names")
    pairs = sorted({(x["callee_name"], x["callee_descriptor"]) for x in sites})
    require(len(pairs) == len(METHOD_NAMES),
            "unexpected overload/ambiguous direct Galena helper signature")
    require(14 <= len(sites) <= 100, "unexpected caller-site cardinality")
    return sorted(sites, key=lambda x: (
        x["caller_owner"], x["caller_name"], x["offset"])), pairs


def probe(jar: Path, caller_report: Path, javap: str, output: Path) -> None:
    verify_artifact(jar)
    require(not output.exists() and output.suffix == ".json",
            "write-once JSON report required")
    sites, pairs = collect_caller_sites(caller_report)
    with ZipFile(jar) as archive:
        names = archive.namelist()
        require(len(set(names)) == len(names), "duplicate JAR members")
        require(sum(x.endswith(".class") for x in names) == 1555,
                "publisher class count drift")
        raw = archive.read(OWNER + ".class")
    reader = ClassReader(raw)
    require(digest(raw) == OWNER_SHA256 and reader.name == OWNER and
            reader.major == 65 and len(reader.methods) == 200 and
            len(reader.fields) == 3,
            "ACCompat publisher class hash/ABI drift")
    declared = {(m["name"], m["descriptor"]): m for m in reader.methods}
    require(len(declared) == 200, "duplicate method descriptors")
    require(all(x in declared and "code_sha256" in declared[x] for x in pairs),
            "selected method body missing in publisher")
    bytecode = disassemble(jar, javap, OWNER)
    require(all(x in bytecode for x in pairs), "javap lacks selected body")
    methods = [summarize(reader, k, bytecode[k]) for k in pairs]
    require(len(methods) == len(METHOD_NAMES), "selected method cardinality drift")
    report = {
        "schema_version": 1,
        "scope": "GALENA_ACCOMPAT_COMBAT_BRIDGES_DISCOVERY_NOT_CERTIFIED",
        "artifact": {
            "filename": "alexscaves-1.0.10-neoforge+1.21.1.jar",
            "version": "1.0.10", "sha1": SHA1,
            "sha256": SHA256, "size_bytes": SIZE,
            "installed_dump_parity": "NOT_VERIFIED",
        },
        "class": {"owner": OWNER, "sha256": digest(raw), "major": reader.major,
                  "declared_methods": len(reader.methods), "fields": len(reader.fields),
                  "selected_methods": methods},
        "caller_evidence": {"source_sha256": CALLER_SHA256,
                            "source_bytes": CALLER_BYTES,
                            "typed_callsites": sites},
        "limits": {
            "delegated_engine_damage_acceptance": "NOT_VERIFIED",
            "delegated_armor_and_attributes": "NOT_VERIFIED",
            "delegated_neoforge_event_and_mining": "NOT_VERIFIED",
            "world_and_inventory_safety": "NOT_VERIFIED",
            "installed_runtime_transformations": "NOT_VERIFIED",
            "other_consumers_complete": False,
        },
        "static_contract": "NOT_CERTIFIED",
        "mutating_hook": "NOT_VERIFIED", "perk_certification": "NOT_CERTIFIED",
        "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
        "provider_universe_closed": False, "semantic_magic_roots_delta": 0,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(report), encoding="utf8")
    print("REPORT_SHA256", digest(output.read_bytes()), "REPORT_BYTES", output.stat().st_size)
    print("PUBLISHER", SHA256, SIZE, "CLASS", digest(raw))
    print("SELECTED", len(methods), "SITES", len(sites))
    for m in methods:
        d = m["declaration"]
        print("METHOD", d["name"], d["descriptor"],
              "INSTRUCTIONS", m["instruction_count"],
              "CODE_SHA", d["code_sha256"],
              "INSTRUCTION_SHA", m["instruction_sha256"])
        # Bounded JVM summary. Full report is in a short-lived Actions artifact.
        for ins in m["instructions"]:
            if (ins["opcode"].startswith(("invoke", "if", "get", "put"))
                    or ins["opcode"] in {
                        "ldc", "ldc_w", "ldc2_w", "bipush", "sipush", "new",
                        "instanceof", "checkcast", "areturn", "ireturn", "freturn",
                        "dreturn", "athrow", "iadd", "fadd", "dadd", "imul", "fmul",
                        "dsub", "fdiv", "dmul", "tableswitch", "lookupswitch",
                    }):
                print("JVM", d["name"], ins["offset"], ins["opcode"],
                      ins["operand"][:40], ins["symbol"][:165])
    for x in sites:
        print("CALL", x["caller_owner"].split("/")[-1], x["caller_name"],
              x["offset"], x["callee_name"], x["callee_descriptor"])
    print("DISCOVERY_ONLY NO_MUTATION NOT_CERTIFIED NOT_TESTED")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jar", required=True, type=Path)
    ap.add_argument("--caller-report", required=True, type=Path)
    ap.add_argument("--javap", default="javap")
    ap.add_argument("--output", required=True, type=Path)
    a = ap.parse_args()
    probe(a.jar, a.caller_report, a.javap, a.output)
