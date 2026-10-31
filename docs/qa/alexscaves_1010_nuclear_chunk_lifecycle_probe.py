#!/usr/bin/env python3
"""Read-only exact 1.0.10 chunk-force/release and NuclearExplosion lifecycle probe.

This reports selected JVM callsites; a method name, constant-pool token or a
boolean at a callsite is not evidence that chunks are eventually released.
No provider runtime is loaded or changed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
from alexscaves_1010_gumball_state_probe import GumballStateProbeError, name_of, strict_pairs
from alexscaves_1010_nuclear_envelope_probe import CLASS, CLASS_SHA

AC_PLATFORM = BASE + "server/misc/ACPlatform.class"
MARKERS = (b"loadChunksAround", b"forceChunk")
INTEREST = (
    "forceChunk", "loadChunksAround", "loadingChunks", "WasLoadingChunks",
    "remove:", "setRemoved:", "onRemovedFromWorld:", "onAddedToWorld:",
    "removeChunk:", "getChunksAffected:", "getViewDistance:",
    "LevelChunk", "unforce", "release", "setForced", "tickets",
)
MAX_CANDIDATES = 80
MAX_CLASS_METHODS = 300
MAX_METHOD_INSNS = 1500
MAX_SITES = 120
MAX_JAR_CLASSES = 3000
WINDOW_RADIUS = 7
MAX_OUTPUT_BYTES = 85000


def method_sha(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True, separators=(",",":"),
                             ensure_ascii=False).encode("utf8")).hexdigest()


def compact(ins):
    return {k: ins[k] for k in ("offset", "opcode", "operand", "symbol")}


def chosen_sites(m):
    ins = m["instructions"]
    if len(ins) > MAX_METHOD_INSNS:
        raise GumballStateProbeError("chunk-lifecycle method instruction budget")
    offsets = [x["offset"] for x in ins]
    if len(offsets) != len(set(offsets)):
        raise GumballStateProbeError("duplicate chunk-lifecycle offset")
    at = [i for i, x in enumerate(ins)
          if any(s.lower() in x["symbol"].lower() for s in INTEREST)]
    if len(at) > MAX_SITES:
        raise GumballStateProbeError("chunk-lifecycle callsite budget")
    return [
        {"at":ins[i]["offset"],"anchor":compact(ins[i]),
         "window":[compact(x) for x in ins[max(0,i-WINDOW_RADIUS):i+WINDOW_RADIUS+1]]}
        for i in at
    ]


def audit(jar, javap_bin):
    if sha_file(jar) != (SHA1,SHA256,SIZE):
        raise GumballStateProbeError("nuclear chunk-lifecycle installed JAR drift")
    with zipfile.ZipFile(jar) as archive:
        allnames = archive.namelist()
        if len(allnames) != len(set(allnames)):
            raise GumballStateProbeError("duplicate publisher JAR entry")
        members=[x for x in allnames if x.startswith(BASE) and x.endswith(".class")]
        if not 100 <= len(members) <= MAX_JAR_CLASSES:
            raise GumballStateProbeError("unexpected class population")
        if hashlib.sha256(archive.read(CLASS)).hexdigest()!=CLASS_SHA:
            raise GumballStateProbeError("NuclearExplosionEntity class SHA drift")
        if AC_PLATFORM not in members:
            raise GumballStateProbeError("ACPlatform not present in exact publisher JAR")
        candidates = sorted(x for x in members if x in (CLASS,AC_PLATFORM)
                            or any(token in archive.read(x) for token in MARKERS))
        if not 2 <= len(candidates) <= MAX_CANDIDATES:
            raise GumballStateProbeError("chunk-lifecycle candidate class budget")
        hashes={x:hashlib.sha256(archive.read(x)).hexdigest() for x in candidates}
    entries=[]
    nuclear_roster=None
    for path in candidates:
        methods=parse_methods(javap(javap_bin,jar,path[:-6].replace("/",".")))
        if len(methods)>MAX_CLASS_METHODS:
            raise GumballStateProbeError("chunk-lifecycle candidate method budget")
        roster=[{"name":name_of(m),"descriptor":m["descriptor"],
                 "instruction_count":len(m["instructions"]),
                 "parsed_method_sha256":method_sha(m)} for m in methods]
        if path==CLASS:
            nuclear_roster=roster
            if len(roster)!=19:
                raise GumballStateProbeError("expected 19 declared nuclear methods")
        matched=[]
        for m in methods:
            sites=chosen_sites(m)
            if not sites and not (path==CLASS and name_of(m) in
                                 {"remove","onRemovedFromWorld","discard",
                                  "addAdditionalSaveData","readAdditionalSaveData"}):
                continue
            matched.append({
                "name":name_of(m),"header":m["header"],
                "descriptor":m["descriptor"],"instruction_count":len(m["instructions"]),
                "parsed_method_sha256":method_sha(m),"sites":sites,
            })
        entries.append({
            "class_path":path,"class_sha256":hashes[path],
            "method_count":len(roster),
            "relevant_methods":matched,
        })
    if nuclear_roster is None:
        raise GumballStateProbeError("NuclearExplosionEntity absent from lifecycle audit")
    return {
        "schema_version":1,
        "scope":"SHA_EXACT_1010_NUCLEAR_CHUNK_LIFECYCLE_AND_PLATFORM_FORCING_REFERENCES",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "nuclear_class_path":CLASS,
        "nuclear_class_sha256":CLASS_SHA,
        "nuclear_declared_method_roster":nuclear_roster,
        "candidate_class_count":len(entries),
        "candidate_classes":entries,
        "limitations":{
            "constant_pool_candidates_are_not_proven_calls":True,
            "static_initializers_excluded_by_parser":True,
            "source_attribution_and_dimension_unload":"NOT_PROVEN",
            "force_chunk_release_at_every_lifecycle_exit":"NOT_PROVEN",
            "ACPlatform_indirection_effective_runtime":"NOT_PROVEN",
            "world_protection_mod_event_cooperation":"NOT_PROVEN",
            "actual_server_runtime_observation":False,
            "world_effect_policy":"NOT_CERTIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "perk_ready":False
        }
    }


def seal(doc):
    candidates=[]
    for c in doc["candidate_classes"]:
        candidates.append({
            "class_path":c["class_path"],"class_sha256":c["class_sha256"],
            "method_count":c["method_count"],
            "relevant_methods":[{
                "name":m["name"],"descriptor":m["descriptor"],
                "instruction_count":m["instruction_count"],
                "parsed_method_sha256":m["parsed_method_sha256"],
                "site_anchors":[s["anchor"] for s in m["sites"]]
            } for m in c["relevant_methods"]]
        })
    return {
        "schema_version":doc["schema_version"],"scope":doc["scope"],
        "artifact":doc["artifact"],"nuclear_class_path":doc["nuclear_class_path"],
        "nuclear_class_sha256":doc["nuclear_class_sha256"],
        "nuclear_declared_method_roster":doc["nuclear_declared_method_roster"],
        "candidate_class_count":doc["candidate_class_count"],
        "candidate_classes":candidates,"limitations":doc["limitations"]
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--snapshot")
    args=p.parse_args()
    doc=audit(Path(args.jar),args.javap)
    manifest=seal(doc)
    if args.snapshot:
        frozen=json.loads(Path(args.snapshot).read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
        if frozen!=manifest:
            raise GumballStateProbeError("nuclear chunk-lifecycle snapshot drift")
    raw=json.dumps(doc,ensure_ascii=False,separators=(",",":"),sort_keys=True)
    if len(raw.encode("utf8"))>MAX_OUTPUT_BYTES:
        raise GumballStateProbeError("nuclear lifecycle evidence size budget")
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(doc,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf8")
    print("NUCLEAR_CHUNK_LIFECYCLE_1010_BEGIN")
    print(json.dumps(manifest,separators=(",",":"),sort_keys=True,ensure_ascii=False))
    print("NUCLEAR_CHUNK_LIFECYCLE_1010_END")
    print("NUCLEAR_CHUNK_LIFECYCLE_WINDOWS_BEGIN")
    print(raw)
    print("NUCLEAR_CHUNK_LIFECYCLE_WINDOWS_END")
    print("NOT_PROVEN: full cleanup, claims, safe mutating bridge, live behavior")


if __name__=="__main__":
    main()
