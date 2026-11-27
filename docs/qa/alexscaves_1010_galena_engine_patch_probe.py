#!/usr/bin/env python3
"""Read-only, version-pinned NeoForge userdev patch footprint for Galena NBT edges.

This is a *patch presence and contextual symbol* census. It does not derive
Minecraft source or claim vanilla method semantics, runtime transforms,
actual save/restart outcomes, mutating hooks or gameplay QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile, BadZipFile

VERSION = '21.1.250'
EXPECTED_NAME = 'neoforge-21.1.250-userdev.jar'
EXPECTED_SHA1 = '45f4a0daf3ecd5864338cb5ab7368afbee02e529'
EXPECTED_SHA256 = 'deb6dd1e002aa85406e92501f49d5429cc8eaefe32fc353433e67030c32d8372'
EXPECTED_BYTES = 3983248
SOURCE_PUBLISHER_SHA = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
SOURCE_HELPER_SHA = 'ca395f3418979d8302363cf9db8d54c620572b16ebdc2ecacee5014fce0add64'
ROOT = 'patches/net/minecraft/'
TARGETS = {
    'ItemStack': ROOT + 'world/item/ItemStack.java.patch',
    'CustomData': ROOT + 'world/item/component/CustomData.java.patch',
    'CompoundTag': ROOT + 'nbt/CompoundTag.java.patch',
}
TOKENS = ('parse', 'save', 'encode', 'decode', 'codec', 'custom_data', 'customdata',
          'copytag', 'putuuid', 'hasuuid', 'getuuid', 'data_components',
          'datacomponents', 'set', 'remove', 'compoundtag', 'dataresult',
          'registry', 'components')
# To avoid misclassifying generic prose as engine coverage, matches are word-boundary
# tokens, with method-name suffixes separated from Java punctuation.
MATCH = re.compile(r'(?i)(?<![a-z0-9_])(?:' + '|'.join(re.escape(w) for w in TOKENS) + r')(?![a-z0-9_])')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def require(cond: bool, reason: str) -> None:
    if not cond:
        raise ValueError(reason)


def canonical(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def diff_kind(line: str) -> str:
    if line.startswith('+++') or line.startswith('---'):
        return 'HEADER'
    if line.startswith('@@'):
        return 'HUNK'
    return {'+': 'ADD', '-': 'DELETE', ' ': 'CONTEXT', '\\': 'META'}.get(line[:1], 'OTHER')


def matches(line: str) -> list[str]:
    return sorted({m.group(0).lower() for m in MATCH.finditer(line)})


def examine_patch(path: str, raw: bytes) -> dict:
    require(len(raw) < 5_000_000, 'patch exceeds per-entry budget')
    content = raw.decode('utf8')
    lines = content.splitlines()
    require(lines and any(x.startswith('@@') for x in lines), 'patch lacks unified hunk')
    hunks = [i + 1 for i, line in enumerate(lines) if line.startswith('@@')]
    findings = []
    for idx, line in enumerate(lines, start=1):
        kind = diff_kind(line)
        if kind not in ('ADD', 'DELETE', 'CONTEXT'):
            continue
        found = matches(line[1:])
        if found:
            findings.append({'line': idx, 'kind': kind, 'tokens': found,
                             'line_sha256': sha(line.encode('utf8')), 'bytes': len(line.encode('utf8'))})
    require(len(findings) <= 1200, 'patch symbol hit budget exceeded')
    return {'path': path, 'sha256': sha(raw), 'size_bytes': len(raw),
            'total_lines': len(lines), 'hunk_count': len(hunks),
            'hunk_line_numbers': hunks, 'matches': findings,
            'matched_counts_by_kind': {k: sum(f['kind'] == k for f in findings)
                                       for k in ('ADD', 'DELETE', 'CONTEXT')},
            'no_patch_body_in_report': True}


def analyze(userdev: Path, output: Path) -> dict:
    raw = userdev.read_bytes()
    require(len(raw) == EXPECTED_BYTES and hashlib.sha1(raw).hexdigest() == EXPECTED_SHA1
            and sha(raw) == EXPECTED_SHA256, 'official NeoForge userdev artifact identity drift')
    require(output.suffix == '.json' and not output.exists(), 'JSON output must be write-once')
    with ZipFile(userdev) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'duplicate entries in userdev archive')
        patch_names = sorted(p for p in names if p.startswith(ROOT) and p.endswith('.java.patch'))
        require(patch_names, 'no Minecraft source patches in verified userdev')
        present = {}
        for short, path in TARGETS.items():
            if path in names:
                present[short] = {'present': True, **examine_patch(path, z.read(path))}
            else:
                present[short] = {'present': False, 'path': path}
        require(present['ItemStack']['present'], 'expected ItemStack patch absent')
        report = {
            'schema_version': 1,
            'scope': 'GALENA_1010_NEOFORGE_211250_NBT_PATCH_FOOTPRINT_ONLY',
            'reference': {'minecraft': '1.21.1', 'neoforge': VERSION, 'userdev_filename': EXPECTED_NAME,
                          'userdev_size': EXPECTED_BYTES, 'userdev_sha1': EXPECTED_SHA1,
                          'userdev_sha256': EXPECTED_SHA256,
                          'official_maven': ('https://maven.neoforged.net/releases/net/neoforged/'
                                             'neoforge/21.1.250/' + EXPECTED_NAME),
                          'alexscaves_publisher_sha256': SOURCE_PUBLISHER_SHA,
                          'accompat_helper_report_sha256': SOURCE_HELPER_SHA},
            'archive': {'entry_count': len(names), 'minecraft_patch_count': len(patch_names),
                        'minecraft_patch_path_roster_sha256': sha(('\n'.join(patch_names) + '\n').encode())},
            'targets': present,
            'limitations': {
                'proof': 'Only which matched lines exist as additions, deletions, or context in exact userdev patches',
                'vanilla_method_body': 'NOT_VERIFIED',
                'userdev_patch_absence_implies_no_runtime_modification': False,
                'installed_transformed_game': 'NOT_VERIFIED',
                'installer_modpack_transformers': 'NOT_VERIFIED',
                'stack_codec_semantics': 'NOT_VERIFIED',
                'physical_save_restart': 'NOT_TESTED',
                'mutation': 'NO_MUTATION', 'mutating_hook': 'NOT_VERIFIED',
                'physical_qa': 'NOT_TESTED', 'static_contract': 'NOT_CERTIFIED',
                'provider_universe_closed': False,
            }
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical(report), encoding='utf8')
    return report


def selftest():
    assert diff_kind('+public class A {}') == 'ADD'
    assert diff_kind('-foo') == 'DELETE'
    assert diff_kind(' bar') == 'CONTEXT'
    assert diff_kind('@@ -1,2 +_,2 @@') == 'HUNK'
    assert matches('ItemStack.parse(context, tag)') == ['parse']
    assert matches('ItemStack.parseNonsense') == []
    assert matches('CustomData.copyTag()') == ['copytag', 'customdata']
    assert matches('CustomData.of(...)') == ['customdata']
    assert matches('DataComponents.CUSTOM_DATA') == ['custom_data', 'datacomponents']
    synthetic = b'--- a/A.java\n+++ b/A.java\n@@ -1,2 +_,2 @@\n public void save() {}\n-    parse(old);\n+    parse(newTag);\n'
    v = examine_patch('sample', synthetic)
    assert v['hunk_count'] == 1 and v['matched_counts_by_kind'] == {'ADD': 1, 'DELETE': 1, 'CONTEXT': 1}
    bad = synthetic.replace(b'@@ -1,2 +_,2 @@', b'== INVALID ==')
    try:
        examine_patch('bad', bad)
    except ValueError:
        pass
    else:
        raise AssertionError('malformed patch accepted')
    print('PASS: patch scanner unit tests + malformed patch rejection (no external JAR tested)')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--userdev', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        selftest()
        return
    require(a.userdev is not None and a.output is not None, 'missing --userdev or --output')
    r = analyze(a.userdev, a.output)
    print('PASS PATCH_FOOTPRINT', r['reference']['userdev_sha256'],
          'PATCHES', r['archive']['minecraft_patch_count'])
    for name, value in r['targets'].items():
        if value['present']:
            print('TARGET', name, 'PRESENT', value['sha256'],
                  'MATCHES', len(value['matches']), value['matched_counts_by_kind'])
        else:
            print('TARGET', name, 'ABSENT_IN_USERDEV_PATCH_ROSTER')
    print('REPORT_SHA256', sha(a.output.read_bytes()), 'BYTES', a.output.stat().st_size)
    print('DISCOVERY_ONLY NO_MUTATION NO_PERK_CERTIFICATION')


if __name__ == '__main__':
    main()
