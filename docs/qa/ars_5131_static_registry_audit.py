#!/usr/bin/env python3
"""Clean-room read-only Ars Nouveau 5.13.1 static registration callsite audit.

This audit proves registration CALLS and class owners in one SHA-equal JAR only.
It does NOT certify each ResourceLocation ID, registry execution or gameplay.
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

FILENAME = 'ars_nouveau-1.21.1-5.13.1.jar'
INSTALLED_SHA1 = '02782d071ee5fab3b5c4b8ced67b7e1748277dfd'
EXPECTED_SIZE = 20107711
OWNER = 'com.hollingsworth.arsnouveau.setup.registry.APIRegistry'
SPELL_CLASSES = '''
MethodProjectile MethodTouch MethodSelf MethodPantomime EffectBreak EffectHarm EffectIgnite
EffectPhantomBlock EffectHeal EffectGrow EffectKnockback EffectLight EffectDispel EffectLaunch
EffectPull EffectBlink EffectExplosion EffectLightning EffectSlowfall EffectFangs EffectSummonVex
AugmentAccelerate AugmentDecelerate AugmentSplit AugmentAmplify AugmentAOE AugmentExtendTime
AugmentPierce AugmentDampen AugmentExtract AugmentFortune EffectEnderChest EffectHarvest
EffectFell EffectPickup EffectInteract EffectPlaceBlock EffectSnare EffectSmelt EffectLeap
EffectDelay EffectRedstone EffectIntangible EffectInvisibility AugmentDurationDown EffectWither
EffectExchange EffectCraft EffectFlare EffectColdSnap EffectConjureWater EffectGravity EffectCut
EffectCrush EffectSummonWolves EffectSummonSteed EffectSummonDecoy EffectHex MethodUnderfoot
EffectGlide EffectRune EffectFreeze EffectName EffectSummonUndead EffectFirework EffectToss
EffectBounce AugmentSensitive EffectWindshear EffectEvaporate EffectLinger EffectSenseMagic
EffectInfuse EffectRotate EffectWall EffectAnimate EffectBurst AugmentRandomize EffectOrbit
EffectReset EffectWololo EffectRewind EffectBubble EffectWindburst EffectPrestidigitation
'''.split()
RITUAL_CLASSES = '''
RitualDig RitualMoonfall RitualCloudshaper RitualSunrise RitualDisintegration
RitualPillagerRaid RitualOvergrowth RitualBreed RitualHealing RitualWarp RitualScrying
RitualFlight RitualGravity RitualWildenSummoning RitualAnimalSummoning RitualBinding
RitualAwakening RitualHarvest RitualMobCapture ConjurePlainsRitual ForestationRitual
FloweringRitual ConjureDesertRitual DenySpawnRitual
'''.split()
class AuditError(ValueError):
    pass

def validate_manifest(spells=SPELL_CLASSES, rituals=RITUAL_CLASSES, enforce_counts=True):
    if enforce_counts and (len(spells), len(rituals)) != (85, 24):
        raise AuditError('manifest must contain 85 spell-part and 24 ritual owners')
    for label, entries in (('spell', spells), ('ritual', rituals)):
        if len(entries) != len(set(entries)):
            raise AuditError('duplicate '+label+' class')
        if any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9]*', x) for x in entries):
            raise AuditError('invalid '+label+' class identity')

def setup_instructions(disassembly):
    m = re.search(r'^  public static void setup\(\);\s*\n\s*Code:\s*$', disassembly, re.M)
    if not m:
        raise AuditError('APIRegistry.setup compiled Code not found')
    lines=[]
    for line in disassembly[m.end():].splitlines():
        match=re.match(r'^\s+(\d+):\s+(\w+)(.*?)$',line)
        if match:
            comment=match.group(3).split('//',1)[1].strip() if '//' in match.group(3) else ''
            lines.append((int(match.group(1)), match.group(2), comment))
            continue
        if line.strip() == '' and not lines:
            continue
        if lines:
            break
    if not lines or lines[-1][1] != 'return':
        raise AuditError('setup instruction list incomplete; terminal return missing')
    return lines

def class_from_field(comment):
    # javap prints either package/Class.FIELD or Class.FIELD depending on owner context.
    found=re.search(r'\bField\s+([\w/$]+)\.INSTANCE:',comment)
    if not found:
        raise AuditError('expected INSTANCE holder field before spell registration')
    return found.group(1).rsplit('/',1)[-1].rsplit('$',1)[-1]

def class_from_new(comment):
    m=re.search(r'\bclass\s+([\w/$]+)',comment)
    if not m:
        raise AuditError('expected constructor target class for ritual')
    return m.group(1).rsplit('/',1)[-1]

def parse(disassembly, spells=SPELL_CLASSES, rituals=RITUAL_CLASSES, enforce_counts=True):
    validate_manifest(spells, rituals, enforce_counts)
    ops=setup_instructions(disassembly)
    got_spells=[];got_rituals=[];registration_indexes=[]
    for i, (_pc, op, comment) in enumerate(ops):
        if op != 'invokestatic':
            continue
        match=re.search(r'\bMethod\s+(?:(?:[\w/$]+\.)?)(registerSpell|registerRitual):',comment)
        if not match:
            continue
        method=match.group(1)
        if i == 0:
            raise AuditError('register call without producer')
        if method == 'registerSpell':
            if ops[i-1][1] != 'getstatic':
                raise AuditError('spell register call not directly fed by static INSTANCE')
            got_spells.append(class_from_field(ops[i-1][2]))
        else:
            if i < 3 or [x[1] for x in ops[i-3:i]] != ['new','dup','invokespecial']:
                raise AuditError('ritual register call not directly fed by constructed owner')
            cls=class_from_new(ops[i-3][2])
            if '<init>' not in ops[i-1][2] or cls not in ops[i-1][2]:
                raise AuditError('ritual constructor target mismatch')
            got_rituals.append(cls)
        registration_indexes.append(i)
    if set(got_spells)!=set(spells) or len(got_spells)!=len(spells):
        raise AuditError('spell-part callsite mismatch: '+json.dumps({
            'expected_count':len(spells),'observed_count':len(got_spells),
            'missing': sorted(set(spells)-set(got_spells)),
            'extra':sorted(set(got_spells)-set(spells)),
            'duplicates':sorted({x for x in got_spells if got_spells.count(x)>1})}))
    if set(got_rituals)!=set(rituals) or len(got_rituals)!=len(rituals):
        raise AuditError('ritual callsite mismatch: '+json.dumps({
            'expected_count':len(rituals),'observed_count':len(got_rituals),
            'missing': sorted(set(rituals)-set(got_rituals)),
            'extra':sorted(set(got_rituals)-set(rituals)),
            'duplicates':sorted({x for x in got_rituals if got_rituals.count(x)>1})}))
    if not registration_indexes:
        raise AuditError('no static registrations')
    relevant=ops[registration_indexes[0]-1:registration_indexes[-1]+1]
    if any(op.startswith(('if','goto','jsr','tableswitch','lookupswitch')) for _,op,_ in relevant):
        raise AuditError('conditional jump found between registration callsites')
    if any(op.startswith('invoke') and ('registerSpell:' in c or 'registerRitual:' in c) and op!='invokestatic'
           for _,op,c in ops):
        raise AuditError('unexpected indirect register calls')
    return {'spell_class_owners':got_spells, 'ritual_class_owners':got_rituals,
            'count_spell_parts':len(got_spells),'count_rituals':len(got_rituals)}

def audit(jar):
    if jar.name!=FILENAME or jar.is_symlink() or not jar.is_file():
        raise AuditError('unexpected/unsafe publisher JAR')
    st=jar.stat()
    if not stat.S_ISREG(st.st_mode) or st.st_size!=EXPECTED_SIZE:
        raise AuditError('publisher size mismatch')
    blob=jar.read_bytes()
    ident=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    if ident(st)!=ident(jar.stat()):
        raise AuditError('JAR changed during read')
    sha1=hashlib.sha1(blob).hexdigest()
    if sha1!=INSTALLED_SHA1:
        raise AuditError('publisher SHA1 differs from installed modlist')
    with zipfile.ZipFile(io.BytesIO(blob)) as zipped:
        members=zipped.namelist()
        if len(members)!=len(set(members)):
            raise AuditError('duplicate archive members')
        if OWNER.replace('.','/')+'.class' not in members:
            raise AuditError('APIRegistry owner class missing')
        meta=zipped.read('META-INF/neoforge.mods.toml')
        if not re.search(rb'\bmodId\s*=\s*["\x27]ars_nouveau["\x27]',meta):
            raise AuditError('incorrect NeoForge mod ID')
    try:
        dis=subprocess.run(['javap','-c','-p','-classpath',str(jar.resolve()),OWNER],
                           capture_output=True,text=True,timeout=70,check=False)
    except (OSError,subprocess.TimeoutExpired) as e:
        raise AuditError('javap 21 unavailable or timed out') from e
    if dis.returncode or not 0<len(dis.stdout)<2500000:
        raise AuditError('compiled APIRegistry javap failed')
    classes=parse(dis.stdout)
    if ident(st)!=ident(jar.stat()) or hashlib.sha1(jar.read_bytes()).hexdigest()!=sha1:
        raise AuditError('publisher JAR changed during audit')
    return {
        'status':'PASS','evidence_class':'SHA_MATCHED_COMPILED_REGISTRATION_CLASS_CALLS_ONLY',
        'filename':FILENAME,'mod_id':'ars_nouveau','version':'5.13.1',
        'physical_sha1':sha1,'publisher_sha256':hashlib.sha256(blob).hexdigest(),
        'bytes':len(blob),**classes,
        'not_verified':['per-class ResourceLocation IDs','loaded GlyphRegistry/RitualRegistry',
                        'configuration and player learning','mana and Source settlement',
                        'spell composition/casting and rituals in Survival',
                        'RPG Skill Tree adapter and Black Arcana world policy interactions']}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--jar',type=Path,required=True)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    try:
        result=audit(args.jar)
        code=0
    except (AuditError,OSError,ValueError,zipfile.BadZipFile,KeyError) as exc:
        result={'status':'FAIL_CLOSED','reason':str(exc)}
        code=1
    payload=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload)
    print(payload)
    return code
if __name__=='__main__':
    raise SystemExit(main())
