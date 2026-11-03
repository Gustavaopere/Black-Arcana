#!/usr/bin/env python3
"""Read-only, SHA-exact 1.0.10 Arrow Inducting identity and consumer probe.

Emits only bounded JVM references and small windows for interoperability.
This is not a complete CFG, gameplay QA, a safe mutation hook, or source reuse.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

SCOPE = "EXACT_ALEXSCAVES_1010_ARROW_INDUCTING_SELECTED_CONSUMERS"
RESOURCE = "data/alexscaves/enchantment/arrow_inducting.json"
CONSUMER = BASE + "server/event/CommonEvents.class"
PROJECTILE = BASE + "server/entity/item/SeekingArrowEntity.class"
GUARD = "ACEnchantmentRegistry.ARROW_INDUCTING:"
MAX_METHOD = 1500
MAX_REFERENCES = 100
MAX_WINDOWS = 14

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def clip(row):
    return {k: row[k] for k in ("offset", "opcode", "operand", "symbol")}

def choose(methods, classname):
    if classname == CONSUMER:
        selected = [m for m in methods
                    if any(GUARD in x["symbol"] for x in m["instructions"])]
        require(len(selected) == 1, "enchantment consumer missing/ambiguous")
    else:
        selected = [m for m in methods if name_of(m) == "tick" and m["descriptor"] == "()V"]
        require(len(selected) == 1, "seeking-arrow tick missing/ambiguous")
    m = selected[0]
    require(1 <= len(m["instructions"]) <= MAX_METHOD, "method size out of bounds")
    return m

def summarize(m, classname):
    ins = m["instructions"]
    offsets = [x["offset"] for x in ins]
    require(offsets == sorted(set(offsets)), "duplicate/unsorted offsets")
    symbols = [clip(x) for x in ins
               if x["opcode"].startswith("invoke")
               or x["opcode"] in {"getstatic", "putstatic", "getfield", "putfield"}]
    require(len(symbols) <= MAX_REFERENCES, "too many JVM references")
    if classname == CONSUMER:
        markers = ("ARROW_INDUCTING:", "ACCompat.enchantLevel:",
                   "SeekingArrowEntity", "addFreshEntity:", ".discard:")
        anchors = [i for i,x in enumerate(ins) if any(token in x["symbol"] for token in markers)]
        require(any(GUARD in x["symbol"] for x in ins), "guard missing")
        require(any("SeekingArrowEntity" in x["symbol"] for x in ins), "arrow creation reference missing")
    else:
        markers = ("getArcTowardsID:", "setArcTowardsID:", "getEntities:",
                   "setDeltaMovement:", "getOwner:", "isAlliedTo:", "getEntity:",
                   "Math.min:", "AABB.inflate:", "Vec3.scale:", "getBbWidth:")
        anchors = [i for i,x in enumerate(ins) if any(token in x["symbol"] for token in markers)]
        require(any("setArcTowardsID:" in x["symbol"] for x in ins), "seeking-arrow target state missing")
    require(1 <= len(anchors) <= MAX_WINDOWS, "unexpected selected anchor population")
    windows = [{"pivot": ins[i]["offset"], "instructions": [clip(x) for x in
                ins[max(0,i-4):min(len(ins),i+7)]]} for i in anchors]
    return {
        "header": m["header"],
        "descriptor": m["descriptor"],
        "parsed_method_sha256": digest_method(m),
        "instruction_count": len(ins),
        "references": symbols,
        "windows": windows,
        "limits": "BOUNDED_REFERENCES_AND_LOCAL_WINDOWS_ONLY",
    }

def check_resource(raw):
    require(len(raw) <= 20000, "enchantment resource oversized")
    j = json.loads(raw)
    require(isinstance(j,dict), "enchantment must be JSON object")
    require("description" in j and "supported_items" in j and
            "max_level" in j and "weight" in j,
            "required enchantment resource fields absent")
    return j

def audit(jar, javap_bin):
    require(sha_file(jar) == (SHA1, SHA256, SIZE), "wrong exact publisher JAR")
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate JAR paths")
        for name in (RESOURCE,CONSUMER,PROJECTILE):
            require(name in names, "missing JAR entry: "+name)
        raw = z.read(RESOURCE)
        data = check_resource(raw)
        classes = []
        for classname in (CONSUMER,PROJECTILE):
            bytecode = z.read(classname)
            methods = parse_methods(javap(javap_bin, jar, classname[:-6].replace("/", ".")))
            m = choose(methods, classname)
            classes.append({
                "path": classname,
                "class_sha256": hashlib.sha256(bytecode).hexdigest(),
                "parsed_method_count": len(methods),
                "selected_method": summarize(m, classname),
            })
    return {
        "schema_version": 1,
        "scope": SCOPE,
        "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
        "enchantment": {"id":"alexscaves:arrow_inducting",
                        "resource_path": RESOURCE,
                        "resource_sha256": hashlib.sha256(raw).hexdigest(),
                        "json": data},
        "classes": classes,
        "limits": {
            "source_111_parameter_authority": False,
            "full_method_cfg": "NOT_RECONSTRUCTED",
            "server_replay_and_pvp": "NOT_VERIFIED",
            "projectile_owner_and_damage_settlement": "NOT_CERTIFIED",
            "datapack_active_enchantment": "NOT_VERIFIED",
            "mutating_hook": "NOT_VERIFIED",
            "physical_qa": "NOT_TESTED",
            "mutation": "NO_MUTATION",
            "perk_certification": "NOT_CERTIFIED",
        },
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", required=True, type=Path)
    ap.add_argument("--javap", default="javap")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--seal", type=Path)
    a = ap.parse_args()
    result = audit(a.jar,a.javap)
    if a.seal:
        actual = json.loads(a.seal.read_text(encoding="utf-8"))
        require(result == actual, "SHA-exact Arrow Inducting seal drift")
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf8")
    print(json.dumps(result, ensure_ascii=False, separators=(",",":")))

if __name__ == "__main__":
    main()
