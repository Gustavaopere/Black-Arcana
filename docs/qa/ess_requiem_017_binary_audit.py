#!/usr/bin/env python3
"""Read-only SHA-gated Requiem 0.1.7 classfile registration/identity audit.

Not a loaded registry, configuration, casting, or Survival verification.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import re
import stat
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

JAR_NAME = 'ess_requiem-0.1.7.jar'
SHA1 = 'c4648cced4f9e96527cfa4e3f5edcdcead43abb1'
MOD_ID = 'ess_requiem'
BASE = 'net.ender.ess_requiem.registries.GGSpellRegistry'
DTE = 'net.ender.ess_requiem.compat.dte.dte_registry.DTESpellRegistry'
CLASSES = {BASE: 55, DTE: 3}
MAX_BYTES = 32 * 1024 * 1024
ID_LINE = re.compile(r'^\| \x60ess_requiem:([a-z0-9_]+)\x60 \| (COUNTED_SOURCE_PINNED|EXCLUDED) \|', re.M)
INSTRUCTION = re.compile(r'^[ \t]*\d+:[ \t]+([\w]+)(?:[ \t]+[^/\n]*)?(?:[ \t]*//[ \t]*(.*))?$', re.M)
FIELD = re.compile(r'^\s*public static final java\.util\.function\.Supplier<[^\n]+\s+([A-Z0-9_]+);$', re.M)

class AuditError(ValueError):
    pass

def expected_inventory(markdown: str) -> dict[str, str]:
    matches = ID_LINE.findall(markdown)
    expected = dict(matches)
    if (len(matches), len(expected)) != (58, 58):
        raise AuditError('expected exactly 58 unique catalog spell IDs')
    if sum(x == 'EXCLUDED' for x in expected.values()) != 5:
        raise AuditError('expected exactly 5 excluded technical roots')
    if sum(x == 'COUNTED_SOURCE_PINNED' for x in expected.values()) != 53:
        raise AuditError('expected exactly 53 counted source roots')
    return expected

def instructions(disassembly: str) -> list[tuple[str, str]]:
    return [(m.group(1), (m.group(2) or '').strip()) for m in INSTRUCTION.finditer(disassembly)]

def registry_classes(disassembly: str, expected_count: int) -> dict[str, str]:
    if disassembly.count('  static {};') != 1:
        raise AuditError('registry static initializer missing or ambiguous')
    declarations, initializer = disassembly.split('  static {};', 1)
    fields = FIELD.findall(declarations)
    if len(fields) != expected_count or len(set(fields)) != expected_count:
        raise AuditError('registry Supplier fields do not match expected count')
    code = instructions(initializer)
    output = {}
    register_calls = 0
    for n, (op, comment) in enumerate(code):
        if op != 'invokestatic' or 'registerSpell:' not in comment:
            continue
        register_calls += 1
        if n < 3 or n + 1 >= len(code):
            raise AuditError('orphaned compiled registration')
        (newop, newcomment), (dupop, _), (ctorop, ctorcomment) = code[n-3:n]
        (storeop, storecomment) = code[n+1]
        if newop != 'new' or dupop != 'dup' or ctorop != 'invokespecial' or storeop != 'putstatic':
            raise AuditError('registration construction shape changed')
        classname = re.search(r'\bclass (net/ender/ess_requiem/[\w/$]+)$', newcomment)
        field = re.search(r'\bField ([A-Z][A-Z0-9_]*):', storecomment)
        if not classname or not field or '"<init>"' not in ctorcomment:
            raise AuditError('compiled registry class/field/constructor unknown')
        cl, f = classname.group(1).replace('/', '.'), field.group(1)
        if f in output:
            raise AuditError('duplicate registry field assignment')
        output[f] = cl
    if register_calls != expected_count or set(output) != set(fields):
        raise AuditError('compiled registrations differ from declared Supplier fields')
    if len(set(output.values())) != expected_count:
        raise AuditError('same spell implementation class reused for multiple registrations')
    return output

def spell_id(disassembly: str) -> str:
    if 'getSpellResource();' not in disassembly:
        raise AuditError('spell implementation has no getSpellResource contract')
    code = instructions(disassembly)
    hits = []
    for n, (op, comment) in enumerate(code):
        if op != 'invokestatic' or 'ResourceLocation.fromNamespaceAndPath:' not in comment:
            continue
        if n < 2 or n + 1 >= len(code):
            continue
        stringop, stringcomment = code[n-1]
        storeop, storecomment = code[n+1]
        if (stringop not in ('ldc', 'ldc_w') or not stringcomment.startswith('String ')
                or storeop != 'putfield' or not re.search(r'\bField spellId:', storecomment)):
            continue
        root = stringcomment[7:]
        if not re.fullmatch(r'[a-z][a-z0-9_]*', root):
            raise AuditError('malformed compiled spell root')
        hits.append(root)
    if len(hits) != 1:
        raise AuditError(f'expected one compiled spellId assignment, found {len(hits)}')
    getter = disassembly.split('getSpellResource();', 1)[1].split('\n  public ', 1)[0]
    if not re.search(r'getfield\s+[^\n]*// Field spellId:', getter) or not re.search(r'\bareturn\b', getter):
        raise AuditError('getSpellResource is not the stored spellId getter')
    return hits[0]

def run_javap(jar: Path, clazz: str) -> str:
    try:
        process = subprocess.run(['javap', '-c', '-p', '-classpath', str(jar), clazz],
                                 capture_output=True, text=True, timeout=35, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AuditError('javap unavailable or timed out') from exc
    if process.returncode or not 0 < len(process.stdout) < 3_000_000:
        raise AuditError('javap failed or class output out of bounds: '+clazz)
    return process.stdout

def audit(jar: Path, inventory: str) -> dict:
    expected = expected_inventory(inventory)
    if jar.name != JAR_NAME or jar.is_symlink() or not jar.is_file():
        raise AuditError('wrong publisher JAR name or type')
    before = jar.stat()
    if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size < MAX_BYTES:
        raise AuditError('JAR size/type invalid')
    raw = jar.read_bytes()
    signature = lambda x: (x.st_dev,x.st_ino,x.st_mtime_ns,x.st_ctime_ns,x.st_size)
    if signature(before) != signature(jar.stat()):
        raise AuditError('JAR modified during read')
    sha1, sha256 = hashlib.sha1(raw).hexdigest(), hashlib.sha256(raw).hexdigest()
    if sha1 != SHA1:
        raise AuditError('publisher bytes do not equal installed physical SHA1')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise AuditError('duplicate JAR entries')
        if not all(k.replace('.','/')+'.class' in names for k in CLASSES):
            raise AuditError('expected registry class missing')
        try:
            metadata = archive.read('META-INF/neoforge.mods.toml')
        except KeyError as exc:
            raise AuditError('NeoForge metadata absent') from exc
        if len(metadata)>256_000 or not re.search(rb'\bmodId\s*=\s*["\x27]ess_requiem["\x27]',metadata):
            raise AuditError('mod ID absent/mismatched')
    records=[]
    for reg, count in CLASSES.items():
        mapping = registry_classes(run_javap(jar.resolve(), reg), count)
        for field, clazz in mapping.items():
            if clazz.replace('.', '/')+'.class' not in names:
                raise AuditError('registered spell class not found in JAR')
            root = spell_id(run_javap(jar.resolve(), clazz))
            records.append(dict(registry='DTE' if reg == DTE else 'BASE',field=field,root=root,clazz=clazz))
    roots=[x['root'] for x in records]
    counts=Counter(roots)
    dte_roots={x['root'] for x in records if x['registry']=='DTE'}
    deviations={
        'missing_ids': sorted(set(expected)-set(roots)),
        'unexpected_ids': sorted(set(roots)-set(expected)),
        'duplicate_ids': sorted(k for k,v in counts.items() if v!=1),
        'dte_root_mismatch': sorted(dte_roots ^ {'forever_dreaming','nightmare','nightmare_scream'}),
        'count_mismatch': len(records)!=58,
    }
    if signature(before)!=signature(jar.stat()) or hashlib.sha256(jar.read_bytes()).hexdigest()!=sha256:
        raise AuditError('JAR modified during inspection')
    passed=not any(deviations.values())
    return {
        'result':'PASS' if passed else 'UNPROVEN_OR_MISMATCH',
        'evidence_class':'SHA1_MATCHED_COMPILED_REGISTRATION_AND_SPELL_ID_NOT_RUNTIME_QA',
        'publisher_jar':JAR_NAME, 'mod_id':MOD_ID,'version':'0.1.7',
        'sha1':sha1,'sha256':sha256,'size_bytes':len(raw),
        'registry_roots':len(records),'base_roots':len(records)-len(dte_roots),
        'conditional_dte_roots':len(dte_roots),'unique_roots':len(counts),
        'semantically_counted':sum(expected.get(x)=='COUNTED_SOURCE_PINNED' for x in roots),
        'technically_excluded':sum(expected.get(x)=='EXCLUDED' for x in roots),
        'deviations':deviations,
        'not_proven':['loaded registry','DTE mod initialization gate','config','player reachability','Survival','real client/server','spell execution','mana and cooldown settlement','RPG Skill Tree bridge']
    }

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument('--jar',type=Path,required=True)
    p.add_argument('--inventory',type=Path,default=Path('wiki/modpack-catalog/providers/✅-enders-spells-and-stuff-requiem/SOURCE-0.1.7-SPELL-INVENTORY.md'))
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    try:
        if args.inventory.stat().st_size>200_000:
            raise AuditError('inventory too large')
        report=audit(args.jar,args.inventory.read_text(encoding='utf-8'))
        status=0 if report['result']=='PASS' else 1
    except (AuditError,OSError,ValueError,UnicodeError,zipfile.BadZipFile) as exc:
        report={'result':'FAIL_CLOSED','reason':str(exc)}
        status=1
    output=json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding='utf-8')
    print(output)
    return status

if __name__=='__main__':
    raise SystemExit(main())
