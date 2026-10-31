#!/usr/bin/env python3
"""Read-only SHA-exact 1.0.10 nuclear tick target/world boundary audit.

Bounded JVM evidence for interoperability. Not a source-code reproduction,
runtime authority test, protected-world guarantee, or safe mutating hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import GumballStateProbeError, name_of, strict_pairs
from alexscaves_1010_nuclear_envelope_probe import CLASS, CLASS_SHA

TICK_SHA = "64f9a412c81a25525edf5b9576d56cec8354f6963ef718a44e6179347fcd8a25"
TICK_COUNT = 348
HIGHLIGHTS = (1, 80, 83, 167, 225, 288, 318, 421, 456, 466,
              570, 586, 605, 618, 623, 643, 659)
HELPER_NAMES = {"isDestroyable", "isNoGriefing", "getSize", "tick",
                "getChunksAffected", "removeChunk", "loadChunksAround"}
MAX_CLASS_METHODS = 120
MAX_HELPER_INSNS = 1250
MAX_TICK_INSNS = 450
MAX_REFERENCES = 250
MAX_BRANCHES = 250
MAX_CONSTANTS = 250
MAX_WINDOWS = 25
WINDOW_HALF = 11
MAX_BYTES = 225000


def digest(method):
    return hashlib.sha256(json.dumps(
        method, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf8")).hexdigest()


def compact(ins):
    return {field: ins[field] for field in ("offset", "opcode", "operand", "symbol")}


def window(method, offset):
    ins = method["instructions"]
    indexes = [i for i, x in enumerate(ins) if x["offset"] == offset]
    if len(indexes) != 1:
        raise GumballStateProbeError("missing/duplicate target world offset " + str(offset))
    index = indexes[0]
    return {"at": offset, "ins": [compact(x) for x in
                                  ins[max(0, index-WINDOW_HALF):index+WINDOW_HALF+1]]}


def scan_method(method):
    name = name_of(method)
    ins = method["instructions"]
    budget = MAX_TICK_INSNS if name == "tick" else MAX_HELPER_INSNS
    if len(ins) > budget or not ins:
        raise GumballStateProbeError("target/world selected-method budget exceeded")
    offsets = [x["offset"] for x in ins]
    if len(offsets) != len(set(offsets)):
        raise GumballStateProbeError("duplicate target/world instruction offsets")
    references = [compact(x) for x in ins if x["symbol"]]
    branches = [compact(x) for x in ins if
                x["opcode"].startswith(("if", "goto", "tableswitch", "lookupswitch"))]
    constants = [compact(x) for x in ins if
                 x["opcode"].startswith(("ldc", "iconst", "fconst", "dconst", "lconst",
                                          "bipush", "sipush"))]
    if (len(references) > MAX_REFERENCES or len(branches) > MAX_BRANCHES
            or len(constants) > MAX_CONSTANTS):
        raise GumballStateProbeError("target/world symbolic budget exceeded")
    return {
        "name": name, "descriptor": method["descriptor"],
        "header": method["header"],
        "instruction_count": len(ins), "parsed_method_sha256": digest(method),
        "references": references, "branches": branches, "constants": constants,
        "windows": [window(method, x) for x in HIGHLIGHTS] if name == "tick" else [],
    }


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1, SHA256, SIZE):
        raise GumballStateProbeError("publisher nuclear target/world artifact drift")
    with zipfile.ZipFile(jar) as archive:
        names=archive.namelist()
        if len(names) != len(set(names)):
            raise GumballStateProbeError("duplicate publisher ZIP member")
        if hashlib.sha256(archive.read(CLASS)).hexdigest() != CLASS_SHA:
            raise GumballStateProbeError("nuclear target/world class SHA drift")
    declared = parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    if len(declared) > MAX_CLASS_METHODS:
        raise GumballStateProbeError("nuclear target/world class population drift")
    selected = {}
    raw = {}
    for m in declared:
        name = name_of(m)
        if name not in HELPER_NAMES:
            continue
        key = name + ":" + m["descriptor"]
        if key in selected:
            raise GumballStateProbeError("ambiguous target/world helper")
        raw[key] = m
        selected[key] = scan_method(m)
    tick_key = "tick:()V"
    if tick_key not in selected or selected[tick_key]["instruction_count"] != TICK_COUNT:
        raise GumballStateProbeError("selected nuclear tick not found or count drift")
    if selected[tick_key]["parsed_method_sha256"] != TICK_SHA:
        raise GumballStateProbeError("nuclear tick SHA-exact digest drift")
    if not any(x.startswith("isDestroyable:") for x in selected):
        raise GumballStateProbeError("isDestroyable helper missing")
    tick = selected[tick_key]
    for at, substring in [
        (80,"getBlockState:"), (83,"isDestroyable:"), (167,"remove:"),
        (421,"getEntitiesOfClass:"), (466,"calculateDamage:"),
        (623,"hurt:"), (643,"setDeltaMovement:")
    ]:
        found = [x for x in tick["references"] if
                 x["offset"] == at and substring in x["symbol"]]
        if len(found) != 1:
            raise GumballStateProbeError("nuclear target/world critical symbolic anchor drift "+str(at))
    if len(tick["windows"]) != len(HIGHLIGHTS) or len(HIGHLIGHTS) > MAX_WINDOWS:
        raise GumballStateProbeError("nuclear target/world snapshot window bound")
    data={
        "schema_version":1,
        "scope":"SHA_EXACT_1010_NUCLEAR_TARGET_WORLD_SELECTED_BYTECODE_BOUNDARIES",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "class_path":CLASS,"class_sha256":CLASS_SHA,
        "declared_method_count":len(declared),
        "selected_methods":selected,
        "limitations":{
            "native_runtime_observed":False,
            "full_control_flow_and_exception_paths":"NOT_RECONSTRUCTED",
            "chunk_loading_and_world_protection":"NOT_VERIFIED",
            "damage_source_owner_pvp":"NOT_VERIFIED",
            "range_cast_or_spell_targeting":"NOT_VERIFIED",
            "safe_mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "complete_perk_ready":False,
            "provider_universe_closed":False
        }
    }
    if len(json.dumps(data).encode("utf8")) > MAX_BYTES:
        raise GumballStateProbeError("target/world snapshot byte budget exceeded")
    return data, raw


def seal(document):
    selected={}
    for key, m in document["selected_methods"].items():
        selected[key]={
            "instruction_count":m["instruction_count"],
            "parsed_method_sha256":m["parsed_method_sha256"],
            "references":m["references"],
            "branches":m["branches"],
            "constants":m["constants"],
            "windows":[{"at":x["at"],"ins":[v for v in x["ins"] if
                        v["offset"] == x["at"]]} for x in m["windows"]]
        }
    return {
        "schema_version":document["schema_version"],
        "scope":document["scope"],
        "artifact":document["artifact"],
        "class_path":document["class_path"],
        "class_sha256":document["class_sha256"],
        "declared_method_count":document["declared_method_count"],
        "selected_methods":selected,
        "limitations":document["limitations"]
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--snapshot")
    args=p.parse_args()
    doc, methods=audit(Path(args.jar),args.javap)
    tick=methods['tick:()V']
    selected=seal(doc)
    if args.snapshot:
        frozen=json.loads(Path(args.snapshot).read_text(encoding="utf8"),
                          object_pairs_hook=strict_pairs)
        if frozen != selected:
            raise GumballStateProbeError("target/world SHA-exact snapshot drift")
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(doc,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf8")
    print("NUCLEAR_TARGET_WORLD_1010_BEGIN")
    print(json.dumps(selected,separators=(",",":"),sort_keys=True,ensure_ascii=False))
    print("NUCLEAR_TARGET_WORLD_1010_END")
    # For human audit in CI logs only, not a checked-in source dump.
    print("NUCLEAR_TARGET_WORLD_TICK_BEGIN")
    print(json.dumps(tick["instructions"],separators=(",",":"),ensure_ascii=False))
    print("NUCLEAR_TARGET_WORLD_TICK_END")
    print("NUCLEAR_TARGET_WORLD_HELPERS_BEGIN")
    print(json.dumps({key: val["instructions"] for key, val in methods.items()
                      if key != "tick:()V"}, separators=(",",":"), ensure_ascii=False))
    print("NUCLEAR_TARGET_WORLD_HELPERS_END")
    print("NO_RUNTIME_MUTATION_OR_PHYSICAL_QA")


if __name__=="__main__":
    main()
