#!/usr/bin/env python3
"""Exact Alex's Caves 1.0.10 Raygun radiation guard ABI probe.

Read-only clean-room static contracts: individual JVM guard branches and the
default publisher datapack tag. Not an execution trace, game test, full CFG,
server-ownership proof, or authority for mutating another provider's effects.
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
from alexscaves_1010_raygun_local_flow_probe import (
    CLASS, CLASS_SHA256, DESC, METHOD_SHA256,
    AuditError, digest_method, require,
)

SCOPE="EXACT_ALEXSCAVES_1010_RAYGUN_RADIATION_GUARD_AND_DEFAULT_TAG_ABI"
TAG="data/alexscaves/tags/entity_type/resists_radiation.json"
PINS={
    1041:("invokestatic","ACCompat.hurt:"),
    1044:("ifeq","1051"),
    1088:("ifne","1157"),
    1111:("sipush","800"),
    1114:("iload","23"),
    1116:("invokespecial","MobEffectInstance."),
    1119:("invokevirtual","LivingEntity.addEffect:"),
    1122:("ifeq","1157"),
    1151:("invokespecial","UpdateEffectVisualityEntityMessage."),
    1154:("invokestatic","AlexsCaves.sendMSGToAll:"),
    1157:("goto","953"),
}
MARKERS={
    "resistance_tag":"ACTagRegistry.RESISTS_RADIATION:",
    "irradiated_effect":"ACEffectRegistry.IRRADIATED:",
    "resistance_test":"Holder$Reference.is:",
    "native_hurt_request":"ACCompat.hurt:",
    "status_request":"LivingEntity.addEffect:",
    "visual_notification":"AlexsCaves.sendMSGToAll:",
}
DIRECT_BRANCHES=(1044,1088,1122,1157)
JVM_TARGET=re.compile(r"^\s*(\d+)(?:\s|$)")
LIMITS={
    "authority_of_tag":"PUBLISHER_DEFAULT_DATAPACK_ONLY_REPLACEABLE",
    "effective_world_datapack":"NOT_VERIFIED",
    "radiation_resistance_application":"STATIC_BRANCH_ONLY",
    "hit_acceptance_and_iteration":"NOT_CERTIFIED",
    "actual_effect_accepted":"NOT_CERTIFIED",
    "visual_packet_delivery":"NOT_OBSERVED",
    "server_authority_and_replay":"NOT_VERIFIED",
    "claims_and_pvp":"NOT_VERIFIED",
    "full_cfg_exception_edges":"NOT_RECONSTRUCTED",
    "safe_mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED",
    "mutation":"NO_MUTATION",
    "perk_certification":"NOT_CERTIFIED",
}

def slim(i):
    return {key:i[key] for key in ("offset","opcode","operand","symbol")}

def probe_method(m):
    ins=m["instructions"]
    require(450<=len(ins)<=900,"unexpected method population")
    offsets=[x["offset"] for x in ins]
    require(offsets==sorted(set(offsets)),"duplicate or unordered JVM offsets")
    positions={x["offset"]:n for n,x in enumerate(ins)}
    for offset,(opcode,needle) in PINS.items():
        require(offset in positions,"missing required pinned offset "+str(offset))
        x=ins[positions[offset]]
        require(x["opcode"]==opcode and needle in x["operand"]+" "+x["symbol"],
                "pinned radiation ABI drift @"+str(offset))
    markers=[]
    for label,signature in MARKERS.items():
        selected=[x for x in ins if signature in x["symbol"]
                  and 1025<=x["offset"]<1160]
        require(len(selected)==1,"ambiguous or missing radiation marker "+label)
        i=positions[selected[0]["offset"]]
        markers.append({
            "name":label,"offset":selected[0]["offset"],
            "opcode":selected[0]["opcode"],"symbol":selected[0]["symbol"],
            "nearby":[slim(x) for x in ins[max(0,i-5):i+6]]
        })
    marker_offsets={x["name"]:x["offset"] for x in markers}
    require(marker_offsets["resistance_tag"]<
            marker_offsets["resistance_test"]<1088,
            "tag resistance predicate not ordered before guard")
    require(1088<marker_offsets["irradiated_effect"]<1116,
            "effect registry reference outside guarded request")
    require(marker_offsets["status_request"]==1119 and
            marker_offsets["visual_notification"]==1154,
            "status / visual request callsite drift")
    branches=[]
    for offset in DIRECT_BRANCHES:
        inst=ins[positions[offset]]
        m=JVM_TARGET.match(inst["operand"])
        require(m is not None,"unreadable JVM branch target @"+str(offset))
        target=int(m.group(1))
        require(target in positions,"branch destination not an instruction")
        idx=positions[offset]
        require(idx+1<len(ins),"missing sequential instruction after branch")
        branches.append({
            "offset":offset,"opcode":inst["opcode"],
            "taken_target":target,"sequential_next":ins[idx+1]["offset"],
            "interpretation":"DIRECT_COMPILED_EDGE_ONLY_NOT_GLOBAL_REACHABILITY",
        })
    require(branches[1]["taken_target"]==1157 and
            branches[2]["taken_target"]==1157,
            "radiation tag or effect result no longer gates visual branch")
    require(branches[0]["offset"]<branches[1]["offset"] and
            branches[1]["offset"]<branches[2]["offset"]<
            branches[3]["offset"],"unexpected guard ordering")
    result={
        "method":"onUseTick","descriptor":DESC,
        "parsed_method_sha256":digest_method(m),
        "instruction_count":len(ins),
        "symbols_with_local_context":markers,
        "selected_branch_edges":branches,
        "interpretation":"STATIC_TAG_AND_ADD_EFFECT_RESULT_GUARDS_NOT_RUNTIME_CERTIFICATION",
    }
    require(len(json.dumps(result,ensure_ascii=False).encode())<17000,
            "guard evidence window budget exceeded")
    return result

def inspect_default_tag(raw):
    require(len(raw)<7000,"unbounded tag JSON resource")
    data=json.loads(raw.decode("utf8"))
    require(isinstance(data,dict) and isinstance(data.get("values"),list),
            "unexpected publisher tag JSON")
    vals=data["values"]
    require(1<=len(vals)<=50 and len(set(map(str,vals)))==len(vals),
            "unexpected tag values or duplication")
    require(all(isinstance(v,str) and 2<=len(v)<=160 for v in vals),
            "unexpected required tag value type")
    replace=data.get("replace",False)
    require(isinstance(replace,bool),"invalid datapack tag replace value")
    return {
        "path":TAG,"sha256":hashlib.sha256(raw).hexdigest(),
        "replace_declared":("replace" in data),
        "replace_effective_default":replace,
        "declared_values":vals,
        "value_count":len(vals),
        "interpretation":"PUBLISHER_DEFAULT_NOT_EFFECTIVE_RUNTIME_REGISTRY",
    }

def analyze(jar,javap_bin):
    jar=Path(jar)
    require(jar.name=="alexscaves-1.0.10.jar","unexpected publisher JAR filename")
    require(sha_file(jar)==(SHA1,SHA256,SIZE),
            "wrong physical publisher JAR fingerprint")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)) and
                CLASS in names and TAG in names,
                "missing pinned JAR resources / duplicate entries")
        require(hashlib.sha256(z.read(CLASS)).hexdigest()==CLASS_SHA256,
                "RaygunItem compiled class fingerprint drift")
        tag=inspect_default_tag(z.read(TAG))
    methods=parse_methods(javap(javap_bin,jar,CLASS[:-6].replace("/",".")))
    found=[m for m in methods if name_of(m)=="onUseTick" and
           m["descriptor"]==DESC]
    require(len(methods)==26 and len(found)==1,
            "Raygun method roster/descriptor drift")
    require(digest_method(found[0])==METHOD_SHA256,
            "onUseTick pinned method fingerprint drift")
    data={
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "class_path":CLASS,"class_sha256":CLASS_SHA256,
        "publisher_default_resistance_tag":tag,
        "radiation_guard_method":probe_method(found[0]),
        "limits":LIMITS,
        "interpretation":"NO_MUTATION_EXACT_VERSION_STATIC_RADIATION_GUARD_SEAMS",
    }
    require(len(json.dumps(data,ensure_ascii=False).encode())<21000,
            "full evidence report budget exceeded")
    return data

def verify_seal(actual,expected):
    require(expected.get("scope")==SCOPE,"wrong static guard manifest scope")
    require(expected.get("limits")==LIMITS,"unsafe limits promotion")
    require(actual==expected,"Raygun radiation guard or publisher tag evidence drift")
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",required=True)
    p.add_argument("--seal")
    args=p.parse_args()
    try:
        out=analyze(args.jar,args.javap)
        if args.seal:
            verify_seal(out,json.loads(Path(args.seal).read_text(encoding="utf8")))
        path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print("PASS: exact 1.0.10 Raygun radiation tag and branch metadata")
        print("tag_members="+str(out["publisher_default_resistance_tag"]["value_count"])+
              " guard_symbols="+str(len(out["radiation_guard_method"]["symbols_with_local_context"])))
        print("NOT_CERTIFIED / NO_MUTATION / physical QA not tested")
    except (AuditError,ValueError,KeyError,TypeError,OSError,UnicodeDecodeError,
            zipfile.BadZipFile) as e:
        p.exit(1,"FAIL-CLOSED: "+str(e)+"\n")

if __name__=="__main__":
    main()
