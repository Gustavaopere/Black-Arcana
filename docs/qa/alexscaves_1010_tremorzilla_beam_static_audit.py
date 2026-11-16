#!/usr/bin/env python3
"""SHA-exact, read-only cross-manifest Tremorzilla Beam damage/targeting audit.

Certifies only a *candidate* static damage-type contract. Neither publisher
bytecode identity nor native branch dominance verifies physical world policy,
mutating hooks, final damage acceptance, PvP or claims enforcement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file
)
from alexscaves_1010_tremorzilla_beam_probe import (
    CLASS, CLASS_SHA, method_name, method_digest
)
from alexscaves_1010_tremorzilla_normal_cfg_probe import normal_edges

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
OLD_BEAM = DIR / "EXACT-TREMORZILLA-BEAM-1.0.10.json"
OLD_WORLD = DIR / "EXACT-TREMORZILLA-WORLD-LOS-1.0.10.json"
OLD_NORMAL = DIR / "EXACT-TREMORZILLA-NORMAL-CFG-1.0.10.json"
FACTORY = BASE + "server/misc/ACDamageTypes.class"
FACTORY_SHA = "389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6"
ENCHANT = "data/alexscaves/damage_type/tremorzilla_beam.json"
DAMAGE_JSON_SHA = "a059d2c010509db8d56f984d6d403a8901d1442d0ba47eff2f009c6998b58e9a"
EXPECTED = (
    "hurtEntitiesAround", "tickBreath", "canEntityBeHurtByBeam",
    "breakBlocksAround", "tick", "tickBeamTargeting", "stompEffect",
    "createInitialBeamVec", "getBeamShootFrom", "getMaxBeamBreakLength",
    "setMaxBeamBreakLength", "getCharge"
)
CALLERS = {
    "tick": [1455, 1537, 1558, 1579, 1599, 1619, 1863],
    "tickBreath": [552, 578],
    "stompEffect": [357],
}
DAMAGE_ANCHORS = {
    65: ("ifeq", "82", ""),
    76: ("invokestatic", "", "causeTremorzillaBeamDamage:"),
    87: ("invokevirtual", "", "DamageSources.mobAttack:"),
    101: ("getstatic", "", "NO_CREATIVE_OR_SPECTATOR"),
    104: ("invokevirtual", "", "getEntitiesOfClass:"),
    139: ("invokevirtual", "", "LivingEntity.is:"),
    148: ("invokevirtual", "", "isAlliedTo:"),
    193: ("invokevirtual", "", "distanceToSqr:"),
    213: ("invokevirtual", "", "canEntityBeHurtByBeam:"),
    226: ("instanceof", "", "KaijuMob"),
    237: ("invokestatic", "", "ACCompat.hurt:"),
    240: ("ifeq", "352", ""),
    285: ("invokevirtual", "", "knockbackTarget:"),
    295: ("invokevirtual", "", "getHealth:"),
    305: ("instanceof", "", "monster/Enemy"),
    318: ("putfield", "", "killCountFromBeam"),
    327: ("getstatic", "", "IRRADIATED"),
    341: ("sipush", "6000", ""),
    344: ("iconst_2", "", ""),
    345: ("invokespecial", "", "MobEffectInstance"),
    348: ("invokevirtual", "", "addEffect:"),
    352: ("goto", "114", "")
}
# Damage/targeting and block-world producer sites are distinct, not one cast.
BREATH = {
    4: ("invokevirtual", "Level.isClientSide:"),
    393: ("invokevirtual", "Level.clip:"),
    494: ("getfield", "devastatingTremorzillaBeam"),
    525: ("invokevirtual", "breakBlocksAround:"),
    552: ("invokevirtual", "hurtEntitiesAround:"),
    578: ("invokevirtual", "hurtEntitiesAround:"),
    585: ("getfield", "devastatingTremorzillaBeam"),
    620: ("invokevirtual", "breakBlocksAround:"),
}
LOS = {27: ("getstatic", "ClipContext$Block.COLLIDER"),
       30: ("getstatic", "ClipContext$Fluid.NONE"),
       37: ("invokevirtual", "Level.clip:"),
       40: ("invokevirtual", "BlockHitResult.getType:")}
BLOCK = {12: ("invokestatic", "ACPlatform.canEntityGrief:"),
         22: ("invokevirtual", "Level.isClientSide:"),
         249: ("invokevirtual", "Level.destroyBlock:"),
         268: ("invokestatic", "ACCompat.onBlockExploded:"),
         296: ("invokestatic", "ACCompat.createEntity:"),
         349: ("invokevirtual", "Level.addFreshEntity:")}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pairs(xs):
    out = {}
    for k, v in xs:
        require(k not in out, "duplicate JSON key "+k)
        out[k] = v
    return out

def load(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def method_index(methods):
    d={}
    for m in methods:
        key=(method_name(m),m["descriptor"])
        require(key not in d, "duplicate JVM method "+str(key))
        d[key]=m
    return d

def method(m, name, descriptor=None):
    rows=[x for (n,d),x in m.items() if n==name and
          (descriptor is None or descriptor==d)]
    require(len(rows)==1, "ambiguous/missing compiled method "+name)
    return rows[0]

def at(m, offset, opcode, token="", operand=""):
    rows=[x for x in m["instructions"] if x["offset"]==offset]
    require(len(rows)==1 and rows[0]["opcode"]==opcode,
            "missing/wrong JVM opcode @"+str(offset))
    r=rows[0]
    require(token in r["symbol"] and
            (not operand or r["operand"]==operand),
            "JVM token/operand drift @"+str(offset))
    return r

def anchors(m, targets, *, triples=False):
    for offset, spec in targets.items():
        if triples:
            opcode, operand, token = spec
        else:
            opcode, token = spec
            operand = ""
        at(m, offset, opcode, token, operand)

def merge_rosters(beam, world, normal):
    expected={}
    for row in beam["selected_method_digests"]:
        key=(row["name"],row["descriptor"])
        expected[key]=row["sha256"]
    for row in world["method_signatures_and_digests"]:
        key=(row["name"],row["descriptor"])
        if key in expected:
            require(expected[key]==row["sha256"], "contradictory historical digest")
        expected[key]=row["sha256"]
    for row in normal["methods"]:
        key=(row["name"],row["descriptor"])
        if key in expected:
            require(expected[key]==row["method_sha256"], "contradictory CFG digest")
        expected[key]=row["method_sha256"]
    require(set(n for n,d in expected)==set(EXPECTED)
            and len(expected)==len(EXPECTED),
            "incomplete compiled native full-method census")
    return expected

def factory_audit(jar, javap_bin):
    parsed=method_index(parse_methods(javap(javap_bin, jar, FACTORY[:-6].replace("/","."))))
    factory=method(parsed, "causeTremorzillaBeamDamage")
    symbols=[r["symbol"] for r in factory["instructions"]]
    require(any("TREMORZILLA_BEAM" in s for s in symbols),
            "DamageSource factory does not read TREMORZILLA_BEAM")
    require(any("DamageSourceRandomMessages" in s for s in symbols),
            "DamageSource subclass constructor absent")
    require(any(r["opcode"]=="areturn" for r in factory["instructions"]),
            "DamageSource factory lacks return")
    return {"owner":FACTORY,"name":"causeTremorzillaBeamDamage",
            "descriptor":factory["descriptor"],
            "parsed_method_sha256":method_digest(factory),
            "instructions":len(factory["instructions"]),
            "reference_tokens":[s for s in symbols
                                if ("TREMORZILLA_BEAM" in s or
                                    "DamageSourceRandomMessages" in s)]}

def audit(jar, javap_bin, inspect=False):
    require(sha_file(jar)==(SHA1,SHA256,SIZE), "wrong publisher SHA1/SHA256/size")
    beam, world, normal = load(OLD_BEAM), load(OLD_WORLD), load(OLD_NORMAL)
    identity={"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE}
    for old in (beam,world,normal):
        require(old["artifact"]==identity and old["class_sha256"]==CLASS_SHA,
                "inconsistent previously sealed publisher/JVM identity")
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        require(len(names)==len(set(names)), "duplicate JAR members")
        require(sha(z.read(CLASS))==CLASS_SHA,"Tremorzilla entity physical SHA drift")
        require(sha(z.read(FACTORY))==FACTORY_SHA,"DamageSources physical SHA drift")
        raw=z.read(ENCHANT)
        require(sha(raw)==DAMAGE_JSON_SHA, "native damage_type resource SHA drift")
        data=json.loads(raw,object_pairs_hook=pairs)
        require(data=={"message_id":"tremorzilla_beam","scaling":"never",
                       "exhaustion":0.3},
                "native damage_type JSON drift")
        # Direct tags are checked only in the published JAR, not in live datapack.
        direct_tags=[]
        for p in names:
            if p.startswith("data/") and "/tags/damage_type/" in p and p.endswith(".json"):
                doc=json.loads(z.read(p),object_pairs_hook=pairs)
                if ENCHANT.removeprefix("data/alexscaves/damage_type/").removesuffix(".json") in str(doc):
                    direct_tags.append(p)
    methods=parse_methods(javap(javap_bin, jar, CLASS[:-6].replace("/", ".")))
    require(len(methods)==116, "TremorzillaEntity method population drift")
    indexed=method_index(methods)
    expected=merge_rosters(beam,world,normal)
    require(len(expected)==12,"expected 12 native methods")
    census=[]
    for (name,desc),digest in sorted(expected.items()):
        compiled=indexed.get((name,desc))
        require(compiled is not None,"missing native full method "+name)
        require(method_digest(compiled)==digest,
                "native full method SHA drift: "+name)
        # Bytecode branch destinations including fallthrough, fail closed on
        # unsupported JVM control transfers for the selected normal-CFG bodies.
        if name in ("tickBreath","canEntityBeHurtByBeam","breakBlocksAround"):
            graph=normal_edges(compiled["instructions"])
            require(len(graph)==len(compiled["instructions"]),
                    "CFG instructions differ from method body")
        census.append({"name":name,"descriptor":desc,
                       "instruction_count":len(compiled["instructions"]),
                       "method_sha256":digest})
    damage=method(indexed,"hurtEntitiesAround",
                  "(Lnet/minecraft/world/phys/Vec3;FFFZZZ)Z")
    require(len(damage["instructions"])==169,
            "native beam damage helper instruction drift")
    anchors(damage,DAMAGE_ANCHORS,triples=True)
    anchors(method(indexed,"tickBreath"),BREATH)
    anchors(method(indexed,"canEntityBeHurtByBeam"),LOS)
    anchors(method(indexed,"breakBlocksAround"),BLOCK)
    callers={}
    for name,offsets in CALLERS.items():
        m=method(indexed,name)
        actual=[x["offset"] for x in m["instructions"]
                if x["opcode"].startswith("invoke")
                and "hurtEntitiesAround:" in x["symbol"]]
        require(actual==offsets,"direct local caller roster drift: "+name)
        callers[name]=actual
    allCallers={}
    for m in methods:
        relevant=[x["offset"] for x in m["instructions"]
                  if x["opcode"].startswith("invoke")
                  and "hurtEntitiesAround:" in x["symbol"]]
        if relevant:
            allCallers[method_name(m)]=relevant
    require(allCallers==callers,"unexpected additional direct helper caller")
    factory=factory_audit(jar,javap_bin)
    report={
      "schema_version":1,
      "claim_scope":"STATIC_DAMAGE_TYPE_EVIDENCE_CANDIDATE_ONLY",
      "enchantment":"alexscaves:tremorzilla_beam",
      "artifact":identity,
      "class_sha256":{CLASS:CLASS_SHA, FACTORY:FACTORY_SHA},
      "resource":{ENCHANT:{"sha256":DAMAGE_JSON_SHA,"json":data}},
      "declared_methods":len(methods),
      "native_full_method_census":census,
      "native_damage_factory":factory,
      "producer_calls":callers,
      "damage_helper_opcode_pivots":len(DAMAGE_ANCHORS),
      "direct_damage_tags_in_publisher":direct_tags,
      "safety":{
        "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
        "mutation":"NO_MUTATION","provider_universe_closed":False,
        "gameplay_hit_damage":"NOT_CERTIFIED","pvp_claims":"NOT_VERIFIED",
        "world_effect_policy":"NOT_VERIFIED","effective_datapack_tags":"NOT_VERIFIED",
      },
    }
    if inspect:
        for n,ranges in (
            ("hurtEntitiesAround",((0,360),)),
            ("canEntityBeHurtByBeam",((0,100),)),
            ("tickBreath",((0,105),(340,655))),
            ("breakBlocksAround",((0,100),(120,285),(286,360))),
            ("getMaxBeamBreakLength",((0,120),)),
            ("getCharge",((0,80),)),
        ):
            m=method(indexed,n)
            print("=== ANALYSIS",n,"BEGIN ===")
            for x in m["instructions"]:
                if any(lo<=x["offset"]<=hi for lo,hi in ranges):
                    print(f'{x["offset"]}: {x["opcode"]} {x["operand"]} // {x["symbol"]}')
            print("=== ANALYSIS",n,"END ===")
    return report

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",type=Path,required=True)
    ap.add_argument("--javap",default="javap")
    ap.add_argument("--seal",type=Path)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--inspect",action="store_true")
    args=ap.parse_args()
    report=audit(args.jar,args.javap,inspect=args.inspect)
    if args.seal:
        require(report==load(args.seal), "candidate Tremorzilla beam seal changed")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",
                               encoding="utf-8")
    print("TREMORZILLA_BEAM_STABLE_REPLAY",json.dumps({
        "methods":len(report["native_full_method_census"]),
        "instructions":sum(m["instruction_count"] for m in report["native_full_method_census"]),
        "factory":report["native_damage_factory"]["parsed_method_sha256"],
        "helper_pivots":report["damage_helper_opcode_pivots"],
        "callers":report["producer_calls"],
        "safety":report["safety"]
    },ensure_ascii=False))
if __name__=="__main__":
    main()
