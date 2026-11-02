#!/usr/bin/env python3
"""Read-only, SHA-exact Raygun local-variable access census (1.0.10).

This is not Java dataflow, reachability or a complete CFG. JVM local slots can
be reassigned across paths. No full method body / provider source is exported.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of

CLASS="com/github/alexmodguy/alexscaves/server/item/RaygunItem.class"
CLASS_SHA256="3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c"
DESC="(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V"
METHOD_SHA256="b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5"
SCOPE="EXACT_ALEXSCAVES_1010_RAYGUN_JVM_LOCAL_SLOT_ACCESS_CENSUS"
SLOTS=(7,8,9,18)
PIVOTS={"distance_source_read":38,"distance_result_store":41,
        "xray_enchant_read":44,"xray_boolean_store":58,
        "damage_option_load":1029,"damage_request":1041}
MAX_SNAPSHOT_BYTES=55000
LIMITS={
    "local_slot_values_and_aliases":"NOT_RECONSTRUCTED",
    "branch_reaching_definitions":"NOT_RECONSTRUCTED",
    "control_flow_graph":"NOT_RECONSTRUCTED",
    "exceptional_edges":"NOT_RECONSTRUCTED",
    "xray_effective_penetration":"NOT_CERTIFIED",
    "effective_distance_or_damage":"NOT_CERTIFIED",
    "world_claim_and_pvp":"NOT_VERIFIED",
    "authoritative_server_mutation_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "perk_certification":"NOT_CERTIFIED",
}
VAR_OP=re.compile(r"^(?P<kind>[ialfd](?:load|store))(?:_(?P<implicit>[0-3]))?$")
INDEX=re.compile(r"^\s*(?P<num>\d+)(?:\s|,|$)")
class AuditError(ValueError):pass
def require(condition,msg):
    if not condition:raise AuditError(msg)
def digest_method(m):
    return hashlib.sha256(json.dumps(m,sort_keys=True,ensure_ascii=False,
                separators=(",",":")).encode("utf-8")).hexdigest()
def local_access(ins):
    opcode=ins["opcode"]
    m=VAR_OP.fullmatch(opcode)
    if m:
        if m.group("implicit") is not None:
            slot=int(m.group("implicit"))
        else:
            n=INDEX.match(ins["operand"])
            require(n is not None,"missing variable index in JVM operand")
            slot=int(n.group("num"))
        return (slot, "WRITE" if "store" in m.group("kind") else "READ")
    if opcode=="iinc":
        n=INDEX.match(ins["operand"])
        require(n is not None,"missing iinc variable index")
        return (int(n.group("num")),"READ_WRITE")
    return None
def trimmed(ins):
    return {k:ins[k] for k in ("offset","opcode","operand","symbol")}
def census(method):
    ins=method["instructions"]
    require(400<=len(ins)<=900,"unexpected onUseTick instruction count")
    offsets=[i["offset"] for i in ins]
    require(len(offsets)==len(set(offsets)) and offsets==sorted(offsets),
            "invalid JVM offsets / duplicates")
    pos={row["offset"]:idx for idx,row in enumerate(ins)}
    for kind,at in PIVOTS.items():
        require(at in pos,"missing selected JVM pivot "+kind)
    expected={38:("fload","7"),41:("fstore","8"),
              44:("getstatic",".X_RAY:"),
              58:("istore","9"),1029:("iload","18"),
              1041:("invokestatic","ACCompat.hurt:")}
    for at,(opcode,needle) in expected.items():
        row=ins[pos[at]]
        require(row["opcode"]==opcode and needle in
                (row["operand"]+" "+row["symbol"]),
                "drift of critical Raygun local/target anchor "+str(at))
    groups={str(i):[] for i in SLOTS}
    stores=[]
    for idx,row in enumerate(ins):
        a=local_access(row)
        if a is None or a[0] not in SLOTS:continue
        slot,direction=a
        item={"offset":row["offset"],"opcode":row["opcode"],
              "operand":row["operand"],"access":direction}
        groups[str(slot)].append(item)
        if direction!="READ":
            stores.append((slot,idx))
        require(len(groups[str(slot)])<=75,"unexpected local access budget")
    require(len(stores)<=35,"excessive relevant local store count")
    windows=[]
    for key,at in PIVOTS.items():
        idx=pos[at]
        windows.append({"name":key,"offset":at,
                        "selected_instructions":[trimmed(x) for x in
                                  ins[max(0,idx-5):idx+6]]})
    write_windows=[]
    for slot,idx in stores:
        write_windows.append({
            "slot":slot,"offset":ins[idx]["offset"],
            "selected_instructions":[trimmed(x) for x in
                                     ins[max(0,idx-3):idx+4]]
        })
    observed={str(k):{"access_count":len(groups[str(k)]),
                       "accesses":groups[str(k)]} for k in SLOTS}
    require(all(observed[str(i)]["access_count"] for i in SLOTS),
            "one of the selected locals has no accesses")
    report={
        "method_name":"onUseTick","method_descriptor":DESC,
        "parsed_method_sha256":digest_method(method),
        "instruction_count":len(ins),
        "selected_slots":observed,
        "critical_windows":windows,
        "selected_write_windows":write_windows,
        "interpretation":"SLOT_ACCESS_AND_NEARBY_INSTRUCTIONS_ONLY_NOT_REACHING_DEFINITIONS"
    }
    require(len(json.dumps(report).encode("utf-8"))<MAX_SNAPSHOT_BYTES,
            "bounded access census output too large")
    return report
def analyze(jar,javap_bin):
    jar=Path(jar)
    require(jar.name=="alexscaves-1.0.10.jar",
            "unexpected publisher filename")
    require(sha_file(jar)==(SHA1,SHA256,SIZE),
            "exact physical artifact checksum mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)) and CLASS in names,
                "missing JVM class or duplicate member")
        require(hashlib.sha256(z.read(CLASS)).hexdigest()==CLASS_SHA256,
                "RaygunItem class checksum drift")
    methods=parse_methods(javap(javap_bin,jar,CLASS[:-6].replace("/",".")))
    selected=[m for m in methods if name_of(m)=="onUseTick" and
              m["descriptor"]==DESC]
    require(len(methods)==26 and len(selected)==1,
            "Raygun method population / signature drift")
    require(digest_method(selected[0])==METHOD_SHA256,
            "pinned Raygun method digest drift")
    out={
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "class_path":CLASS,"class_sha256":CLASS_SHA256,
        "declared_method_count":len(methods),
        "local_access_census":census(selected[0]),"limits":LIMITS,
        "interpretation":"OBSERVED_LOCAL_SLOTS_NOT_COMPLETE_DATAFLOW_OR_SAFE_PERK_SURFACE",
    }
    require(len(json.dumps(out).encode("utf-8"))<70000,
            "evidence file budget exceeded")
    return out
def verify_seal(observed,expected):
    require(expected.get("scope")==SCOPE,"wrong seal scope")
    require(expected.get("limits")==LIMITS,"seal safety drift")
    require(observed==expected,"exact Raygun local-access evidence drift")
    return True
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--output",required=True)
    ap.add_argument("--seal")
    args=ap.parse_args()
    try:
        result=analyze(args.jar,args.javap)
        if args.seal:
            verify_seal(result,json.loads(Path(args.seal).read_text(encoding="utf8")))
        out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        counts={s:d["access_count"] for s,d in
                result["local_access_census"]["selected_slots"].items()}
        print("PASS: exact Alex's Caves 1.0.10 Raygun JVM local slot census")
        print("selected_local_access_counts="+json.dumps(counts,sort_keys=True))
        print("NO_MUTATION / NOT_CERTIFIED / no complete CFG or physical QA")
    except (AuditError,ValueError,KeyError,TypeError,OSError) as e:
        ap.exit(1,"FAIL-CLOSED: "+str(e)+"\n")
if __name__=="__main__":main()
