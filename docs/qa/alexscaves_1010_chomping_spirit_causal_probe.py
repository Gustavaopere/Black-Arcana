#!/usr/bin/env python3
"""Clean-room, read-only Chomping Spirit JVM audit for installed Alex's Caves 1.0.10.

Reconciles the previously certified Spirit Dinosaur damage manifest against the
physical JAR. Captures only typed method metadata, branches, selected symbolic
call-sites and exact fingerprints for the Chomping Spirit native causal graph.
It does not run the game, implement provider code, prove damage acceptance,
discover a mutating hook or grant Mastery/XP attribution.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from alexscaves_1010_damage_consumer_probe import (
    SHA1, SHA256, SIZE, sha_file, javap, parse_methods, CODE_LINE, METHOD_LINE,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method
from alexscaves_1010_charting_call_causal_probe import (
    method_roster, unique_pairs, strict_method
)
from alexscaves_1010_bouncy_ball_causal_probe import (
    branch_edges, method_switch_tables
)

BASE = "com/github/alexmodguy/alexscaves/server/"
ITEM = BASE + "item/ExtinctionSpearItem.class"
SPEAR = BASE + "item/SpearItem.class"
SPIRIT = BASE + "entity/item/DinosaurSpiritEntity.class"
THROWN = BASE + "entity/item/ExtinctionSpearEntity.class"
REGISTRY = BASE + "enchantment/ACEnchantmentRegistry.class"
ENCHANT = "data/alexscaves/enchantment/chomping_spirit.json"
ITEM_TAG = "data/alexscaves/tags/item/enchantable/extinction_spear.json"
OWNERS = (ITEM, SPEAR, SPIRIT, THROWN)
RESOURCES = (ENCHANT, ITEM_TAG)
# Each pair is a native JVM signature, not an API promise to external mods.
CORE = {
    ITEM: (
        ("acHurtEnemy", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"),
    ),
    SPEAR: (
        ("acHurtEnemy", "(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z"),
    ),
    SPIRIT: (
        ("tick", "()V"),
        ("tickTremorsaurus", "(Lnet/minecraft/world/entity/player/Player;)V"),
    ),
    THROWN: (
        ("onHitEntity", "(Lnet/minecraft/world/phys/EntityHitResult;)V"),
    ),
}
RELATED = {
    ITEM: ("releaseUsing", "onUseTick"),
    SPIRIT: (
        "getUsingPlayer", "getAttackingEntity", "getEnchantmentLevel",
        "setEnchantmentLevel", "getPlayerUUID", "setPlayerUUID",
        "getDinosaurType", "setDinosaurType", "getDelaySpawn", "setDelaySpawn",
        "setAttackingEntityId", "getAbilityProgress", "defineSynchedData",
        "addAdditionalSaveData", "readAdditionalSaveData"
    ),
}
# Specific cross-method cause/effect anchors independently fixed in the old
# sealed, SHA-exact publisher contract. Offsets are not stable extension APIs.
PIVOTS = {
    (ITEM, "acHurtEnemy"): {
        3: ("invokevirtual", "igniteForSeconds:"),
        21: ("invokestatic", "createEntity:"),
        71: ("getstatic", "TREMORSAURUS:"),
        74: ("invokevirtual", "setDinosaurType:"),
        83: ("invokevirtual", "setPlayerUUID:"),
        89: ("getstatic", "CHOMPING_SPIRIT:"),
        92: ("invokestatic", "enchantLevel:"),
        95: ("invokevirtual", "setEnchantmentLevel:"),
        104: ("invokevirtual", "setAttackingEntityId:"),
        122: ("invokevirtual", "setDelaySpawn:"),
        131: ("invokevirtual", "addFreshEntity:"),
        134: ("pop", ""),
        139: ("invokespecial", "SpearItem.acHurtEnemy:"),
    },
    (SPEAR, "acHurtEnemy"): {
        6: ("invokestatic", "hurtAndBreak:"),
    },
    (SPIRIT, "tick"): {
        279: ("tableswitch", ""),
        322: ("invokevirtual", "tickTremorsaurus:"),
    },
    (SPIRIT, "tickTremorsaurus"): {
        1: ("invokevirtual", "getAttackingEntity:"),
        27: ("invokevirtual", "distanceTo:"),
        32: ("invokevirtual", "getBbWidth:"),
        98: ("invokevirtual", "setUsingAbility:"),
        112: ("iflt", "159"),
        119: ("ifne", "154"),
        131: ("invokestatic", "causeSpiritDinosaurDamage:"),
        134: ("iconst_3", ""),
        135: ("iconst_2", ""),
        137: ("invokevirtual", "getEnchantmentLevel:"),
        140: ("imul", ""),
        141: ("iadd", ""),
        142: ("i2f", ""),
        143: ("invokestatic", "ACCompat.hurt:"),
        146: ("ifeq", "154"),
        151: ("putfield", "dealtDamage:"),
        156: ("invokevirtual", "setFading:"),
        161: ("getfield", "duration:"),
        172: ("if_icmple", "180"),
        177: ("invokevirtual", "setFading:"),
    },
    (THROWN, "onHitEntity"): {
        58: ("invokestatic", "causeSpiritDinosaurDamage:"),
    },
}
SAVE_KEYS = ("UsingPlayerUUID", "DinosaurType")
NON_SAVE_FIELDS = (
    "ENCHANTMENT_LEVEL", "ATTACKING_ENTITY_ID", "DELAY_SPAWN",
    "setEnchantmentLevel", "getEnchantmentLevel",
    "setAttackingEntityId", "setDelaySpawn",
)

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def digest(b: bytes):
    return hashlib.sha256(b).hexdigest()

def read_native_methods(raw):
    """Supplement shared method parser's intentional exclusion of '<clinit>'.

    Original parser skips the static initializer so it cannot be accidentally
    attached to a preceding damage factory. This audit must compare it because
    the earlier Spirit Dinosaur manifest intentionally seals its exact offsets.
    """
    methods=parse_methods(raw)
    lines=raw.splitlines()
    starts=[i for i,line in enumerate(lines) if line.strip()=="static {};"]
    require(len(starts)<=1,"duplicate native JVM static initializer")
    if not starts:
        return methods
    start=starts[0]+1
    next_header=len(lines)
    for i in range(start,len(lines)):
        if lines[i]=="}":
            next_header=i
            break
        match=METHOD_LINE.match(lines[i])
        if match and "(" in match.group(1):
            next_header=i
            break
    section=lines[start:next_header]
    descriptor=[line.strip().split("descriptor:",1)[1].strip()
                for line in section if line.strip().startswith("descriptor:")]
    require(descriptor==["()V"],
            "missing exact static initializer JVM descriptor")
    rows=[]
    for line in section:
        match=CODE_LINE.match(line)
        if not match:
            continue
        offset,opcode,operand,symbol=match.groups()
        rows.append({"offset":int(offset),"opcode":opcode,
                     "operand":operand.strip(),"symbol":(symbol or "").strip()})
    require(1<=len(rows)<=3000 and
            [x["offset"] for x in rows]==sorted({x["offset"] for x in rows}),
            "malformed native static initializer Code block")
    methods.append({"header":"static {};","descriptor":"()V","instructions":rows})
    return methods


def native_name(method, owner):
    """Normalize javap source headings to JVM constructor/initializer names."""
    header=method["header"].strip()
    name=name_of(method)
    short=owner.rsplit("/",1)[-1].removesuffix(".class")
    if name==short or name==short.rsplit("$",1)[-1]:
        return "<init>"
    if header.startswith("static {}") or header.startswith("static {};"):
        return "<clinit>"
    return name

def selected(m):
    rows=strict_method(m)
    result=[{k:x[k] for k in ("offset","opcode","operand","symbol")}
            for x in rows if x["opcode"].startswith(
                ("invoke","getfield","putfield","getstatic","putstatic"))]
    require(len(result)<=350, "unbounded relevant JVM symbolic references")
    return result

def exact_anchors(method, old, owner):
    """Reconcile *all* previously sealed selected JVM anchors for this method."""
    rows={x["offset"]:x for x in strict_method(method)}
    require(old["descriptor"]==method["descriptor"] and
            old["name"]==native_name(method,owner), "prior method descriptor drift")
    anchors=old["anchors"]
    require(1<=len(anchors)<=280, "unbounded parent selected anchors")
    require(len(anchors)==len({a["offset"] for a in anchors}),
            "duplicate parent JVM anchor")
    for anchor in anchors:
        current=rows.get(anchor["offset"])
        # The older sealed probe normalizes javap's invokeinterface
        # "#83,  1" spacing differently from the shared parser. Preserve
        # opcode, offsets and semantic operand/symbol tokens, not whitespace.
        normalize=lambda value: " ".join(str(value).split())
        require(current is not None and
                current["offset"]==anchor["offset"] and
                current["opcode"]==anchor["opcode"] and
                normalize(current["operand"])==normalize(anchor["operand"]) and
                normalize(current["symbol"])==normalize(anchor["symbol"]),
                "parent SHA-exact selected JVM anchor drift "
                +owner+"."+name_of(method)+"@"+str(anchor["offset"]))
    return len(anchors)

def causal_pivots(method, owner):
    points=PIVOTS.get((owner,name_of(method)))
    if not points:
        return []
    rows={x["offset"]:x for x in strict_method(method)}
    output=[]
    for offset,(opcode,token) in points.items():
        ins=rows.get(offset)
        require(ins is not None and ins["opcode"]==opcode and
                token in (ins["operand"]+" "+ins["symbol"]),
                "Chomping Spirit native causal pivot drift "
                +name_of(method)+"@"+str(offset))
        output.append({k:ins[k] for k in
                       ("offset","opcode","operand","symbol")})
    return output

def local_nbt(methods):
    out={}
    for name in ("addAdditionalSaveData","readAdditionalSaveData"):
        found=[m for m in methods if name_of(m)==name]
        require(len(found)==1,"ambiguous or missing Dinosaur Spirit native NBT")
        m=found[0]
        rows=strict_method(m)
        symbols=" ".join(row["symbol"] for row in rows)
        for key in SAVE_KEYS:
            require("String "+key in symbols,
                    "missing own native NBT field "+key)
        for key in NON_SAVE_FIELDS:
            require(key not in symbols,
                    "own native NBT now serializes other targeted field "+key)
        out[name]={
            "instruction_count":len(rows),
            "parsed_method_sha256":digest_method(m),
            "exact_own_nbt_keys":list(SAVE_KEYS),
            "enchantment_level_and_victim_id_in_own_overrides":False,
            "inherited_engine_persistence":"NOT_VERIFIED",
        }
    require(out["addAdditionalSaveData"]["instruction_count"]==15 and
            out["readAdditionalSaveData"]["instruction_count"]==15,
            "own native NBT method length drift")
    return out

def analyze(jar: Path, parent_path: Path, javap_bin: str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "wrong publisher 1.0.10 SHA1/SHA256/size")
    parent_raw=parent_path.read_bytes()
    prior=json.loads(parent_raw,object_pairs_hook=unique_pairs)
    require(prior["artifact_sha1"]==SHA1 and
            prior["artifact_sha256"]==SHA256 and
            prior["artifact_size_bytes"]==SIZE and
            prior["claim_scope"]=="STATIC_TECHNICAL_CATALOG_ONLY",
            "prior Spirit Dinosaur manifest identity or scope drift")
    previous=prior["classes"]
    require(all(k in previous for k in (*OWNERS,REGISTRY)),
            "incomplete previous owner class fingerprint roster")
    require(all(k in prior["resources"] for k in RESOURCES),
            "incomplete prior exact enchantment resource roster")
    resources={}
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)),"duplicate publisher JAR archive entries")
        for owner in (*OWNERS,REGISTRY):
            require(digest(z.read(owner))==previous[owner]["sha256"],
                    "native classfile hash drift: "+owner)
        for path in RESOURCES:
            raw=z.read(path)
            require(digest(raw)==prior["resources"][path],
                    "native publisher resource hash drift: "+path)
            require(len(raw)<=8000, "unbounded native enchantment resource")
            resources[path]={"sha256":digest(raw),
                             "json":json.loads(raw,object_pairs_hook=unique_pairs)}
        # Delimited *direct classfile tokens*, not all logical callsites.
        refs=sorted(x for x in paths if x.endswith(".class") and
                    b"CHOMPING_SPIRIT" in z.read(x))
    require(ITEM in refs and REGISTRY in refs and len(refs)<=12,
            "unexpected native Chomping Spirit direct class token population")
    enchant=resources[ENCHANT]["json"]
    require(enchant["description"]["translate"]==
            "enchantment.alexscaves.chomping_spirit" and
            enchant["max_level"]==2 and
            enchant["supported_items"]=="#alexscaves:enchantable/extinction_spear" and
            enchant["weight"]==2 and enchant["anvil_cost"]==4 and
            enchant["slots"]==["mainhand"],
            "unexpected Chomping Spirit declared enchantment contract")
    require("alexscaves:extinction_spear" in
            resources[ITEM_TAG]["json"]["values"],
            "native extinction spear tag no longer contains item")
    parsed={}
    raws={}
    rosters=[]
    all_selected={}
    for owner in OWNERS:
        raw=javap(javap_bin,jar,owner[:-6].replace("/","."))
        methods=read_native_methods(raw)
        rows=method_roster(methods)
        require(len(rows)==len(methods) and len(rows)>=4,
                "unexpected or duplicate native method roster")
        parsed[owner]=methods
        raws[owner]=raw
        rosters.append({"owner":owner,"class_sha256":previous[owner]["sha256"],
                        "declared_method_count":len(rows),"methods":rows})
        bysig={(native_name(m,owner),m["descriptor"]):m for m in methods}
        for sealed in previous[owner]["methods"]:
            name,desc=sealed["name"],sealed["descriptor"]
            require((name,desc) in bysig,
                    "missing declared previous selected owner method "+name)
            if bysig[(name,desc)]["instructions"]:
                exact_anchors(bysig[(name,desc)],sealed,owner)
        all_selected[owner]=bysig
    consumers=[]
    for owner,specs in CORE.items():
        for name,desc in specs:
            method=all_selected[owner].get((name,desc))
            require(method is not None,"missing exact core method "+name)
            switches=method_switch_tables(method,raws[owner])
            edges=branch_edges(method,switches)
            consumers.append({
                "owner":owner,"name":name,"descriptor":desc,
                "instruction_count":len(strict_method(method)),
                "parsed_method_sha256":digest_method(method),
                "verified_direct_branches":edges,
                "verified_switch_tables":switches,
                "verified_causal_pivots":causal_pivots(method,owner),
                "selected_references":selected(method),
            })
    require(len(consumers)==5, "unexpected central Chomping Spirit causal graph")
    extra=[]
    for owner,names in RELATED.items():
        for name in names:
            candidates=[m for m in parsed[owner] if name_of(m)==name]
            require(len(candidates)==1,
                    "missing or overloaded native ancillary method "+name)
            m=candidates[0]
            extra.append({
                "owner":owner,"name":name,
                "descriptor":m["descriptor"],
                "instruction_count":len(strict_method(m)),
                "parsed_method_sha256":digest_method(m),
                "selected_references":selected(m),
            })
    nbt=local_nbt(parsed[SPIRIT])
    require(any(x["opcode"]=="tableswitch" for x in
                next(m for m in consumers if m["owner"]==SPIRIT
                     and m["name"]=="tick")["verified_switch_tables"]),
            "missing native three-way dinosaur dispatcher")
    return {
        "schema_version":1,
        "scope":"CHOMPING_SPIRIT_EXACT_NATIVE_MELEE_TO_TREMORSAURUS_DAMAGE_AND_STATE",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
        "parent_manifest_sha256":digest(parent_raw),
        "resources":resources,
        "direct_class_token_CHOMPING_SPIRIT":refs,
        "owner_method_rosters":rosters,
        "core_consumers":consumers,
        "ancillary_native_consumers":extra,
        "spirit_own_nbt_overrides":nbt,
        "limits":{
            "melee_vs_thrown_spirit_damage":"SEPARATE_NATIVE_CAUSAL_PATHS",
            "runtime_hit_acceptance":"NOT_TESTED",
            "net_hp_loss":"NOT_VERIFIED",
            "entity_spawn_acceptance":"NOT_TESTED",
            "inherited_engine_persistence":"NOT_VERIFIED",
            "unload_reload_after_enchantment_level_change":"NOT_TESTED",
            "other_jar_mixins_and_datapacks":"NOT_VERIFIED",
            "full_interprocedural_exception_flow":"NOT_RECONSTRUCTED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "claim_scope":"STATIC_TECHNICAL_CATALOG_ONLY",
        },
    }


def compact_seal(report):
    """Durable digest-bound summary; full report is reproducible CI evidence.

    This compact seal preserves exact identities, per-consumer method hashes,
    branch populations and NBT boundaries. SHA256 also binds every unabridged
    symbolic ref, owner method roster, branch destination and resource byte
    from the full deterministic read-only report.
    """
    core=report["core_consumers"]
    def key(entry):
        return entry["owner"].rsplit("/",1)[-1].removesuffix(".class")+"."+entry["name"]
    tick=next(x for x in core
              if x["owner"]==SPIRIT and x["name"]=="tick")
    return {
        "schema_version":report["schema_version"],
        "scope":report["scope"],
        "artifact":report["artifact"],
        "parent_manifest_sha256":report["parent_manifest_sha256"],
        "full_report_sha256":digest(json.dumps(
            report,ensure_ascii=False,sort_keys=True,
            separators=(",",":")).encode("utf-8")),
        "owner_method_counts":{
            x["owner"].rsplit("/",1)[-1]:x["declared_method_count"]
            for x in report["owner_method_rosters"]},
        "core_method_sha256":{key(x):x["parsed_method_sha256"] for x in core},
        "core_direct_branch_counts":{
            key(x):len(x["verified_direct_branches"]) for x in core},
        "dispatcher_switch_cases":tick["verified_switch_tables"],
        "direct_class_token_CHOMPING_SPIRIT":
            report["direct_class_token_CHOMPING_SPIRIT"],
        "spirit_own_nbt_overrides":report["spirit_own_nbt_overrides"],
        "limits":report["limits"],
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--jar",type=Path,required=True)
    parser.add_argument("--parent",type=Path,required=True)
    parser.add_argument("--javap",default="javap")
    parser.add_argument("--snapshot",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=analyze(args.jar,args.parent,args.javap)
    if args.snapshot:
        sealed=json.loads(args.snapshot.read_bytes(),object_pairs_hook=unique_pairs)
        require(compact_seal(result)==sealed,"Chomping Spirit causal snapshot drift")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("CHOMPING_SPIRIT_CAUSAL="+json.dumps(result,ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":
    main()
