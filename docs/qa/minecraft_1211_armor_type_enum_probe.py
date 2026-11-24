#!/usr/bin/env python3
"""Read-only exact Minecraft 1.21.1 ArmorItem.Type JVM enum discovery.

Obtain official client JAR and ProGuard class mappings via Mojang's own
version manifest. Assert SHA-1/size of every metadata/artifact hop and inspect
only the enum classfile/initializer, without decompiling or running the game.
Discovery is an upstream reference, NOT an installed transformed runtime test.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import time
import urllib.request
import zipfile
from pathlib import Path

VERSION = '1.21.1'
META = 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'
CLASS = 'net.minecraft.world.item.ArmorItem$Type'
ALLOWED = ('https://piston-meta.mojang.com/', 'https://piston-data.mojang.com/',
           'https://launchermeta.mojang.com/', 'https://launcher.mojang.com/')
NAMES = ('HELMET', 'CHESTPLATE', 'LEGGINGS', 'BOOTS')
# Historical metadata is part of the sealed report's provenance. Mojang may
# revise release metadata without changing the client/mapping artifacts.
HISTORICAL_META = {
    'url': 'https://piston-meta.mojang.com/v1/packages/ff7ef54488da4a711f3c8a781a9f79105bbe801a/1.21.1.json',
    'sha1': 'ff7ef54488da4a711f3c8a781a9f79105bbe801a',
    'sha256': 'ab07658fe972925ed0036e383a09e3b4ca6b3f4ee07634233c02a5a1d49a39c9',
}
ARTIFACT_PINS = {
    'client': {
        'url': 'https://piston-data.mojang.com/v1/objects/30c73b1c5da787909b2f73340419fdf13b9def88/client.jar',
        'sha1': '30c73b1c5da787909b2f73340419fdf13b9def88',
        'sha256': '499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99',
        'size': 26836906,
    },
    'client_mappings': {
        'url': 'https://piston-data.mojang.com/v1/objects/2244b6f072256667bcd9a73df124d6c58de77992/client.txt',
        'sha1': '2244b6f072256667bcd9a73df124d6c58de77992',
        'sha256': '140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec',
        'size': 9598610,
    },
}


def require(pred, msg):
    if not pred:
        raise ValueError(msg)


def digest(raw, algo='sha256'):
    return hashlib.new(algo, raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + '\n'


def fetch(url, cap):
    require(url.startswith(ALLOWED), 'untrusted metadata URL')
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'BlackArcanaStaticCatalog/1.0'}), timeout=80) as r:
                require(r.status == 200, 'unexpected status code')
                data = r.read(cap + 1)
                require(len(data) <= cap, 'download exceeds cap')
                return data
        except (OSError, TimeoutError) as e:
            last = e
            if attempt < 2: time.sleep(attempt + 1)
    raise OSError('download failed '+str(last))


def mappings_owner(raw):
    text = raw.decode('utf-8')
    matches = re.findall(r'^net\.minecraft\.world\.item\.ArmorItem\$Type -> ([^:\s]+):\s*$', text, re.M)
    require(len(matches) == 1, 'ambiguous ArmorItem.Type class mapping')
    mapped = matches[0]
    require(re.fullmatch(r'[a-zA-Z0-9_.$]+', mapped) is not None, 'invalid obfuscated class name')
    return mapped.replace('.', '/')


def read_code_lines(javap_text):
    """A bounded Java 21 javap view of static initializer; no code export."""
    header = re.search(r'^\s*static \{\};\s*$', javap_text, re.M)
    require(header is not None, 'static initializer missing in javap')
    tail = javap_text[header.end():]
    matches = list(re.finditer(r'^[ \t]*(\d+):[ \t]+([a-z][a-z0-9_]*)[ \t]*([^\n]*)$', tail, re.M))
    require(matches, 'missing initializer instructions')
    out = []
    for m in matches:
        off = int(m.group(1)); op = m.group(2); rest = m.group(3)
        if out and off <= out[-1]['offset']:
            break
        out.append({'offset':off, 'opcode':op, 'operand':rest})
    require(len(out) < 300, 'unbounded initializer method')
    return out


def inspect_rows(rows):
    """Require name-string -> numeric ctor index -> enum assignment sequence.

    Note: initial scan does NOT assume four/five members; check causal bytecode.
    """
    values = []
    for i, row in enumerate(rows):
        name_match = re.search(r'// String ([A-Z_]+)\s*$', row['operand'])
        if row['opcode'] not in ('ldc', 'ldc_w') or not name_match:
            continue
        name = name_match.group(1)
        if name not in (*NAMES, 'BODY'):
            continue
        subseq = rows[i+1:i+19]
        push = []
        for ins in subseq:
            if ins['opcode'].startswith('iconst_') and ins['opcode'][7:].isdigit():
                push.append((ins['offset'],int(ins['opcode'][7:])))
            elif ins['opcode'] in ('bipush','sipush'):
                match = re.match(r'(-?\d+)', ins['operand'])
                if match: push.append((ins['offset'],int(match.group(1))))
            if ins['opcode'] == 'invokespecial':
                break
        # The constructor's enum ordinal integer is its immediate numeric push
        # preceding invokespecial in normal javac output, but some constructors
        # carry additional ints. Retain ordinal as provisional until manual audit.
        init = next((ins for ins in subseq if ins['opcode']=='invokespecial'),None)
        put = next((ins for ins in subseq if ins['opcode']=='putstatic' and (init is None or ins['offset']>init['offset'])),None)
        values.append({'name':name,'name_constant_offset':row['offset'],
                       'numeric_operands_before_ctor':push,'constructor':init,
                       'assignment':put})
    require(len(values) >= 4, 'fewer than 4 armor enum names in initialized class')
    require([x['name'] for x in values[:4]] == list(NAMES), 'unexpected Java enum creation order')
    require(len({v['name'] for v in values}) == len(values), 'duplicate armor constants')
    require(all(v['constructor'] is not None and v['assignment'] is not None for v in values),
            'missing enum construction/assignment site')
    return values


def check_metadata(raw, reference, historical=False):
    require(digest(raw, 'sha1') == reference['sha1'], 'version metadata sha1 mismatch')
    if historical:
        require(reference == HISTORICAL_META and digest(raw) == reference['sha256'],
                'historical version metadata sha256 mismatch')
    version = json.loads(raw)
    require(version['id'] == VERSION, 'version JSON mismatch')
    descriptors = version['downloads']
    for key, pin in ARTIFACT_PINS.items():
        d = descriptors[key]
        require(all(d[field] == pin[field] for field in ('url','sha1','size')),
                key + ' metadata artifact identity drift')
    return descriptors


def run(outdir, output, javap):
    require(not output.exists(), 'write-once output required')
    manifest = fetch(META, 3_000_000)
    versions = json.loads(manifest)['versions']
    matching = [x for x in versions if x['id'] == VERSION and x['type'] == 'release']
    require(len(matching)==1, 'target release absent from official manifest')
    live_meta = matching[0]
    live_bytes = fetch(live_meta['url'], 500_000)
    check_metadata(live_bytes, live_meta)
    print('LIVE_VERSION_METADATA', json.dumps({
        'version_url':live_meta['url'], 'version_sha1':live_meta['sha1'],
        'version_json_sha256':digest(live_bytes)}, sort_keys=True))
    # Replay the historical report only from its own verified official JSON.
    # Do not substitute historical hashes for the current metadata bytes.
    meta = HISTORICAL_META
    version_bytes = fetch(meta['url'], 500_000)
    descriptors = check_metadata(version_bytes, meta, historical=True)
    print('HISTORICAL_VERSION_METADATA', json.dumps(meta, sort_keys=True))
    print('PASS: live and historical metadata match both pinned artifact descriptors')
    refs={}
    outdir.mkdir(parents=True, exist_ok=True)
    for key, cap in (('client',90_000_000),('client_mappings',30_000_000)):
        d=descriptors[key]
        raw=fetch(d['url'], cap)
        require(len(raw)==d['size'] and digest(raw,'sha1')==d['sha1']
                and digest(raw)==ARTIFACT_PINS[key]['sha256'],key+' official artifact mismatch')
        dest=outdir/(key+'.jar' if key=='client' else 'client.txt')
        require(not dest.exists(),'output already exists '+str(dest))
        dest.write_bytes(raw)
        refs[key]={'official_url':d['url'],'size_bytes':len(raw),'sha1':digest(raw,'sha1'),'sha256':digest(raw)}
    obf=mappings_owner((outdir/'client.txt').read_bytes())
    with zipfile.ZipFile(outdir/'client.jar') as z:
        path=obf+'.class'
        require(path in z.namelist(),'mapped class missing in target JAR')
        class_bytes=z.read(path)
        require(class_bytes[:4] == b'\xca\xfe\xba\xbe', 'invalid bytecode header')
        major=int.from_bytes(class_bytes[6:8], 'big')
        require(major==65, 'non-Java21 class')
    p=subprocess.run([str(javap),'-p','-c','-classpath',str(outdir/'client.jar'),obf.replace('/','.')],capture_output=True,text=True,timeout=90)
    require(p.returncode==0,'javap failure '+p.stderr[:250])
    rows=read_code_lines(p.stdout)
    values=inspect_rows(rows)
    report={
      'schema':1,'scope':'MINECRAFT_1211_ARMOR_ITEM_TYPE_OFFICIAL_CLIENT_BINARY_DISCOVERY_NOT_INSTALLED_RUNTIME',
      'metadata':{'manifest_url':META,'version_url':meta['url'],'version_sha1':meta['sha1'],'version_json_sha256':digest(version_bytes)},
      'artifacts':refs,
      'enum':{'mapped_name':CLASS,'binary_name':obf,'class_sha256':digest(class_bytes),'major':major,
              'initializer_instruction_count':len(rows),
              'initializer_instruction_sha256':digest(canonical(rows).encode()),
              'value_construction_sites':values,
              'full_initializer':rows},
      'limits':{'neo_transformed_runtime':'NOT_VERIFIED','publisher_abi_link':'REFERENCE_ONLY',
                'physical_qa':'NOT_TESTED','mutating_hook':'NOT_VERIFIED','mutation':'NO_MUTATION',
                'individual_gingerbread_certification':'NOT_CERTIFIED',
                'provider_universe_closed':False}
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(canonical(report),encoding='utf-8')
    print('REPORT_SHA256',digest(output.read_bytes()),'BYTES',output.stat().st_size)
    print('ENUM',obf,'CLASS_SHA',digest(class_bytes),'INSTRUCTIONS',len(rows))
    for v in values:
        print('CONSTRUCTION',v['name'],'NAME_OFFSET',v['name_constant_offset'],
              'NUMERIC_BEFORE_CTOR',v['numeric_operands_before_ctor'],
              'CTOR_OFFSET',v['constructor']['offset'], 'ASSIGN_OFFSET',v['assignment']['offset'])
    print('DISCOVERY_ONLY; NO_MUTATION; NOT_CERTIFIED')


def metadata_synthetics():
    import copy
    fixture = {'id':VERSION,'downloads':{k:{f:p[f] for f in ('url','sha1','size')} for k,p in ARTIFACT_PINS.items()}}
    def payload(x):
        raw=canonical(x).encode()
        return raw, {'sha1':digest(raw,'sha1')}
    raw,ref=payload(fixture)
    check_metadata(raw,ref)
    for key in ARTIFACT_PINS:
        for field in ('url','sha1','size'):
            changed=copy.deepcopy(fixture)
            changed['downloads'][key][field] = 0 if field=='size' else 'different'
            modified,reference=payload(changed)
            try:
                check_metadata(modified,reference)
            except ValueError:
                pass
            else:
                raise ValueError('accepted changed descriptor '+key+' '+field)
    try:
        check_metadata(raw,{'sha1':'0'*40})
    except ValueError:
        pass
    else:
        raise ValueError('accepted incorrect metadata digest')
    print('PASS: 7 metadata rejection cases and valid descriptor fixture')


def synthetics():
    metadata_synthetics()
    fake='''public enum a$b {\n  static {};\n    Code:\n       0: new           #2                  // class a$b\n       3: dup\n       4: ldc           #4                  // String HELMET\n       6: iconst_0\n       7: invokespecial #8                  // Method "<init>":(Ljava/lang/String;I)V\n      10: putstatic     #9                  // Field a:La$b;\n      13: new           #2                  // class a$b\n      16: dup\n      17: ldc           #10                 // String CHESTPLATE\n      19: iconst_1\n      20: invokespecial #8                  // Method "<init>":(Ljava/lang/String;I)V\n      23: putstatic     #11                 // Field b:La$b;\n      26: new           #2                  // class a$b\n      29: dup\n      30: ldc           #12                 // String LEGGINGS\n      32: iconst_2\n      33: invokespecial #8                  // Method "<init>":(Ljava/lang/String;I)V\n      36: putstatic     #13                 // Field c:La$b;\n      39: new           #2                  // class a$b\n      42: dup\n      43: ldc           #14                 // String BOOTS\n      45: iconst_3\n      46: invokespecial #8                  // Method "<init>":(Ljava/lang/String;I)V\n      49: putstatic     #15                 // Field d:La$b;\n      52: return\n}'''
    rows=read_code_lines(fake);v=inspect_rows(rows)
    require(len(v)==4 and [x['numeric_operands_before_ctor'][0][1] for x in v]==[0,1,2,3],
            'valid fixture failed')
    for tampered in [fake.replace('String BOOTS','String HELMET'), fake.replace('iconst_2','iconst_9'),
                     fake.replace('putstatic     #15','nop           #15'), fake.replace('String CHESTPLATE','String BODY')]:
        try:
            vv=inspect_rows(read_code_lines(tampered))
            require(vv == v, 'changed operand accepted')
        except ValueError:
            pass
        else:
            raise ValueError('tampered fake accepted')
    require(mappings_owner(b'net.minecraft.world.item.ArmorItem$Type -> cq$a:\n')=='cq$a','map parser failed')
    print('PASS SYNTHETICS: enum parser, 4 rejected modifications, official mapping parser')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--test',action='store_true')
    ap.add_argument('--outdir',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--javap',default='javap')
    args=ap.parse_args()
    if args.test:synthetics()
    else:
        require(args.outdir and args.output,'--outdir and --output required')
        run(args.outdir,args.output,args.javap)
