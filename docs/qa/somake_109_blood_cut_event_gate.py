#!/usr/bin/env python3
"""Bounded clean-room survey for Blood Cut event registration metadata.

Inspect symbolic class/method annotations and JVM callsites only. No provider
method body, classfiles, proprietary code or assets leave the CI runner.
"""
from __future__ import annotations
import re

DECL = re.compile(r'^  (?:public|protected|private)\b[^\n]*\([^;\n]*\);\s*$',re.M)
ANNOT = re.compile(r'(?m)^\s*\d+:\s+#\d+\([^\n)]*\)\s*\n\s+([A-Za-z_$][\w/$.-]*)\s*$')


def annotation_scopes(verbose: str, method: str = 'onLivingDamage') -> dict:
    """Separate class annotations from one uniquely located method declaration.

    An annotation is *metadata*, not proof that the server has dispatched an event.
    """
    if not isinstance(verbose,str) or not 100 < len(verbose) < 1_500_000:
        raise ValueError('invalid/oversized class metadata')
    opens=re.search(r'(?m)^\{$',verbose)
    ends=re.search(r'(?m)^}$',verbose)
    if not opens or not ends or opens.end() >= ends.start():
        raise ValueError('class header/body boundary absent')
    body=verbose[opens.end():ends.start()]
    headers=list(DECL.finditer(body))
    hits=[(i,m) for i,m in enumerate(headers)
          if re.search(r'\b'+re.escape(method)+r'\([^;]*\);\s*$',m.group(0))]
    if len(hits)!=1:
        raise ValueError('event method absent or ambiguous')
    index,match=hits[0]
    until=headers[index+1].start() if index+1<len(headers) else len(body)
    section=body[match.end():until]
    own=re.search(r'(?m)^    RuntimeVisibleAnnotations:\s*$',section)
    method_content=section[own.end():] if own else ''
    tail=verbose[ends.end():]
    klass=re.search(r'(?m)^RuntimeVisibleAnnotations:\s*$',tail)
    class_content=tail[klass.end():] if klass else ''
    return {
        'method_annotations': sorted(set(ANNOT.findall(method_content)))[:20],
        'class_annotations': sorted(set(ANNOT.findall(class_content)))[:20],
    }

def certify_registration_annotations(metadata: dict) -> bool:
    """Fail closed on missing native registration declaration annotations."""
    if not isinstance(metadata, dict):
        raise ValueError("missing scoped class/method annotations")
    class_marker = "net.neoforged.fml.common.EventBusSubscriber"
    method_marker = "net.neoforged.bus.api.SubscribeEvent"
    if (class_marker not in metadata.get("class_annotations", ())
            or method_marker not in metadata.get("method_annotations", ())):
        raise ValueError("Blood Cut native class/method registration annotation drift")
    return True


def event_callsite_survey(rows: list[tuple[int,str,str,str]]) -> dict:
    """Report sparse member/guard coordinates, never a disassembled method."""
    if not 2 <= len(rows) <= 300:
        raise ValueError('event method size outside bounded proof')
    if [r[0] for r in rows] != sorted(set(r[0] for r in rows)):
        raise ValueError('malformed JVM instruction coordinates')
    call=lambda needle: [i for i,op,arg,comment in rows
                         if op.startswith('invoke') and needle in comment]
    applied=call('DamageSources.applyDamage:')
    read=call('LivingDamageEvent$Post.getNewDamage:')
    if len(applied)!=1 or len(read)!=1:
        raise ValueError('expected exactly one native secondary-damage call/read')
    branches=[(i,op) for i,op,arg,comment in rows if op.startswith(('if','goto'))]
    return {
        'instruction_count':len(rows),
        'branch_count':len(branches),
        'guard_opcodes':[op for _,op in branches],
        'damage_call_sites':applied,
        'host_damage_reads':read,
        'source_calls':call('LivingDamageEvent$Post.getSource:') + call('DamageSource.getEntity:'),
        'effect_reads':call('LivingEntity.getEffect:'),
        'amplifier_reads':call('MobEffectInstance.getAmplifier:'),
        'post_event_entity_reads':call('LivingDamageEvent$Post.getEntity:'),
        'damage_source_builds':call('BloodCutSpell.getDamageSource:'),
        'boundary':'Static call ordering does not prove eligibility, listener registration, branch truth, proc counts, recursion protection or delivered damage.',
    }


def inspect(jar) -> dict:
    """Release-exact inspection; only bounded semantic coordinates are exported."""
    import hashlib
    import subprocess
    import zipfile
    from pathlib import Path
    from somake_109_perk_method_probe import FILENAME, SHA1, GateError
    from somake_109_radius_irons_contract import sections, opcode_rows
    from somake_109_blood_cut_refs import discover_member, EFFECT_SUFFIX, EFFECT_PREFIX
    jar=Path(jar)
    if jar.is_symlink() or not jar.is_file() or jar.name != FILENAME:
        raise GateError('wrong physical artifact')
    blob=jar.read_bytes()
    if not 100 < len(blob) < 20_000_000 or hashlib.sha1(blob).hexdigest()!=SHA1:
        raise GateError('Somake exact installed/publisher hash mismatch')
    with zipfile.ZipFile(jar) as z:
        names=z.namelist()
        entry=discover_member(names,suffix=EFFECT_SUFFIX,prefix=EFFECT_PREFIX)
        meta=z.read('META-INF/neoforge.mods.toml')
        if len(meta)>250_000 or not re.search(rb"\bmodId\s*=\s*['\"]somakespells['\"]",meta):
            raise GateError('mod ID mismatch')
    clazz=entry[:-6].replace('/','.')
    def javap(*options):
        p=subprocess.run(['javap',*options,'-classpath',str(jar.resolve()),clazz],
                         text=True,capture_output=True,timeout=40,check=False)
        if p.returncode or not 100<len(p.stdout)<1_500_000:
            raise GateError('bounded javap failed')
        return p.stdout
    verbose=javap('-v','-p','-s')
    ann=annotation_scopes(verbose)
    certify_registration_annotations(ann)
    parsed=sections(javap('-p','-s','-c'))
    EXPECT={
      'onLivingDamage':'(Lnet/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post;)V',
      'getDamageModifier':'(ILnet/minecraft/world/entity/LivingEntity;)F',
    }
    result={}
    for name,desc in EXPECT.items():
        bodies=[opcode_rows(body) for n,d,body in parsed if n==name and d==desc]
        if len(bodies)!=1:raise GateError('method signature mismatch: '+name)
        rows=bodies[0]
        if name=='onLivingDamage':
            info=event_callsite_survey(rows)
            if info['branch_count']!=5:
                raise GateError('event 5-branch native fingerprint drift')
            result[name]=info
        else:
            count=sum(op.startswith(('if','goto')) for _,op,_,_ in rows)
            if count!=2:raise GateError('modifier 2-branch native fingerprint drift')
            result[name]={'instruction_count':len(rows), 'branch_count':count,
                          'entity_power_multiplier_reference':sum(
                              'BloodCutSpell.getEntityPowerMultiplier:' in c and op.startswith('invoke')
                              for _,op,_,c in rows)}
    if hashlib.sha1(jar.read_bytes()).hexdigest()!=SHA1:
        raise GateError('JAR changed during read')
    return {
      'status':'PASS_SHA_EXACT_BLOOD_CUT_EVENT_ANNOTATION_AND_CALLSITE_SURVEY',
      'mod_id':'somakespells','version':'1.0.9','artifact_sha1':SHA1,
      'effect_class':clazz,'annotations':ann,'methods':result,
      'limit':'Method/class annotations and symbolic callsite coordinates alone do not establish runtime event bus dispatch, mutation hooks, damage application, or per-player control.'
    }


def main():
    import argparse, json
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('--jar',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=inspect(args.jar)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('SOMAKE_BLOOD_CUT_EVENT_SURVEY', result['status'],result['artifact_sha1'])
    print('ANNOTATION_SCOPE',json.dumps(result['annotations'],sort_keys=True))
    print('DAMAGE_SITES',json.dumps(result['methods'],sort_keys=True))


if __name__=='__main__':
    main()
