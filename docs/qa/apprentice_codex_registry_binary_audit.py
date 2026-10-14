#!/usr/bin/env python3
"""Exact-hash classfile proof of registered spell ID/field pairs (NOT runtime registry QA).

Requires the installed 0.9.7.1 JAR byte hash and the canonical per-spell catalog.
Only inspects bytecode instructions; never loads a Minecraft mod.
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

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_MD = ROOT / 'wiki/modpack-catalog/providers/✅-apprentice-codex/README.md'
EXPECTED_JAR = 'apprentice_codex-0.9.7.1+mc1.21.1.jar'
EXPECTED_SHA1 = 'b514315add32b93b0049c8673075627d7ef812e0'
EXPECTED_SHA256 = 'f0dfab67154f344c02c6fbe561f73456fa46ed9d018fae661dcdf4da95c67fe2'
MOD_ID = 'apprenticecodex'
CLASS = 'jp.aquafactory.apprenticecodex.registry.SpellRegistry'
CLASS_MEMBER = CLASS.replace('.', '/') + '.class'
EVIDENCE = 'EXACT_HASH_STATIC_INITIALIZER_REGISTRATION_PAIRS_NOT_LOADED_REGISTRY'
MAX_JAR = 32 * 1024 * 1024
INSTRUCTION = re.compile(r'^\s*\d+:\s+(?P<opcode>[\w_]+)(?:\s+[^/\n]*)?(?:\s*//\s*(?P<comment>.*))?$', re.M)
FIELD = re.compile(r'^\s*public static final [^\n]*DeferredHolder[^\n]*\s+([A-Z][A-Z0-9_]*);$', re.M)
ID_LINE = re.compile(r'^- `apprenticecodex:([a-z][a-z0-9_]*)`\s*$', re.M)
REGEX_ID = re.compile(r'^[a-z][a-z0-9_]*$')


class AuditError(Exception):
    pass


def registry_ids(markdown: str, count: int = 83) -> list[str]:
    if markdown.count('## Exact spell registry — 83/83') != 1:
        raise AuditError('canonical 83 spell registry section missing or duplicated')
    section = markdown.split('## Exact spell registry — 83/83', 1)[1].split('\n## ', 1)[0]
    ids = ID_LINE.findall(section)
    if len(ids) != count or len(set(ids)) != count:
        raise AuditError(f'canonical IDs unexpected/duplicated: {len(ids)} (expected {count})')
    return ids


def parse_static_registrations(disassembly: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Correlate LDC ID -> Supplier -> reg(String,Supplier) -> static DeferredHolder."""
    if disassembly.count('  static {};') != 1:
        raise AuditError('static initializer missing or ambiguous')
    pre, body = disassembly.split('  static {};', 1)
    if '    Code:' not in body:
        raise AuditError('static initializer has no bytecode')
    instructions = [(m.group('opcode'), (m.group('comment') or '').strip())
                    for m in INSTRUCTION.finditer(body)]
    spell_fields = FIELD.findall(pre)
    pairs: list[tuple[str, str]] = []
    for idx in range(len(instructions) - 3):
        (op0, com0), (op1, com1), (op2, com2), (op3, com3) = instructions[idx:idx + 4]
        if (op0 not in ('ldc', 'ldc_w') or not com0.startswith('String ')
                or op1 != 'invokedynamic'
                or op2 != 'invokestatic' or 'Method reg:' not in com2
                or 'Ljava/lang/String;Ljava/util/function/Supplier;' not in com2
                or op3 != 'putstatic' or 'Field ' not in com3):
            continue
        spell_id = com0[len('String '):]
        field = re.search(r'\bField ([A-Z][A-Z0-9_]*):', com3)
        if not REGEX_ID.fullmatch(spell_id) or not field:
            raise AuditError('malformed registration ID or field in compiled initializer')
        pairs.append((spell_id, field.group(1)))
    return pairs, spell_fields


def reconcile(markdown: str | list[str], disassembly: str, count: int = 83) -> dict:
    expected = registry_ids(markdown, count=count) if count == 83 else list(markdown)
    if count != 83 and (len(expected) != count or len(set(expected)) != count):
        raise AuditError('test-only expected ID list is malformed')
    pairs, declared = parse_static_registrations(disassembly)
    duplicate_names = sorted(k for k, n in Counter(x for x, _ in pairs).items() if n != 1)
    duplicate_fields = sorted(k for k, n in Counter(f for _, f in pairs).items() if n != 1)
    expected_set = set(expected)
    compiled_set = set(id for id, _ in pairs)
    unbound = sorted(f for _, f in pairs if f not in declared)
    never_registered_fields = sorted(set(declared) - set(f for _, f in pairs))
    malformed_fields = sorted(f'{id}:{f}' for id, f in pairs if f != id.upper())
    deviations = {
        'missing_ids': sorted(expected_set - compiled_set),
        'unexpected_ids': sorted(compiled_set - expected_set),
        'duplicate_ids': duplicate_names,
        'duplicate_fields': duplicate_fields,
        'fields_not_declared': unbound,
        'declared_fields_without_registration': never_registered_fields,
        'field_to_id_mismatches': malformed_fields,
        'count_mismatch': len(pairs) != count,
    }
    pass_ = not any(deviations.values())
    return {
        'status': 'PASS' if pass_ else 'UNPROVEN_OR_MISMATCH',
        'expected_count': count,
        'registration_pairs_count': len(pairs),
        'unique_registration_ids': len(compiled_set),
        'registration_ids': sorted(compiled_set) if pass_ else [],
        'deviations': deviations,
    }


def audit(jar: Path, markdown: str, javap: str = 'javap') -> dict:
    if jar.name != EXPECTED_JAR or jar.is_symlink() or not jar.is_file():
        raise AuditError('JAR filename/path invalid or symlinked')
    before = jar.stat()
    if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= MAX_JAR:
        raise AuditError('unexpected JAR size or file type')
    data = jar.read_bytes()
    after = jar.stat()
    sig = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if sig(before) != sig(after):
        raise AuditError('JAR replaced/modified during read')
    sha1, sha256 = hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest()
    if (sha1, sha256) != (EXPECTED_SHA1, EXPECTED_SHA256):
        raise AuditError('SHA-1/SHA-256 do not match installed physical version')
    with zipfile.ZipFile(io.BytesIO(data)) as zip_file:
        names = zip_file.namelist()
        if len(names) != len(set(names)) or CLASS_MEMBER not in names:
            raise AuditError('duplicate ZIP entry or missing SpellRegistry.class')
        try:
            meta = zip_file.read('META-INF/neoforge.mods.toml')
        except KeyError as exc:
            raise AuditError('NeoForge metadata absent') from exc
        if len(meta) > 256_000 or not re.search(rb'\bmodId\s*=\s*["\x27]apprenticecodex["\x27]', meta):
            raise AuditError('unexpected mod ID metadata')
    try:
        run = subprocess.run([javap, '-c', '-p', '-classpath', str(jar.resolve()), CLASS],
                             capture_output=True, text=True, check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AuditError('javap missing or timed out') from exc
    if run.returncode or len(run.stdout) > 2 * 1024 * 1024:
        raise AuditError('javap failed or output exceeds bound')
    if sig(jar.stat()) != sig(before) or hashlib.sha256(jar.read_bytes()).hexdigest() != sha256:
        raise AuditError('JAR mutated during classfile inspection')
    outcome = reconcile(markdown, run.stdout)
    return {
        'evidence_class': EVIDENCE,
        'result': outcome['status'],
        'provider': MOD_ID,
        'minecraft': '1.21.1',
        'version': '0.9.7.1',
        'filename': jar.name,
        'sha1': sha1, 'sha256': sha256,
        'size_bytes': len(data),
        'registry': outcome,
        'not_proven': ['loaded NeoForge registry', 'actual cast reachability', 'mods co-loaded',
                       'client/dedicated-server behavior', 'configuration', 'Survival',
                       'RPG Skill Tree contract', 'full compiled implementation equality'],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path, required=True)
    parser.add_argument('--registry-md', type=Path, default=REGISTRY_MD)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        if args.registry_md.stat().st_size > 256_000:
            raise AuditError('catalog is oversized')
        report = audit(args.jar, args.registry_md.read_text(encoding='utf-8'))
        exit_code = 0 if report['result'] == 'PASS' else 1
    except (AuditError, OSError, UnicodeError, zipfile.BadZipFile) as exc:
        report = {'evidence_class': 'UNVERIFIED', 'result': 'FAIL_CLOSED', 'reason': str(exc)}
        exit_code = 1
    data = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data + '\n', encoding='utf-8')
    print(data)
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
