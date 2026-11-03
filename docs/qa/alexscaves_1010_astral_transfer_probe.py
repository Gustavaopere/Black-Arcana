#!/usr/bin/env python3
"""SHA-exact publisher 1.0.10 Astral Transferring static interoperability probe.

Read-only bounded JVM instruction references, not a complete method decompile,
CFG/reaching-definition proof, live acceptance, or a mutating integration API.
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

SCOPE = "EXACT_ALEXSCAVES_1010_ASTRAL_TRANSFERRING_SELECTED_CONSUMER_ABI"
OWNER = BASE + "server/item/TotemOfPossessionItem.class"
PINNED_CLASS_SHA256 = "bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e"
DESC = "(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V"
ROOT = "data/alexscaves/"
RESOURCES = (
    ROOT+"enchantment/astral_transferring.json",
    ROOT+"enchantment/detonating_death.json",
    ROOT+"tags/item/enchantable/totem_of_possession.json",
    ROOT+"tags/entity_type/resists_totem_of_possession.json",
)
MARKERS = (
    "ASTRAL_TRANSFERRING:",
    "RESISTS_TOTEM_OF_POSSESSION:",
    "ACCompat.enchantLevel:",
    "getHealth:",
    "setLastHurtByMob:",
    "setPossessed:",
    "BoundEntityUUID",
    "BoundEntityTag",
    "putUUID:",
    "serializeEntity:",
    "ACCompat.setTag:",
    "updateEntityIdFromServer:",
)
SYMBOLIC = {"getfield", "putfield", "getstatic", "putstatic",
            "invokevirtual", "invokestatic", "invokespecial", "invokeinterface"}
BRANCH_PREFIXES = ("if", "goto")
NUMERIC = {"iconst_0","iconst_1","iconst_2","iconst_3","iconst_4","iconst_5",
           "bipush","sipush","ldc","ldc_w","ldc2_w","irem","fcmpl","fcmpg"}

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def slim(x):
    return {k: x[k] for k in ("offset","opcode","operand","symbol")}

def load_resource(z, path):
    data = z.read(path)
    require(len(data)<=16000, "resource exceeds bounded inspection: "+path)
    parsed = json.loads(data)
    require(isinstance(parsed,dict), "JSON object required: "+path)
    return {"path":path, "sha256":hashlib.sha256(data).hexdigest(), "json":parsed}

def pick(methods,name,desc=None):
    xs=[m for m in methods if name_of(m)==name and (desc is None or m["descriptor"]==desc)]
    require(len(xs)==1,"missing/ambiguous "+name+" "+str(desc))
    return xs[0]

def select_consumer(methods):
    m=pick(methods,"onUseTick",DESC)
    ins=m["instructions"]
    require(500<=len(ins)<=2600,"unexpected onUseTick size")
    offsets=[x["offset"] for x in ins]
    require(offsets==sorted(set(offsets)),"duplicate/out of order JVM instruction offset")
    direct=[x for x in ins if "ACEnchantmentRegistry.ASTRAL_TRANSFERRING:" in x["symbol"]]
    require(len(direct)==1,"no unique exact enchantment guard")
    require(860<=direct[0]["offset"]<=1035, "unexpected enchantment guard location")
    return m

def view_consumer(method):
    ins=method["instructions"]
    selected=[x for x in ins if 840<=x["offset"]<=1065]
    pivots=[]
    for marker in MARKERS:
        matches=[i for i,x in enumerate(ins) if 840<=x["offset"]<=1065 and marker in x["symbol"]]
        if matches:
            pivots.append({"marker":marker,"matches":len(matches),
                           "first_offset":ins[matches[0]]["offset"],
                           "nearby":[slim(x) for x in ins[max(0,matches[0]-5):matches[0]+7]]})
    require(any(x["marker"]=="ASTRAL_TRANSFERRING:" for x in pivots),"missing guard pivot")
    require(any(x["marker"]=="setPossessed:" for x in pivots),"missing possession setter")
    require(any(x["marker"]=="BoundEntityUUID" for x in pivots),"missing NBT UUID write")
    require(len(pivots)<=len(MARKERS),"too many pivot populations")
    syms=[slim(x) for x in selected if x["opcode"] in SYMBOLIC]
    branches=[slim(x) for x in selected if x["opcode"].startswith(BRANCH_PREFIXES)]
    nums=[slim(x) for x in selected if x["opcode"] in NUMERIC]
    require(len(syms)<=85 and len(branches)<=70 and len(nums)<=80,
            "unbounded consumer selection")
    return {"header":method["header"],"descriptor":method["descriptor"],
            "instruction_count":len(ins),"parsed_method_sha256":digest_method(method),
            "scan_window_offsets":[840,1065],
            "selected_symbolic_references":syms,
            "selected_branch_instructions":branches,
            "selected_numeric_instructions":nums,
            "selected_local_windows":pivots,
            "interpretation":"SELECTED_JVM_WINDOWS_ONLY_NOT_CONTROL_FLOW_GRAPH"}

def view_helper(method):
    xs=method["instructions"]
    require(1<=len(xs)<=500,"helper instruction count outside bound")
    references=[slim(x) for x in xs if x["opcode"] in SYMBOLIC]
    require(len(references)<=60,"unbounded helper references")
    return {"name":name_of(method),"header":method["header"],
            "descriptor":method["descriptor"],"instruction_count":len(xs),
            "parsed_method_sha256":digest_method(method),
            "symbolic_references":references,
            "interpretation":"HELPER_SYMBOLS_ONLY_NOT_WHOLE_METHOD"}

def audit(jar,javap_bin):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"exact publisher JAR fingerprint mismatch")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate JAR entry")
        require(all(p in names for p in RESOURCES+(OWNER,)),"required compiled/resource path missing")
        raw=z.read(OWNER)
        require(hashlib.sha256(raw).hexdigest()==PINNED_CLASS_SHA256,
                "Totem owner class differs from previously certified exact contract")
        resources=[load_resource(z,x) for x in RESOURCES]
    ench=resources[0]["json"]
    require(ench.get("description",{}).get("translate")=="enchantment.alexscaves.astral_transferring",
            "enchantment identity drift")
    require(ench.get("supported_items")=="#alexscaves:enchantable/totem_of_possession",
            "supported tag drift")
    require(isinstance(ench.get("max_level"),int) and ench["max_level"]>=1,
            "invalid enchantment max level")
    methods=parse_methods(javap(javap_bin,jar,OWNER[:-6].replace("/",".")))
    primary=select_consumer(methods)
    helpers=[view_helper(pick(methods,"setPossessed")),
             view_helper(pick(methods,"updateEntityIdFromServer"))]
    return {"schema_version":1,"scope":SCOPE,
            "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "owner":{"class":OWNER,"sha256":PINNED_CLASS_SHA256,"parsed_methods":len(methods)},
            "resources":resources,
            "consumer":view_consumer(primary),
            "helpers":helpers,
            "limits":{"source_111_is_parameter_authority":False,
                      "full_cfg_and_all_guards":"NOT_RECONSTRUCTED",
                      "server_authoritative_settlement":"NOT_CERTIFIED",
                      "effective_pack_datapacks":"NOT_VERIFIED",
                      "prior_target_marker_cleanup":"NOT_CERTIFIED",
                      "duplicate_controller_and_replay":"NOT_VERIFIED",
                      "player_gate_and_claim_protection":"NOT_CERTIFIED",
                      "safe_mutating_hook":"NOT_VERIFIED",
                      "physical_qa":"NOT_TESTED",
                      "mutation":"NO_MUTATION",
                      "perk_certification":"NOT_CERTIFIED"}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",type=Path,required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--seal",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    out=audit(args.jar,args.javap)
    if args.seal:
        expected=json.loads(args.seal.read_text(encoding="utf8"))
        require(out==expected,"sealed Astral Transferring JVM evidence drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(out,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
