#!/usr/bin/env python3
"""Bounded SHA-exact 1.0.10 numeric and explosion guard contract evidence.

Full selected *instruction records*, not source code. Bytecode is read-only,
not gameplay/mitigation/owner proof. No hooks or mod runtime are modified.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import GumballStateProbeError, name_of, strict_pairs

# Every class/method digest has been published by previous publisher-JAR CI.
SPECS = {
    "server/entity/item/NuclearExplosionEntity.class": {
        "sha256": "d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912",
        "methods": {
            ("calculateDamage", "(FF)F"): ("9cedbccfd5048497dd0dc492232ca72dc8064fad3aa9257c03053f2efef5f547", 26),
        },
    },
    "server/entity/living/NucleeperEntity.class": {
        "sha256": "5c25275ba23c5760ca4c63ddaeff3a0b8ca48a3c4cc7dfa5de999887c7d4beb2",
        "methods": {
            ("explode", "()V"): ("3ab58237a2034998d177e1a2afd78620b3fe799b5506fe2bc03265a8106913f0", 34),
        },
    },
    "server/entity/item/NuclearBombEntity.class": {
        "sha256": "36ccc6ce0993d0ff7884c50857a11f6edb7bace66c15c1b157e8013627b4f3d3",
        "methods": {
            ("explode", "()V"): ("9472b45fd5e0e8164835d1714f540ff44811d28f2715e54de59425043b8ca1ac", 24),
        },
    },
}
MAX_METHODS = 250
MAX_INSNS = 100
OUTPUT_LIMIT = 130000


def verify_method(m, expected):
    if len(m["instructions"]) > MAX_INSNS:
        raise GumballStateProbeError("numeric method instruction budget exceeded")
    offsets = [i["offset"] for i in m["instructions"]]
    if len(set(offsets)) != len(offsets):
        raise GumballStateProbeError("duplicate numeric instruction offsets")
    digest = hashlib.sha256(json.dumps(
        m, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf8")).hexdigest()
    expected_digest, expected_length = expected
    if (digest, len(offsets)) != (expected_digest, expected_length):
        raise GumballStateProbeError("pinned prior numeric method hash/length drift: " + m["header"])
    return {
        "name": name_of(m), "header": m["header"], "descriptor": m["descriptor"],
        "sha256": digest, "instruction_count": len(offsets),
        "instructions": m["instructions"],
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise GumballStateProbeError("publisher 1.0.10 JAR SHA1/SHA256/size drift")
    with zipfile.ZipFile(jar) as arc:
        members = arc.namelist()
        if len(members) != len(set(members)):
            raise GumballStateProbeError("duplicate ZIP member")
        records = []
        for relative, spec in SPECS.items():
            cls = BASE + relative
            data = arc.read(cls)
            if hashlib.sha256(data).hexdigest() != spec["sha256"]:
                raise GumballStateProbeError("pinned nuclear class SHA drift: " + cls)
            methods = parse_methods(javap(javap_bin, jar, cls[:-6].replace("/", ".")))
            if len(methods) > MAX_METHODS:
                raise GumballStateProbeError("class method budget exceeded")
            found = {}
            for method in methods:
                key = (name_of(method), method["descriptor"])
                if key in spec["methods"]:
                    if key in found:
                        raise GumballStateProbeError("duplicate selected numeric method: " + str(key))
                    found[key] = verify_method(method, spec["methods"][key])
            if set(found) != set(spec["methods"]):
                raise GumballStateProbeError("selected numeric method absent or different")
            records.append({
                "class_path": cls, "class_sha256": spec["sha256"],
                "methods": [found[key] for key in spec["methods"]],
            })
    by_path = {x["class_path"]: x for x in records}
    calc = by_path[BASE+"server/entity/item/NuclearExplosionEntity.class"]["methods"][0]["instructions"]
    nucl = by_path[BASE+"server/entity/living/NucleeperEntity.class"]["methods"][0]["instructions"]
    bomb = by_path[BASE+"server/entity/item/NuclearBombEntity.class"]["methods"][0]["instructions"]
    if not any("getSize:()F" in i["symbol"] for i in calc):
        raise GumballStateProbeError("size operand absent in nuclear damage helper")
    if not any("setSize:(F)V" in i["symbol"] for i in nucl):
        raise GumballStateProbeError("Nucleeper size producer absent")
    if not any("RULE_MOBGRIEFING" in i["symbol"] for i in nucl):
        raise GumballStateProbeError("Nucleeper mobgriefing guard absent")
    if not any("DoubleValue.get:()" in i["symbol"] for i in bomb):
        raise GumballStateProbeError("nuclear bomb config value absent")
    output = {
        "schema_version": 1,
        "scope": "SHA_EXACT_1010_NUCLEAR_CALCULATE_DAMAGE_AND_TWO_EMITTERS_FULL_SELECTED_BYTECODE",
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "parent_snapshots": [
            "EXACT-NUCLEAR-ENVELOPE-1.0.10.json",
            "EXACT-NUCLEAR-PRODUCERS-1.0.10.json",
        ],
        "classes": records,
        "limits": {
            "compiled_selected_methods_only": True,
            "float_math_semantics": "JVM_BYTECODE_EXACT_NOT_A_RUNTIME_DAMAGE_PREDICTION",
            "nonselected_methods_and_initializers": "NOT_CLOSED",
            "configuration_effective_values": "NOT_VERIFIED",
            "damage_after_mitigation": "NOT_VERIFIED",
            "world_protection_and_pvp": "NOT_VERIFIED",
            "owner_and_mastery": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "complete_perk_ready": False,
            "provider_universe_closed": False,
        },
    }
    if len(json.dumps(output).encode("utf8")) > OUTPUT_LIMIT:
        raise GumballStateProbeError("numeric snapshot size budget")
    return output


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar", required=True)
    p.add_argument("--javap", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--snapshot")
    args=p.parse_args()
    doc=audit(Path(args.jar),args.javap)
    if args.snapshot:
        expected=json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                            object_pairs_hook=strict_pairs)
        if doc != expected:
            raise GumballStateProbeError("numeric publisher-JAR snapshot drift")
    dest=Path(args.output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(doc,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("NUCLEAR_NUMERIC_1010_BEGIN")
    print(json.dumps(doc,sort_keys=True,separators=(",",":"),ensure_ascii=False))
    print("NUCLEAR_NUMERIC_1010_END")
    print("NO_RUNTIME_OR_MUTATING_HOOK_CERTIFICATION")


if __name__=="__main__":
    main()
