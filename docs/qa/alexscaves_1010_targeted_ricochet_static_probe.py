#!/usr/bin/env python3
"""Clean-room exact-JAR Targeted Ricochet / Gumball JVM auditor (read-only).

Proof limited to publisher 1.0.10, direct bytecode references, bounded
instruction windows, full parsed-method hashes, resources, and explicit CFG
anchors. It is NOT real-world physical QA or permission for a mutating hook.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from alexscaves_1010_damage_consumer_probe import (
    BASE, SHA1, SHA256, SIZE, javap, parse_methods, sha_file,
)
from alexscaves_1010_gumball_state_probe import name_of
from alexscaves_1010_raygun_local_flow_probe import digest_method

ID = "alexscaves:targeted_ricochet"
ENCH = "data/alexscaves/enchantment/targeted_ricochet.json"
TAG = "data/alexscaves/tags/item/enchantable/shot_gum.json"
LANG = "assets/alexscaves/lang/en_us.json"
GUM = BASE + "server/entity/item/GumballEntity.class"
SHOT = BASE + "server/item/ShotGumItem.class"
REG = BASE + "server/enchantment/ACEnchantmentRegistry.class"
GUM_SHA = "343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535"
SHOT_SHA = "08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238"
TAG_SHA = "3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d"
ENCH_SHA = "adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e"
REG_SHA = "60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32"
METHODS = {
    SHOT: ["acInventoryTick"],
    GUM: ["bounceFromDirection", "onHit", "onHitEntity",
          "defineSynchedData", "setTargetsOnBounce", "targetsOnBounce",
          "getMaximumBounces", "getBounces", "setBounces",
          "addAdditionalSaveData", "readAdditionalSaveData", "tick"],
}
FULL_SMALL_METHOD = {"setTargetsOnBounce", "targetsOnBounce",
                     "getMaximumBounces", "getBounces", "setBounces",
                     "addAdditionalSaveData", "readAdditionalSaveData"}
WINDOWS = {
    "acInventoryTick": [83, 138, 144, 147, 151, 152, 291, 306, 432, 434, 474, 518],
    "bounceFromDirection": [3, 7, 12, 19, 39, 42, 46, 54, 72, 86, 95,
                            101, 133, 149, 155, 172, 180, 193, 196,
                            203, 205, 209, 214, 217, 225, 227, 231,
                            238, 241, 248, 250, 260, 263, 266, 287,
                            318, 383, 395, 407, 420, 428, 441, 445, 458],
    "onHit": [2, 46, 54, 57, 64, 77, 80, 90, 98, 107, 155, 168],
    "onHitEntity": [6, 77, 86, 105, 113, 139, 144, 147, 284, 289,
                    296, 305, 308, 317, 326, 335, 338, 346],
    "defineSynchedData": [49, 52, 53, 56],
    "tick": [1, 176, 183, 190, 207, 242, 247],
}
METHOD_DIGEST_PRIOR = {
    ("acInventoryTick", SHOT): "6f9325406aaf142af4b415bff94b9123882b72a2ab981370d9be30a5e7c18093",
    ("bounceFromDirection", GUM): "0f687d784c92e2b8e7eebfc3cc9a85041b5fdfb37c6c5e4a32aaa2489df66282",
}
MAX_REPORT = 100000


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def row_slim(row: dict) -> dict:
    return {k: row[k] for k in ("offset", "opcode", "operand", "symbol")}


def select(methods: list[dict], name: str) -> dict:
    selected = [m for m in methods if name_of(m) == name]
    require(len(selected) == 1, "ambiguous/missing method " + name)
    return selected[0]


def anchors(method: dict, offsets: list[int]) -> list[dict]:
    instructions = method["instructions"]
    require(instructions and len(instructions) < 1700,
            "unbounded or missing method instructions " + name_of(method))
    byoff = {x["offset"]: i for i, x in enumerate(instructions)}
    require(len(byoff) == len(instructions),
            "duplicate JVM instruction offset " + name_of(method))
    require(len(offsets) <= 50, "excessive anchor count")
    chosen = []
    for off in offsets:
        require(off in byoff, "JVM anchor missing " + name_of(method) + ":" + str(off))
        idx = byoff[off]
        xs = instructions[max(0, idx-3):min(len(instructions), idx+5)]
        chosen.append({"offset": off, "window": [row_slim(x) for x in xs]})
    return chosen


def check(method: dict, specs: dict[int, tuple[str,str|None,str|None]]) -> None:
    byoff = {x["offset"]: x for x in method["instructions"]}
    for off, (opcode, symbol, target) in specs.items():
        x = byoff.get(off)
        require(x is not None and x["opcode"] == opcode and
                (symbol is None or symbol in x["symbol"]) and
                (target is None or x["operand"] == target),
                "publisher 1.0.10 CFG mismatch " + name_of(method) + " @" + str(off))


def certify(shot: dict, gum: dict) -> dict:
    check(shot, {
        138: ("getstatic", "TARGETED_RICOCHET", None),
        141: ("invokestatic", "ACCompat.enchantLevel:", None),
        144: ("ifle", None, "151"),
        147: ("iconst_1", None, None),
        151: ("iconst_0", None, None),
        152: ("istore", None, "9"),
        432: ("iload", None, "9"),
        434: ("invokevirtual", "setTargetsOnBounce:", None),
    })
    check(gum["bounceFromDirection"], {
        3: ("invokevirtual", "getBounces:", None),
        7: ("invokevirtual", "getMaximumBounces:", None),
        12: ("if_icmple", None, "38"),
        19: ("ifeq", None, "38"),
        39: ("invokevirtual", "targetsOnBounce:", None),
        42: ("ifeq", None, "290"),
        46: ("invokevirtual", "getOwner:", None),
        54: ("astore", None, "4"),
        72: ("ldc2_w", "double -10.0d", None),
        86: ("ldc2_w", "double 10.0d", None),
        101: ("invokevirtual", "Level.getEntitiesOfClass:", None),
        133: ("aload_3", None, None),
        140: ("invokevirtual", "is:", None),
        143: ("ifne", None, "200"),
        149: ("invokevirtual", "isAlliedTo:", None),
        152: ("ifne", None, "200"),
        155: ("aload_0", None, None),
        167: ("invokeinterface", "List.contains:", None),
        172: ("ifne", None, "200"),
        183: ("invokevirtual", "distanceTo:", None),
        189: ("invokevirtual", "distanceTo:", None),
        193: ("ifge", None, "200"),
        196: ("aload", None, "7"),
        205: ("ifnull", None, "290"),
        209: ("istore_2", None, None),
        214: ("invokevirtual", "Level.isClientSide:", None),
        217: ("ifne", None, "230"),
        227: ("invokevirtual", "setBounces:", None),
        238: ("if_icmple", None, "248"),
        242: ("invokevirtual", "discard:", None),
        250: ("invokevirtual", "getEyePosition:", None),
        260: ("invokevirtual", "Vec3.normalize:", None),
        263: ("ldc2_w", "double 0.800000011920929d", None),
        266: ("invokevirtual", "Vec3.scale:", None),
        287: ("invokevirtual", "setDeltaMovement:", None),
        318: ("ifne", None, "461"),
        420: ("ifne", None, "433"),
        430: ("invokevirtual", "setBounces:", None),
        441: ("if_icmple", None, "451"),
        445: ("invokevirtual", "discard:", None),
        458: ("invokevirtual", "setDeltaMovement:", None),
    })
    check(gum["onHit"], {
        2: ("invokespecial", "ThrowableProjectile.onHit:", None),
        54: ("invokevirtual", "bounceFromDirection:", None),
        98: ("invokevirtual", "getEntity:", None),
        107: ("invokeinterface", "List.add:", None),
        155: ("invokevirtual", "splitsOnHit:", None),
        168: ("invokevirtual", "bounceFromDirection:", None),
    })
    check(gum["onHitEntity"], {
        139: ("invokevirtual", "Entity.hurt:", None),
        144: ("invokevirtual", "splitsOnHit:", None),
        305: ("invokevirtual", "targetsOnBounce:", None),
        308: ("invokevirtual", "setTargetsOnBounce:", None),
        335: ("invokevirtual", "Level.addFreshEntity:", None),
    })
    check(gum["defineSynchedData"], {
        49: ("getstatic", "TARGETS_ON_BOUNCE:", None),
        52: ("iconst_0", None, None),
        56: ("invokevirtual", "SynchedEntityData$Builder.define:", None),
    })
    check(gum["addAdditionalSaveData"], {
        2: ("invokespecial", "ThrowableProjectile.addAdditionalSaveData:", None),
        13: ("invokevirtual", "CompoundTag.putInt:", None),
    })
    check(gum["readAdditionalSaveData"], {
        2: ("invokespecial", "ThrowableProjectile.readAdditionalSaveData:", None),
        13: ("invokevirtual", "setColor:", None),
    })
    return {
        "scope": "EXACT_COMPILED_SHOTGUM_TARGETED_BOUNCE_CONTRACT",
        "launch_gate": "positive enchantment level -> TARGETS_ON_BOUNCE=true",
        "search_box": "gumball eye position +/-10D per coordinate (20D cube AABB)",
        "candidate_type": "LivingEntity only",
        "candidate_filters": "not owner if present; not allied to owner when present; not in hitEntityIds",
        "target_order": "nearest eligible by Entity.distanceTo(projectile), no explicit line-of-sight call in own method",
        "targeted_velocity": "normalize(target eye - gumball position) * 0.800000011920929D",
        "bounce_count_authority": "increments when targeting found and server-side; discards if count>maximum",
        "no_target": "falls back to directional normal ricochet branch",
        "split_children": "onHitEntity copies TARGETS_ON_BOUNCE into three child constructions; owner copy not evidenced in this body",
        "own_NBT_flag": "TARGETS_ON_BOUNCE not written by own NBT overrides (only Color); inherited persistence NOT_VERIFIED",
        "effective_hit_and_world_policy": "NOT_TESTED",
        "mutating_hook": "NOT_VERIFIED",
        "physical_qa": "NOT_TESTED",
        "mutation": "NO_MUTATION",
    }


def inspect_binary(jar: Path, javap_bin: str) -> dict:
    require(jar.is_file() and sha_file(jar) == (SHA1,SHA256,SIZE),
            "unexpected physical publisher SHA/size")
    with zipfile.ZipFile(jar) as z:
        paths = z.namelist()
        require(len(paths) == len(set(paths)), "duplicate JAR entries")
        for p in (ENCH,TAG,LANG,GUM,SHOT,REG):
            require(p in paths, "missing publisher path " + p)
        parts = {p:z.read(p) for p in (ENCH,TAG,LANG,GUM,SHOT,REG)}
        hashes = {p:digest(b) for p,b in parts.items()}
        require(hashes[ENCH] == ENCH_SHA and hashes[TAG] == TAG_SHA and
                hashes[GUM] == GUM_SHA and hashes[SHOT] == SHOT_SHA and
                hashes[REG] == REG_SHA, "drift from publisher 1.0.10 member fingerprints")
        e = json.loads(parts[ENCH])
        tag = json.loads(parts[TAG])
        require(e.get("description",{}).get("translate") ==
                "enchantment.alexscaves.targeted_ricochet",
                "wrong enchantment resource")
        require(e.get("supported_items") == "#alexscaves:enchantable/shot_gum",
                "wrong enchantment item tag")
        require("alexscaves:shot_gum" in tag.get("values",[]), "Shot Gum not in tag")
        lang = json.loads(parts[LANG])
        locale = {k:v for k,v in lang.items() if
                  k.startswith("enchantment.alexscaves.targeted_ricochet")}
        classes = [p for p in paths if p.startswith(BASE) and p.endswith(".class")]
        require(100 <= len(classes) <= 3000, "JAR classfile count unexpected")
        hits = sorted(p for p in classes if b"TARGETED_RICOCHET" in z.read(p))
        require(SHOT in hits and REG in hits and len(hits)<=20,
                "TARGETED_RICOCHET unexpected direct consumer set")
        flag_hits = sorted(p for p in classes if b"TARGETS_ON_BOUNCE" in z.read(p))
        require(GUM in flag_hits and len(flag_hits)<=20,
                "TARGETS_ON_BOUNCE compiled field not located")
    methods:dict[str,dict] = {}
    for owner,names in METHODS.items():
        parsed = parse_methods(javap(javap_bin,jar,owner[:-6].replace("/", ".")))
        require(12 <= len(parsed) <= 100, "owner method census outside limits")
        result={}
        for name in names:
            method = select(parsed,name)
            rows=method["instructions"]
            require(1 <= len(rows) <= 1700, "unbounded method " + name)
            ordered=[x["offset"] for x in rows]
            require(ordered==sorted(set(ordered)), "invalid JVM instruction offsets")
            method_hash=digest_method(method)
            prior=METHOD_DIGEST_PRIOR.get((name,owner))
            if prior: require(method_hash==prior, "prior same-JAR complete method digest changed")
            offsets=WINDOWS.get(name,[])
            if name in FULL_SMALL_METHOD:
                require(len(rows) <= 20, "small method grew beyond budget")
                windowed=[{"offset":0,"window":[row_slim(x) for x in rows]}]
            else:
                windowed=anchors(method,offsets)
            result[name]={"descriptor":method["descriptor"],
                          "instruction_count":len(rows),
                          "parsed_method_sha256":method_hash,
                          "bounded_windows":windowed}
        methods[owner]=result
    # Compile-only contract CFG checks against freshly parsed methods,
    # not against information supplied by the report or earlier snapshots.
    parsed_shot=parse_methods(javap(javap_bin,jar,SHOT[:-6].replace("/", ".")))
    parsed_gum=parse_methods(javap(javap_bin,jar,GUM[:-6].replace("/", ".")))
    proof=certify(select(parsed_shot,"acInventoryTick"),
                  {name:select(parsed_gum,name) for name in METHODS[GUM]})
    report={
        "schema_version":1,
        "claim_scope":"TARGETED_RICOCHET_1010_SHA_EXACT_STATIC_CONTRACT",
        "artifact":{"sha1":SHA1,"sha256":SHA256,"bytes":SIZE},
        "resource":{"path":ENCH,"bytes":len(parts[ENCH]),"sha256":hashes[ENCH],"json":e},
        "item_tag":{"path":TAG,"sha256":hashes[TAG],"json":tag},
        "locale":{"path":LANG,"sha256":hashes[LANG],"own_keys":locale},
        "owner_class_hashes":{p:hashes[p] for p in (GUM,SHOT,REG)},
        "direct_scan":{"classfiles":len(classes),"ench_token_hits":hits,"synched_flag_hits":flag_hits},
        "methods":methods,
        "compiled_contract":proof,
        "limits":{"individual_static_contract":"CERTIFIED_STATIC_ONLY",
                  "valid_same_version":"1.0.10","whole_provider_closed":False,
                  "mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
                  "mutation":"NO_MUTATION","effective_ricochet":"NOT_TESTED",
                  "inherited_NBT":"NOT_VERIFIED","external_hooks":"NOT_VERIFIED",
                  "complete_third_party_runtime":"NOT_VERIFIED"}
    }
    return report


def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--javap",default="javap")
    p.add_argument("--seal",type=Path)
    p.add_argument("--output",type=Path)
    x=p.parse_args()
    report=inspect_binary(x.jar,x.javap)
    canonical=json.dumps(report,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    require(len(canonical.encode("utf8")) <= MAX_REPORT,
            "bounded clean-room report exceeds limit")
    if x.seal:
        require(json.loads(x.seal.read_text(encoding="utf8"))==report,
                "individual SHA-exact 1.0.10 seal mismatch")
    if x.output:
        x.output.parent.mkdir(parents=True,exist_ok=True)
        x.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",
                            encoding="utf8")
    print("TARGETED_RICOCHET_REPORT="+canonical)
    print("TARGETED_RICOCHET_AUDIT_READONLY_NO_MUTATION")


if __name__ == "__main__":
    main()
