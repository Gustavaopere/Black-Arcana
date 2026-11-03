#!/usr/bin/env python3
"""Read-only SHA-exact 1.0.10 Bonking death-loot interoperability probe.

Bounded JVM field/method calls, branch instructions, constants and local
windows. Neither complete bytecode/source, a runtime execution trace,
nor a verified mutating hook or physical gameplay test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

SCOPE = "EXACT_ALEXSCAVES_1010_BONKING_DEATH_EVENT_AND_LOOT_BRIDGE"
ENCHANTMENT_ID = "alexscaves:bonking"
ENCHANTMENT_RESOURCE = "data/alexscaves/enchantment/bonking.json"
ITEM_TAG = "data/alexscaves/tags/item/enchantable/primitive_club.json"
EVENT_CLASS = BASE + "server/event/CommonEvents.class"
MIXIN_CLASS = BASE + "mixin/MobMixin.class"
CLUB_CLASS = BASE + "server/item/PrimitiveClubItem.class"
EVENT_CLASS_SHA256 = "d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43"
SYMBOLIC = {"getfield", "putfield", "getstatic", "putstatic",
            "invokestatic", "invokevirtual", "invokespecial", "invokeinterface",
            "invokedynamic"}
NUMERIC = {"bipush", "sipush", "ldc", "ldc_w", "ldc2_w",
           "fconst_0", "fconst_1", "fconst_2", "iconst_0", "iconst_1",
           "iconst_2", "iconst_3", "iconst_4", "aconst_null"}
EVENT_MARKERS = (
    "ACEnchantmentRegistry.BONKING:",
    "ACCompat.enchantLevel:",
    "RandomSource.nextFloat:",
    "ACItemRegistry.PRIMITIVE_CLUB:",
    "EntityType.CREEPER:",
    "EntityType.LIGHTNING_BOLT:",
    "ACCompat.createEntity:",
    "setVisualOnly:",
    "thunderHit:",
    "DamageSources.mobAttack:",
    "ac_getEquipmentDropChance:",
    "ac_setDropChance:",
    "ac_dropCustomDeathLoot:",
)
BRIDGE_NAMES = (
    "ac_getEquipmentDropChance",
    "ac_setDropChance",
    "ac_dropCustomDeathLoot",
)

def require(test, message):
    if not test:
        raise ValueError(message)

def slim(row):
    return {k: row[k] for k in ("offset", "opcode", "operand", "symbol")}

def only_method(methods, name, desc=None):
    group = [m for m in methods if name_of(m) == name and
             (desc is None or m["descriptor"] == desc)]
    require(len(group) == 1, "missing/ambiguous JVM method "+name)
    return group[0]

def inspect_resource(archive, path):
    raw = archive.read(path)
    require(len(raw) < 16000, "unexpected large JSON resource "+path)
    decoded = json.loads(raw.decode("utf-8"))
    require(isinstance(decoded, dict), "unexpected JSON value "+path)
    return {"path":path, "sha256":hashlib.sha256(raw).hexdigest(),
            "json":decoded}

def choose_event(methods):
    selected = only_method(methods, "livingDie")
    require("LivingDeathEvent;" in selected["descriptor"],"unrecognized death event signature")
    ins = selected["instructions"]
    require(90 <= len(ins) <= 1500, "unexpected compiled death handler size")
    offsets = [x["offset"] for x in ins]
    require(offsets == sorted(set(offsets)), "duplicate or unordered JVM offsets")
    matches = [x for x in ins if "ACEnchantmentRegistry.BONKING:" in x["symbol"]]
    require(len(matches) == 1,"missing/ambiguous Bonking event consumer")
    for marker in ("ac_getEquipmentDropChance:", "ac_setDropChance:",
                   "ac_dropCustomDeathLoot:"):
        require(any(marker in x["symbol"] for x in ins),
                "missing loot bridge reference "+marker)
    return selected

def select_death_evidence(method):
    ins = method["instructions"]
    candidates = []
    for marker in EVENT_MARKERS:
        at = [i for i,x in enumerate(ins) if marker in x["symbol"]]
        if at:
            i=at[0]
            candidates.append({"marker":marker,"matches":len(at),
                               "pivot":ins[i]["offset"],
                               "nearby":[slim(x) for x in ins[max(0,i-4):i+7]]})
    require(any(x["marker"]=="ACEnchantmentRegistry.BONKING:" for x in candidates),
            "no Bonking marker window")
    require(any(x["marker"]=="ac_dropCustomDeathLoot:" for x in candidates),
            "no loot bridge marker window")
    require(len(candidates) <= len(EVENT_MARKERS),"unexpected marker population")
    guarded_index = next(i for i,x in enumerate(ins) if
                         "ACEnchantmentRegistry.BONKING:" in x["symbol"])
    region=ins[max(0,guarded_index-30):min(len(ins),guarded_index+185)]
    symbolic=[slim(x) for x in region if x["opcode"] in SYMBOLIC]
    branches=[slim(x) for x in region if x["opcode"].startswith(("if","goto"))]
    numeric=[slim(x) for x in region if x["opcode"] in NUMERIC]
    require(len(symbolic) <= 115 and len(branches) <= 100 and
            len(numeric) <= 100,"unbounded event evidence")
    return {"header":method["header"],"descriptor":method["descriptor"],
            "parsed_method_sha256":digest_method(method),
            "instruction_count":len(ins),
            "region_scope":"BOUNDED_INSTRUCTIONS_AROUND_BONKING_BRANCH",
            "selected_symbolic_refs":symbolic,
            "selected_branches":branches,
            "selected_numeric_operands":numeric,
            "selected_windows":candidates}

def inspect_mixin(methods):
    results=[]
    for name in BRIDGE_NAMES:
        method=only_method(methods,name)
        instructions=method["instructions"]
        require(1<=len(instructions)<=220,"unbounded bridge method "+name)
        refs=[slim(x) for x in instructions if x["opcode"] in SYMBOLIC]
        require(len(refs)<=45,"unbounded bridge references")
        results.append({"name":name,"descriptor":method["descriptor"],
                        "parsed_method_sha256":digest_method(method),
                        "instruction_count":len(instructions),
                        "selected_symbolic_refs":refs,
                        "interpretation":"READ_ONLY_HELPER_SYMBOLS_NOT_MIXIN_APPLICATION_PROOF"})
    return results

def audit(jar, javap_bin):
    require(sha_file(jar)==(SHA1,SHA256,SIZE),"exact publisher JAR mismatch")
    with zipfile.ZipFile(jar) as arc:
        paths=arc.namelist()
        require(len(paths)==len(set(paths)), "duplicate publisher archive entries")
        required=(ENCHANTMENT_RESOURCE,ITEM_TAG,EVENT_CLASS,MIXIN_CLASS,CLUB_CLASS)
        require(all(p in paths for p in required),"missing exact publisher resource/class")
        resources=[inspect_resource(arc,p) for p in (ENCHANTMENT_RESOURCE,ITEM_TAG)]
        cls={p:hashlib.sha256(arc.read(p)).hexdigest()
             for p in (EVENT_CLASS,MIXIN_CLASS,CLUB_CLASS)}
    require(cls[EVENT_CLASS]==EVENT_CLASS_SHA256,"exact CommonEvents class drift")
    json_enchantment=resources[0]["json"]
    require(json_enchantment.get("description",{}).get("translate")==
            "enchantment.alexscaves.bonking","wrong enchantment ID")
    require(json_enchantment.get("supported_items")==
            "#alexscaves:enchantable/primitive_club","unexpected support tag")
    require(json_enchantment.get("max_level")==1,"unexpected max level")
    require("alexscaves:primitive_club" in resources[1]["json"].get("values",[]),
            "expected publisher club not in tag")
    event_methods=parse_methods(javap(javap_bin,jar,EVENT_CLASS[:-6].replace("/",".")))
    mixin_methods=parse_methods(javap(javap_bin,jar,MIXIN_CLASS[:-6].replace("/",".")))
    club_methods=parse_methods(javap(javap_bin,jar,CLUB_CLASS[:-6].replace("/",".")))
    consumer=choose_event(event_methods)
    club_bonking=[{"method":name_of(m),"descriptor":m["descriptor"]}
                  for m in club_methods if any("ACEnchantmentRegistry.BONKING:" in
                  x["symbol"] for x in m["instructions"])]
    require(not club_bonking,"unexpected direct Bonking consumer in PrimitiveClubItem")
    return {
        "schema_version":1,"scope":SCOPE,
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "enchantment":{"id":ENCHANTMENT_ID,"resource":resources[0]},
        "item_tag":resources[1],
        "classes":[{"path":path,"sha256":cls[path]} for path in
                   (EVENT_CLASS,MIXIN_CLASS,CLUB_CLASS)],
        "events_parsed":len(event_methods),"mixin_methods_parsed":len(mixin_methods),
        "club_methods_parsed":len(club_methods),
        "death_consumer":select_death_evidence(consumer),
        "loot_bridge":inspect_mixin(mixin_methods),
        "club_direct_bonking_consumers":club_bonking,
        "limits":{
            "complete_death_handler_cfg":"NOT_RECONSTRUCTED",
            "actual_skull_drop":"NOT_TESTED",
            "effective_drop_probability":"NOT_CERTIFIED",
            "effective_modded_loot_pipeline":"NOT_VERIFIED",
            "mixin_application_and_order":"NOT_VERIFIED",
            "drop_chance_restoration_under_exceptions":"NOT_CERTIFIED",
            "actual_datapacks":"NOT_VERIFIED",
            "multiplayer_server_and_replay":"NOT_VERIFIED",
            "safe_mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "perk_certification":"NOT_CERTIFIED"}}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",required=True,type=Path)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--seal",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=audit(args.jar,args.javap)
    if args.seal:
        seal=json.loads(args.seal.read_text(encoding="utf8"))
        require(result==seal,"Bonking sealed exact-JAR manifest drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
