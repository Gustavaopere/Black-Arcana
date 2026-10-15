#!/usr/bin/env python3
"""Vampirism 1.10.13 exact SHA-gated *compiled* player action audit.

Read-only Java 21 classfile inspection. This proves registered static action
identities and their constructor suppliers, never loaded registry or Survival.
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

JAR_NAME="Vampirism-1.21-1.10.13.jar"
SHA1="349b6e4ea893c98a580775b1725399903e222228"
SOURCE_PIN="e1ed095713cef5e9eb151d0ee58908fa830d6bb7"
ROOT="de.teamlapen.vampirism.entity.player."
GROUPS={
    "vampire.actions.VampireActions":{
        "bat":("BAT","BatVampireAction"),
        "dark_blood_projectile":("DARK_BLOOD_PROJECTILE","DarkBloodProjectileAction"),
        "disguise_vampire":("DISGUISE_VAMPIRE","DisguiseVampireAction"),
        "freeze":("FREEZE","FreezeVampireAction"),
        "half_invulnerable":("HALF_INVULNERABLE","HalfInvulnerableAction"),
        "regen":("REGEN","RegenVampireAction"),
        "sunscreen":("SUNSCREEN","SunscreenVampireAction"),
        "summon_bat":("SUMMON_BAT","SummonBatVampireAction"),
        "teleport":("TELEPORT","TeleportVampireAction"),
        "vampire_invisibility":("VAMPIRE_INVISIBILITY","InvisibilityVampireAction"),
        "vampire_rage":("VAMPIRE_RAGE","RageVampireAction"),
        "hissing":("HISSING","HissingAction"),
        "infect":("INFECT","InfectAction"),
        "jump_boost":("JUMP_BOOST","JumpBoostAction")
    },
    "hunter.actions.HunterActions":{
        "awareness_hunter":("AWARENESS_HUNTER","AwarenessHunterAction"),
        "disguise_hunter":("DISGUISE_HUNTER","DisguiseHunterAction"),
        "potion_resistance_hunter":("POTION_RESISTANCE_HUNTER","PotionResistanceHunterAction")
    },
    "lord.actions.LordActions":{
        "lord_speed":("LORD_SPEED","SpeedLordAction"),
        "lord_attack_speed":("LORD_ATTACK_SPEED","AttackSpeedLordAction")
    }
}

class AuditError(ValueError):
    pass

def expected():
    if [len(g) for g in GROUPS.values()] != [14,3,2]:
        raise AuditError("expected 14/3/2 static action breakdown changed")
    combined=[k for g in GROUPS.values() for k in g]
    if len(combined)!=19 or len(set(combined))!=19:
        raise AuditError("19 action ID manifest drift")
    return {k:ROOT+k for k in GROUPS}

def code_instructions(blob: str):
    result=[]
    for match in re.finditer(r"^\s*(\d+):\s+([a-z][\w]*)([^\n]*)$",blob,re.M):
        tail=match.group(3)
        operand=tail.split("//",1)[0].strip()
        comment=tail.split("//",1)[1].strip() if "//" in tail else ""
        result.append((int(match.group(1)),match.group(2),operand,comment))
    return result

def compiled_static_initializer(disassembly: str):
    m=re.search(r"^  static \{\};$",disassembly,re.M)
    if m is None: raise AuditError("compiled action registry lacks class initializer")
    rest=disassembly[m.end():]
    body=re.search(r"^    Code:$",rest,re.M)
    if body is None: raise AuditError("compiled initializer lacks Code")
    after=rest[body.end():]
    end=re.search(r"^      (?:LineNumberTable|LocalVariableTable|StackMapTable):",after,re.M)
    if not end: raise AuditError("compiled initializer footer missing")
    return code_instructions(after[:end.start()])

def bootstrap_constructors(disassembly: str):
    section=re.search(r"^BootstrapMethods:\s*$",disassembly,re.M)
    if not section: raise AuditError("compiled LambdaMetafactory bootstrap table absent")
    result={}
    idx=None
    is_lambda=False
    for line in disassembly[section.end():].splitlines():
        m=re.match(r"^  (\d+):\s+(.+)$",line)
        if m:
            idx=int(m.group(1))
            is_lambda=("LambdaMetafactory.metafactory:" in m.group(2))
            continue
        if line.startswith(("InnerClasses:","NestMembers:","Signature:")):
            break
        if idx is not None and "REF_newInvokeSpecial" in line:
            if not is_lambda: raise AuditError("constructor handle outside LambdaMetafactory")
            ref=re.search(r'REF_newInvokeSpecial\s+([\w/$]+)\."<init>":\(\)V',line)
            if not ref: raise AuditError("unexpected action supplier constructor signature")
            if idx in result: raise AuditError("more than one constructor for bootstrap")
            result[idx]=ref.group(1).replace("/",".").split(".")[-1]
    return result

def verify_bus_registration(disassembly: str):
    match=re.search(r"^  public static void register\([^\n;]*IEventBus\);$",disassembly,re.M)
    if not match: raise AuditError("action DeferredRegister bus hook absent")
    rest=disassembly[match.end():]
    body=re.search(r"^    Code:$",rest,re.M)
    if not body: raise AuditError("bus registration hook has no compiled Code")
    next_method=re.search(r"^  (?:public|private|protected|static) ",rest[body.end():],re.M)
    sample=rest[body.end():][:next_method.start() if next_method else 1500]
    ins=code_instructions(sample)
    if not (any(op=="getstatic" and "ACTIONS:" in comment for _,op,_,comment in ins)
            and any(op=="aload_0" for _,op,_,_ in ins)
            and any(op in ("invokevirtual","invokeinterface")
                    and "DeferredRegister.register:" in comment for _,op,_,comment in ins)):
        raise AuditError("bus register hook does not forward ACTIONS to IEventBus")

def parse_registry(disassembly: str, wanted: dict[str, tuple[str,str]]):
    expected()
    bs=bootstrap_constructors(disassembly)
    ins=compiled_static_initializer(disassembly)
    if not any(op in ("invokestatic",) and "DeferredRegister.create:" in comment
               for _,op,_,comment in ins):
        raise AuditError("DeferredRegister creation absent")
    if not any(op=="ldc" and "String vampirism" in comment for _,op,_,comment in ins):
        raise AuditError("wrong or unresolved provider namespace")
    if not any(op=="getstatic" and "VampirismRegistries$Keys.ACTION:" in comment
               for _,op,_,comment in ins):
        raise AuditError("provider ACTION registry key not proven")
    result={}
    for pos,(_,op,_,comment) in enumerate(ins):
        if op not in ("invokevirtual","invokeinterface") or "DeferredRegister.register:" not in comment:
            continue
        if pos<3 or pos+1>=len(ins):
            raise AuditError("truncated action registration flow")
        get, literal, supplier=ins[pos-3:pos]
        put=ins[pos+1]
        if not (get[1]=="getstatic" and "Field ACTIONS:" in get[3]
                and literal[1] in ("ldc","ldc_w") and literal[3].startswith("String ")
                and supplier[1]=="invokedynamic"
                and put[1]=="putstatic" and "Field " in put[3]):
            raise AuditError("action registration is not direct ACTIONS→id→factory→field")
        name=literal[3][7:]
        field=re.search(r"Field ([A-Z0-9_]+):",put[3])
        bootstrap=re.search(r"InvokeDynamic #(\d+):",supplier[3])
        if not field or not bootstrap:
            raise AuditError("cannot resolve action field or lambda bootstrap")
        owner=bs.get(int(bootstrap.group(1)))
        if not owner:
            raise AuditError("action supplier is not a direct constructor handle: "+name)
        if name in result: raise AuditError("duplicate player action ID: "+name)
        result[name]=(field.group(1),owner)
    if len(result)!=len(wanted) or set(result)!=set(wanted):
        raise AuditError("compiled player registry IDs differ from exact source pin: "+str({
            "missing":sorted(set(wanted)-set(result)),
            "extra":sorted(set(result)-set(wanted)),
            "count":len(result)
        }))
    mistakes={name:{"expected":wanted[name],"compiled":result[name]}
              for name in wanted if wanted[name]!=result[name]}
    if mistakes:
        raise AuditError("compiled action constructor or holder mismatch: "+
                         json.dumps(mistakes,sort_keys=True))
    verify_bus_registration(disassembly)
    return result

def javap(jar: Path, classname: str):
    try:
        cp=subprocess.run(["javap","-v","-c","-p","-classpath",str(jar),classname],
                          text=True,capture_output=True,check=False,timeout=60)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise AuditError("Java21 javap failed or timed out") from exc
    if cp.returncode or not 0<len(cp.stdout)<4_000_000:
        raise AuditError("compiled registry cannot be inspected: "+classname)
    return cp.stdout

def audit(jar: Path):
    groups=expected()
    if jar.name!=JAR_NAME or jar.is_symlink() or not jar.is_file():
        raise AuditError("wrong installed publisher JAR path or type")
    stat0=jar.stat()
    if not stat.S_ISREG(stat0.st_mode) or not 0<stat0.st_size<24_000_000:
        raise AuditError("publisher archive outside safety size boundary")
    stamp=lambda s:(s.st_dev,s.st_ino,s.st_mtime_ns,s.st_ctime_ns,s.st_size)
    raw=jar.read_bytes()
    if stamp(jar.stat())!=stamp(stat0): raise AuditError("publisher JAR mutated during read")
    sha1=hashlib.sha1(raw).hexdigest()
    if sha1!=SHA1: raise AuditError("publisher JAR SHA1 differs from installed modlist")
    sha256=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        if len(names)!=len(set(names)): raise AuditError("duplicate publisher ZIP entries")
        if not all(path.replace(".","/")+".class" in names for path in groups.values()):
            raise AuditError("one or more compiled faction action registry classfiles absent")
        if not any(k.startswith("META-INF/") and k.endswith("mods.toml") for k in names):
            raise AuditError("NeoForge mod metadata absent")
    observations={}
    for group,cls in groups.items():
        observations[group]=parse_registry(javap(jar.resolve(),cls),GROUPS[group])
    if stamp(stat0)!=stamp(jar.stat()) or hashlib.sha256(jar.read_bytes()).hexdigest()!=sha256:
        raise AuditError("publisher archive mutated during audit")
    return {
        "result":"PASS",
        "evidence_class":"SHA1_MATCHED_STATIC_NE0FORGE_DEFERRED_ACTION_REGISTRY_AND_CONSTRUCTOR_PROOF",
        "jar":JAR_NAME,"mod_id":"vampirism","version":"1.10.13",
        "physical_sha1":sha1,"publisher_sha256":sha256,"size_bytes":len(raw),
        "registry_counts":{k:len(v) for k,v in observations.items()},
        "unique_registered_player_actions":sum(map(len,observations.values())),
        "identities":{k:{name:{"holder":h,"constructor":ctor} for name,(h,ctor) in sorted(v.items())}
                      for k,v in observations.items()},
        "deviations":{},
        "not_proven":[
            "modpack boots 1.10.13 on exact NeoForge runtime or registered event bus executes",
            "active server configuration and faction skill unlock reachability",
            "blood/saturation/exhaustion and action cooldown settlement",
            "action activation success or effects in dedicated Survival",
            "client ActionWheel UI, multiplayer, relog/death/restart and Lord skill access",
            "Vampire Spells Addon, Bloodlines, Werewolves or other cross-mod interop",
            "RPG Skill Tree bridge or Black Arcana authority over provider actions"
        ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        report=audit(args.jar)
        exitcode=0
    except (AuditError,OSError,ValueError,zipfile.BadZipFile) as exc:
        report={"result":"FAIL_CLOSED","reason":str(exc)}
        exitcode=1
    output=json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding="utf8")
    print(output)
    return exitcode
if __name__=="__main__":
    raise SystemExit(main())
