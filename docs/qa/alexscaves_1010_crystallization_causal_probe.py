#!/usr/bin/env python3
"""SHA-exact, read-only Crystallization / Galena Gauntlet causal JVM audit.

Reconciles every previously sealed method window with publisher 1.0.10,
checks direct branch destinations and validated javap switch tables, and
traces only the relevant inventory/owner/cost/target/damage/mining hand-offs.
This is not physical gameplay QA, a safe mutating hook, or a second spell.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_crystallization_probe import (
    GAUNTLET, WEAPON, ENCH_REGISTRY, TAG_REGISTRY,
    ENCHANT, METHODS, require, check_resources,
)
from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_bouncy_ball_causal_probe import (
    branch_edges, method_switch_tables,
)
from alexscaves_1010_charting_call_causal_probe import (
    strict_method, method_roster, unique_pairs,
)

OWNERS=(GAUNTLET,WEAPON)
# Bytecode anchor offsets are evidence of this exact compiled build, never a
# stable provider extension API.
PIVOTS={
    (GAUNTLET,"use"):{
        35:("getstatic","CRYSTALLIZATION:"),
        38:("invokestatic","enchantLevel:"),
        58:("getstatic","GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS:"),
        64:("getstatic","MAGNETIC_ITEMS:"),
        67:("invokevirtual","ItemStack.is:"),
        84:("invokestatic","hurtAndBreakUsedHand:"),
        89:("invokevirtual","startUsingItem:"),
        94:("invokestatic","useConsume:"),
        100:("invokestatic","useFail:"),
    },
    (GAUNTLET,"onUseTick"):{
        67:("getstatic","CRYSTALLIZATION:"),
        90:("getstatic","GALENA_GAUNTLET_CRYSTALLIZATION_ITEMS:"),
        96:("getstatic","MAGNETIC_ITEMS:"),
        112:("ldc2_w",""),
        115:("ldc2_w",""),
        118:("ldc2_w",""),
        121:("invokevirtual","inflate:"),
        124:("invokevirtual","getEntitiesOfClass:"),
        193:("invokevirtual","copy:"),
        201:("invokevirtual","setCount:"),
        216:("invokestatic","createEntity:"),
        228:("invokevirtual","setItemStack:"),
        252:("invokevirtual","setControllerUUID:"),
        258:("invokevirtual","addFreshEntity:"),
        261:("pop",""),
    },
    (GAUNTLET,"releaseUsing"):{
        26:("invokestatic","addCooldown:"),
    },
    (WEAPON,"tick"):{
        109:("invokevirtual","plopItem:"),
        382:("invokevirtual","hurtEntity:"),
        608:("getstatic","FERROUS_HASTE:"),
        626:("getstatic","FIELD_EXTENSION:"),
        659:("invokestatic","getHitResultOnViewVector:"),
        771:("invokevirtual","hurtEntity:"),
        1290:("invokevirtual","destroyBlock:"),
        1329:("invokevirtual","destroyBlock:"),
    },
    (WEAPON,"hurtEntity"):{
        99:("invokestatic","ACCompat.hurt:"),
        115:("invokestatic","postAttackEffects:"),
        120:("invokevirtual","damageItem:"),
        239:("invokevirtual","hurtEnemy:"),
    },
    (WEAPON,"getController"):{11:("invokevirtual","getControllerUUID:")},
    (WEAPON,"getTarget"):{4:("getstatic","TARGET_ID:")},
    (WEAPON,"isOwnerWearingGauntlet"):{21:("getstatic","GALENA_GAUNTLET:")},
    (WEAPON,"plopItem"):{17:("invokestatic","spawnAtLocation:")},
    (WEAPON,"addAdditionalSaveData"):{
        11:("ldc_w","WeaponStack"),40:("ldc_w","ControllerUUID"),
    },
    (WEAPON,"readAdditionalSaveData"):{
        1:("ldc_w","WeaponStack"),32:("ldc_w","ControllerUUID"),
    },
}
NBT=("addAdditionalSaveData","readAdditionalSaveData")
NBT_KEYS=("WeaponStack","ControllerUUID")
MONITOR=("WeaponStack","ControllerUUID","TARGET_ID","getTarget",
         "getController","getControllerUUID","setControllerUUID",
         "setItemStack","getItemStack","plopItem","spawnAtLocation",
         "setCount","copy","addFreshEntity","destroyBlock",
         "damageItem","hurtEntity","isClientSide","setFading",
         "getEntitiesOfClass")

def digest(value:bytes)->str:
    return hashlib.sha256(value).hexdigest()

def compact(row:dict)->dict:
    return {k:row[k] for k in ("offset","opcode","operand","symbol")}

def normalized(value):
    return " ".join(str(value).split())

def reconcile_prior(method,prior):
    """Compare ALL old published JVM windows including their operands."""
    rows=strict_method(method)
    require(name_of(method)==prior["name"] and
            method["descriptor"]==prior["descriptor"] and
            len(rows)==prior["instruction_count"] and
            digest_method(method)==prior["parsed_method_sha256"],
            "parent 1.0.10 parsed method identity/digest drift")
    require(len(prior["pivot_windows"])<=32,"unbounded previous pivot population")
    positions={r["offset"]:i for i,r in enumerate(rows)}
    count=0
    for pivot in prior["pivot_windows"]:
        needle=pivot["needle"]
        matches=[i for i,row in enumerate(rows) if needle in row["symbol"]]
        require(len(matches)==pivot["match_count"],
                "previous symbolic reference count changed "+needle)
        require(len(pivot["locations"])==min(2,len(matches)),
                "previous bounded window count changed")
        for location,index in zip(pivot["locations"],matches[:2]):
            require(location["at"]==rows[index]["offset"],
                    "previous native pivot offset changed")
            current=rows[max(0,index-5):index+7]
            sealed=location["window"]
            require(len(current)==len(sealed),
                    "previous native pivot window length changed")
            for actual,old in zip(current,sealed):
                require(actual["offset"]==old["offset"] and
                        actual["opcode"]==old["opcode"] and
                        normalized(actual["operand"])==normalized(old["operand"]) and
                        normalized(actual["symbol"])==normalized(old["symbol"]),
                        "previous SHA-exact JVM window drift "+needle)
        count+=len(pivot["locations"])
    return count

def causal_pivots(method,owner):
    rows={r["offset"]:r for r in strict_method(method)}
    expected=PIVOTS.get((owner,name_of(method)),{})
    output=[]
    for off,(opcode,token) in expected.items():
        row=rows.get(off)
        require(row is not None and row["opcode"]==opcode and
                token in row["symbol"]+" "+row["operand"],
                "Crystallization native causal pivot drift: "+
                name_of(method)+"@"+str(off))
        if off in (112,115,118):
            require("64.0" in row["symbol"] or "64.0" in row["operand"],
                    "wrong AABB expansion constant")
        output.append(compact(row))
    return output

def own_nbt(methods):
    result={}
    for name in NBT:
        rows=[m for m in methods if name_of(m)==name]
        require(len(rows)==1,"missing or overloaded native magnetic weapon NBT")
        m=rows[0]
        ins=strict_method(m)
        symbols=" ".join(r["symbol"] for r in ins)
        for key in NBT_KEYS:
            require("String "+key in symbols,
                    "missing own magnetic weapon NBT key "+key)
        result[name]={
            "parsed_method_sha256":digest_method(m),
            "instruction_count":len(ins),
            "explicit_keys":list(NBT_KEYS),
            "inherited_engine_state":"NOT_VERIFIED",
            "actual_inventory_restoration":"NOT_TESTED",
        }
    require(all(x["instruction_count"]==23 for x in result.values()),
            "native magnetic weapon NBT body changed")
    return result

def source_reference_roster(m):
    selected=[compact(r) for r in strict_method(m)
              if r["opcode"].startswith(
                  ("invoke","getfield","putfield","getstatic","putstatic"))
              and any(w.lower() in r["symbol"].lower() for w in MONITOR)]
    require(len(selected)<=180,"unbounded selected native refs")
    return selected

def audit(jar:Path,parent_path:Path,javap_bin:str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "wrong exact publisher 1.0.10 SHA1/SHA256/size")
    parent_raw=parent_path.read_bytes()
    parent=json.loads(parent_raw,object_pairs_hook=unique_pairs)
    artifact={"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE}
    require(parent["artifact"]==artifact and
            parent["limits"]["mutation"]=="NO_MUTATION",
            "original Crystallization seal artifact/scope drift")
    expected={c["path"]:c["sha256"] for c in parent["class_evidence"]}
    require(set(expected)=={GAUNTLET,WEAPON,ENCH_REGISTRY,TAG_REGISTRY},
            "previous class roster drift")
    with zipfile.ZipFile(jar) as arc:
        names=arc.namelist()
        require(len(names)==len(set(names)),"duplicate publisher archive entry")
        for owner,sha in expected.items():
            require(digest(arc.read(owner))==sha,
                    "wrong native classfile digest "+owner)
        resources={}
        for group,v in parent["resource_evidence"].items():
            raw=arc.read(v["path"])
            require(digest(raw)==v["sha256"] and len(raw)==v["size_bytes"],
                    "wrong native resource digest "+group)
            resources[group]={"path":v["path"],"sha256":digest(raw),
                              "size_bytes":len(raw),
                              "json":json.loads(raw,object_pairs_hook=unique_pairs)}
        check_resources(resources)
        class_tokens=sorted(x for x in names if x.endswith(".class") and
                            b"CRYSTALLIZATION" in arc.read(x))
    require(GAUNTLET in class_tokens and ENCH_REGISTRY in class_tokens and
            len(class_tokens)<=14,"unexpected direct CRYSTALLIZATION token census")
    require(len(resources["crystallization"]["json"]["values"])==10 and
            len(resources["ferromagnetic"]["json"]["values"])==82,
            "unexpected native declared tag entry counts")
    cls=[]
    selected=[]
    for owner in OWNERS:
        raw=javap(javap_bin,jar,owner[:-6].replace("/","."))
        methods=parse_methods(raw)
        roster=method_roster(methods)
        cls.append({"owner":owner,"sha256":expected[owner],
                    "declared_method_count":len(roster),"methods":roster})
        by_sig={(name_of(m),m["descriptor"]):m for m in methods}
        require(len(by_sig)==len(methods),"duplicate native method signature")
        for old in parent["selected_consumers"]:
            if old["owner"]!=owner:continue
            identity=old["method"]
            method=by_sig.get((identity["name"],identity["descriptor"]))
            require(method is not None,"missing original native consumer")
            windows=reconcile_prior(method,identity)
            switches=method_switch_tables(method,raw)
            branches=branch_edges(method,switches)
            selected.append({
                "owner":owner,"name":name_of(method),
                "descriptor":method["descriptor"],
                "instruction_count":len(strict_method(method)),
                "parsed_method_sha256":digest_method(method),
                "prior_window_count":windows,
                "direct_branch_edges":branches,
                "verified_switch_tables":switches,
                "verified_causal_pivots":causal_pivots(method,owner),
                "selected_native_state_and_effect_refs":
                    source_reference_roster(method),
            })
    require(len(selected)==11 and len(cls)==2,
            "missing native original 11-consumer causal family")
    nbt=own_nbt(methods) # methods is last iteration: MagneticWeaponEntity
    return {
        "schema_version":1,
        "scope":"CRYSTALLIZATION_1010_NATIVE_GAUNTLET_INVENTORY_MAGNETIC_WEAPON_CFG",
        "artifact":artifact,
        "parent_manifest_sha256":digest(parent_raw),
        "resources":resources,
        "direct_CRYSTALLIZATION_class_tokens":class_tokens,
        "owner_method_rosters":cls,
        "consumers":selected,
        "own_magnetic_weapon_nbt_overrides":nbt,
        "limits":{
            "enchantment_semantic_root":"NATIVE_GALENA_GAUNTLET_ITEM_ELIGIBILITY_NOT_NEW_CAST",
            "effective_tag_resolution":"NOT_VERIFIED",
            "other_mod_tags_and_item_compatibility":"NOT_VERIFIED",
            "spawn_acceptance_after_setCount0":"NOT_TESTED",
            "inventory_transaction_rollback":"NOT_VERIFIED",
            "real_melee_hit_and_mining":"NOT_TESTED",
            "controller_identity_reload":"NOT_TESTED",
            "engine_inherited_persistence":"NOT_VERIFIED",
            "external_mixins_and_datapacks":"NOT_VERIFIED",
            "interprocedural_exception_cfg":"NOT_RECONSTRUCTED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY",
        },
    }

def compact_seal(report):
    """Reproducible compact publisher seal bound to complete native report."""
    keys={x["owner"].rsplit("/",1)[-1].removesuffix(".class")+"."+x["name"]:
          x for x in report["consumers"]}
    return {
        "schema_version":report["schema_version"],
        "scope":report["scope"],
        "artifact":report["artifact"],
        "parent_manifest_sha256":report["parent_manifest_sha256"],
        "full_report_sha256":digest(json.dumps(
            report,sort_keys=True,ensure_ascii=False,
            separators=(",",":")).encode("utf-8")),
        "resources_sha256":{k:v["sha256"] for k,v in report["resources"].items()},
        "direct_CRYSTALLIZATION_class_tokens":
            report["direct_CRYSTALLIZATION_class_tokens"],
        "owner_method_counts":{x["owner"].rsplit("/",1)[-1]:
            x["declared_method_count"] for x in report["owner_method_rosters"]},
        "consumer_method_sha256":{k:v["parsed_method_sha256"] for k,v in keys.items()},
        "consumer_instruction_counts":{k:v["instruction_count"] for k,v in keys.items()},
        "consumer_direct_branch_counts":{k:len(v["direct_branch_edges"]) for k,v in keys.items()},
        "consumer_switch_tables":{k:v["verified_switch_tables"] for k,v in keys.items()
                                   if v["verified_switch_tables"]},
        "consumer_pivots":{k:v["verified_causal_pivots"] for k,v in keys.items()
                           if v["verified_causal_pivots"]},
        "own_magnetic_weapon_nbt_overrides":
            report["own_magnetic_weapon_nbt_overrides"],
        "limits":report["limits"],
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--parent",required=True,type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--snapshot",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    report=audit(a.jar,a.parent,a.javap)
    seal=compact_seal(report)
    if a.snapshot:
        previous=json.loads(a.snapshot.read_bytes(),object_pairs_hook=unique_pairs)
        require(seal==previous,"Crystallization native causal compact seal drift")
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",
                            encoding="utf8")
    print("CRYSTALLIZATION_CAUSAL_SEAL="+json.dumps(seal,ensure_ascii=False,
                                                  separators=(",",":")))
if __name__=="__main__":
    main()
