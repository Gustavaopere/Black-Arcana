#!/usr/bin/env python3
"""SHA-1 gated, read-only physical resource audit: Eidolon 0.5.0.2.

42 distinct recipe identities, not a claim about RecipeManager/Survival.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import zipfile

JAR_NAME="eidolon_repraised-1.21.1-0.5.0.2.jar"
SHA1="1f05ffd2f9fa672dc2ecff3c32de092cdbcde989"
MOD_ID="eidolon_repraised"
RECIPE_ROOT="data/eidolon_repraised/recipe/"
CHANTS=frozenset("""dark_prayer dark_animal_sacrifice dark_touch darklight_chant
 dark_villager_sacrifice zombify_villager enthrall_spell light_prayer light_chant
 holy_touch lay_on_hands cure_zombie smite_chant sunder_armor reinforce_armor
 frost_touch fire_chant create_water""".split())
CONVERSIONS=frozenset("convert_inlay_holy convert_inlay_unholy convert_top_hat convert_disc".split())
GENERIC=frozenset("""crystal deceit allure repelling daylight moonlight purify
 recharging_soulfire recharging_chill absorption""".split())
SUMMONS=frozenset("""summon_zombie summon_skeleton summon_phantom summon_creeper
 summon_wither_skeleton summon_husk summon_drowned summon_stray summon_wraith
 summon_slimy_slug summon_raven""".split())
CRAFTING=frozenset("brazier_craft_sapping_sword brazier_craft_sanguine_amulet".split())
LOCATION=frozenset(["ritual_locate_catacombs"])
RITUALS=GENERIC|SUMMONS|CRAFTING|LOCATION
RITUAL_TYPES={
 "generic":"eidolon_repraised:ritual_brazier",
 "summon":"eidolon_repraised:ritual_brazier_summoning",
 "crafting":"eidolon_repraised:ritual_brazier_crafting",
 "location":"eidolon_repraised:ritual_brazier_location"
}
PROVIDER_RECIPE_TYPES={"eidolon_repraised:chant","eidolon_repraised:chant_conversion",*RITUAL_TYPES.values()}

class AuditError(ValueError):
    pass

def manifest():
    if tuple(map(len,(CHANTS,CONVERSIONS,GENERIC,SUMMONS,CRAFTING,LOCATION)))!=(18,4,10,11,2,1):
        raise AuditError("identity manifest cardinality drift")
    if len(CHANTS|CONVERSIONS|RITUALS)!=46:
        raise AuditError("overlapping semantic recipe identities")
    for k in CHANTS|CONVERSIONS|RITUALS:
        if not re.fullmatch(r"[a-z][a-z0-9_]*",k):
            raise AuditError("invalid recipe identity")

def ritual_type(name):
    if name in GENERIC: return RITUAL_TYPES["generic"]
    if name in SUMMONS: return RITUAL_TYPES["summon"]
    if name in CRAFTING: return RITUAL_TYPES["crafting"]
    if name in LOCATION: return RITUAL_TYPES["location"]
    raise AuditError("unknown ritual name "+name)

def read_recipe(z,name):
    info=z.getinfo(name)
    if not 2<info.file_size<250000:
        raise AuditError("unsafe recipe entry size "+name)
    obj=json.loads(z.read(info).decode("utf-8"))
    if not isinstance(obj,dict) or not isinstance(obj.get("type"),str):
        raise AuditError("invalid data recipe "+name)
    return obj

def validate(obj,stem,group):
    if group=="chant":
        signs=obj.get("signs")
        if obj.get("type")!="eidolon_repraised:chant" or obj.get("id")!=MOD_ID+":"+stem:
            raise AuditError("chant runtime ID/type mismatch "+stem)
        if not isinstance(signs,list) or not 2<=len(signs)<=16:
            raise AuditError("invalid ordered chant signs "+stem)
        if any(not isinstance(s,dict) or not re.fullmatch(r"eidolon_repraised:[a-z_]+",str(s.get("sign",""))) for s in signs):
            raise AuditError("invalid chant sign "+stem)
    elif group=="conversion":
        if obj.get("type")!="eidolon_repraised:chant_conversion":
            raise AuditError("chant conversion type mismatch "+stem)
        if not isinstance(obj.get("input"),dict) or not isinstance(obj.get("output"),dict) or not isinstance(obj["output"].get("id"),str):
            raise AuditError("conversion input/output invalid "+stem)
    elif group=="ritual":
        if obj.get("type")!=ritual_type(stem) or not isinstance(obj.get("reagent"),dict) or not isinstance(obj.get("pedestal_items"),list):
            raise AuditError("ritual recipe type/ingredients mismatch "+stem)
        if stem in GENERIC and obj.get("ritual")!=MOD_ID+":"+stem:
            raise AuditError("generic ritual provider ID mismatch "+stem)
        if stem in SUMMONS:
            output=(MOD_ID+":" if stem in {"summon_wraith","summon_slimy_slug","summon_raven"} else "minecraft:")+stem.removeprefix("summon_")
            if obj.get("output")!=output or type(obj.get("count")) is not int or obj["count"]<1:
                raise AuditError("summon output/count mismatch "+stem)
        if stem in CRAFTING and (not isinstance(obj.get("result"),dict) or not isinstance(obj["result"].get("id"),str) or obj.get("health_requirement") not in (20,40)):
            raise AuditError("crafting ritual result/health mismatch "+stem)
        if stem in LOCATION and obj.get("structure")!=MOD_ID+":catacombs":
            raise AuditError("locator structure ID mismatch "+stem)
    else:
        raise AuditError("unknown semantic recipe type")

def scan(z):
    manifest()
    entries=z.namelist()
    if len(entries)!=len(set(entries)): raise AuditError("duplicate JAR entries")
    try:
        meta=z.read("META-INF/neoforge.mods.toml")
    except KeyError as ex:
        raise AuditError("NeoForge mod metadata absent") from ex
    if len(meta)>250000 or not re.search(rb'\bmodId\s*=\s*["\x27]eidolon_repraised["\x27]',meta):
        raise AuditError("publisher modId mismatch")
    seen={"chants":set(),"rituals":set(),"conversions":set()}
    types=Counter()
    for path in entries:
        if not path.startswith(RECIPE_ROOT) or not path.endswith(".json"): continue
        tail=path[len(RECIPE_ROOT):]
        if tail.startswith("rituals/"):
            if tail.count("/")!=1: raise AuditError("nested ritual resource")
            stem=tail[len("rituals/"):-5]
            group="rituals"
            if stem not in RITUALS: raise AuditError("unknown packaged ritual "+stem)
            obj=read_recipe(z,path)
        else:
            obj=read_recipe(z,path)
            if obj["type"]=="eidolon_repraised:chant":
                group="chants"
            elif obj["type"]=="eidolon_repraised:chant_conversion":
                group="conversions"
            elif obj["type"] in RITUAL_TYPES.values():
                raise AuditError("ritual outside ritual folder "+tail)
            else:
                continue
            if "/" in tail: raise AuditError("unexpected nested spell recipe")
            stem=tail[:-5]
            if stem not in (CHANTS if group=="chants" else CONVERSIONS):
                raise AuditError("unknown packaged "+group+" identity "+stem)
        if stem in seen[group]: raise AuditError("duplicate semantic recipe ID "+stem)
        seen[group].add(stem)
        validate(obj,stem,{"chants":"chant","conversions":"conversion","rituals":"ritual"}[group])
        types[obj["type"]]+=1
    for group,expected in {"chants":CHANTS,"rituals":RITUALS,"conversions":CONVERSIONS}.items():
        if seen[group]!=expected:
            raise AuditError(group+" identities mismatch: "+json.dumps({"missing":sorted(expected-seen[group]),"extra":sorted(seen[group]-expected)}))
    return {"normal_chants":sorted(CHANTS),"ritual_recipes":sorted(RITUALS),
            "conversion_dependencies":sorted(CONVERSIONS),
            "ritual_type_counts":{k:types[k] for k in sorted(RITUAL_TYPES.values())},
            "semantic_magic_roots":42,
            "technical_spell_registry_excluded_from_normal_chants":["basic_incense","undead_lure"]}

def audit(path):
    if path.name!=JAR_NAME or path.is_symlink() or not path.is_file():
        raise AuditError("wrong or unsafe physical JAR path")
    before=path.stat()
    signature=lambda s:(s.st_dev,s.st_ino,s.st_mtime_ns,s.st_ctime_ns,s.st_size)
    if not stat.S_ISREG(before.st_mode) or not 0<before.st_size<16000000:
        raise AuditError("unsafe physical publisher size or mode")
    raw=path.read_bytes()
    if signature(path.stat())!=signature(before):
        raise AuditError("physical artifact changed during read")
    sha1=hashlib.sha1(raw).hexdigest()
    if sha1!=SHA1: raise AuditError("publisher JAR does not match physical installed SHA-1")
    sha256=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z: proof=scan(z)
    if signature(path.stat())!=signature(before) or hashlib.sha256(path.read_bytes()).hexdigest()!=sha256:
        raise AuditError("physical JAR changed during audit")
    return {"result":"PASS","evidence_class":"SHA_MATCHED_STATIC_PACKAGED_CHANT_RITUAL_JSON_NOT_RECIPE_MANAGER",
            "version":"0.5.0.2","mod_id":MOD_ID,"jar":JAR_NAME,"physical_sha1":sha1,
            "sha256":sha256,"size_bytes":len(raw),**proof,
            "not_proven":["20 Spells.init technical entries compiled and linked",
             "recipe serializer registration / loaded server RecipeManager / datapack overrides",
             "chants/rituals Survival unlock, configuration, mana and health settlement",
             "dedicated client, modpack, multiplayer, persistence or reload",
             "RPG Skill Tree adapter or transfer of Black Arcana spell runtime authority"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        report=audit(args.jar)
        status=0
    except (AuditError,OSError,UnicodeError,ValueError,zipfile.BadZipFile) as ex:
        report={"result":"FAIL_CLOSED","reason":str(ex)}
        status=1
    result=json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding="utf8")
    print(result)
    return status

if __name__=="__main__":
    raise SystemExit(main())
