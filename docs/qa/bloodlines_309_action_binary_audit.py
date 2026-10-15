#!/usr/bin/env python3
"""Installed-SHA-gated Bloodlines 3.0.9 compiled IAction registry identity auditor.

Physical static facts only: holder + ID + constructor + mod-bus register link.
Never asserts actual server registration, acquisition, lifecycle or action success.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import subprocess
import zipfile

from vampirism_11013_action_registry_binary_audit import (
    AuditError, bootstrap_constructors, compiled_static_initializer, code_instructions
)

JAR_NAME="bloodlines-1.21-3.0.9.jar"
SHA1="b14ff359c7530c0e40ca289cc023bd1c19a070af"
MOD_ID="bloodlines"
REGISTRY_CLASS="com.thedrofdoctoring.bloodlines.skills.actions.BloodlineActions"
MAIN_CLASS="com.thedrofdoctoring.bloodlines.Bloodlines"
SOURCE_PIN="TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c"
MANIFEST=json.loads(r"""{
  "gravebound_devour_soul_action": [
    "GRAVEBOUND_DEVOUR_SOUL",
    "GraveboundDevourSoulAction"
  ],
  "gravebound_soul_infusion_action": [
    "GRAVEBOUND_SOUL_INFUSION",
    "GraveboundSoulInfusionAction"
  ],
  "gravebound_lingering_devour": [
    "GRAVEBOUND_LINGERING_DEVOUR",
    "GraveboundLingeringDevourAction"
  ],
  "gravebound_soul_claiming": [
    "GRAVEBOUND_SOUL_CLAIMING",
    "GraveboundSoulClaimingAction"
  ],
  "gravebound_crit_action": [
    "GRAVEBOUND_SORCEROUS_STRIKE",
    "GraveboundCritStrikeAction"
  ],
  "gravebound_mist_form_action": [
    "GRAVEBOUND_MIST_FORM",
    "GraveboundMistFormAction"
  ],
  "gravebound_end_mist_form_action": [
    "GRAVEBOUND_END_FORM_ACTION",
    "GraveboundForceEndMistFormAction"
  ],
  "gravebound_phylactery_teleport_action": [
    "GRAVEBOUND_PHYLACTERY_TELEPORT_ACTION",
    "GraveboundPhylacteryTeleportAction"
  ],
  "gravebound_ghost_walk_action": [
    "GRAVEBOUND_GHOST_WALK_ACTION",
    "GraveboundGhostWalkAction"
  ],
  "gravebound_phylactery_soul_transfer_action": [
    "GRAVEBOUND_SOUL_PHYLACTERY_ACTION",
    "GraveboundSoulTransferPhylacteryAction"
  ],
  "gravebound_possession_action": [
    "GRAVEBOUND_POSSESSION_ACTION",
    "GraveboundPossessionAction"
  ],
  "gravebound_possession_swap_action": [
    "GRAVEBOUND_POSSESSION_SWAP_ACTION",
    "GraveboundPossessionSwapAction"
  ],
  "noble_celerity_action": [
    "NOBLE_CELERITY_ACTION",
    "NobleCelerityAction"
  ],
  "noble_mesmerise_action": [
    "NOBLE_MESMERISE_ACTION",
    "NobleMesmeriseAction"
  ],
  "noble_leeching_action": [
    "NOBLE_LEECHING_ACTION",
    "NobleLeechingAction"
  ],
  "noble_invisibility_action": [
    "NOBLE_INVISIBILITY_ACTION",
    "NobleInvisibilityAction"
  ],
  "noble_flank_action": [
    "NOBLE_FLANK_ACTION",
    "NobleFlankAction"
  ],
  "zealot_shadowwalk_action": [
    "ZEALOT_SHADOWWALK_ACTION",
    "ZealotShadowwalkAction"
  ],
  "zealot_darkcloak_action": [
    "ZEALOT_DARK_CLOAK_ACTION",
    "ZealotDarkCloakAction"
  ],
  "zealot_wall_climb_action": [
    "ZEALOT_WALL_CLIMB_ACTION",
    "ZealotWallClimbAction"
  ],
  "zealot_frenzy_action": [
    "ZEALOT_FRENZY_ACTION",
    "ZealotFrenzyAction"
  ],
  "ectotherm_frostlord_action": [
    "ECTOTHERM_FROST_LORD_ACTION",
    "EctothermFrostLord"
  ],
  "ectotherm_dolphin_leap_action": [
    "ECTOTHERM_DOLPHIN_LEAP_ACTION",
    "EctothermDolphinLeap"
  ],
  "ectotherm_ink_splash_action": [
    "ECTOTHERM_INK_SPLASH_ACTION",
    "EctothermInkSplash"
  ],
  "bloodknight_crimson_leap_action": [
    "BLOODKNIGHT_CRIMSON_LEAP",
    "BloodknightCrimsonLeap"
  ],
  "bloodknight_sanguine_infusion_action": [
    "BLOODKNIGHT_SANGUINE_INFUSION",
    "BloodknightSanguineInfusion"
  ],
  "bloodknight_blood_hunt_action": [
    "BLOODKNIGHT_BLOOD_HUNT",
    "BloodknightBloodHunt"
  ],
  "bloodknight_day_walker_action": [
    "BLOODKNIGHT_DAY_WALKER",
    "BloodknightDayWalker"
  ],
  "bloodknight_blood_extraction_action": [
    "BLOODKNIGHT_BLOOD_EXTRACTION",
    "BloodknightBloodExtraction"
  ]
}""")
EXCLUDED="gravebound_crit_action"

def validate_manifest():
    if len(MANIFEST)!=29 or len(set(MANIFEST))!=29 or EXCLUDED not in MANIFEST:
        raise AuditError("source-pinned Bloodlines 29/28/1 identity manifest drift")
    counts={}
    for key, pair in MANIFEST.items():
        group=key.split("_",1)[0]
        counts[group]=counts.get(group,0)+1
        if not re.fullmatch(r"[a-z][a-z0-9_]*",key) or not all(re.fullmatch(r"[A-Za-z0-9_]+",x) for x in pair):
            raise AuditError("unsafe manifest identity")
    if counts!={"gravebound":12,"noble":5,"zealot":4,"ectotherm":3,"bloodknight":5}:
        raise AuditError("source faction/action cardinalities changed")

def inspect_registry(disassembly):
    validate_manifest()
    bootstrap=bootstrap_constructors(disassembly)
    instructions=compiled_static_initializer(disassembly)
    if not any(op=="getstatic" and "VampirismRegistries$Keys.ACTION:" in comment for _,op,_,comment in instructions):
        raise AuditError("Vampirism ACTION registry key not used")
    if not any(op in ("invokestatic",) and "DeferredRegister.create:" in comment for _,op,_,comment in instructions):
        raise AuditError("DeferredRegister factory missing")
    if not any(op in ("ldc","ldc_w") and ("String bloodlines" in comment) for _,op,_,comment in instructions):
        # The mod ID may be obtained as a static constant getstatic, but this
        # requires an exact validated constant from the owning class.
        raise AuditError("Bloodlines namespace literal absent from registry bootstrap")
    hits={}
    for i,(_,op,_,comment) in enumerate(instructions):
        if op not in ("invokevirtual","invokeinterface") or "DeferredRegister.register:" not in comment:
            continue
        if i<3 or i+1>=len(instructions):raise AuditError("registration bytecode truncated")
        get,name,lambda_=instructions[i-3:i]
        field=instructions[i+1]
        if (get[1]!="getstatic" or "Field ACTIONS:" not in get[3]
                or name[1] not in ("ldc","ldc_w") or not name[3].startswith("String ")
                or lambda_[1]!="invokedynamic" or field[1]!="putstatic"):
            raise AuditError("action not direct ACTIONS → ID → supplier → DeferredHolder")
        act_id=name[3][7:]
        member=re.search(r"Field ([A-Z0-9_]+):",field[3])
        bootstrap_idx=re.search(r"InvokeDynamic #(\d+):",lambda_[3])
        if not member or not bootstrap_idx:
            raise AuditError("cannot resolve compiled field or supplier for "+act_id)
        constructor=bootstrap.get(int(bootstrap_idx.group(1)))
        if not constructor: raise AuditError("no direct constructor handle for "+act_id)
        if act_id in hits: raise AuditError("duplicate action ID "+act_id)
        hits[act_id]=[member.group(1),constructor]
    if set(hits)!=set(MANIFEST):
        raise AuditError("action registry exact ID mismatch: "+json.dumps({
            "missing":sorted(set(MANIFEST)-set(hits)),
            "extra":sorted(set(hits)-set(MANIFEST))},sort_keys=True))
    if hits!=MANIFEST:
        raise AuditError("compiled field → constructor mismatches: "+
                         json.dumps({k:[MANIFEST[k],hits[k]] for k in hits if hits[k]!=MANIFEST[k]},sort_keys=True))
    return hits

def verify_main_bus(disassembly, *, synthetic_local_bus=False):
    # Constrain to this mod's public @Mod constructor; a different method
    # merely mentioning register is not evidence.
    matches=list(re.finditer(r"^  public [^\n]*Bloodlines\([^\n]*IEventBus[^\n]*\);$",disassembly,re.M))
    if len(matches)!=1:raise AuditError("unique Bloodlines Mod(IEventBus...) ctor unavailable")
    after=disassembly[matches[0].end():]
    code=re.search(r"^    Code:$",after,re.M)
    if not code:raise AuditError("main mod constructor bytecode absent")
    rest=after[code.end():]
    end=re.search(r"^      (?:LineNumberTable|LocalVariableTable|StackMapTable):",rest,re.M)
    if not end:raise AuditError("main mod constructor Code footer missing")
    instr=code_instructions(rest[:end.start()])
    has_source=any(op=="getstatic" and "BloodlineActions.ACTIONS:" in comment for _,op,_,comment in instr)
    has_bus=any(op in ("aload_1","aload") and (op=="aload_1" or operand=="1") for _,op,operand,_ in instr)
    exact_descriptor=("DeferredRegister.register:(LIEventBus;)V" if synthetic_local_bus
                      else "DeferredRegister.register:(Lnet/neoforged/bus/api/IEventBus;)V")
    has_hook=any(op in ("invokevirtual","invokeinterface") and exact_descriptor in comment
                 for _,op,_,comment in instr)
    if not (has_source and has_bus and has_hook):
        raise AuditError("mod constructor does not forward BloodlineActions.ACTIONS to IEventBus")

def javap(path,qualified):
    try:
        r=subprocess.run(["javap","-v","-c","-p","-classpath",str(path),qualified],
                         text=True,capture_output=True,timeout=60,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise AuditError("javap Java21 unavailable") from exc
    if r.returncode or not 0<len(r.stdout)<5_000_000:
        raise AuditError("missing or unreadable compiled class "+qualified)
    return r.stdout

def audit(path):
    validate_manifest()
    if path.is_symlink() or path.name!=JAR_NAME or not path.is_file():
        raise AuditError("publisher filename/path invalid")
    before=path.stat()
    signature=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    if not stat.S_ISREG(before.st_mode) or not 0<before.st_size<12000000:
        raise AuditError("unsafe publisher archive size")
    raw=path.read_bytes()
    if signature(before)!=signature(path.stat()):raise AuditError("publisher JAR mutated during read")
    sha1=hashlib.sha1(raw).hexdigest()
    if sha1!=SHA1:raise AuditError("publisher SHA1 does not match installed physical")
    sha256=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        filenames=z.namelist()
        if len(filenames)!=len(set(filenames)):raise AuditError("duplicate ZIP archive members")
        for clazz in [REGISTRY_CLASS,MAIN_CLASS]:
            if clazz.replace(".","/")+".class" not in filenames:
                raise AuditError("required compiled registry or mod entrypoint absent "+clazz)
        try:meta=z.read("META-INF/neoforge.mods.toml")
        except KeyError as exc:raise AuditError("NeoForge mod metadata missing") from exc
        if len(meta)>250000 or not re.search(rb'\bmodId\s*=\s*["\x27]bloodlines["\x27]',meta):
            raise AuditError("publisher modId metadata mismatch")
    reg=inspect_registry(javap(path.resolve(),REGISTRY_CLASS))
    verify_main_bus(javap(path.resolve(),MAIN_CLASS))
    if signature(before)!=signature(path.stat()) or hashlib.sha256(path.read_bytes()).hexdigest()!=sha256:
        raise AuditError("publisher archive modified during audit")
    return {
      "result":"PASS","evidence_class":"SHA1_MATCHED_STATIC_IACTION_REGISTRY_HOLDER_CONSTRUCTOR_AND_MOD_EVENT_BUS_CALL",
      "mod_id":MOD_ID,"jar":JAR_NAME,"physical_sha1":sha1,
      "publisher_sha256":sha256,"size_bytes":len(raw),"source_pin":SOURCE_PIN,
      "registered_actions":29,"source_normally_reachable_actions":28,
      "excluded_registered_action":EXCLUDED,
      "faction_counts":{"gravebound":12,"noble":5,"zealot":4,"ectotherm":3,"bloodknight":5},
      "identities":dict(sorted(reg.items())),"deviations":{},
      "not_proven":["loaded registry or event-bus execution in assembled pack",
         "Gravebound tree/rank grant after datapack overrides or Sorcerous Strike actual unlock",
         "blood or Souls debit/credit and cooldown settlement",
         "skill-tree/point wallet persistence, reload, relog and respec",
         "activation success, effects or Survival gameplay",
         "client/server movement and Vampirism/addon cross-mod event ordering",
         "Black Arcana bridge or RPG Skill Tree provider authority"]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        proof=audit(args.jar);status=0
    except (AuditError,OSError,ValueError,zipfile.BadZipFile) as exc:
        proof={"result":"FAIL_CLOSED","reason":str(exc)};status=1
    output=json.dumps(proof,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding="utf8")
    print(output)
    return status
if __name__=="__main__":
    raise SystemExit(main())
